"""
Urban Heat Mitigation engine - estimates cooling effects of vegetation
in urban landscapes.

Models two primary cooling mechanisms:
1. Shade provision - reduction in surface temperature beneath canopy
2. Evapotranspirative cooling - latent heat flux from plant transpiration

For arid urban environments, these effects can reduce local ambient
temperature by 2-8°C and surface temperature by 10-25°C.

References:
- Oke, T.R. (1989). The micrometeorology of the urban forest.
- Rahman, M.A. et al. (2017). A model of shading and evapotranspirative
  cooling by urban trees.
- Shashua-Bar, L. & Hoffman, M.E. (2000). Vegetation as a climatic
  component in the design of an urban street.
"""

from dataclasses import dataclass, field
from natureos.species import Species, GrowthForm
import math


# ── Cooling parameters by growth form ─────────────────────────────────

# Typical canopy area at maturity (m²)
CANOPY_AREA_M2 = {
    GrowthForm.TREE: 50.0,        # ~8m diameter crown
    GrowthForm.SHRUB: 8.0,        # ~3m diameter
    GrowthForm.GROUNDCOVER: 2.0,  # ~1.6m diameter
    GrowthForm.GRASS: 1.0,
    GrowthForm.MANGROVE: 30.0,    # ~6m diameter
    GrowthForm.SUCCULENT: 1.0,
    GrowthForm.CLIMBER: 5.0,
}

# Shade cooling intensity (°C reduction in surface temperature beneath canopy)
# Depends on canopy density and leaf area index
SHADE_COOLING_DELTA_C = {
    GrowthForm.TREE: 15.0,         # Dense canopy — significant surface cooling
    GrowthForm.SHRUB: 8.0,
    GrowthForm.GROUNDCOVER: 4.0,
    GrowthForm.GRASS: 3.0,
    GrowthForm.MANGROVE: 12.0,
    GrowthForm.SUCCULENT: 2.0,
    GrowthForm.CLIMBER: 6.0,
}

# Evapotranspiration rate (mm/day) during summer for established plants
# Arid-adapted species have lower ET rates than temperate species
ET_RATE_MM_DAY = {
    GrowthForm.TREE: 4.0,
    GrowthForm.SHRUB: 2.0,
    GrowthForm.GROUNDCOVER: 1.5,
    GrowthForm.GRASS: 3.0,         # Grass can have high ET if irrigated
    GrowthForm.MANGROVE: 6.0,
    GrowthForm.SUCCULENT: 0.5,     # CAM photosynthesis — very low ET
    GrowthForm.CLIMBER: 2.5,
}

# Latent heat of vaporization (MJ per mm of water over 1 m²)
# 1 mm water over 1 m² = 1 litre = 1 kg
# Latent heat of vaporization = ~2.45 MJ/kg at 20°C
LATENT_HEAT_MJ_PER_MM_M2 = 2.45

# Specific heat capacity of air (MJ/kg·K) — for estimating ambient cooling
# Rough conversion: 1 MJ of latent heat flux cools ~340 m³ of air by 1°C
AIR_VOLUME_COOLED_PER_MJ = 340.0  # m³ of air cooled by 1°C per MJ


@dataclass
class HeatMitigationResult:
    """Output of urban heat mitigation assessment."""

    species_count: int
    total_individuals: int
    total_canopy_area_m2: float
    canopy_cover_pct: float               # % of site area covered by canopy
    shade_cooled_area_m2: float
    avg_surface_cooling_c: float           # Weighted average °C reduction
    daily_et_volume_m3: float              # Total evapotranspiration (m³/day)
    daily_latent_heat_mj: float            # Latent heat flux (MJ/day)
    ambient_cooling_volume_m3: float       # Volume of air cooled by 1°C
    cooling_capacity_kw: float             # Equivalent cooling power in kW

    def summary(self) -> str:
        return (
            f"Urban Heat Mitigation Assessment\n"
            f"────────────────────────────────\n"
            f"Species: {self.species_count}\n"
            f"Individuals: {self.total_individuals}\n"
            f"Canopy cover: {self.canopy_cover_pct:.1f}% of site\n"
            f"Avg surface cooling: {self.avg_surface_cooling_c:.1f}°C\n"
            f"Daily ET: {self.daily_et_volume_m3:.1f} m³\n"
            f"Daily latent heat: {self.daily_latent_heat_mj:.0f} MJ\n"
            f"Equivalent cooling: {self.cooling_capacity_kw:.1f} kW"
        )


