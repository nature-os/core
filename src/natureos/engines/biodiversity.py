"""
Biodiversity Index engine — computes ecological diversity metrics for
planting designs and species assemblages.

Implements standard community ecology indices used in conservation biology,
landscape ecology, and environmental impact assessment.

References:
- Shannon, C.E. (1948). A mathematical theory of communication.
- Simpson, E.H. (1949). Measurement of diversity.
- Pielou, E.C. (1966). The measurement of diversity in different types
  of biological collections.
"""

from dataclasses import dataclass, field
from collections import Counter
from natureos.species import Species
import math


@dataclass
class BiodiversityResult:
    """Output of a biodiversity assessment for a species assemblage."""

    species_count: int
    total_individuals: int
    shannon_index: float
    simpson_index: float
    simpson_diversity: float          # 1 - Simpson dominance (higher = more diverse)
    pielou_evenness: float            # Shannon / ln(species_count)
    native_ratio: float               # Proportion of native species (by species count)
    species_abundance: dict[str, int] = field(default_factory=dict)

    def summary(self) -> str:
        return (
            f"Biodiversity Assessment\n"
            f"───────────────────────\n"
            f"Species richness: {self.species_count}\n"
            f"Total individuals: {self.total_individuals}\n"
            f"Shannon index (H'): {self.shannon_index:.3f}\n"
            f"Simpson diversity (1-D): {self.simpson_diversity:.3f}\n"
            f"Pielou evenness (J'): {self.pielou_evenness:.3f}\n"
            f"Native species ratio: {self.native_ratio:.1%}"
        )

    @property
    def interpretation(self) -> str:
        """Qualitative interpretation of the Shannon index for landscape contexts."""
        if self.shannon_index >= 3.0:
            return "Very high diversity — comparable to species-rich natural ecosystems"
        elif self.shannon_index >= 2.0:
            return "High diversity — ecologically robust planting design"
        elif self.shannon_index >= 1.0:
            return "Moderate diversity — functional but could benefit from more species"
        elif self.shannon_index >= 0.5:
            return "Low diversity — monoculture risk, limited ecological function"
        else:
            return "Very low diversity — ecologically poor, high vulnerability"


@dataclass
class BiodiversityIndex:
    """
    Computes biodiversity metrics for a species assemblage.

    The engine accepts a list of Species objects with optional abundance
    counts. If abundances are not provided, all species are assumed to
    have equal abundance (1 individual each), and evenness will be 1.0.

    For planting designs, provide actual planned quantities per species
    to get meaningful evenness and dominance metrics.

    Parameters
    ----------
    species_abundances : dict[Species, int] | None
        Mapping of species to number of individuals. If None, uses
        equal abundance.
    """

    species_abundances: dict[Species, int] = field(default_factory=dict)

    def calculate(self) -> BiodiversityResult:
        """
        Compute all biodiversity metrics.

        Returns
        -------
        BiodiversityResult
            Complete biodiversity assessment

        Raises
        ------
        ValueError
            If no species are provided
        """
        if not self.species_abundances:
            raise ValueError(
                "Species abundance dictionary cannot be empty. "
                "Provide at least one species with abundance count."
            )

        species_list = list(self.species_abundances.keys())
        abundances = list(self.species_abundances.values())
        total_individuals = sum(abundances)
        species_count = len(species_list)

        # ── Shannon-Wiener Index (H') ────────────────────────────────
        # H' = -Σ (p_i × ln(p_i))
        # where p_i = proportion of individuals belonging to species i
        shannon = 0.0
        for count in abundances:
            if count > 0:
                p_i = count / total_individuals
                shannon -= p_i * math.log(p_i)

        # ── Simpson's Diversity Index (D) ────────────────────────────
        # D = Σ (n_i(n_i - 1)) / (N(N - 1))
        # This is Simpson's dominance - probability two random individuals
        # are the same species. Lower = more diverse.
        n_total = total_individuals
        if n_total > 1:
            simpson_dominance = sum(
                count * (count - 1) for count in abundances
            ) / (n_total * (n_total - 1))
        else:
            simpson_dominance = 1.0  # Single individual

        simpson_diversity = 1.0 - simpson_dominance  # Higher = more diverse

        # ── Pielou's Evenness (J') ───────────────────────────────────
        # J' = H' / H'_max = H' / ln(S)
        # where S = species richness
        if species_count > 1:
            h_max = math.log(species_count)
            pielou = shannon / h_max if h_max > 0 else 0.0
        else:
            pielou = 1.0  # Single species = perfectly "even"

        # ── Native Species Ratio ─────────────────────────────────────
        native_count = sum(
            1 for sp in species_list if sp.is_native
        )
        native_ratio = native_count / species_count if species_count > 0 else 0.0

        # ── Build abundance dict keyed by scientific name ─────────────
        abundance_dict = {
            sp.scientific_name: count
            for sp, count in self.species_abundances.items()
        }

        return BiodiversityResult(
            species_count=species_count,
            total_individuals=total_individuals,
            shannon_index=round(shannon, 4),
            simpson_index=round(simpson_dominance, 4),
            simpson_diversity=round(simpson_diversity, 4),
            pielou_evenness=round(pielou, 4),
            native_ratio=round(native_ratio, 4),
            species_abundance=abundance_dict,
        )

    @classmethod
    def from_equal_abundance(cls, species_list: list[Species]) -> "BiodiversityIndex":
        """
        Convenience constructor: all species have equal abundance (1 each).

        Use this when comparing species lists rather than designed planting
        quantities. Evenness will be 1.0.

        Parameters
        ----------
        species_list : list[Species]
            Species to include in the assessment

        Returns
        -------
        BiodiversityIndex
            Configured with equal abundances
        """
        return cls(species_abundances={sp: 1 for sp in species_list})

    @classmethod
    def from_counts(
        cls, species_counts: dict[Species, int]
    ) -> "BiodiversityIndex":
        """
        Convenience constructor: species with specified abundance counts.

        Use this for designed planting plans where quantities are known.

        Parameters
        ----------
        species_counts : dict[Species, int]
            Mapping of species to number of individuals

        Returns
        -------
        BiodiversityIndex
            Configured with the given abundances
        """
        return cls(species_abundances=species_counts)
