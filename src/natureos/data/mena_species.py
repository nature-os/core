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


# ── Expanded MENA species (v0.2) ────────────────────────────────────

Salvia_spinosa = Species(
    scientific_name="Salvia spinosa",
    common_names=["Spiny Sage"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.MOUNTAIN_WADI,
        EcosystemType.DESERT_SCRUB,
    ],
    mature_height_m=0.5,
    canopy_spread_m=0.6,
    root_depth_m=1.5,
    is_native=True,
    wildlife_value="Aromatic foliage attracts pollinators; seeds support granivorous birds.",
    carbon_sequestration_potential="low",
)

Ochradenus_baccatus = Species(
    scientific_name="Ochradenus baccatus",
    common_names=["Taily Weed", "Qurraya"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.MOUNTAIN_WADI,
        EcosystemType.DESERT_SCRUB,
    ],
    mature_height_m=1.5,
    canopy_spread_m=1.5,
    root_depth_m=3.0,
    is_native=True,
    wildlife_value="Berries eaten by birds and small mammals; drought-deciduous adaptation.",
    carbon_sequestration_potential="low",
)

Calotropis_procera = Species(
    scientific_name="Calotropis procera",
    common_names=["Sodom's Apple", "Ushar"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.COASTAL_SABKHA,
    ],
    mature_height_m=3.0,
    canopy_spread_m=2.5,
    root_depth_m=4.0,
    is_native=True,
    wildlife_value="Host plant for monarch butterfly relatives; fibrous bark used by birds for nesting.",
    carbon_sequestration_potential="medium",
)

Moringa_peregrina = Species(
    scientific_name="Moringa peregrina",
    common_names=["Wild Moringa", "Yasar"],
    growth_form=GrowthForm.TREE,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.MOUNTAIN_WADI,
    ],
    mature_height_m=5.0,
    canopy_spread_m=4.0,
    root_depth_m=8.0,
    is_native=True,
    wildlife_value="Seeds produce valuable oil; flowers attract bees; drought-resistant pioneer species.",
    carbon_sequestration_potential="medium",
)

Fagonia_indica = Species(
    scientific_name="Fagonia indica",
    common_names=["Dhamasa"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
    ],
    mature_height_m=0.3,
    canopy_spread_m=0.5,
    root_depth_m=1.0,
    is_native=True,
    wildlife_value="Ground-level cover in extreme desert; flowers provide nectar for small insects.",
    carbon_sequestration_potential="low",
)

Rhazya_stricta = Species(
    scientific_name="Rhazya stricta",
    common_names=["Harmal"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.MOUNTAIN_WADI,
    ],
    mature_height_m=1.0,
    canopy_spread_m=1.2,
    root_depth_m=2.5,
    is_native=True,
    wildlife_value="Drought-tolerant evergreen shrub; provides year-round cover in arid landscapes.",
    carbon_sequestration_potential="low",
)

Capparis_spinosa = Species(
    scientific_name="Capparis spinosa",
    common_names=["Caper Bush", "Shafallah"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.HIGH,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.MOUNTAIN_WADI,
        EcosystemType.COASTAL_SABKHA,
    ],
    mature_height_m=0.5,
    canopy_spread_m=1.5,
    root_depth_m=3.0,
    is_native=True,
    wildlife_value="Edible flower buds; flowers attract pollinators; deep-rooted soil stabilizer.",
    carbon_sequestration_potential="low",
)

Tamarix_aphylla = Species(
    scientific_name="Tamarix aphylla",
    common_names=["Athel Tree", "Tarfah"],
    growth_form=GrowthForm.TREE,
    water_regime=WaterRegime.LOW,
    salinity_tolerance=SalinityTolerance.HIGH,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.COASTAL_SABKHA,
        EcosystemType.DESERT_SCRUB,
        EcosystemType.URBAN_PARK,
    ],
    mature_height_m=10.0,
    canopy_spread_m=6.0,
    root_depth_m=12.0,
    is_native=True,
    wildlife_value="Windbreak and shade tree; salt-tolerant pioneer; habitat for birds in saline environments.",
    carbon_sequestration_potential="high",
)

Ziziphus_nummularia = Species(
    scientific_name="Ziziphus nummularia",
    common_names=["Wild Jujube"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
    ],
    mature_height_m=2.0,
    canopy_spread_m=2.5,
    root_depth_m=4.0,
    is_native=True,
    wildlife_value="Thorny thicket provides protective nesting sites; fruits eaten by birds and mammals.",
    carbon_sequestration_potential="medium",
)

Cenchrus_ciliaris = Species(
    scientific_name="Cenchrus ciliaris",
    common_names=["Buffel Grass", "Sabat"],
    growth_form=GrowthForm.GRASS,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.MOUNTAIN_WADI,
        EcosystemType.URBAN_PARK,
    ],
    mature_height_m=0.8,
    canopy_spread_m=0.5,
    root_depth_m=2.0,
    is_native=True,
    wildlife_value="Key forage grass for wildlife and livestock; soil stabilizer; fire-resistant.",
    carbon_sequestration_potential="low",
)

