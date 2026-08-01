"""
Design Brief Generator - Decision Intelligence Engine.

Transforms raw computational engine outputs into actionable
professional deliverables: Planting Spec Sheets, Financial ROI,
Compliance Reports, and Risk Assessments.

This is the layer that makes NatureOS worth paying for.
"""

from dataclasses import dataclass, field
from enum import Enum
from natureos.species import Species, GrowthForm
from natureos.site import Site
from natureos.engines.financials import (
    Jurisdiction, JurisdictionRules, ComplianceRule,
    JURISDICTION_PRESETS, WATER_TARIFFS,
    SOIL_VAULT_COST_PER_M3, ROOT_BARRIER_COST_PER_LM,
    NURSERY_COSTS, PLANTING_LABOR_COST,
    ANNUAL_MAINTENANCE_COST, CARBON_CREDIT_PRICE_PER_TCO2E,
    GreenBuildingCredits,
)
from typing import Optional


# ── Output Models ────────────────────────────────────────────────────

@dataclass
class PlantingSpec:
    """A single species planting specification."""
    species: Species
    quantity: int
    spacing_m: float
    soil_volume_m3_per_unit: float
    total_soil_volume_m3: float
    root_barrier_required: bool
    root_barrier_depth_m: float = 1.2
    water_establishment_l_day: float = 0.0
    water_mature_l_day: float = 0.0
    nursery_spec: str = ""
    function: str = ""


@dataclass
class FinancialAnalysis:
    """Financial ROI and CAPEX/OPEX breakdown."""
    total_capex_aed: float
    total_opex_annual_aed: float
    standard_baseline_opex_aed: float
    annual_savings_aed: float
    savings_pct: float
    water_cost_potable_aed: float
    water_cost_tse_aed: float
    tse_compatible_pct: float
    carbon_credit_value_usd: float
    soil_engineering_cost_aed: float
    payback_years: float = 0.0


@dataclass
class ComplianceReport:
    """Municipal compliance pass/fail report."""
    jurisdiction: str
    rules_checked: list[dict] = field(default_factory=list)
    pass_count: int = 0
    fail_count: int = 0
    warn_count: int = 0
    overall_status: str = "PASS"


@dataclass
class DesignBriefOutput:
    """Complete design brief — the high-value product output."""
    site_name: str
    site_area_hectares: float
    jurisdiction: str
    planting_specs: list[PlantingSpec] = field(default_factory=list)
    financials: Optional[FinancialAnalysis] = None
    compliance: Optional[ComplianceReport] = None
    green_building_credits: Optional[GreenBuildingCredits] = None
    climate_risk_note: str = ""


# ── Main Generator Engine ────────────────────────────────────────────

