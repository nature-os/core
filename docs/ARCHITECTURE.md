NatureOS Core Architecture

Version: 0.1.0
Status: Pre-release foundational architecture


Design Philosophy

NatureOS Core is designed to be the ecological equivalent of GDAL or OpenStreetMap foundational open infrastructure for a domain that currently has none.

It is not a standalone application. It is a framework that other tools like GIS platforms, CAD software, AI co-pilots, municipal dashboards, digital twin platforms to integrate into their workflows.

Every architectural decision is guided by three principles:

1. Scientific integrity: engines must be deterministic, testable, and methodology-transparent
2. Separation of concerns: data, computation, AI, and integration layers are strictly separated
3. Open-core sustainability: the foundation is open; commercial services fund development


Layer Architecture
┌─────────────────────────────────────────────────┐
│ AI Reasoning Layer │
│ (EcologyAdvisor, DesignGenerator, SiteAnalyzer) │
│ Calls engines. Never embedded within them. │
├─────────────────────────────────────────────────┤
│ Computational Engines │
│ (HabitatSuitability, WaterBudget, │
│ BiodiversityIndex, CarbonEstimator, │
│ SpeciesInteraction, DesignOptimizer, │
│ UrbanHeatMitigation) │
│ Deterministic. Testable. AI-free. │
├─────────────────────────────────────────────────┤
│ Domain Data Models │
│ (Species, Site, SoilProfile, DesignBrief, │
│ Objective, Constraint, EcosystemType) │
│ Strongly-typed. Validated. Extensible. │
├─────────────────────────────────────────────────┤
│ Data & Integrations │
│ (Community datasets, Certified datasets, │
│ QGIS plugin, APIs, CAD connectors) │
│ Engines are data-agnostic. │
└─────────────────────────────────────────────────┘


Rationale:
- Engines remain deterministic and testable without any LLM dependency
- Scientific users can trust that core computation is not influenced by AI hallucination
- Engines can be used in regulated environments (government, legal) where AI is not permitted
- The AI layer adds value through orchestration, not by modifying ecological science

2. Data Independence

Decision: Engines operate on data models, not on specific datasets or file formats.

A `HabitatSuitability` engine does not know or care whether species data came from:
- A community-contributed JSON file
- A NatureOS Certified dataset
- A municipal PostgreSQL database
- A GeoPackage file from a government agency

Rationale:
- Keeps engines testable with mock data
- Enables the Community → Certified data product pipeline
- Allows regional customization without engine modification
- Follows the OpenStreetMap model: data is separate from tools

3. Open-Core Model

Decision: Foundational models, algorithms, and schemas are open source under Apache 2.0. Commercial services provide infrastructure, certification, and enterprise workflows.

| Layer | License | Rationale |
|-------|---------|-----------|
| Data models | Apache 2.0 | Must be auditable by researchers |
| Engines | Apache 2.0 | Scientific methodology must be transparent |
| Community data | Apache 2.0 | Collaborative knowledge belongs to commons |
| Certified data | Commercial | Customers pay for validation, not access |
| Cloud compute | Commercial | Infrastructure has operating costs |
| Enterprise API | Commercial | SLAs, support, custom integrations |

4. Modular Repository Ecosystem

Decision: NatureOS is organized as a federation of repositories, not a monolith.
nature-os/
├── core/ ← Open Source: Computational framework
├── mena-species/ ← Open Source: Regional ecological data
├── qgis-plugin/ ← Open Source: GIS integration
├── docs/ ← Open Source: Centralized documentation
├── examples/ ← Open Source: Worked examples & tutorials
├── api/ ← Commercial: Cloud & Enterprise API
├── cloud/ ← Commercial: SaaS platform
├── enterprise/ ← Commercial: On-premise, custom deployments
└── ai-platform/ ← Commercial: Hosted AI agents & reasoning

Rationale:
- Clear boundary between community and commercial
- Each repo has independent versioning, issues, and contribution workflow
- Users can adopt only what they need (e.g., core + mena-species without touching commercial)
- Commercial repos can be private while open repos remain fully public

5. MENA-First, Global Architecture

Decision: Launch with deep regional specificity (UAE & Arabian Peninsula) on a region-agnostic architecture.

Rationale:
- Arid environments demand the highest ecological precision a strong test case
- MENA ecosystems are massively underserved by existing tools
- Architecture supports any region; MENA is the first implementation
- Regional depth + global scalability = defensible positioning

6. DesignBrief as First-Class Model

Decision: A `DesignBrief` (objectives + constraints + budget) is a first-class domain model, not an afterthought.

Rationale:
- In real projects, objectives are properties of the brief, not the site
- The optimizer and AI layer consume DesignBrief, not raw sites
- Enables scenario comparison: same site, different briefs
- Separates "where we are" (Site) from "what we want" (DesignBrief)

Data Flow

Typical Computational Ecology Workflow
User defines Site
↓
User creates DesignBrief (objectives, constraints)
↓
Species pool selected (from Community or Certified data)
↓
HabitatSuitability filters species for site
↓
DesignOptimizer generates candidate palettes
↓
Each candidate evaluated through engines:
• BiodiversityIndex
• WaterBudget
• CarbonEstimator
• UrbanHeatMitigation
• SpeciesInteraction
↓
Pareto-optimal solutions presented
↓
AI layer (optional) interprets results, explains trade-offs

AI-Assisted Workflow (Future)
User: "Design a public park in Dubai that maximizes shade
and biodiversity, uses minimal water, and meets
Dubai Municipality LSP-2025 standards."

AI Layer:

Parses natural language → DesignBrief
Calls HabitatSuitability with site context
Invokes DesignOptimizer with brief objectives
Evaluates top candidates through all engines
Returns ranked options with trade-off explanations
Generates human-readable rationale for each option


Engine Design Standards
All computational engines follow these standards:

| Standard | Requirement |
|----------|-------------|
| Determinism | Same inputs → same outputs. Random elements expose seed parameters. |
| Type safety | All inputs and outputs use typed dataclasses or Pydantic models. |
| Documentation | NumPy-style docstrings with parameter descriptions and return types. |
| Testability | Engines accept data models, not file paths or database connections. |
| Isolation | Engines do not import from other engines unless composing (optimizer calls others). |
| Performance awareness | Algorithms document complexity for large spatial datasets. |
| Methodology traceability | Scientific references included in module docstrings. |


Future Architectural Evolution

Short-term (v0.1 → v0.3)
- [ ] Models directory when model count exceeds 8 files
- [ ] External dataset format specification (JSON Schema, GeoPackage profile)
- [ ] AI reasoning layer (`src/natureos/ai/`)
- [ ] Example notebooks (`nature-os/examples`)

Medium-term (v0.3 → v0.5)
- [ ] GeoPackage support for spatial species data
- [ ] Dataset validation tooling
- [ ] REST API implementation (`nature-os/api`)
- [ ] QGIS plugin functional prototype

Long-term (v1.0+)
- [ ] Cloud simulation platform
- [ ] Enterprise on-premise deployment
- [ ] Certification program launch
- [ ] Municipality dashboard
- [ ] Digital twin integration
