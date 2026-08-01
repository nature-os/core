"""
Climate Projection Engine - adjusts species suitability for future
climate scenarios using IPCC CMIP6 projections.

Projects how temperature and precipitation changes under different
Shared Socioeconomic Pathways (SSPs) will affect species viability
at a given site.

References:
- IPCC Sixth Assessment Report (AR6, 2021)
- CMIP6 Global Climate Projections
- WorldClim future climate data
"""

from dataclasses import dataclass, field
from enum import Enum
from natureos.species import Species, ThermalTolerance, WaterRegime
from natureos.site import Site, ClimateZone
from natureos.engines.habitat import HabitatSuitability, SuitabilityResult
from typing import Optional


class ClimateScenario(str, Enum):
    """IPCC Shared Socioeconomic Pathways."""
    SSP126 = "ssp126"   # Low emissions — ~1.8°C by 2100
    SSP245 = "ssp245"   # Intermediate — ~2.7°C by 2100
    SSP585 = "ssp585"   # High emissions — ~4.4°C by 2100


# ── Regional temperature deltas by 2050 under SSP5-8.5 ────────────────
# Simplified from CMIP6 multi-model mean. Full grid integration: v0.5

TEMP_DELTA_2050 = {
    # Middle East / North Africa
    "BWh": 2.8,    # Arid desert hot — severe warming
    "BWk": 2.5,    # Arid desert cold
    "BSh": 2.4,    # Semi-arid hot
    "BSk": 2.2,    # Semi-arid cold
    # Mediterranean
    "Csa": 2.2,
    "Csb": 2.0,
    # Temperate
    "Cfa": 2.0,
    "Cfb": 1.8,
    # Tropical
    "Aw": 1.8,
    "Am": 1.6,
    "Af": 1.5,
    # Continental
    "Dfa": 2.5,
    "Dfb": 2.2,
    # Default
    "default": 2.2,
}

# ── Precipitation change factors by 2050 under SSP5-8.5 ───────────────
# Multiplier: 1.0 = no change, 0.7 = 30% reduction, 1.2 = 20% increase

PRECIP_FACTOR_2050 = {
    "BWh": 0.85,   # Arid regions — slight drying
    "BWk": 0.88,
    "BSh": 0.82,   # Semi-arid — significant drying
    "BSk": 0.85,
    "Csa": 0.75,   # Mediterranean — severe drying
    "Csb": 0.78,
    "Cfa": 1.05,   # Humid subtropical — slight increase
    "Cfb": 1.05,
    "Aw": 0.90,    # Tropical savanna — slight drying
    "Am": 0.95,
    "Af": 1.02,
    "Dfa": 1.08,
    "Dfb": 1.08,
    "default": 0.95,
}


@dataclass
class ClimateProjectionResult:
    """Projected suitability for a species under future climate."""

    species: Species
    current_score: float
    projected_score: float
    score_change: float                 # Positive = more suitable, negative = less
    climate_scenario: ClimateScenario
    target_year: int
    temp_increase_c: float
    precip_factor: float
    risk_level: str                     # low / moderate / high / critical

    def summary(self) -> str:
        direction = "↑" if self.score_change > 0 else "↓" if self.score_change < 0 else "→"
        return (
            f"{self.species.display_name}: {self.current_score:.0%} → "
            f"{self.projected_score:.0%} ({direction}{abs(self.score_change):.0%}) "
            f"— {self.risk_level.upper()} risk"
        )


