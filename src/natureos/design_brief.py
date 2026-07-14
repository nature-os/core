"""
Design Brief — the conceptual bridge between a site and a design solution.

In real projects, the site defines where we are, but the design brief
defines what we want to achieve. Objectives, constraints, budgets, and
regulatory requirements are properties of the brief, not the site.

This module provides the data models that the optimizer and AI reasoning
layer consume to generate and evaluate planting designs.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from natureos.site import Site


class ObjectiveType(str, Enum):
    """Categories of design objectives."""
    MAXIMIZE_BIODIVERSITY = "maximize_biodiversity"
    MINIMIZE_WATER_USE = "minimize_water_use"
    MAXIMIZE_CARBON_SEQUESTRATION = "maximize_carbon_sequestration"
    MAXIMIZE_SHADE = "maximize_shade"
    MINIMIZE_MAINTENANCE = "minimize_maintenance"
    MAXIMIZE_NATIVE_RATIO = "maximize_native_ratio"
    MAXIMIZE_AESTHETIC_VALUE = "maximize_aesthetic_value"
    MINIMIZE_COST = "minimize_cost"


class ConstraintType(str, Enum):
    """Categories of design constraints."""
    WATER_BUDGET = "water_budget"               # Maximum annual irrigation (m³)
    BUDGET = "budget"                            # Maximum project budget (currency)
    MAINTENANCE_LEVEL = "maintenance_level"      # low / medium / high
    NATIVE_RATIO_MINIMUM = "native_ratio_minimum" # Minimum % native species
    SPECIES_COUNT_RANGE = "species_count_range"  # Min and max species in palette
    REQUIRED_SPECIES = "required_species"        # Species that must be included
    EXCLUDED_SPECIES = "excluded_species"        # Species that must not be used
    MAX_HEIGHT = "max_height"                    # Height restrictions (e.g., utilities)
    REGULATORY_STANDARD = "regulatory_standard"  # Municipality or agency requirement


class MaintenanceLevel(str, Enum):
    """Maintenance intensity categories."""
    MINIMAL = "minimal"         # Rainfall only once established, no pruning
    LOW = "low"                  # Supplemental irrigation, annual pruning
    MODERATE = "moderate"        # Regular irrigation, seasonal maintenance
    HIGH = "high"                # Frequent irrigation, intensive maintenance


@dataclass
class Objective:
    """
    A single design objective with priority weighting.

    Parameters
    ----------
    objective_type : ObjectiveType
        What to optimize
    weight : float
        Relative importance (0.0 to 1.0). Sum of all objective weights
        should equal 1.0 in a well-formed brief.
    target_value : Optional[float]
        Specific target if applicable (e.g., 0.8 for 80% native ratio)
    """

    objective_type: ObjectiveType
    weight: float = 0.25
    target_value: Optional[float] = None


@dataclass
class Constraint:
    """
    A hard constraint that must be satisfied.

    Unlike objectives (which are optimized), constraints must be met.
    """

    constraint_type: ConstraintType
    value: object  # Type depends on constraint: float, str, list, tuple
    description: str = ""


@dataclass
class DesignBrief:
    """
    A complete design brief connecting a site to design intent.

    This is the input to the optimizer and AI reasoning layer. It captures
    what the project is trying to achieve, within what constraints, at what
    budget, and for whom.

    Parameters
    ----------
    name : str
        Project name or identifier
    site : Site
        The physical site
    objectives : list[Objective]
        Ordered list of design objectives with weights
    constraints : list[Constraint]
        Hard constraints that must be satisfied
    water_budget_m3_yr : Optional[float]
        Maximum annual irrigation water allocation
    budget_currency : Optional[str]
        Currency code for project budget
    budget_amount : Optional[float]
        Total project budget
    maintenance_level : MaintenanceLevel
        Target maintenance intensity
    regulatory_standards : list[str]
        Applicable regulations or standards (e.g., "Dubai Municipality LSP-2025")
    stakeholder_notes : str
        Any qualitative brief from client, community, or stakeholders
    """

    name: str
    site: Site
    objectives: list[Objective] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)
    water_budget_m3_yr: Optional[float] = None
    budget_currency: str = "AED"
    budget_amount: Optional[float] = None
    maintenance_level: MaintenanceLevel = MaintenanceLevel.LOW
    regulatory_standards: list[str] = field(default_factory=list)
    stakeholder_notes: str = ""

    @property
    def weighted_objectives(self) -> dict[ObjectiveType, float]:
        """Return objectives as a dict with normalized weights."""
        total = sum(obj.weight for obj in self.objectives)
        if total == 0:
            return {}
        return {
            obj.objective_type: obj.weight / total
            for obj in self.objectives
        }

    @property
    def primary_objective(self) -> Optional[ObjectiveType]:
        """Return the highest-weighted objective."""
        if not self.objectives:
            return None
        return max(self.objectives, key=lambda o: o.weight).objective_type

    @property
    def is_conservation_focused(self) -> bool:
        """True if biodiversity or native ratio is the primary objective."""
        primary = self.primary_objective
        return primary in {
            ObjectiveType.MAXIMIZE_BIODIVERSITY,
            ObjectiveType.MAXIMIZE_NATIVE_RATIO,
        }

    @property
    def is_climate_focused(self) -> bool:
        """True if heat mitigation or carbon is the primary objective."""
        primary = self.primary_objective
        return primary in {
            ObjectiveType.MAXIMIZE_SHADE,
            ObjectiveType.MAXIMIZE_CARBON_SEQUESTRATION,
        }

    @property
    def is_cost_focused(self) -> bool:
        """True if minimizing water or budget is the primary objective."""
        primary = self.primary_objective
        return primary in {
            ObjectiveType.MINIMIZE_WATER_USE,
            ObjectiveType.MINIMIZE_COST,
        }

    def summary(self) -> str:
        """Human-readable summary of the design brief."""
        lines = [
            f"Design Brief: {self.name}",
            f"────────────────{'─' * len(self.name)}",
            f"Site: {self.site.name} ({self.site.area_hectares:.1f} ha)",
            f"Climate: {self.site.climate_zone.value}",
            f"Land use: {self.site.land_use.value}",
            f"Maintenance: {self.maintenance_level.value}",
        ]

        if self.objectives:
            lines.append("\nObjectives:")
            for obj in sorted(self.objectives, key=lambda o: o.weight, reverse=True):
                lines.append(f"  • {obj.objective_type.value} (weight: {obj.weight:.0%})")

        if self.constraints:
            lines.append("\nConstraints:")
            for con in self.constraints:
                lines.append(f"  • {con.constraint_type.value}: {con.value}")

        if self.water_budget_m3_yr:
            lines.append(f"\nWater budget: {self.water_budget_m3_yr:,.0f} m³/yr")

        if self.budget_amount:
            lines.append(f"Project budget: {self.budget_currency} {self.budget_amount:,.0f}")

        if self.regulatory_standards:
            lines.append(f"Standards: {', '.join(self.regulatory_standards)}")

        if self.stakeholder_notes:
            lines.append(f"\nNotes: {self.stakeholder_notes}")

        return "\n".join(lines)
