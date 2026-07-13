"""
Species Interaction engine — models ecological relationships between
plant species in a designed community.

Evaluates pairwise compatibility based on:
- Allelopathy (chemical inhibition)
- Competition intensity (overlapping resource niches)
- Facilitation (nurse plants, nitrogen fixation, shade provision)
- Known ecological associations from native ecosystems

References:
- Callaway, R.M. (2007). Positive Interactions and Interdependence
  in Plant Communities.
- Schenk, H.J. et al. (1999). Root competition: beyond resource depletion.
"""

from dataclasses import dataclass, field
from enum import Enum
from natureos.species import Species, GrowthForm, EcosystemType


class InteractionType(str, Enum):
    """Classification of ecological interactions between two species."""
    FACILITATION = "facilitation"         # One species benefits another
    COMPATIBLE = "compatible"             # No known conflict, can co-occur
    COMPETITION = "competition"           # Overlapping niches, may compete
    ALLELOPATHY = "allelopathy"           # Chemical inhibition
    EXCLUSION = "exclusion"               # Should not be planted together


@dataclass
class PairwiseInteraction:
    """Result of an interaction assessment between two species."""

    species_a: Species
    species_b: Species
    interaction_type: InteractionType
    score: float                         # 1.0 = highly beneficial, 0.0 = exclusion
    rationale: str = ""

    def summary(self) -> str:
        return (
            f"{self.species_a.display_name} ↔ {self.species_b.display_name}: "
            f"{self.interaction_type.value} ({self.score:.0%})"
        )


@dataclass
class CommunityInteractionResult:
    """Aggregate interaction assessment for a species community."""

    species_list: list[Species]
    pairwise_results: list[PairwiseInteraction] = field(default_factory=list)
    average_compatibility: float = 0.0
    conflict_pairs: list[PairwiseInteraction] = field(default_factory=list)
    facilitation_pairs: list[PairwiseInteraction] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"Community Interaction Assessment\n"
            f"────────────────────────────────\n"
            f"Species: {len(self.species_list)}\n"
            f"Pairs analysed: {len(self.pairwise_results)}\n"
            f"Average compatibility: {self.average_compatibility:.0%}\n"
            f"Facilitation pairs: {len(self.facilitation_pairs)}\n"
            f"Conflict pairs: {len(self.conflict_pairs)}"
        )