Pennisetum_divisum = Species(
    scientific_name="Pennisetum divisum",
    common_names=["Desert Fountain Grass"],
    growth_form=GrowthForm.GRASS,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.LOW,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.MOUNTAIN_WADI,
    ],
    mature_height_m=1.0,
    canopy_spread_m=0.8,
    root_depth_m=1.5,
    is_native=True,
    wildlife_value="Ornamental native grass; seeds for granivorous birds; dune stabilization.",
    carbon_sequestration_potential="low",
)

Salsola_imbricata = Species(
    scientific_name="Salsola imbricata",
    common_names=["Salt Wort", "Hamd"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.HALOPHYTE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.COASTAL_SABKHA,
        EcosystemType.DESERT_SCRUB,
    ],
    mature_height_m=0.5,
    canopy_spread_m=0.8,
    root_depth_m=1.5,
    is_native=True,
    wildlife_value="Halophytic pioneer species; stabilizes saline soils; forage for camels.",
    carbon_sequestration_potential="low",
)

Arthrocnemum_macrostachyum = Species(
    scientific_name="Arthrocnemum macrostachyum",
    common_names=["Glasswort"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.HIGH,
    salinity_tolerance=SalinityTolerance.HALOPHYTE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.COASTAL_SABKHA,
        EcosystemType.MANGROVE_WETLAND,
    ],
    mature_height_m=0.6,
    canopy_spread_m=0.5,
    root_depth_m=1.0,
    is_native=True,
    wildlife_value="Critical salt marsh species; provides microhabitat for intertidal invertebrates; carbon sink in coastal sediments.",
    carbon_sequestration_potential="medium",
)

Suaeda_vermiculata = Species(
    scientific_name="Suaeda vermiculata",
    common_names=["Seablite", "Suwaid"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.LOW,
    salinity_tolerance=SalinityTolerance.HALOPHYTE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.COASTAL_SABKHA,
    ],
    mature_height_m=0.8,
    canopy_spread_m=1.0,
    root_depth_m=2.0,
    is_native=True,
    wildlife_value="Dominant shrub in saline coastal plains; provides cover for ground-nesting birds.",
    carbon_sequestration_potential="low",
)

Bassia_muricata = Species(
    scientific_name="Bassia muricata",
    common_names=["Spiny Bassia"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.HIGH,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.COASTAL_SABKHA,
    ],
    mature_height_m=0.4,
    canopy_spread_m=0.6,
    root_depth_m=1.0,
    is_native=True,
    wildlife_value="Annual pioneer on disturbed saline soils; rapid ground cover establishment.",
    carbon_sequestration_potential="low",
)

Convolvulus_prostratus = Species(
    scientific_name="Convolvulus prostratus",
    common_names=["Desert Bindweed"],
    growth_form=GrowthForm.GROUNDCOVER,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.URBAN_PARK,
    ],
    mature_height_m=0.15,
    canopy_spread_m=1.0,
    root_depth_m=0.8,
    is_native=True,
    wildlife_value="Prostrate groundcover with showy white flowers; attracts pollinators; suitable for green roof and xeriscape.",
    carbon_sequestration_potential="low",
)

Teucrium_stocksianum = Species(
    scientific_name="Teucrium stocksianum",
    common_names=["Desert Germander"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.LOW,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.MOUNTAIN_WADI,
    ],
    mature_height_m=0.3,
    canopy_spread_m=0.4,
    root_depth_m=1.0,
    is_native=True,
    wildlife_value="Aromatic dwarf shrub of Hajar Mountain wadis; bee forage species.",
    carbon_sequestration_potential="low",
)

Gaillonia_aucheri = Species(
    scientific_name="Gaillonia aucheri",
    common_names=["Mountain Gaillonia"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.LOW,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.MOUNTAIN_WADI,
    ],
    mature_height_m=0.5,
    canopy_spread_m=0.6,
    root_depth_m=1.5,
    is_native=True,
    wildlife_value="Endemic to Hajar Mountains; stabilizes rocky wadi slopes; nectar source for native bees.",
    carbon_sequestration_potential="low",
)

Pulicaria_glutinosa = Species(
    scientific_name="Pulicaria glutinosa",
    common_names=["Sticky Fleabane"],
    growth_form=GrowthForm.SHRUB,
    water_regime=WaterRegime.VERY_LOW,
    salinity_tolerance=SalinityTolerance.MODERATE,
    thermal_tolerance=ThermalTolerance.EXTREME,
    ecosystems=[
        EcosystemType.DESERT_SCRUB,
        EcosystemType.MOUNTAIN_WADI,
    ],
    mature_height_m=0.6,
    canopy_spread_m=0.7,
    root_depth_m=1.5,
    is_native=True,
    wildlife_value="Yellow daisy-like flowers attract desert butterflies; aromatic foliage; drought-deciduous.",
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
    # v0.2 additions
    Salvia_spinosa,
    Ochradenus_baccatus,
    Calotropis_procera,
    Moringa_peregrina,
    Fagonia_indica,
    Rhazya_stricta,
    Capparis_spinosa,
    Tamarix_aphylla,
    Ziziphus_nummularia,
    Cenchrus_ciliaris,
    Pennisetum_divisum,
    Salsola_imbricata,
    Arthrocnemum_macrostachyum,
    Suaeda_vermiculata,
    Bassia_muricata,
    Convolvulus_prostratus,
    Teucrium_stocksianum,
    Gaillonia_aucheri,
    Pulicaria_glutinosa,
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
