"""
Water budget engine — estimates irrigation demand for planting designs.

Critical for arid environments where water is the primary constraint.
"""

from dataclasses import dataclass
from natureos.species import Species, WaterRegime
from natureos.site import Site


# Reference evapotranspiration by WaterRegime (mm/year) for arid climate (BWh)
WATER_DEMAND_MM = {
    WaterRegime.VERY_LOW: 200,
    WaterRegime.LOW: 400,
    WaterRegime.MODERATE: 800,
    WaterRegime.HIGH: 1400,
}

ESTABLISHMENT_YEARS = 2


@dataclass
class WaterBudgetResult:
    """Output of a water budget calculation."""
    species_count: int
    total_area_hectares: float
    annual_demand_established_m3: float
    annual_demand_establishment_m3: float
    annual_rainfall_supply_m3: float
    net_irrigation_required_m3: float

    def summary(self) -> str:
        return (
            f"Water Budget Summary\n"
            f"────────────────────\n"
            f"Species: {self.species_count}\n"
            f"Area: {self.total_area_hectares:.1f} ha\n"
            f"Annual irrigation (established): {self.annual_demand_established_m3:.0f} m³\n"
            f"Annual irrigation (establishment): {self.annual_demand_establishment_m3:.0f} m³\n"
            f"Rainfall contribution: {self.annual_rainfall_supply_m3:.0f} m³\n"
            f"Net irrigation required: {self.net_irrigation_required_m3:.0f} m³"
        )


@dataclass
class WaterBudget:
    """
    Estimates irrigation water demand for a species palette on a site.

    Parameters
    ----------
    site : Site
        The site being assessed
    irrigation_efficiency : float
        System efficiency (0.0 to 1.0). Drip ≈ 0.9, sprinkler ≈ 0.75
    """

    site: Site
    irrigation_efficiency: float = 0.85

    def calculate(self, species_list: list[Species]) -> WaterBudgetResult:
        """Calculate water demand for a list of species."""
        if not species_list:
            raise ValueError("Species list cannot be empty")

        total_demand_mm = sum(
            WATER_DEMAND_MM.get(sp.water_regime, 800)
            for sp in species_list
        )
        avg_demand_mm = total_demand_mm / len(species_list)

        area_m2 = self.site.area_hectares * 10_000
        demand_m3 = (avg_demand_mm / 1000) * area_m2
        demand_established_m3 = demand_m3 / self.irrigation_efficiency
        demand_establishment_m3 = demand_established_m3 * 2.0

        rainfall_m = self.site.annual_rainfall_mm / 1000
        rainfall_supply_m3 = rainfall_m * area_m2 * 0.6

        net_irrigation = max(0, demand_established_m3 - rainfall_supply_m3)

        return WaterBudgetResult(
            species_count=len(species_list),
            total_area_hectares=self.site.area_hectares,
            annual_demand_established_m3=demand_established_m3,
            annual_demand_establishment_m3=demand_establishment_m3,
            annual_rainfall_supply_m3=rainfall_supply_m3,
            net_irrigation_required_m3=net_irrigation,
        )