@dataclass
class ClimateProjection:
    """
    Projects species suitability under future climate scenarios.

    Parameters
    ----------
    site : Site
        Current site conditions
    scenario : ClimateScenario
        IPCC scenario to project under
    target_year : int
        Future year to project to (2030-2100)
    """

    site: Site
    scenario: ClimateScenario = ClimateScenario.SSP585
    target_year: int = 2050

    def project_species(self, species: Species) -> ClimateProjectionResult:
        """
        Project how a single species' suitability changes.

        Creates a modified site with projected climate, then
        re-evaluates habitat suitability.

        Parameters
        ----------
        species : Species
            Species to project

        Returns
        -------
        ClimateProjectionResult
            Current vs projected suitability
        """
        # Calculate temperature and precipitation deltas
        base_delta = TEMP_DELTA_2050.get(
            self.site.climate_zone.value,
            TEMP_DELTA_2050["default"]
        )
        base_precip = PRECIP_FACTOR_2050.get(
            self.site.climate_zone.value,
            PRECIP_FACTOR_2050["default"]
        )

        # Scale by scenario and year
        scenario_multipliers = {
            ClimateScenario.SSP126: 0.45,
            ClimateScenario.SSP245: 0.72,
            ClimateScenario.SSP585: 1.0,
        }
        sc_mult = scenario_multipliers.get(self.scenario, 1.0)

        # Year scaling: 2050 = 1.0, 2100 = ~1.8, 2030 = ~0.55
        year_fraction = (self.target_year - 2020) / 30
        year_mult = year_fraction * 1.0

        temp_increase = base_delta * sc_mult * year_mult
        precip_factor = 1.0 - (1.0 - base_precip) * sc_mult * year_mult

        # Create projected site
        projected_site = Site(
            name=f"{self.site.name} ({self.target_year})",
            climate_zone=self.site.climate_zone,
            soil=self.site.soil,
            area_hectares=self.site.area_hectares,
            land_use=self.site.land_use,
            annual_rainfall_mm=self.site.annual_rainfall_mm * precip_factor,
            max_summer_temp_c=self.site.max_summer_temp_c + temp_increase,
        )

        # Run suitability on current and projected
        current_engine = HabitatSuitability(self.site)
        current_result = current_engine.evaluate(species)

        projected_engine = HabitatSuitability(projected_site)
        projected_result = projected_engine.evaluate(species)

        score_change = projected_result.overall_score - current_result.overall_score

        # Risk assessment
        if projected_result.overall_score < 0.3:
            risk = "critical"
        elif projected_result.overall_score < 0.5:
            risk = "high"
        elif score_change < -0.1:
            risk = "moderate"
        else:
            risk = "low"

        return ClimateProjectionResult(
            species=species,
            current_score=current_result.overall_score,
            projected_score=projected_result.overall_score,
            score_change=round(score_change, 4),
            climate_scenario=self.scenario,
            target_year=self.target_year,
            temp_increase_c=round(temp_increase, 1),
            precip_factor=round(precip_factor, 3),
            risk_level=risk,
        )

    def project_all(
        self, species_list: list[Species]
    ) -> list[ClimateProjectionResult]:
        """
        Project all species and return ranked by projected suitability.

        Parameters
        ----------
        species_list : list[Species]
            Species to evaluate

        Returns
        -------
        list[ClimateProjectionResult]
            Results sorted by projected score (descending)
        """
        results = [self.project_species(sp) for sp in species_list]
        results.sort(key=lambda r: r.projected_score, reverse=True)
        return results

    def climate_resilient_species(
        self,
        species_list: list[Species],
        min_projected_score: float = 0.5,
        max_risk: str = "moderate",
    ) -> list[ClimateProjectionResult]:
        """
        Return species likely to remain viable under projected climate.

        Parameters
        ----------
        species_list : list[Species]
            Species to evaluate
        min_projected_score : float
            Minimum projected suitability (0.0-1.0)
        max_risk : str
            Maximum acceptable risk level

        Returns
        -------
        list[ClimateProjectionResult]
            Climate-resilient species
        """
        risk_order = {"low": 0, "moderate": 1, "high": 2, "critical": 3}
        results = self.project_all(species_list)
        return [
            r for r in results
            if r.projected_score >= min_projected_score
            and risk_order.get(r.risk_level, 4) <= risk_order.get(max_risk, 1)
        ]

    def summary_report(
        self, species_list: list[Species]
    ) -> str:
        """
        Generate a human-readable climate resilience report.

        Parameters
        ----------
        species_list : list[Species]
            Species to include in report

        Returns
        -------
        str
            Formatted report
        """
        results = self.project_all(species_list)
        resilient = self.climate_resilient_species(species_list)
        at_risk = [r for r in results if r.risk_level in ("high", "critical")]

        lines = [
            f"CLIMATE PROJECTION REPORT",
            f"════════════════════════",
            f"Site: {self.site.name}",
            f"Scenario: {self.scenario.value.upper()}",
            f"Target Year: {self.target_year}",
            f"Temperature Increase: {results[0].temp_increase_c if results else 'N/A'}°C",
            f"Precipitation Factor: {results[0].precip_factor if results else 'N/A'}×",
            f"",
            f"Climate-Resilient Species ({len(resilient)}):",
        ]

        for r in resilient[:10]:
            lines.append(
                f"  • {r.species.display_name} — "
                f"Current: {r.current_score:.0%} → "
                f"Projected: {r.projected_score:.0%} "
                f"({r.risk_level.upper()} risk)"
            )

        if at_risk:
            lines.append(f"")
            lines.append(f"Species at Risk ({len(at_risk)}):")
            for r in at_risk:
                lines.append(
                    f"  ⚠ {r.species.display_name} — "
                    f"Projected: {r.projected_score:.0%} "
                    f"({r.risk_level.upper()} risk)"
                )

        return "\n".join(lines)
