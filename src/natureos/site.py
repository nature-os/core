"""
Site and habitat data models.

Represents a physical location and its environmental conditions
for ecological design assessment.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ClimateZone(str, Enum):
    """Köppen-Geiger climate classification subset relevant to MENA."""
    BWH = "BWh"   # Arid desert hot
    BWK = "BWk"   # Arid desert cold
    BSH = "BSh"   # Semi-arid hot
    BSK = "BSk"   # Semi-arid cold


class SoilTexture(str, Enum):
    """Soil texture classes."""
    SAND = "sand"
    LOAMY_SAND = "loamy_sand"
    SANDY_LOAM = "sandy_loam"
    LOAM = "loam"
    SILT_LOAM = "silt_loam"
    CLAY = "clay"


class LandUse(str, Enum):
    """Land use categories for designed landscapes."""
    PUBLIC_PARK = "public_park"
    STREETSCAPE = "streetscape"
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    ECOLOGICAL_RESTORATION = "ecological_restoration"
    WETLAND_CONSERVATION = "wetland_conservation"
    DESERT_HABITAT = "desert_habitat"


@dataclass
class SoilProfile:
    """Soil characteristics at a site."""
    texture: SoilTexture = SoilTexture.SANDY_LOAM
    salinity_dsm: float = 0.0          # Electrical conductivity (dS/m)
    organic_matter_pct: float = 0.0    # Organic matter percentage
    ph: float = 7.0                    # Soil pH
    depth_cm: float = 100.0            # Usable soil depth in cm


@dataclass
class Site:
    """
    Represents a physical site for ecological design.

    Attributes
    ----------
    name : str
        Site identifier or project name
    climate_zone : ClimateZone
        Köppen-Geiger climate classification
    soil : SoilProfile
        Soil characteristics
    area_hectares : float
        Total site area in hectares
    land_use : LandUse
        Intended land use category
    annual_rainfall_mm : float
        Average annual rainfall in mm
    max_summer_temp_c : float
        Average maximum summer temperature in °C
    latitude : Optional[float]
        Decimal degrees
    longitude : Optional[float]
        Decimal degrees
    """

    name: str
    climate_zone: ClimateZone = ClimateZone.BWH
    soil: SoilProfile = field(default_factory=SoilProfile)
    area_hectares: float = 0.0
    land_use: LandUse = LandUse.PUBLIC_PARK
    annual_rainfall_mm: float = 100.0
    max_summer_temp_c: float = 45.0
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @property
    def is_arid(self) -> bool:
        """True if the site is in an arid climate zone."""
        return self.climate_zone in {ClimateZone.BWH, ClimateZone.BWK}

    @property
    def is_saline(self) -> bool:
        """True if soil salinity exceeds moderate threshold."""
        return self.soil.salinity_dsm > 4.0
