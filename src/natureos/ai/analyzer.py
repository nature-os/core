"""
SiteAnalyzer — AI agent that interprets site conditions and recommends
ecological interventions.

Open source: Agent architecture, site analysis logic, recommendation framework.
Commercial (NatureOS Cloud): Optimized prompts, hosted LLM, regional benchmarking,
                             comparative site analytics, regulatory compliance checks.

The SiteAnalyzer reads site parameters (climate, soil, land use) and generates
actionable ecological recommendations with supporting computational evidence.
"""

from dataclasses import dataclass, field
from natureos.ai.models import AIResponse, Confidence, DesignRecommendation, RecommendationType
from natureos.site import Site, ClimateZone, LandUse
from natureos.species import Species
from typing import Optional


@dataclass
class SiteAnalyzer:
    """
    Analyses a site and recommends ecological interventions.

    Composes computational engines to assess site constraints and
    opportunities, then generates prioritized recommendations.

    Parameters
    ----------
    site : Site
        The site to analyze
    available_species : list[Species]
        Species pool for recommendation generation
    """

    site: Site
    available_species: list[Species] = field(default_factory=list)

    def analyze(self) -> AIResponse:
        """
        Perform comprehensive site analysis and generate recommendations.

        Returns
        -------
        AIResponse
            Structured analysis with prioritized recommendations
        """
        if not self.available_species:
            return AIResponse(
                agent_name="SiteAnalyzer",
                query_summary=f"Analyze site: {self.site.name}",
                response_text="No species database loaded. Cannot generate species-specific recommendations.",
                confidence=Confidence.LOW,
            )

        # Run core analyses
        constraints = self._analyze_constraints()
        opportunities = self._analyze_opportunities()
        suitable = self._find_suitable_species()
        recommendations = self._generate_recommendations(constraints, opportunities, suitable)

        # Build response
        constraint_text = "\n".join(f"  • {c}" for c in constraints)
        opportunity_text = "\n".join(f"  • {o}" for o in opportunities)

        if suitable:
            species_preview = "\n".join(
                f"  • {sp.display_name}"
                for sp in suitable[:5]
            )
        else:
            species_preview = "  No species evaluated — load MENA species database."

        response_text = (
            f"Site Analysis: {self.site.name}\n"
            f"{'─' * (18 + len(self.site.name))}\n\n"
            f"Location: {self.site.climate_zone.value} climate, "
            f"{self.site.land_use.value}\n"
            f"Area: {self.site.area_hectares} ha\n"
            f"Soil: {self.site.soil.texture.value}, "
            f"salinity {self.site.soil.salinity_dsm} dS/m, "
            f"pH {self.site.soil.ph}\n"
            f"Rainfall: {self.site.annual_rainfall_mm} mm/yr\n"
            f"Max summer temp: {self.site.max_summer_temp_c}°C\n\n"
            f"Constraints identified:\n{constraint_text}\n\n"
            f"Opportunities identified:\n{opportunity_text}\n\n"
            f"Potentially suitable species:\n{species_preview}\n\n"
            f"🔒 Pro tier: Full habitat suitability scoring with factor breakdown.\n"
            f"🔒 Enterprise: Batch site analysis, regional benchmarking, compliance checks."
        )

        return AIResponse(
            agent_name="SiteAnalyzer",
            query_summary=f"Analyze site: {self.site.name}",
            response_text=response_text,
            confidence=Confidence.HIGH,
            references=[
                "NatureOS Habitat Suitability Engine v0.1",
                "Environment Agency – Abu Dhabi",
            ],
            engine_results={
                "constraint_count": len(constraints),
                "opportunity_count": len(opportunities),
                "suitable_species_count": len(suitable),
            },
        )

    def _analyze_constraints(self) -> list[str]:
        """Identify ecological constraints from site parameters."""
        constraints = []

        if self.site.is_arid:
            constraints.append(
                f"Arid climate ({self.site.climate_zone.value}) — "
                f"water is the primary limiting factor. Only {self.site.annual_rainfall_mm}mm "
                f"annual rainfall. Irrigation will be required for most non-native species."
            )

        if self.site.is_saline:
            constraints.append(
                f"Saline soil ({self.site.soil.salinity_dsm} dS/m) — "
                f"only salt-tolerant species (halophytes, high salinity tolerance) "
                f"will thrive without soil remediation."
            )

        if self.site.max_summer_temp_c > 45:
            constraints.append(
                f"Extreme summer temperatures ({self.site.max_summer_temp_c}°C) — "
                f"species must have extreme thermal tolerance. Reflected heat from "
                f"pavement and buildings may add 3-5°C in urban settings."
            )

        if self.site.soil.organic_matter_pct < 1.0:
            constraints.append(
                f"Low soil organic matter ({self.site.soil.organic_matter_pct}%) — "
                f"soil amendment with compost or biochar recommended for establishment."
            )

        if self.site.soil.depth_cm < 100:
            constraints.append(
                f"Shallow soil depth ({self.site.soil.depth_cm}cm) — "
                f"limits deep-rooted species. Select shrubs and shallow-rooted trees."
            )

        if self.site.soil.ph > 8.0:
            constraints.append(
                f"Alkaline soil (pH {self.site.soil.ph}) — "
                f"limits nutrient availability. Select species adapted to calcareous soils."
            )

        if not constraints:
            constraints.append("No significant ecological constraints identified.")

        return constraints

    def _analyze_opportunities(self) -> list[str]:
        """Identify ecological opportunities from site parameters."""
        opportunities = []

        if self.site.is_arid:
            opportunities.append(
                "Arid-adapted native species require minimal irrigation once established — "
                "opportunity for low-maintenance, authentic regional landscape character."
            )

        if self.site.land_use == LandUse.PUBLIC_PARK:
            opportunities.append(
                "Public park — opportunity for educational native species displays, "
                "pollinator gardens, and community engagement with local ecology."
            )

        if self.site.land_use == LandUse.ECOLOGICAL_RESTORATION:
            opportunities.append(
                "Ecological restoration — opportunity for high-impact biodiversity recovery. "
                "Use only native species. Monitor successional development over time."
            )

        if self.site.land_use == LandUse.WETLAND_CONSERVATION:
            opportunities.append(
                "Wetland conservation — opportunity for blue carbon sequestration. "
                "Mangrove and salt marsh species provide shoreline protection, "
                "nursery habitat, and migratory bird support."
            )

        if self.site.soil.salinity_dsm > 8:
            opportunities.append(
                "High salinity site — opportunity to showcase halophyte species "
                "that are uniquely adapted and often visually distinctive."
            )

        if self.site.area_hectares >= 1.0:
            opportunities.append(
                f"Site size ({self.site.area_hectares} ha) allows for "
                f"zoned planting — create distinct ecological zones with different "
                f"species assemblages and microclimates."
            )

        if not opportunities:
            opportunities.append("Standard ecological design approach recommended.")

        return opportunities

    def _find_suitable_species(self) -> list[Species]:
        """Find species suitable for this site using Habitat Suitability."""
        from natureos.engines.habitat import HabitatSuitability, SuitabilityClass

        engine = HabitatSuitability(self.site)
        results = engine.evaluate_all(self.available_species)

        return [
            r.species for r in results
            if r.suitability_class in (
                SuitabilityClass.HIGHLY_SUITABLE,
                SuitabilityClass.SUITABLE,
            )
        ]

    def _generate_recommendations(
        self,
        constraints: list[str],
        opportunities: list[str],
        suitable_species: list[Species],
    ) -> list[DesignRecommendation]:
        """Generate prioritized design recommendations."""
        recommendations = []

        # Water recommendation for arid sites
        if self.site.is_arid:
            recommendations.append(
                DesignRecommendation(
                    recommendation_type=RecommendationType.IRRIGATION_STRATEGY,
                    title="Water-Efficient Irrigation Strategy",
                    description=(
                        f"With only {self.site.annual_rainfall_mm}mm annual rainfall, "
                        f"prioritize species with VERY_LOW or LOW water regime. "
                        f"Use drip irrigation (90% efficiency). Group species by "
                        f"hydrozone to avoid overwatering drought-adapted plants."
                    ),
                    species_suggestions=[
                        sp.scientific_name for sp in suitable_species[:3]
                        if sp.water_regime.value in ("very_low", "low")
                    ],
                    rationale="Water is the primary limiting factor in arid environments.",
                    confidence=Confidence.HIGH,
                )
            )

        # Salinity recommendation
        if self.site.is_saline:
            halophytes = [
                sp for sp in suitable_species
                if sp.salinity_tolerance.value in ("high", "halophyte")
            ]
            recommendations.append(
                DesignRecommendation(
                    recommendation_type=RecommendationType.SPECIES_SELECTION,
                    title="Salt-Tolerant Species Strategy",
                    description=(
                        f"Soil salinity of {self.site.soil.salinity_dsm} dS/m requires "
                        f"halophytic or highly salt-tolerant species. "
                        f"{len(halophytes)} suitable salt-tolerant species identified."
                    ),
                    species_suggestions=[sp.scientific_name for sp in halophytes[:5]],
                    rationale="Saline soils exclude most conventional landscape species.",
                    confidence=Confidence.HIGH,
                )
            )

        # Heat mitigation for urban sites
        if self.site.land_use in (LandUse.PUBLIC_PARK, LandUse.STREETSCAPE, LandUse.RESIDENTIAL, LandUse.COMMERCIAL):
            recommendations.append(
                DesignRecommendation(
                    recommendation_type=RecommendationType.HEAT_MITIGATION,
                    title="Urban Cooling Strategy",
                    description=(
                        f"Summer temperatures reach {self.site.max_summer_temp_c}°C. "
                        f"Prioritize trees with large canopy spread for shade. "
                        f"Multi-layer planting (trees + shrubs + groundcover) provides "
                        f"cumulative cooling through combined shade and evapotranspiration."
                    ),
                    species_suggestions=[],
                    rationale=(
                        "Urban heat island effect can be reduced 2-8°C through "
                        "strategic vegetation placement."
                    ),
                    confidence=Confidence.MEDIUM,
                )
            )

        # Restoration recommendation
        if self.site.land_use == LandUse.ECOLOGICAL_RESTORATION:
            native_suitable = [sp for sp in suitable_species if sp.is_native]
            recommendations.append(
                DesignRecommendation(
                    recommendation_type=RecommendationType.HABITAT_RESTORATION,
                    title="Native Ecosystem Restoration",
                    description=(
                        f"Ecological restoration site — use only native species. "
                        f"{len(native_suitable)} native species are suitable for "
                        f"this site. Plant in naturalistic clusters mimicking "
                        f"wild community structure. Zero irrigation after establishment."
                    ),
                    species_suggestions=[sp.scientific_name for sp in native_suitable[:5]],
                    rationale="Restoration requires genetic integrity — no introduced species.",
                    confidence=Confidence.HIGH,
                )
            )

        return recommendations
