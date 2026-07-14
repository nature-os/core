NatureOS Core

Open infrastructure for computational ecology. The ecological equivalent of GDAL or OpenStreetMap a foundation others build upon.

NatureOS Core provides the reusable building blocks: data models, computational engines, and AI reasoning pipelines that architects, developers, researchers, landscape architects, urban planners, municipalities and governments need to build software that designs living ecosystems instead of decorative landscapes.

Vision
The future of cities and landscapes should be designed as interconnected ecosystems.

Why NatureOS Exists
The world has open infrastructure for geography (GDAL, OpenStreetMap), for scientific computing (NumPy, SciPy), and for machine learning (PyTorch, scikit-learn).

There is no equivalent for computational ecology.

The Problem We're Solving 
Modern design software is extraordinarily capable at geometry, visualization, and construction documentation. But ecological intelligence knowing which species will thrive where, how much water they'll need, how they'll interact, what biodiversity value they'll create - remains fragmented across:

- Scientific papers locked behind paywalls
- Proprietary software with closed data models
- Local expertise trapped in consultancies and individual practitioners
- Static PDF planting guides that can't be queried or composed

There is no open, programmatic, composable foundation for computational ecology in the built environment.
NatureOS Core is being built to become that foundation.
NatureOS is infrastructure designed to be integrated into GIS platforms, CAD tools, AI co-pilots, municipal dashboards, and digital twins.


What NatureOS Provides

Computational Engines

Seven deterministic, testable, scientifically-grounded engines:

| Engine | What It Computes |
|--------|------------------|
| `HabitatSuitability` | Which species fit a site's climate, soil, and ecology |
| `WaterBudget` | Irrigation demand for any planting design |
| `BiodiversityIndex` | Shannon, Simpson, evenness, and native ratios |
| `CarbonEstimator` | Biomass and soil carbon sequestration over time |
| `SpeciesInteraction` | Compatibility, competition, and facilitation between species |
| `UrbanHeatMitigation` | Shade provision and evapotranspirative cooling |
| `DesignOptimizer` | Multi-objective evolutionary optimization of species palettes |

Domain Data Models

Strongly-typed, validated representations of ecological design concepts: `Species`, `Site`, `SoilProfile`, `DesignBrief`, `Objective`, `Constraint`, and more.

AI Reasoning (Future)

An AI orchestration layer that composes engines, interprets design intent, and generates recommendations — **strictly separated from the deterministic engines** to ensure scientific trust.

Architecture
┌──────────────────────────────────────┐
│ AI Reasoning Layer │
│ (Calls engines. Never inside them.) │
├──────────────────────────────────────┤
│ Computational Engines │
│ (Deterministic. Testable. AI-free.) │
├──────────────────────────────────────┤
│ Domain Data Models │
│ (Species, Site, DesignBrief...) │
├──────────────────────────────────────┤
│ Data & Integrations │
│ (Community data, Certified data, │
│ QGIS, APIs, CAD connectors) │
└──────────────────────────────────────┘


[Full Architecture Document →](docs/ARCHITECTURE.md)


Starting Region: MENA
NatureOS launches with deep focus on UAE and Arabian Peninsula ecosystems as one of the world's most climatically extreme and ecologically underserved regions.

- Arid environments demand the highest level of ecological intelligence - every drop of water, every degree of heat, every species choice matters
- Most ecological software is built for temperate climates and performs poorly in desert conditions
- The UAE has significant native biodiversity that is poorly represented in digital tools
- Local expertise exists but is not systematized into open, reusable infrastructure
- Climate change is making arid-region ecological knowledge globally relevant

Initial ecosystem coverage:

| Ecosystem | Key Species |
|-----------|-------------|
| Coastal sabkha & saline landscapes | Avicennia marina, Halocnemum strobilaceum, Salsola spp. |
| Mangrove & coastal wetlands | Avicennia marina* (primary ecosystem engineer) |
| Mountain wadi (Hajar range) | Prosopis cineraria (Ghaf), Ziziphus spina-christi (Sidr), Acacia tortilis (Samr) |
| Desert scrub & gravel plains | Calligonum comosum (Arta), Haloxylon salicornicum (Rimth), Lycium shawii, Aerva javanica, Leptadenia pyrotechnica |
| Urban parks & streetscapes | Prosopis cineraria, Ziziphus spina-christi, Phoenix dactylifera, Tephrosia apollinea |

