"""
EcologyAdvisor — Conversational AI agent for ecological design questions.

Open source: Agent architecture, engine composition logic, response formatting.
Commercial (NatureOS Cloud): Optimized prompts, hosted LLM, persistent memory.

The EcologyAdvisor interprets natural language questions about ecological
design, composes the appropriate computational engines, and returns
structured recommendations with supporting analysis.
"""

from dataclasses import dataclass, field
from natureos.ai.models import AIResponse, Confidence, DesignRecommendation, RecommendationType
from natureos.site import Site
from natureos.species import Species
from natureos.design_brief import DesignBrief
from typing import Optional


@dataclass
class EcologyAdvisor:
    """
    AI agent that answers ecological design questions by composing
    NatureOS computational engines.

    This is the open-source architecture. It demonstrates how an AI agent
    would structure queries and compose engine results. The actual LLM
    integration is provided by NatureOS Cloud (commercial).

    Parameters
    ----------
    site : Site | None
        Optional site context for the conversation
    design_brief : DesignBrief | None
        Optional design brief for project-aware responses
    available_species : list[Species]
        Species pool available for recommendations
    """

    site: Optional[Site] = None
    design_brief: Optional[DesignBrief] = None
    available_species: list[Species] = field(default_factory=list)

    def ask(self, query: str) -> AIResponse:
        """
        Process a natural language query and return an ecological recommendation.

        This method demonstrates the agent architecture. In production (Cloud),
        the query would be processed by an LLM with optimized ecological prompts.

        Parameters
        ----------
        query : str
            Natural language question about ecological design

        Returns
        -------
        AIResponse
            Structured response with recommendations and engine results
        """
        query_lower = query.lower()

        # Route query to appropriate handler based on intent
        if any(word in query_lower for word in ["species", "which plant", "what tree", "recommend"]):
            return self._handle_species_query(query)
        elif any(word in query_lower for word in ["water", "irrigation", "drought"]):
            return self._handle_water_query(query)
        elif any(word in query_lower for word in ["biodiversity", "diverse", "variety"]):
            return self._handle_biodiversity_query(query)
        elif any(word in query_lower for word in ["heat", "cool", "shade", "temperature"]):
            return self._handle_heat_query(query)
        elif any(word in query_lower for word in ["carbon", "climate", "sequester"]):
            return self._handle_carbon_query(query)
        else:
            return self._handle_general_query(query)

    def _handle_species_query(self, query: str) -> AIResponse:
        """Handle species selection and recommendation queries."""
        engine_results = {}

        # Run Habitat Suitability if site is available
        if self.site and self.available_species:
            from natureos.engines.habitat import HabitatSuitability
            engine = HabitatSuitability(self.site)
            results = engine.evaluate_all(self.available_species)
            top = results[:5]
            engine_results["habitat_suitability"] = {
                "top_species": [
                    {
                        "name": r.species.display_name,
                        "score": r.overall_score,
                        "class": r.suitability_class.value,
                    }
                    for r in top
                ]
            }

        # Build response
        if engine_results:
            species_list = "\n".join(
                f"  • {s['name']} ({s['score']:.0%} suitable — {s['class']})"
                for s in engine_results["habitat_suitability"]["top_species"]
            )
            response_text = (
                f"Based on habitat suitability analysis for your site "
                f"({self.site.name}, {self.site.area_hectares} ha, "
                f"{self.site.climate_zone.value}), the top recommended species are:\n\n"
                f"{species_list}\n\n"
                f"These species are best adapted to your site's climate, soil, "
                f"and ecological conditions."
            )
            confidence = Confidence.HIGH
            references = ["NatureOS Habitat Suitability Engine v0.1"]
        else:
            response_text = (
                "To provide specific species recommendations, please define "
                "a site and load a species database. The EcologyAdvisor can then "
                "run habitat suitability analysis to identify the best species "
                "for your conditions."
            )
            confidence = Confidence.LOW
            references = []

        return AIResponse(
            agent_name="EcologyAdvisor",
            query_summary=query[:100],
            response_text=response_text,
            confidence=confidence,
            references=references,
            engine_results=engine_results,
        )

    def _handle_water_query(self, query: str) -> AIResponse:
        """Handle water budget and irrigation queries."""
        engine_results = {}

        if self.site and self.available_species:
            from natureos.engines.water import WaterBudget
            engine = WaterBudget(site=self.site)
            # Use top 5 most suitable species
            from natureos.engines.habitat import HabitatSuitability
            hab = HabitatSuitability(self.site)
            hab_results = hab.evaluate_all(self.available_species)
            top_species = [r.species for r in hab_results[:5]]

            water_result = engine.calculate(top_species)
            engine_results["water_budget"] = {
                "annual_demand_m3": water_result.annual_demand_established_m3,
                "net_irrigation_m3": water_result.net_irrigation_required_m3,
                "rainfall_contribution_m3": water_result.annual_rainfall_supply_m3,
            }

            response_text = (
                f"Water budget analysis for {self.site.name}:\n\n"
                f"  • Estimated annual irrigation demand: "
                f"{water_result.annual_demand_established_m3:.0f} m³\n"
                f"  • Rainfall contribution: "
                f"{water_result.annual_rainfall_supply_m3:.0f} m³\n"
                f"  • Net irrigation required: "
                f"{water_result.net_irrigation_required_m3:.0f} m³\n\n"
                f"To minimize water use, prioritize species rated 'very_low' "
                f"or 'low' in water regime. Consider drip irrigation (90% efficiency) "
                f"and hydrozoning to group species with similar water needs."
            )
            confidence = Confidence.HIGH
            references = ["NatureOS WaterBudget Engine v0.1", "FAO Irrigation and Drainage Paper 56"]
        else:
            response_text = (
                "To estimate water demand, please define a site and load a species "
                "database. The EcologyAdvisor will run water budget calculations "
                "using species-specific evapotranspiration estimates."
            )
            confidence = Confidence.LOW
            references = []

        return AIResponse(
            agent_name="EcologyAdvisor",
            query_summary=query[:100],
            response_text=response_text,
            confidence=confidence,
            references=references,
            engine_results=engine_results,
        )

    def _handle_biodiversity_query(self, query: str) -> AIResponse:
        """Handle biodiversity assessment queries."""
        if self.available_species:
            from natureos.engines.biodiversity import BiodiversityIndex
            bio = BiodiversityIndex.from_equal_abundance(self.available_species)
            result = bio.calculate()

            response_text = (
                f"Biodiversity assessment of current species pool "
                f"({len(self.available_species)} species):\n\n"
                f"  • Shannon Index (H'): {result.shannon_index:.3f}\n"
                f"  • Simpson Diversity (1-D): {result.simpson_diversity:.3f}\n"
                f"  • Pielou Evenness (J'): {result.pielou_evenness:.3f}\n"
                f"  • Native species ratio: {result.native_ratio:.0%}\n\n"
                f"Interpretation: {result.interpretation}\n\n"
                f"To improve biodiversity, consider adding more native species "
                f"with diverse growth forms (trees + shrubs + groundcovers)."
            )
            confidence = Confidence.HIGH
            references = ["NatureOS BiodiversityIndex Engine v0.1", "Shannon (1948)", "Simpson (1949)"]
            engine_results = {"biodiversity": result.__dict__}
        else:
            response_text = "Please load a species database to assess biodiversity."
            confidence = Confidence.LOW
            references = []
            engine_results = {}

        return AIResponse(
            agent_name="EcologyAdvisor",
            query_summary=query[:100],
            response_text=response_text,
            confidence=confidence,
            references=references,
            engine_results=engine_results,
        )

    def _handle_heat_query(self, query: str) -> AIResponse:
        """Handle urban heat mitigation queries."""
        if self.site and self.available_species:
            response_text = (
                f"For urban heat mitigation on {self.site.name}:\n\n"
                f"  • Prioritize trees with large canopy spread for maximum shade\n"
                f"  • Select species with high evapotranspiration rates\n"
                f"  • Native species adapted to {self.site.max_summer_temp_c}°C "
                f"summer temperatures are essential\n"
                f"  • Consider multi-layer planting (trees + shrubs + groundcover) "
                f"for cumulative cooling effect\n\n"
                f"Run UrbanHeatMitigation engine with specific planting quantities "
                f"for quantitative cooling estimates."
            )
            confidence = Confidence.MEDIUM
            engine_results = {}
        else:
            response_text = "Define a site and species palette to assess heat mitigation potential."
            confidence = Confidence.LOW
            engine_results = {}

        return AIResponse(
            agent_name="EcologyAdvisor",
            query_summary=query[:100],
            response_text=response_text,
            confidence=confidence,
            references=["Oke (1989)", "Rahman et al. (2017)"],
            engine_results=engine_results,
        )

    def _handle_carbon_query(self, query: str) -> AIResponse:
        """Handle carbon sequestration queries."""
        if self.site and self.available_species:
            response_text = (
                f"Carbon sequestration potential depends on species selection, "
                f"planting density, and time horizon.\n\n"
                f"Key factors for {self.site.name}:\n"
                f"  • Trees sequester more carbon than shrubs (larger biomass)\n"
                f"  • Mangroves have the highest soil carbon accumulation rates\n"
                f"  • Arid environments have slower growth rates — use conservative estimates\n"
                f"  • Soil carbon accumulates gradually over decades\n\n"
                f"Run CarbonEstimator with specific planting quantities for "
                f"quantitative sequestration projections."
            )
            confidence = Confidence.MEDIUM
            engine_results = {}
        else:
            response_text = "Define a site and planting plan to estimate carbon sequestration."
            confidence = Confidence.LOW
            engine_results = {}

        return AIResponse(
            agent_name="EcologyAdvisor",
            query_summary=query[:100],
            response_text=response_text,
            confidence=confidence,
            references=["IPCC (2006)", "Chave et al. (2014)"],
            engine_results=engine_results,
        )

    def _handle_general_query(self, query: str) -> AIResponse:
        """Handle general ecological design queries."""
        site_info = ""
        if self.site:
            site_info = (
                f"Current site: {self.site.name} — {self.site.area_hectares} ha, "
                f"{self.site.climate_zone.value}, {self.site.land_use.value}.\n\n"
            )

        response_text = (
            f"{site_info}"
            f"I can help with:\n"
            f"  • Species selection and habitat suitability\n"
            f"  • Water budget and irrigation planning\n"
            f"  • Biodiversity assessment\n"
            f"  • Carbon sequestration estimates\n"
            f"  • Urban heat mitigation strategies\n"
            f"  • Species interaction and compatibility\n\n"
            f"Please ask a specific question about your ecological design project."
        )

        return AIResponse(
            agent_name="EcologyAdvisor",
            query_summary=query[:100],
            response_text=response_text,
            confidence=Confidence.MEDIUM,
            references=[],
            engine_results={},
        )