@dataclass
class DesignBriefGenerator:
    """
    Generates high-value professional deliverables from raw engine outputs.

    Parameters
    ----------
    site : Site
        The project site
    selected_species : list[tuple[Species, float]]
        Species with suitability scores from Habitat engine
    water_budget_m3_yr : float
        Annual irrigation demand
    carbon_tco2e : float
        Carbon sequestration in tCO₂e
    canopy_cover_pct : float
        Percentage canopy cover
    avg_surface_cooling_c : float
        Average surface temperature reduction
    biodiversity_shannon : float
        Shannon diversity index
    jurisdiction : Jurisdiction
        Target regulatory jurisdiction
    """

    site: Site
    selected_species: list  # list of (Species, score)
    water_budget_m3_yr: float = 0.0
    carbon_tco2e: float = 0.0
    canopy_cover_pct: float = 0.0
    avg_surface_cooling_c: float = 0.0
    biodiversity_shannon: float = 0.0
    jurisdiction: Jurisdiction = Jurisdiction.DUBAI_MUNICIPALITY

    def generate(self) -> DesignBriefOutput:
        """Generate the complete design brief."""
        specs = self._generate_planting_specs()
        financials = self._generate_financials(specs)
        compliance = self._generate_compliance()
        credits = self._estimate_green_building_credits()

        return DesignBriefOutput(
            site_name=self.site.name,
            site_area_hectares=self.site.area_hectares,
            jurisdiction=self.jurisdiction.value,
            planting_specs=specs,
            financials=financials,
            compliance=compliance,
            green_building_credits=credits,
            climate_risk_note=self._climate_risk_note(),
        )

    def _generate_planting_specs(self) -> list[PlantingSpec]:
        """Generate planting specifications with quantities and engineering."""
        specs = []
        total_area_m2 = self.site.area_hectares * 10000
        target_canopy = max(self.canopy_cover_pct / 100, 0.25)

        for i, (sp, score) in enumerate(self.selected_species[:7]):
            # Quantity based on growth form and canopy target
            if sp.growth_form == GrowthForm.TREE:
                spacing = 8.0
                canopy_per_tree = 50.0
                target_tree_area = total_area_m2 * target_canopy
                quantity = max(3, int(target_tree_area / canopy_per_tree / 3))
            elif sp.growth_form == GrowthForm.SHRUB:
                spacing = 1.5
                quantity = max(20, int(total_area_m2 * 0.02))
            elif sp.growth_form == GrowthForm.GRASS:
                spacing = 0.5
                quantity = max(100, int(total_area_m2 * 0.05))
            elif sp.growth_form == GrowthForm.GROUNDCOVER:
                spacing = 0.4
                quantity = max(200, int(total_area_m2 * 0.08))
            else:
                spacing = 2.0
                quantity = 30

             # Global soil volume — uses species data when available, falls back to baselines
            growth_form = sp.growth_form

            # Baseline by growth form
            baseline_volumes = {
                GrowthForm.TREE: 12.0,
                GrowthForm.SHRUB: 0.4,
                GrowthForm.GRASS: 0.08,
                GrowthForm.GROUNDCOVER: 0.05,
                GrowthForm.CLIMBER: 0.2,
                GrowthForm.SUCCULENT: 0.15,
                GrowthForm.MANGROVE: 8.0,
            }
            soil_volume = baseline_volumes.get(growth_form, 0.5)

            # Scale by species dimensions if available
            height = sp.mature_height_m
            spread = sp.canopy_spread_m
            root_depth = sp.root_depth_m

            if growth_form == GrowthForm.TREE and height is not None:
                if height >= 20.0:
                    soil_volume = 30.0
                elif height >= 10.0:
                    soil_volume = 15.0
                elif height < 5.0:
                    soil_volume = 6.0

            # Exact cylindrical root zone if spread and depth available
            if spread is not None and root_depth is not None and spread > 0 and root_depth > 0:
                import math
                radius = spread / 2.0
                calculated = math.pi * (radius ** 2) * root_depth * 0.6
                soil_volume = max(0.05, min(round(calculated, 2), 50.0))

            total_soil = round(soil_volume * quantity, 2)
            # Root barrier required if deep-rooted and near hardscape
            root_barrier = sp.growth_form == GrowthForm.TREE and (sp.root_depth_m or 5) > 3.0

            # Water per plant
            water_l_day = (self.water_budget_m3_yr * 1000) / (quantity * 365) if quantity > 0 else 0

            # Nursery spec
            if sp.growth_form == GrowthForm.TREE:
                nursery = "Min. 2.5m height, container-grown, multi-stem"
            elif sp.growth_form == GrowthForm.SHRUB:
                nursery = "5-gallon container, min. 40cm spread"
            elif sp.growth_form in (GrowthForm.GRASS, GrowthForm.GROUNDCOVER):
                nursery = "Plug tray, 72-cell"
            else:
                nursery = "Container-grown, healthy specimen"

            # Ecological function
            if sp.wildlife_value:
                function = sp.wildlife_value[:80]
            else:
                function = "General ecological value"

            specs.append(PlantingSpec(
                species=sp,
                quantity=quantity,
                spacing_m=spacing,
                soil_volume_m3_per_unit=round(soil_volume, 1),
                total_soil_volume_m3=round(total_soil, 1),
                root_barrier_required=root_barrier,
                water_establishment_l_day=round(water_l_day * 2, 1),
                water_mature_l_day=round(water_l_day, 1),
                nursery_spec=nursery,
                function=function,
            ))

        return specs

    def _generate_financials(self, specs: list[PlantingSpec]) -> FinancialAnalysis:
        """Generate financial ROI analysis."""
        # Jurisdiction tariff resolution with type-safe fallbacks
        tariffs = WATER_TARIFFS.get(self.jurisdiction, WATER_TARIFFS.get(Jurisdiction.GENERIC))
        potable_rate = float(tariffs.get("potable", 3.5))
        tse_rate = float(tariffs.get("tse", 1.0))
        tse_available = bool(tariffs.get("tse_availability", False))
        tse_max_fraction = float(tariffs.get("tse_max_fraction", 0.85)) if tse_available else 0.0
        currency_code = tariffs.get("currency", "AED")
        total_area = self.site.area_hectares * 10000

        # CAPEX
        planting_capex = 0.0
        for spec in specs:
            if spec.species.growth_form == GrowthForm.TREE:
                plant_cost = NURSERY_COSTS["tree_2m_container"]
                labor = PLANTING_LABOR_COST["tree"]
            elif spec.species.growth_form == GrowthForm.SHRUB:
                plant_cost = NURSERY_COSTS["shrub_5g"]
                labor = PLANTING_LABOR_COST["shrub"]
            else:
                plant_cost = NURSERY_COSTS["groundcover_plug"]
                labor = PLANTING_LABOR_COST["groundcover"]
            planting_capex += (plant_cost + labor) * spec.quantity

        total_soil_m3 = sum(s.total_soil_volume_m3 for s in specs)
        soil_engineering = total_soil_m3 * SOIL_VAULT_COST_PER_M3
        total_capex = planting_capex + soil_engineering

        # OPEX
        opex_annual = 0.0
        for spec in specs:
            if spec.species.growth_form == GrowthForm.TREE:
                maint = ANNUAL_MAINTENANCE_COST["tree_establishment"]
            elif spec.species.growth_form == GrowthForm.SHRUB:
                maint = ANNUAL_MAINTENANCE_COST["shrub"]
            else:
                maint = ANNUAL_MAINTENANCE_COST["groundcover"]
            opex_annual += maint * spec.quantity

        # Water costs — potable, TSE, and blended
        annual_water_m3 = float(self.water_budget_m3_yr)
        water_cost_potable = round(annual_water_m3 * potable_rate, 2)
        water_cost_tse = round(annual_water_m3 * tse_rate, 2)
        tse_compatible_pct = round(tse_max_fraction * 100.0, 1)

        if tse_available:
            blended_water_cost = round(
                (annual_water_m3 * tse_max_fraction * tse_rate) +
                (annual_water_m3 * (1.0 - tse_max_fraction) * potable_rate), 2
            )
        else:
            blended_water_cost = water_cost_potable

        total_opex = opex_annual + blended_water_cost

        # Baseline: standard turf + exotic palm landscape (~AED 6.5/m²/yr)
        standard_opex = total_area * 6.5
        annual_savings = standard_opex - total_opex
        if annual_savings < 0:
            annual_savings = 0
        savings_pct = (annual_savings / standard_opex * 100) if standard_opex > 0 else 0

        carbon_value = self.carbon_tco2e * CARBON_CREDIT_PRICE_PER_TCO2E

        return FinancialAnalysis(
            total_capex_aed=round(total_capex, 0),
            total_opex_annual_aed=round(total_opex, 0),
            standard_baseline_opex_aed=round(standard_opex, 0),
            annual_savings_aed=round(annual_savings, 0),
            savings_pct=round(savings_pct, 1),
            water_cost_potable_aed=round(water_cost_potable, 0),
            water_cost_tse_aed=round(water_cost_tse, 0),
            tse_compatible_pct=tse_compatible_pct,
            carbon_credit_value_usd=round(carbon_value, 0),
            soil_engineering_cost_aed=round(soil_engineering, 0),
            payback_years=round(total_capex / annual_savings, 1) if annual_savings > 0 else 0,
        )

    def _generate_compliance(self) -> ComplianceReport:
        """Check compliance against jurisdiction rules."""
        rules = JURISDICTION_PRESETS.get(self.jurisdiction, JURISDICTION_PRESETS[Jurisdiction.GENERIC])
        total_area = self.site.area_hectares * 10000
        water_per_m2 = self.water_budget_m3_yr / total_area if total_area > 0 else 999

        native_count = sum(1 for sp, _ in self.selected_species if sp.is_native)
        total_count = len(self.selected_species)
        native_pct = (native_count / total_count * 100) if total_count > 0 else 0

        checked = []
        passed = 0
        failed = 0
        warned = 0

        # Check native quota
        if rules.native_species_quota_pct > 0:
            status = "PASS" if native_pct >= rules.native_species_quota_pct else "FAIL"
            if status == "PASS":
                passed += 1
            else:
                failed += 1
            checked.append({
                "rule": f"Native Species Quota (≥{rules.native_species_quota_pct:.0f}%)",
                "value": f"{native_pct:.0f}%",
                "status": status,
            })

        # Check water budget
        if rules.max_water_use_m3_m2_yr < 999:
            status = "PASS" if water_per_m2 <= rules.max_water_use_m3_m2_yr else "FAIL"
            if status == "PASS":
                passed += 1
            else:
                failed += 1
            checked.append({
                "rule": f"Water Budget (≤{rules.max_water_use_m3_m2_yr} m³/m²/yr)",
                "value": f"{water_per_m2:.3f} m³/m²/yr",
                "status": status,
            })

        # Check canopy cover
        if rules.min_canopy_cover_pct > 0:
            status = "PASS" if self.canopy_cover_pct >= rules.min_canopy_cover_pct else "WARN"
            if status == "PASS":
                passed += 1
            else:
                warned += 1
            checked.append({
                "rule": f"Canopy Cover (≥{rules.min_canopy_cover_pct:.0f}%)",
                "value": f"{self.canopy_cover_pct:.1f}%",
                "status": status,
            })

        # Check biodiversity
        if rules.min_biodiversity_shannon > 0:
            status = "PASS" if self.biodiversity_shannon >= rules.min_biodiversity_shannon else "WARN"
            if status == "PASS":
                passed += 1
            else:
                warned += 1
            checked.append({
                "rule": f"Biodiversity Index (≥{rules.min_biodiversity_shannon})",
                "value": f"{self.biodiversity_shannon:.2f}",
                "status": status,
            })

        overall = "PASS" if failed == 0 and warned == 0 else ("WARN" if failed == 0 else "FAIL")

        return ComplianceReport(
            jurisdiction=rules.name,
            rules_checked=checked,
            pass_count=passed,
            fail_count=failed,
            warn_count=warned,
            overall_status=overall,
        )

    def _estimate_green_building_credits(self) -> GreenBuildingCredits:
        """Estimate green building certification credits."""
        total_area = self.site.area_hectares * 10000
        water_per_m2 = self.water_budget_m3_yr / total_area if total_area > 0 else 999

        native_count = sum(1 for sp, _ in self.selected_species if sp.is_native)
        total_count = len(self.selected_species)
        native_pct = (native_count / total_count * 100) if total_count > 0 else 0

        achieved = []
        potential = []

        if native_pct >= 60:
            achieved.append("NS-1: Native Species (Estidama) / SS Credit: Habitat (LEED)")
        elif native_pct >= 30:
            potential.append("NS-1: Increase native species to 60% for full credit")

        if water_per_m2 <= 0.4:
            achieved.append("PW-2: Water Efficient Landscaping (Estidama) / WE Credit (LEED)")
        elif water_per_m2 <= 0.6:
            potential.append("PW-2: Reduce water use to 0.4 m³/m²/yr for full credit")

        if self.carbon_tco2e > 50:
            achieved.append("Carbon Sequestration: Eligible for voluntary carbon credits")

        if self.canopy_cover_pct >= 30:
            achieved.append("Urban Heat Island Reduction: Meets LEED SS credit threshold")

        rating = "Estidama 2-Pearl / LEED Silver equivalent" if len(achieved) >= 2 else "Estidama 1-Pearl / LEED Certified equivalent"

        return GreenBuildingCredits(
            jurisdiction=self.jurisdiction,
            credits_achieved=achieved,
            credits_potential=potential,
            rating_impact=rating,
        )

    def _climate_risk_note(self) -> str:
        """Generate climate risk summary note."""
        if self.site.is_arid:
            return (
                f"Arid site ({self.site.climate_zone.value}). "
                f"Under SSP5-8.5, temperatures projected to rise 2.5-2.8°C by 2050. "
                f"Selected desert-adapted species are pre-adapted to these conditions. "
                f"Monitor irrigation demand post-2040 for potential 15-25% increase."
            )
        return "Climate risk assessment available with Pro tier."
