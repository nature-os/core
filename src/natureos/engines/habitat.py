"""
Habitat Suitability engine — evaluates species fitness for a given site.

Implements multi-criteria suitability scoring based on species ecological
parameters matched against site environmental conditions.

Methodology: Weighted linear combination of suitability factors, with
threshold-based exclusion for fatal mismatches. Designed to be transparent
and auditable — each factor is independently scored and weighted.

Reference: FAO Land Evaluation Framework (1976); adapted for arid landscape
design contexts.
"""

from dataclasses import dataclass, field
from enum import Enum
from natureos.species import Species, WaterRegime, SalinityTolerance, ThermalTolerance
from natureos.site import Site


class SuitabilityClass(str, Enum):
    """Suitability classification for a species on a site."""
    HIGHLY_SUITABLE = "highly_suitable"       # >= 80%
    SUITABLE = "suitable"                      # >= 60%
    MODERATELY_SUITABLE = "moderately_suitable" # >= 40%
    MARGINAL = "marginal"                      # >= 20%
    NOT_SUITABLE = "not_suitable"              # < 20% or excluded


#  Default weights for suitability factors 
# These reflect relative importance in arid environments.
# Weights are configurable for different regional contexts.

DEFAULT_WEIGHTS = {
    "water_compatibility": 0.30,       # Most critical in arid climates
    "thermal_compatibility": 0.25,     # Extreme heat is a primary constraint
    "salinity_compatibility": 0.20,    # Saline soils are common in MENA
    "ecosystem_match": 0.15,           # Species should fit the ecosystem type
    "soil_texture_match": 0.10,        # Soil texture affects establishment
}



def _score_water(species: Species, site: Site) -> float:
    """
    Score water regime compatibility.

    Logic: Species with lower water requirements than the site's capacity
    are favoured. Species requiring more water than sustainable in the
    site's climate are penalised but not excluded — irrigation can compensate.
    """
    # Arid sites favour low-water species
    if site.is_arid:
        if species.water_regime == WaterRegime.VERY_LOW:
            return 1.0
        elif species.water_regime == WaterRegime.LOW:
            return 0.85
        elif species.water_regime == WaterRegime.MODERATE:
            return 0.5
        elif species.water_regime == WaterRegime.HIGH:
            return 0.2
    else:
        # Non-arid sites can accommodate a wider range
        water_scores = {
            WaterRegime.VERY_LOW: 0.9,
            WaterRegime.LOW: 1.0,
            WaterRegime.MODERATE: 0.8,
            WaterRegime.HIGH: 0.5,
        }
        return water_scores.get(species.water_regime, 0.5)
    return 0.5


def _score_thermal(species: Species, site: Site) -> float:
    """
    Score thermal tolerance compatibility.

    Logic: Species must tolerate the site's maximum summer temperature.
    Extreme tolerance species are preferred on sites with max temps > 45°C.
    """
    if site.max_summer_temp_c > 45:
        if species.thermal_tolerance == ThermalTolerance.EXTREME:
            return 1.0
        elif species.thermal_tolerance == ThermalTolerance.HIGH:
            return 0.6
        else:
            return 0.2  # Moderate tolerance in extreme heat — risky
    elif site.max_summer_temp_c > 40:
        if species.thermal_tolerance == ThermalTolerance.EXTREME:
            return 1.0
        elif species.thermal_tolerance == ThermalTolerance.HIGH:
            return 0.9
        else:
            return 0.5
    else:
        # Milder climate  most species can cope
        if species.thermal_tolerance == ThermalTolerance.EXTREME:
            return 1.0
        elif species.thermal_tolerance == ThermalTolerance.HIGH:
            return 1.0
        else:
            return 0.8
    return 0.5


def _score_salinity(species: Species, site: Site) -> float:
    """
    Score salinity tolerance compatibility.

    Logic: If the site is saline (dS/m > 4.0), halophytes and high-tolerance
    species score highest. On non-saline sites, salinity tolerance is neutral.
    """
    if site.is_saline:
        salinity_scores = {
            SalinityTolerance.HALOPHYTE: 1.0,
            SalinityTolerance.HIGH: 0.9,
            SalinityTolerance.MODERATE: 0.5,
            SalinityTolerance.LOW: 0.2,
            SalinityTolerance.NONE: 0.0,
        }
        return salinity_scores.get(species.salinity_tolerance, 0.3)
    else:
        # Non-saline site salinity tolerance is not a constraint
        return 1.0


