"""
Carbon Estimator engine — estimates carbon sequestration and storage
for planting designs.

Uses simplified allometric equations for above-ground and below-ground
biomass, plus soil organic carbon accumulation estimates.

Methodology adapted from:
- IPCC Guidelines for National Greenhouse Gas Inventories (2006)
- Chave et al. (2014). Improved allometric models to estimate the
  aboveground biomass of tropical trees.
- Cairns et al. (1997). Root biomass allocation in the world's upland forests.

For arid environments, biomass accumulation rates are conservative.
Species-specific allometric coefficients will be added as the MENA
species database expands.
"""

from dataclasses import dataclass, field
from enum import Enum
from natureos.species import Species, GrowthForm


class CarbonPool(str, Enum):
    """Carbon pools as defined by IPCC."""
    ABOVEGROUND_BIOMASS = "aboveground_biomass"
    BELOWGROUND_BIOMASS = "belowground_biomass"
    SOIL_ORGANIC_CARBON = "soil_organic_carbon"
    TOTAL = "total"


# ── Default carbon parameters by growth form ─────────────────────────
# Values are conservative estimates for arid/semi-arid environments.
# Wood density and biomass expansion factors from IPCC defaults for
# subtropical dry forest / shrubland.

# Estimated above-ground dry biomass at maturity (kg per plant)
# For arid-adapted species — lower than temperate equivalents
AGB_MATURITY_KG = {
    GrowthForm.TREE: 250.0,        # Small to medium arid trees (~8m)
    GrowthForm.SHRUB: 15.0,        # Medium shrub (~1.5m)
    GrowthForm.GRASS: 0.5,         # Perennial grass
    GrowthForm.GROUNDCOVER: 0.3,   # Low groundcover
    GrowthForm.CLIMBER: 5.0,       # Woody climber
    GrowthForm.SUCCULENT: 2.0,     # Succulent — low biomass
    GrowthForm.MANGROVE: 180.0,    # Mangrove (~4m) — dense wood
}

# Root-to-shoot ratio (below-ground / above-ground biomass)
# Cairns et al. (1997) mean for tropical dry forest: ~0.28
# Adjusted upward for arid species which invest more in roots
ROOT_SHOOT_RATIO = {
    GrowthForm.TREE: 0.35,
    GrowthForm.SHRUB: 0.50,
    GrowthForm.GRASS: 0.80,
    GrowthForm.GROUNDCOVER: 0.60,
    GrowthForm.CLIMBER: 0.30,
    GrowthForm.SUCCULENT: 0.20,
    GrowthForm.MANGROVE: 0.40,
}

# Carbon fraction of dry biomass (IPCC default: 0.47 for woody biomass,
# 0.45 for herbaceous)
CARBON_FRACTION = {
    GrowthForm.TREE: 0.47,
    GrowthForm.SHRUB: 0.47,
    GrowthForm.MANGROVE: 0.47,
    GrowthForm.GRASS: 0.45,
    GrowthForm.GROUNDCOVER: 0.45,
    GrowthForm.CLIMBER: 0.47,
    GrowthForm.SUCCULENT: 0.45,
}

# Annual soil organic carbon accumulation rate (tC/ha/year)
# Conservative for arid restored landscapes. Temperate values are ~1-2 tC/ha/yr.
# Mangrove soils accumulate significantly more.
SOC_ACCUMULATION_RATE_THA_YR = {
    "default": 0.2,        # Arid scrub/grassland restoration
    "mangrove": 1.5,       # Mangrove wetland — high soil carbon
    "urban_park": 0.3,     # Maintained urban landscape
    "desert_scrub": 0.1,   # Natural desert — very slow accumulation
}

# Maturity timeframe in years — time to reach AGB_MATURITY_KG
# Arid species grow slowly
MATURITY_YEARS = {
    GrowthForm.TREE: 25,
    GrowthForm.SHRUB: 10,
    GrowthForm.GRASS: 3,
    GrowthForm.GROUNDCOVER: 3,
    GrowthForm.CLIMBER: 8,
    GrowthForm.SUCCULENT: 8,
    GrowthForm.MANGROVE: 20,
}


