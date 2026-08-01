"""
Financial constants and jurisdiction presets for NatureOS.

Provides CAPEX/OPEX reference data, water tariffs, soil engineering
costs, and municipal compliance rules for UAE and global jurisdictions.

All costs in AED (UAE Dirham) with USD equivalents. Update with
current market rates for production use.

Sources: Dubai Municipality, DEWA, Abu Dhabi UPC Estidama,
         LEED v4, Green Riyadh Program, RSMeans.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ── Jurisdictions ────────────────────────────────────────────────────

class Jurisdiction(str, Enum):
    """Supported regulatory jurisdictions."""
    DUBAI_MUNICIPALITY = "dubai_municipality"
    ABU_DHABI_ESTIDAMA = "abu_dhabi_estidama"
    SAUDI_GREEN_RIYADH = "saudi_green_riyadh"
    LEED_V4 = "leed_v4"
    SITES_V2 = "sites_v2"
    GENERIC = "generic"


# ── Water Tariffs (AED per m³) ──────────────────────────────────────

WATER_TARIFFS = {
    Jurisdiction.DUBAI_MUNICIPALITY: {
        "potable": 3.5,       # AED/m³ — DEWA commercial rate
        "tse": 0.8,           # Treated Sewage Effluent — subsidized
        "tse_availability": True,
    },
    Jurisdiction.ABU_DHABI_ESTIDAMA: {
        "potable": 3.2,
        "tse": 0.6,
        "tse_availability": True,
    },
    Jurisdiction.SAUDI_GREEN_RIYADH: {
        "potable": 2.8,
        "tse": 0.5,
        "tse_availability": True,
    },
    Jurisdiction.LEED_V4: {
        "potable": 2.5,       # US average commercial rate
        "tse": 1.2,
        "tse_availability": False,
    },
    Jurisdiction.GENERIC: {
        "potable": 3.0,
        "tse": 1.0,
        "tse_availability": False,
    },
}


# ── Soil Engineering Costs (AED) ─────────────────────────────────────

SOIL_VAULT_COST_PER_M3 = 320.0      # Soil cell suspended pavement system
ROOT_BARRIER_COST_PER_LM = 85.0     # Per linear meter, 1.2m depth
STANDARD_SOIL_COST_PER_M3 = 45.0    # Uncompacted planting soil
IRRIGATION_HOOKUP_COST = 3500.0     # Per connection point
TREE_STAKING_COST = 120.0           # Per tree


# ── Nursery & Planting CAPEX (AED per plant) ─────────────────────────

# Costs vary by container size / maturity
NURSERY_COSTS = {
    "tree_2m_container": 850.0,      # 2m height, container-grown
    "tree_3m_rootball": 2200.0,      # 3m height, rootball
    "shrub_1g": 12.0,                # 1-gallon shrub
    "shrub_5g": 35.0,                # 5-gallon shrub
    "groundcover_plug": 3.5,         # Plug tray
    "grass_seed_m2": 2.0,            # Per m² seeded
    "grass_sod_m2": 8.0,             # Per m² sod
}

PLANTING_LABOR_COST = {
    "tree": 180.0,                   # Per tree installation
    "shrub": 15.0,                   # Per shrub installation
    "groundcover": 2.0,              # Per plug installation
    "grass_m2": 5.0,                 # Per m² installation
}


# ── Maintenance OPEX (AED per plant per year) ────────────────────────

ANNUAL_MAINTENANCE_COST = {
    "tree_established": 250.0,       # Pruning, pest, mulching
    "tree_establishment": 450.0,     # First 2 years — intensive
    "shrub": 35.0,
    "groundcover": 8.0,
    "grass_m2": 12.0,
}


# ── Municipal Compliance Rules ───────────────────────────────────────

@dataclass
class ComplianceRule:
    """A single municipal compliance requirement."""
    rule_id: str
    description: str
    requirement: str               # e.g., ">= 60", "<= 0.5"
    unit: str                       # %, m³/m²/yr, count
    pass_message: str
    fail_message: str


@dataclass
class JurisdictionRules:
    """All compliance rules for a jurisdiction."""
    jurisdiction: Jurisdiction
    name: str
    rules: list[ComplianceRule] = field(default_factory=list)
    native_species_quota_pct: float = 0.0
    max_water_use_m3_m2_yr: float = 999.0
    min_canopy_cover_pct: float = 0.0
    min_biodiversity_shannon: float = 0.0


# ── Jurisdiction Presets ─────────────────────────────────────────────

DUBAI_MUNICIPALITY_RULES = JurisdictionRules(
    jurisdiction=Jurisdiction.DUBAI_MUNICIPALITY,
    name="Dubai Municipality — Urban Forest Regulations",
    native_species_quota_pct=60.0,
    max_water_use_m3_m2_yr=0.5,
    min_canopy_cover_pct=25.0,
    min_biodiversity_shannon=1.0,
    rules=[
        ComplianceRule(
            rule_id="DM-NAT-001",
            description="Native Species Quota",
            requirement=">= 60%",
            unit="%",
            pass_message="Native species ratio meets DM minimum (≥60%).",
            fail_message="Increase native species. Current ratio below DM 60% minimum.",
        ),
        ComplianceRule(
            rule_id="DM-WAT-001",
            description="Water Budget Threshold",
            requirement="<= 0.5 m³/m²/yr",
            unit="m³/m²/yr",
            pass_message="Water budget within DM arid zone efficiency cap.",
            fail_message="Water budget exceeds DM 0.5 m³/m²/yr efficiency threshold.",
        ),
        ComplianceRule(
            rule_id="DM-CAN-001",
            description="Minimum Canopy Cover",
            requirement=">= 25%",
            unit="%",
            pass_message="Canopy cover meets DM minimum for public parks.",
            fail_message="Canopy cover below DM 25% minimum. Add more trees.",
        ),
        ComplianceRule(
            rule_id="DM-BIO-001",
            description="Biodiversity Minimum",
            requirement=">= 1.0 Shannon",
            unit="H'",
            pass_message="Shannon diversity meets DM ecological minimum.",
            fail_message="Increase species diversity. Shannon index below DM 1.0 minimum.",
        ),
    ],
)

ABU_DHABI_ESTIDAMA_RULES = JurisdictionRules(
    jurisdiction=Jurisdiction.ABU_DHABI_ESTIDAMA,
    name="Abu Dhabi — Estidama Pearl Rating (PW-2, NS-1)",
    native_species_quota_pct=50.0,
    max_water_use_m3_m2_yr=0.4,
    min_canopy_cover_pct=30.0,
    min_biodiversity_shannon=1.2,
    rules=[
        ComplianceRule(
            rule_id="EST-PW2-001",
            description="Water Efficient Landscaping (Credit PW-2)",
            requirement=">= 50% reduction vs baseline",
            unit="%",
            pass_message="Meets Estidama PW-2 water reduction credit.",
            fail_message="Does not meet PW-2 50% water reduction threshold.",
        ),
        ComplianceRule(
            rule_id="EST-NS1-001",
            description="Natural Systems — Native Species (Credit NS-1)",
            requirement=">= 50% native",
            unit="%",
            pass_message="Meets Estidama NS-1 native species requirement.",
            fail_message="Native species below Estidama NS-1 50% threshold.",
        ),
    ],
)

LEED_V4_RULES = JurisdictionRules(
    jurisdiction=Jurisdiction.LEED_V4,
    name="LEED v4 — WE & SS Credits",
    native_species_quota_pct=30.0,
    max_water_use_m3_m2_yr=0.6,
    min_canopy_cover_pct=20.0,
    min_biodiversity_shannon=0.8,
    rules=[
        ComplianceRule(
            rule_id="LEED-WE-001",
            description="Outdoor Water Use Reduction (WE Credit)",
            requirement=">= 30% reduction vs baseline",
            unit="%",
            pass_message="Meets LEED WE outdoor water reduction credit.",
            fail_message="Water use reduction below LEED 30% threshold.",
        ),
        ComplianceRule(
            rule_id="LEED-SS-001",
            description="Habitat Restoration (SS Credit)",
            requirement=">= 30% native",
            unit="%",
            pass_message="Meets LEED SS habitat restoration credit threshold.",
            fail_message="Increase native species for LEED SS credit eligibility.",
        ),
    ],
)

SAUDI_GREEN_RIYADH_RULES = JurisdictionRules(
    jurisdiction=Jurisdiction.SAUDI_GREEN_RIYADH,
    name="Saudi Arabia — Green Riyadh Program",
    native_species_quota_pct=70.0,
    max_water_use_m3_m2_yr=0.3,
    min_canopy_cover_pct=35.0,
    min_biodiversity_shannon=1.5,
    rules=[
        ComplianceRule(
            rule_id="SGR-NAT-001",
            description="High-Density Native Planting",
            requirement=">= 70% native",
            unit="%",
            pass_message="Exceeds Green Riyadh native species requirement.",
            fail_message="Increase native species to meet Green Riyadh 70% target.",
        ),
        ComplianceRule(
            rule_id="SGR-WAT-001",
            description="Extreme Drought Water Budget",
            requirement="<= 0.3 m³/m²/yr",
            unit="m³/m²/yr",
            pass_message="Within Green Riyadh extreme drought water allocation.",
            fail_message="Reduce water demand to meet Green Riyadh 0.3 m³/m²/yr cap.",
        ),
    ],
)

# Jurisdiction lookup
JURISDICTION_PRESETS = {
    Jurisdiction.DUBAI_MUNICIPALITY: DUBAI_MUNICIPALITY_RULES,
    Jurisdiction.ABU_DHABI_ESTIDAMA: ABU_DHABI_ESTIDAMA_RULES,
    Jurisdiction.LEED_V4: LEED_V4_RULES,
    Jurisdiction.SAUDI_GREEN_RIYADH: SAUDI_GREEN_RIYADH_RULES,
    Jurisdiction.SITES_V2: LEED_V4_RULES,  # Similar thresholds
    Jurisdiction.GENERIC: DUBAI_MUNICIPALITY_RULES,  # Default to DM
}


# ── Green Building Credit Estimator ──────────────────────────────────

@dataclass
class GreenBuildingCredits:
    """Estimated green building certification credits."""
    jurisdiction: Jurisdiction
    credits_achieved: list[str] = field(default_factory=list)
    credits_potential: list[str] = field(default_factory=list)
    rating_impact: str = ""

    def summary(self) -> str:
        achieved = "\n".join(f"  ✓ {c}" for c in self.credits_achieved)
        potential = "\n".join(f"  ○ {c}" for c in self.credits_potential)
        return (
            f"Green Building Credits — {self.jurisdiction.value}\n"
            f"{'─' * 45}\n"
            f"Achieved:\n{achieved}\n\n"
            f"Within Reach:\n{potential}\n\n"
            f"Rating Impact: {self.rating_impact}"
        )


# ── Carbon Credit Value ──────────────────────────────────────────────

CARBON_CREDIT_PRICE_PER_TCO2E = 25.0  # USD — voluntary carbon market avg