Reference institutions: Environment Agency – Abu Dhabi, Dubai Municipality, International Centre for Biosaline Agriculture (ICBA), Al Wathba Wetland Reserve, Jebel Hafeet National Park.
11 species with full ecological parameters. Community-contributed. Certified versions available commercially.

[Species Database →](https://github.com/nature-os/mena-species)


Global Vision
While starting in MENA, NatureOS is architected to support diverse ecosystems worldwide:

- Desert and arid ecosystems
- Tropical and subtropical systems
- Temperate forests and woodlands
- Coastal and marine interfaces
- Urban environments globally
- Agricultural and agroforestry landscapes

The platform enables regional ecological knowledge to become part of a shared, computable global framework - contributed and maintained by local experts.


Quick Start

```python
from natureos.data.mena_species import ALL_SPECIES, species_by_ecosystem
from natureos.engines.habitat import HabitatSuitability
from natureos.engines.water import WaterBudget
from natureos.site import Site, ClimateZone, LandUse, SoilProfile

# Define a site in Dubai
site = Site(
    name="Al Barsha South Park",
    climate_zone=ClimateZone.BWH,
    soil=SoilProfile(texture="sandy_loam", salinity_dsm=4.2),
    area_hectares=2.3,
    land_use=LandUse.PUBLIC_PARK,
    max_summer_temp_c=47.0,
)

# Find suitable species
suitability = HabitatSuitability(site)
results = suitability.evaluate_all(ALL_SPECIES)

for r in results[:5]:
    print(r.summary())

# Estimate water demand for top species
top_species = [r.species for r in results[:5] if r.suitability_class.value in ("highly_suitable", "suitable")]
water = WaterBudget(site)
water_result = water.calculate(top_species)
print(water_result.summary())
Open-Core Model
NatureOS follows an open-core model:

Layer	Access	Pricing
Core framework	Open source (Apache 2.0)	Free, forever
Community data	Open source (Apache 2.0)	Free, forever
Cloud API	Commercial	Subscription
Enterprise	Commercial	Annual contract
Scientific Certification	Commercial	Per-product
The foundation is and will remain open. Commercial services fund sustainable development.

API & Commercial Tiers →

Repository Ecosystem
Repository	Status	Purpose
nature-os/core	✅ Active	Computational framework
nature-os/mena-species	✅ Active	Structured ecological data
nature-os/qgis-plugin Early	QGIS integration
nature-os/docs	🔲 Planned	Centralized documentation
nature-os/examples	🔲 Planned	Worked examples & tutorials
nature-os/api	🔲 Planned	Cloud & Enterprise API (commercial)
Roadmap
Phase	Milestone	Status
Foundation	Core data models, 7 engines, MENA dataset, architecture docs	✅
AI Layer	EcologyAdvisor, DesignGenerator, SiteAnalyzer agents	🔲
Integrations	QGIS plugin prototype, REST API specification	🔲
Examples	Dubai Urban Park, Wadi Restoration, Mangrove Buffer notebooks	🔲
Commercial	Cloud API, Certified Data products, Enterprise tier	🔲
Contributing
NatureOS welcomes contributors across disciplines ecologists, landscape architects, urban planners, software engineers, researchers.

Contributing
NatureOS welcomes contributors from multiple disciplines:
Ecologists & botanists: species data, trait parameters, ecological relationships
Landscape architects & urban planners: design scenarios, validation cases, regional knowledge
Software developers: algorithms, integrations, tests, documentation
Researchers: models, literature synthesis, methodological review

See CONTRIBUTING.md for guidelines and ARCHITECTURE.md for design philosophy.

License
NatureOS Core is released under the Apache 2.0 License. See LICENSE.
The core framework and community data are open source. Commercial services are separate.

Author
NatureOS is created and maintained by Zahed, a computational architect and full-stack developer with 15 years of experience working at the intersection of architecture, urban planning, artificial intelligence, and digital platforms in the UAE.

Status
NatureOS Core is currently in the data modeling and architecture phase. Pre-release foundational architecture established. Seven computational engines operational. MENA species dataset v0.1 published. We welcome early contributors interested in computational ecology, AI-assisted design, climate resilience, and open-source infrastructure for the built environment.
