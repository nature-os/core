"""
NatureOS AI Reasoning Layer.

Provides intelligent agents that compose computational engines
to answer ecological design questions and generate recommendations.

Agents:
    EcologyAdvisor  — Conversational interface for ecological questions
    DesignGenerator — Natural language brief → species palette
    SiteAnalyzer    — Site interpretation → ecological recommendations

The AI layer strictly calls engines — it never modifies their logic.
Engines remain deterministic, testable, and AI-free.

Open source: Agent architecture, prompt templates, orchestration logic.
Commercial (NatureOS Cloud): Optimized prompts, hosted LLM, persistent
                              memory, vector stores, multi-turn sessions.

Usage:
    from natureos.ai import EcologyAdvisor, DesignGenerator, SiteAnalyzer

    advisor = EcologyAdvisor(site=my_site, available_species=my_species)
    response = advisor.ask("What species will thrive here?")
    print(response.summary())
"""

from natureos.ai.advisor import EcologyAdvisor
from natureos.ai.generator import DesignGenerator
from natureos.ai.analyzer import SiteAnalyzer
from natureos.ai.models import AIResponse, Confidence, DesignRecommendation, RecommendationType

__all__ = [
    "EcologyAdvisor",
    "DesignGenerator",
    "SiteAnalyzer",
    "AIResponse",
    "Confidence",
    "DesignRecommendation",
    "RecommendationType",
]