@dataclass
class UrbanHeatMitigation:
    """
    Estimates cooling effects of vegetation in urban landscapes.

    Parameters
    ----------
    species_counts : dict[Species, int]
        Mapping of species to number of individuals planted
    site_area_m2 : float
        Total site area in square meters
    """

    species_counts: dict[Species, int] = field(default_factory=dict)
    site_area_m2: float = 10000.0  # Default: 1 hectare

    def assess(self) -> HeatMitigationResult:
        """
        Calculate heat mitigation metrics.

        Returns
        -------
        HeatMitigationResult
            Complete cooling assessment
        """
        if not self.species_counts:
            raise ValueError("Species counts dictionary cannot be empty")

        total_individuals = sum(self.species_counts.values())

        # ── Canopy area and shade cooling ────────────────────────────
        total_canopy_area = 0.0
        weighted_cooling_sum = 0.0

        for sp, count in self.species_counts.items():
            canopy_per_plant = CANOPY_AREA_M2.get(sp.growth_form, 2.0)
            species_canopy = canopy_per_plant * count
            total_canopy_area += species_canopy

            cooling_per_plant = SHADE_COOLING_DELTA_C.get(sp.growth_form, 4.0)
            weighted_cooling_sum += cooling_per_plant * species_canopy

        avg_surface_cooling = (
            weighted_cooling_sum / total_canopy_area
            if total_canopy_area > 0 else 0.0
        )

        # Canopy cover as percentage of site area
        canopy_cover_pct = (total_canopy_area / self.site_area_m2) * 100

        # Shade-cooled area (area directly under canopies)
        shade_cooled_area = min(total_canopy_area, self.site_area_m2)

        # ── Evapotranspirative cooling ───────────────────────────────
        daily_et_m3 = 0.0

        for sp, count in self.species_counts.items():
            canopy_per_plant = CANOPY_AREA_M2.get(sp.growth_form, 2.0)
            et_rate = ET_RATE_MM_DAY.get(sp.growth_form, 2.0)

            # ET volume = rate (mm/day) × area (m²) / 1000 (convert mm to m)
            et_per_plant_m3 = (et_rate / 1000) * canopy_per_plant
            daily_et_m3 += et_per_plant_m3 * count

        # Latent heat flux
        # 1 mm of water over 1 m² = 1 kg water evaporated
        # Energy = mass × latent heat of vaporization
        # daily_et_m3 = daily_et in m³ = daily_et in tonnes of water (1 m³ = 1000 kg)
        daily_et_kg = daily_et_m3 * 1000  # kg of water
        daily_latent_heat_mj = daily_et_kg * LATENT_HEAT_MJ_PER_MM_M2

        # Ambient cooling: how much air volume is cooled by 1°C
        ambient_cooling_volume = daily_latent_heat_mj * AIR_VOLUME_COOLED_PER_MJ

        # Equivalent cooling power (kW)
        # Daily MJ / seconds per day = MW, then × 1000 = kW
        cooling_capacity_kw = (daily_latent_heat_mj / 86400) * 1000

        return HeatMitigationResult(
            species_count=len(self.species_counts),
            total_individuals=total_individuals,
            total_canopy_area_m2=round(total_canopy_area, 2),
            canopy_cover_pct=round(canopy_cover_pct, 2),
            shade_cooled_area_m2=round(shade_cooled_area, 2),
            avg_surface_cooling_c=round(avg_surface_cooling, 2),
            daily_et_volume_m3=round(daily_et_m3, 4),
            daily_latent_heat_mj=round(daily_latent_heat_mj, 2),
            ambient_cooling_volume_m3=round(ambient_cooling_volume, 2),
            cooling_capacity_kw=round(cooling_capacity_kw, 2),
        )
