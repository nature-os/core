"""
MENA species dataset — UAE and Arabian Peninsula native plants.

Structured ecological data for species used in landscape design,
ecological restoration, and conservation in arid environments.

Data sources: Environment Agency – Abu Dhabi, Dubai Municipality,
International Centre for Biosaline Agriculture (ICBA), field observation.
"""

from natureos.species import (
    Species, GrowthForm, WaterRegime,
    SalinityTolerance, ThermalTolerance, EcosystemType
)


# ── UAE Native & Regionally Adapted Species ──────────────────────────

Prosopis_cineraria = Species(
    scientific_name="Prosopis cineraria",
    common_names=["Ghaf"],
    growth_form=GrowthForm.TREE,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.MOUNTAIN_WADI,
        EcosystemType.URBAN_PARK
    ],
    mature_height_m=8.0,
    canopy_spread_m=10.0,
    root_depth_m=15.0,
    is_native=True,
    wildlife_value="Keystone species — provides shade, fodder, and habitat for birds and insects",
    carbon_sequestration_potential="high",
)

Ziziphus_spina_christi = Species(
    scientific_name="Ziziphus spina-christi",
    common_names=["Sidr"],
    growth_form=GrowthForm.TREE,
    water_regime=WaterRegime.LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.HIGH,
    ecosystems=[
        EcosystemType.MOUNTAIN_WADI,
        EcosystemType.URBAN_PARK
    ],
    mature_height_m=6.0,
    canopy_spread_m=7.0,
    root_depth_m=10.0,
    is_native=True,
    wildlife_value="Important pollinator species — attracts bees; fruits support birds",
    carbon_sequestration_potential="medium",
)

Acacia_tortilis = Species(
    scientific_name="Acacia tortilis",
    common_names=["Samr"],
    growth_form=GrowthForm.TREE,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.MOUNTAIN_WADI
    ],
    mature_height_m=5.0,
    canopy_spread_m=8.0,
    root_depth_m=12.0,
    is_native=True,
    wildlife_value="Nitrogen-fixing — improves soil fertility; provides browse and shade",
    carbon_sequestration_potential="medium",
)

Avicennia_marina = Species(
    scientific_name="Avicennia marina",
    common_names=["Grey Mangrove"],
    growth_form=GrowthForm.MANGROVE,
    water_regime=WaterRegime.HIGH,
    salinity_tolerance=SalinityTolerance.HALOPHYTE,
    thermal_tolerance=ThermalTolerance.HIGH,
    ecosystems=[
        EcosystemType.MANGROVE_WETLAND,
        EcosystemType.COASTAL_SABKHA
    ],
    mature_height_m=4.0,
    canopy_spread_m=5.0,
    root_depth_m=3.0,
    is_native=True,
    wildlife_value="Critical coastal habitat — nursery for fish, supports migratory birds, shoreline stabilization",
    carbon_sequestration_potential="high",
)

Phoenix_dactylifera = Species(
    scientific_name="Phoenix dactylifera",
    common_names=["Date Palm"],
    growth_form=GrowthForm.TREE,
    water_regime=WaterRegime.MODERATE,
    salinity_tolerance=SalinityTolerance.HIGH,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.URBAN_PARK
    ],
    mature_height_m=20.0,
    canopy_spread_m=6.0,
    root_depth_m=6.0,
    is_native=False,  # Naturalized — culturally integral
    wildlife_value="Provides fruit, shade, and roosting habitat",
    carbon_sequestration_potential="medium",
)

Calligonum_comosum = Species(
    scientific_name="Calligonum comosum",
    common_names=["Arta"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB
    ],
    mature_height_m=2.0,
    canopy_spread_m=2.5,
    root_depth_m=5.0,
    is_native=True,
    wildlife_value="Dune stabilization; provides forage for camels and wildlife",
    carbon_sequestration_potential="low",
)

Haloxylon_salicornicum = Species(
    scientific_name="Haloxylon salicornicum",
    common_names=["Rimth"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.HIGH,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.COASTAL_SABKHA
    ],
    mature_height_m=1.0,
    canopy_spread_m=1.5,
    root_depth_m=3.0,
    is_native=True,
    wildlife_value="Provides ground cover in extreme conditions; grazing for small mammals",
    carbon_sequestration_potential="low",
)

Lycium_shawii = Species(
    scientific_name="Lycium shawii",
    common_names=["Desert Thorn"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.MOUNTAIN_WADI
    ],
    mature_height_m=1.5,
    canopy_spread_m=2.0,
    root_depth_m=4.0,
    is_native=True,
    wildlife_value="Berries attract birds; thorny cover provides nesting protection",
    carbon_sequestration_potential="low",
)

Aerva_javanica = Species(
    scientific_name="Aerva javanica",
    common_names=["Desert Cotton"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB
    ],
    mature_height_m=0.8,
    canopy_spread_m=1.0,
    root_depth_m=2.0,
    is_native=True,
    wildlife_value="Seasonal ground cover; seeds support granivorous birds",
    carbon_sequestration_potential="low",
)

Leptadenia_pyrotechnica = Species(
    scientific_name="Leptadenia pyrotechnica",
    common_names=["Markh"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.LOW,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB
    ],
    mature_height_m=2.5,
    canopy_spread_m=2.0,
    root_depth_m=6.0,
    is_native=True,
    wildlife_value="Deep-rooted shrub stabilizing sandy soils; browse for camels",
    carbon_sequestration_potential="low",
)

Tephrosia_apollinea = Species(
    scientific_name="Tephrosia apollinea",
    common_names=["Dhafra"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.MOUNTAIN_WADI
    ],
    mature_height_m=0.6,
    canopy_spread_m=0.8,
    root_depth_m=2.0,
    is_native=True,
    wildlife_value="Nitrogen-fixing legume; improves soil; attracts pollinators",
    carbon_sequestration_potential="low",
)

# ── Species collections ──────────────────────────────────────────────

ALL_SPECIES = [
    Prosopis_cineraria,
    Ziziphus_spina_christi,
    Acacia_tortilis,
    Avicennia_marina,
    Phoenix_dactylifera,
    Calligonum_comosum,
    Haloxylon_salicornicum,
    Lycium_shawii,
    Aerva_javanica,
    Leptadenia_pyrotechnica,
    Tephrosia_apollinea,
]


def species_by_ecosystem(ecosystem: EcosystemType) -> list[Species]:
    """Return all species associated with a given ecosystem type."""
    return [s for s in ALL_SPECIES if ecosystem in s.ecosystems]


def native_species() -> list[Species]:
    """Return only species native to the MENA region."""
    return [s for s in ALL_SPECIES if s.is_native]


def low_water_species() -> list[Species]:
    """Return species with VERY_LOW or LOW water regime."""
    return [
        s for s in ALL_SPECIES
        if s.water_regime in {WaterRegime.VERY_LOW, WaterRegime.LOW}
    ]