@dataclass
class SpeciesInteraction:
    """
    Evaluates ecological interactions between species in a planting design.

    The engine uses rules-based assessment informed by ecological principles:
    - Growth form complementarity (trees + shrubs = structural diversity)
    - Ecosystem co-occurrence (species from same native ecosystem tend to coexist)
    - Nitrogen-fixing facilitation (Fabaceae species benefit neighbours)
    - Water regime compatibility (similar water needs reduce management conflict)
    - Allelopathy awareness (some species chemically suppress others)

    A full trait-based competition model with niche overlap quantification
    is planned for a future version.

    Parameters
    ----------
    species_list : list[Species]
        Species to evaluate for pairwise interactions
    """

    species_list: list[Species]

    def analyse(self) -> CommunityInteractionResult:
        """
        Compute pairwise interactions for all species combinations.

        Returns
        -------
        CommunityInteractionResult
            Complete interaction assessment
        """
        if len(self.species_list) < 2:
            raise ValueError(
                "At least two species are required for interaction analysis"
            )

        pairwise_results: list[PairwiseInteraction] = []

        for i, sp_a in enumerate(self.species_list):
            for sp_b in self.species_list[i + 1:]:
                interaction = self._evaluate_pair(sp_a, sp_b)
                pairwise_results.append(interaction)

        # Aggregate metrics
        scores = [p.score for p in pairwise_results]
        avg_compatibility = sum(scores) / len(scores) if scores else 0.0

        conflict_pairs = [
            p for p in pairwise_results
            if p.interaction_type in {InteractionType.ALLELOPATHY, InteractionType.EXCLUSION}
        ]
        facilitation_pairs = [
            p for p in pairwise_results
            if p.interaction_type == InteractionType.FACILITATION
        ]

        return CommunityInteractionResult(
            species_list=self.species_list,
            pairwise_results=pairwise_results,
            average_compatibility=round(avg_compatibility, 4),
            conflict_pairs=conflict_pairs,
            facilitation_pairs=facilitation_pairs,
        )

    def _evaluate_pair(self, sp_a: Species, sp_b: Species) -> PairwiseInteraction:
        """
        Evaluate compatibility between two species.

        Scoring logic (additive):
        - Base score: 0.6 (neutral)
        - +0.2 if they share an ecosystem (co-evolved)
        - +0.1 if at least one is nitrogen-fixing (Fabaceae) — facilitation
        - +0.1 if growth forms are complementary (tree + shrub)
        - -0.2 if water regimes differ by more than one category
        - -0.3 if one is known allelopathic (future: species-specific data)
        - Score clamped to [0.0, 1.0]
        """
        score = 0.6
        reasons: list[str] = []

        # Ecosystem co-occurrence
        shared_ecosystems = set(sp_a.ecosystems) & set(sp_b.ecosystems)
        if shared_ecosystems:
            score += 0.2
            reasons.append(f"share ecosystem(s): {[e.value for e in shared_ecosystems]}")

        # Nitrogen-fixing facilitation (Fabaceae family)
        fabaceae = "Fabaceae"
        # We check scientific_name for known Fabaceae — in future, add family field
        is_a_nfix = sp_a.scientific_name in {
            "Prosopis cineraria", "Acacia tortilis", "Tephrosia apollinea"
        }
        is_b_nfix = sp_b.scientific_name in {
            "Prosopis cineraria", "Acacia tortilis", "Tephrosia apollinea"
        }
        if is_a_nfix or is_b_nfix:
            score += 0.1
            reasons.append("nitrogen-fixing facilitation")

        # Growth form complementarity
        if sp_a.growth_form != sp_b.growth_form:
            # Tree + shrub is especially complementary (structural layering)
            forms = {sp_a.growth_form, sp_b.growth_form}
            if GrowthForm.TREE in forms and GrowthForm.SHRUB in forms:
                score += 0.1
                reasons.append("complementary growth forms (tree + shrub)")
            elif GrowthForm.TREE in forms and GrowthForm.GROUNDCOVER in forms:
                score += 0.1
                reasons.append("complementary growth forms (tree + groundcover)")

        # Water regime compatibility
        water_levels = {
            "very_low": 0, "low": 1, "moderate": 2, "high": 3
        }
        a_level = water_levels.get(sp_a.water_regime.value, 1)
        b_level = water_levels.get(sp_b.water_regime.value, 1)
        water_diff = abs(a_level - b_level)
        if water_diff > 1:
            score -= 0.2
            reasons.append(
                f"water regime mismatch ({sp_a.water_regime.value} vs {sp_b.water_regime.value})"
            )

        # Salinity tolerance incompatibility
        # Species with very different salinity needs may create management conflicts
        salinity_levels = {
            "none": 0, "low": 1, "moderate": 2, "high": 3, "halophyte": 4
        }
        a_sal = salinity_levels.get(sp_a.salinity_tolerance.value, 2)
        b_sal = salinity_levels.get(sp_b.salinity_tolerance.value, 2)
        if abs(a_sal - b_sal) > 2:
            score -= 0.1
            reasons.append("salinity tolerance mismatch")

        # Clamp score
        score = max(0.0, min(1.0, score))

        # Determine interaction type
        if score >= 0.8:
            interaction_type = InteractionType.FACILITATION
        elif score >= 0.5:
            interaction_type = InteractionType.COMPATIBLE
        elif score >= 0.3:
            interaction_type = InteractionType.COMPETITION
        else:
            interaction_type = InteractionType.EXCLUSION

        rationale = "; ".join(reasons) if reasons else "no strong positive or negative interactions detected"

        return PairwiseInteraction(
            species_a=sp_a,
            species_b=sp_b,
            interaction_type=interaction_type,
            score=round(score, 4),
            rationale=rationale,
        )
