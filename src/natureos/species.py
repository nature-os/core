"""
Species data model — the foundational ecological entity in NatureOS.

Defines plant species with traits relevant to ecological design
in arid and semi-arid environments.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class GrowthForm(str, Enum):
    """Morphological growth form of a species."""
    TREE = "tree"
    SHRUB = "shrub"
    GRASS = "grass"
    GROUNDCOVER = "groundcover"
    CLIMBER = "climber"
    SUCCULENT = "succulent"
    MANGROVE = "mangrove"


class WaterRegime(str, Enum):
    """Irrigation / water requirement category."""
    VERY_LOW = "very_low"       # Rainfall only once established
    LOW = "low"                  # Supplemental irrigation in dry season
    MODERATE = "moderate"        # Regular irrigation
    HIGH = "high"                # Frequent irrigation


class SalinityTolerance(str, Enum):
    """Tolerance to soil / water salinity."""
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    HALOPHYTE = "halophyte"      # Salt-requiring or salt-thriving


class ThermalTolerance(str, Enum):
    """Tolerance to extreme high temperatures."""
    MODERATE = "moderate"        # Up to ~40°C
    HIGH = "high"                # Up to ~45°C
    EXTREME = "extreme"          # Above ~45°C


class EcosystemType(str, Enum):
    """Ecosystem / landscape type where species naturally occur."""
    COASTAL_SABKHA = "coastal_sabkha"
    MANGROVE_WETLAND = "mangrove_wetland"
    MOUNTAIN_WADI = "mountain_wadi"
    DESERT_SCRUB = "desert_scrub"
    URBAN_PARK = "urban_park"


@dataclass
class Species:
    """
    Represents a plant species with ecological traits.

    Attributes
    ----------
    scientific_name : str
        Binomial name (e.g., "Prosopis cineraria")
    common_names : list[str]
        Local / common names (e.g., ["Ghaf"])
    growth_form : GrowthForm
        Morphological form
    water_regime : WaterRegime
        Irrigation requirement category
    salinity_tolerance : SalinityTolerance
        Tolerance to saline conditions
    thermal_tolerance : ThermalTolerance
        Tolerance to extreme heat
    ecosystems : list[EcosystemType]
        Ecosystems where this species naturally occurs
    mature_height_m : Optional[float]
        Typical mature height in meters
    canopy_spread_m : Optional[float]
        Typical canopy spread in meters
    root_depth_m : Optional[float]
        Typical rooting depth in meters
    is_native : bool
        Whether native to the region of application
    wildlife_value : Optional[str]
        Ecological role (pollinator support, bird habitat, etc.)
    carbon_sequestration_potential : Optional[str]
        Qualitative assessment (low / medium / high)
    """

    scientific_name: str
    common_names: list[str] = field(default_factory=list)
    growth_form: GrowthForm = GrowthForm.SHRUB
    water_regime: WaterRegime = WaterRegime.LOW
    salinity_tolerance: SalinityTolerance = SalinityTolerance.MODERATE
    thermal_tolerance: ThermalTolerance = ThermalTolerance.HIGH
    ecosystems: list[EcosystemType] = field(default_factory=list)
    mature_height_m: Optional[float] = None
    canopy_spread_m: Optional[float] = None
    root_depth_m: Optional[float] = None
    is_native: bool = True
    wildlife_value: Optional[str] = None
    carbon_sequestration_potential: Optional[str] = None

    @property
    def display_name(self) -> str:
        """Human-readable display name with common name if available."""
        if self.common_names:
            return f"{self.scientific_name} ({self.common_names[0]})"
        return self.scientific_name
