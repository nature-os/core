"""
NatureOS AI Reasoning Layer.

Provides intelligent agents that compose computational engines
to answer ecological design questions and generate recommendations.

The AI layer strictly calls engines - it never modifies their logic.
Engines remain deterministic, testable, and AI-free.

Open source: Agent architecture, prompt templates, orchestration.
Commercial (future): Hosted LLM, optimized prompts, persistent memory,
                      vector stores, multi-turn project sessions.
"""

__all__ = [
    "EcologyAdvisor",
    "DesignGenerator",
    "SiteAnalyzer",
    "AIResponse",
    "DesignRecommendation",
]