def _score_ecosystem(species: Species, site: Site) -> float:
    """
    Score ecosystem match between species' natural range and site's land use.

    Logic: Direct ecosystem match = 1.0. Adjacent or overlapping ecosystems
    score partially. Species with no ecosystem overlap are not excluded
    (many species adapt beyond their native range) but scored lower.
    """
    from natureos.species import EcosystemType

    # Map site land use to ecosystem types
    land_use_to_ecosystem = {
        "public_park": EcosystemType.URBAN_PARK,
        "streetscape": EcosystemType.URBAN_PARK,
        "residential": EcosystemType.URBAN_PARK,
        "commercial": EcosystemType.URBAN_PARK,
        "ecological_restoration": EcosystemType.DESERT_SCRUB,
        "wetland_conservation": EcosystemType.MANGROVE_WETLAND,
        "desert_habitat": EcosystemType.DESERT_SCRUB,
    }

    site_ecosystem = land_use_to_ecosystem.get(site.land_use.value)

    if site_ecosystem is None:
        return 0.5  # Unknown — neutral

    if site_ecosystem in species.ecosystems:
        return 1.0

    # Check for overlapping ecosystem categories
    # Coastal and wetland species share saline adaptation
    coastal_wetland = {EcosystemType.COASTAL_SABKHA, EcosystemType.MANGROVE_WETLAND}
    species_set = set(species.ecosystems)
    if site_ecosystem in coastal_wetland and species_set & coastal_wetland:
        return 0.7

    # Desert scrub and mountain wadi species sometimes overlap
    arid_natural = {EcosystemType.DESERT_SCRUB, EcosystemType.MOUNTAIN_WADI}
    if site_ecosystem in arid_natural and species_set & arid_natural:
        return 0.7

    if site_ecosystem == EcosystemType.URBAN_PARK and species_set:
        return 0.5

    return 0.3  # Minimal overlap


def _score_soil_texture(species: Species, site: Site) -> float:
    """
    Score soil texture compatibility.

    Simplified: Most native MENA species are adapted to sandy/sandy-loam soils.
    Heavy clay soils are more challenging in arid environments due to drainage
    and salinity accumulation. This is a coarse filter — detailed soil-species
    matrices planned for future versions.
    """
    soil = site.soil
    # Sandy soils — ideal for most arid-adapted species
    if soil.texture.value in ("sand", "loamy_sand", "sandy_loam"):
        return 1.0
    elif soil.texture.value == "loam":
        return 0.8
    elif soil.texture.value == "silt_loam":
        return 0.6
    elif soil.texture.value == "clay":
        return 0.4
    return 0.5


@dataclass
class SuitabilityResult:
    """Result of a habitat suitability evaluation for a single species."""
    species: Species
    overall_score: float                    # 0.0 to 1.0
    suitability_class: SuitabilityClass
    factor_scores: dict[str, float] = field(default_factory=dict)
    exclusions: list[str] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"{self.species.display_name}: "
            f"{self.overall_score:.0%} — {self.suitability_class.value}"
        )


@dataclass
class HabitatSuitability:
    """
    Evaluates species suitability for a given site.

    Parameters
    ----------
    site : Site
        The site to evaluate against
    weights : dict[str, float]
        Weighting for each suitability factor. Uses DEFAULT_WEIGHTS if not set.
    minimum_score : float
        Species scoring below this threshold are classified as NOT_SUITABLE.
    """

    site: Site
    weights: dict[str, float] = field(default_factory=lambda: DEFAULT_WEIGHTS.copy())
    minimum_score: float = 0.2

    def evaluate(self, species: Species) -> SuitabilityResult:
        """
        Evaluate a single species for the site.

        Returns a SuitabilityResult with overall score and factor breakdown.
        """
        # Compute individual factor scores
        factor_scores = {
            "water_compatibility": _score_water(species, self.site),
            "thermal_compatibility": _score_thermal(species, self.site),
            "salinity_compatibility": _score_salinity(species, self.site),
            "ecosystem_match": _score_ecosystem(species, self.site),
            "soil_texture_match": _score_soil_texture(species, self.site),
        }

        # Weighted combination
        overall = sum(
            factor_scores[factor] * self.weights.get(factor, 0.0)
            for factor in factor_scores
        )

        # Determine suitability class
        if overall >= 0.8:
            suitability_class = SuitabilityClass.HIGHLY_SUITABLE
        elif overall >= 0.6:
            suitability_class = SuitabilityClass.SUITABLE
        elif overall >= 0.4:
            suitability_class = SuitabilityClass.MODERATELY_SUITABLE
        elif overall >= self.minimum_score:
            suitability_class = SuitabilityClass.MARGINAL
        else:
            suitability_class = SuitabilityClass.NOT_SUITABLE

        return SuitabilityResult(
            species=species,
            overall_score=round(overall, 4),
            suitability_class=suitability_class,
            factor_scores=factor_scores,
            exclusions=[],
        )

    def evaluate_all(self, species_list: list[Species]) -> list[SuitabilityResult]:
        """
        Evaluate a list of species and return results sorted by suitability.

        Parameters
        ----------
        species_list : list[Species]
            Species to evaluate

        Returns
        -------
        list[SuitabilityResult]
            Results sorted from highest to lowest suitability score
        """
        if not species_list:
            raise ValueError("Species list cannot be empty")

        results = [self.evaluate(sp) for sp in species_list]
        results.sort(key=lambda r: r.overall_score, reverse=True)
        return results

    def top_species(
        self, species_list: list[Species], n: int = 5
    ) -> list[SuitabilityResult]:
        """
        Return the top N most suitable species for the site.

        Parameters
        ----------
        species_list : list[Species]
            Species to evaluate
        n : int
            Number of top results to return

        Returns
        -------
        list[SuitabilityResult]
            Top N results by suitability score
        """
        return self.evaluate_all(species_list)[:n]