@dataclass
class CarbonResult:
    """Output of a carbon estimation for a species or planting design."""

    species_count: int
    total_individuals: int
    aboveground_carbon_kg: float
    belowground_carbon_kg: float
    total_biomass_carbon_kg: float
    total_biomass_carbon_t: float        # Metric tonnes
    soil_carbon_accumulation_tha_yr: float
    soil_carbon_total_tha: float         # Over maturity period
    co2_equivalent_t: float              # tC × (44/12) = tCO2e
    time_horizon_years: float

    def summary(self) -> str:
        return (
            f"Carbon Estimation\n"
            f"─────────────────\n"
            f"Species: {self.species_count}\n"
            f"Individuals: {self.total_individuals}\n"
            f"Above-ground carbon: {self.aboveground_carbon_kg:.1f} kg C\n"
            f"Below-ground carbon: {self.belowground_carbon_kg:.1f} kg C\n"
            f"Total biomass carbon: {self.total_biomass_carbon_t:.2f} t C\n"
            f"Soil carbon accumulation: {self.soil_carbon_total_tha:.2f} t C/ha\n"
            f"CO₂ equivalent: {self.co2_equivalent_t:.2f} t CO₂e\n"
            f"Time horizon: {self.time_horizon_years:.0f} years"
        )


@dataclass
class CarbonEstimator:
    """
    Estimates carbon sequestration and storage for a planting design.

    Parameters
    ----------
    species_counts : dict[Species, int]
        Mapping of species to number of individuals planted
    site_area_hectares : float
        Total planted area in hectares (for soil carbon scaling)
    ecosystem_type : str
        Ecosystem category for soil carbon rate selection.
        Options: "default", "mangrove", "urban_park", "desert_scrub"
    time_horizon_years : float | None
        Time horizon for carbon estimation. If None, uses the maximum
        maturity period across all species.
    """

    species_counts: dict[Species, int] = field(default_factory=dict)
    site_area_hectares: float = 1.0
    ecosystem_type: str = "urban_park"
    time_horizon_years: float | None = None

    def calculate(self) -> CarbonResult:
        """
        Calculate carbon stocks and sequestration.

        Returns
        -------
        CarbonResult
            Complete carbon estimation
        """
        if not self.species_counts:
            raise ValueError("Species counts dictionary cannot be empty")

        total_individuals = sum(self.species_counts.values())

        # Determine time horizon
        if self.time_horizon_years is not None:
            time_horizon = self.time_horizon_years
        else:
            time_horizon = max(
                MATURITY_YEARS.get(sp.growth_form, 25)
                for sp in self.species_counts
            )

        # ── Above-ground biomass carbon ──────────────────────────────
        agc_kg = 0.0
        bgc_kg = 0.0

        for sp, count in self.species_counts.items():
            agb_maturity = AGB_MATURITY_KG.get(sp.growth_form, 15.0)
            maturity_years = MATURITY_YEARS.get(sp.growth_form, 25)

            # Linear growth assumption: biomass accumulates proportionally
            # to time, capped at maturity biomass
            growth_fraction = min(1.0, time_horizon / maturity_years)
            agb_per_plant = agb_maturity * growth_fraction

            # Apply carbon fraction
            carbon_fraction = CARBON_FRACTION.get(sp.growth_form, 0.47)
            agc_per_plant = agb_per_plant * carbon_fraction

            # Below-ground carbon via root-to-shoot ratio
            root_ratio = ROOT_SHOOT_RATIO.get(sp.growth_form, 0.35)
            bgc_per_plant = agc_per_plant * root_ratio

            agc_kg += agc_per_plant * count
            bgc_kg += bgc_per_plant * count

        total_biomass_c_kg = agc_kg + bgc_kg
        total_biomass_c_t = total_biomass_c_kg / 1000.0

        # ── Soil organic carbon ──────────────────────────────────────
        soc_rate = SOC_ACCUMULATION_RATE_THA_YR.get(
            self.ecosystem_type,
            SOC_ACCUMULATION_RATE_THA_YR["default"]
        )
        soc_total_tha = soc_rate * time_horizon
        # Total soil carbon for the site area
        soc_total_t = soc_total_tha * self.site_area_hectares

        # ── CO₂ equivalent ───────────────────────────────────────────
        # 1 tonne C = 44/12 = 3.67 tonnes CO₂
        total_c_t = total_biomass_c_t + soc_total_t
        co2e_t = total_c_t * (44.0 / 12.0)

        return CarbonResult(
            species_count=len(self.species_counts),
            total_individuals=total_individuals,
            aboveground_carbon_kg=round(agc_kg, 2),
            belowground_carbon_kg=round(bgc_kg, 2),
            total_biomass_carbon_kg=round(total_biomass_c_kg, 2),
            total_biomass_carbon_t=round(total_biomass_c_t, 4),
            soil_carbon_accumulation_tha_yr=round(soc_rate, 4),
            soil_carbon_total_tha=round(soc_total_tha, 4),
            co2_equivalent_t=round(co2e_t, 4),
            time_horizon_years=time_horizon,
        )
