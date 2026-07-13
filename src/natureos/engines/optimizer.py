"""
Design Optimizer engine — multi-objective optimization for ecological
planting design.

Implements a simplified multi-objective evolutionary approach inspired by
NSGA-II (Deb et al., 2002) to find Pareto-optimal species palettes that
balance competing ecological and practical objectives.

Optimization objectives:
- Maximize biodiversity (Shannon index)
- Minimize water demand
- Maximize carbon sequestration
- Minimize cost (species count as proxy for complexity)

The optimizer treats species selection as a combinatorial optimization
problem over a candidate species pool with ecological constraints.

References:
- Deb, K. et al. (2002). A fast and elitist multiobjective genetic
  algorithm: NSGA-II.
- Coello Coello, C.A. et al. (2007). Evolutionary Algorithms for
  Solving Multi-Objective Problems.
"""

from dataclasses import dataclass, field
from enum import Enum
from natureos.species import Species
from natureos.site import Site
from natureos.engines.water import WaterBudget
from natureos.engines.biodiversity import BiodiversityIndex
from natureos.engines.carbon import CarbonEstimator
import random
import math


class Objective(str, Enum):
    """Optimization objectives."""
    MAXIMIZE_BIODIVERSITY = "maximize_biodiversity"
    MINIMIZE_WATER = "minimize_water"
    MAXIMIZE_CARBON = "maximize_carbon"
    MINIMIZE_COST = "minimize_cost"


@dataclass
class DesignSolution:
    """A single solution in the optimization — a species palette."""

    species: list[Species]
    biodiversity_score: float = 0.0
    water_demand_m3: float = 0.0
    carbon_sequestration_t: float = 0.0
    species_count: int = 0
    fitness: float = 0.0                # Weighted aggregate fitness
    rank: int = 0                       # Pareto rank (lower = better)
    crowding_distance: float = 0.0      # Diversity within same rank

    def summary(self) -> str:
        species_names = [sp.display_name for sp in self.species]
        return (
            f"Design Solution\n"
            f"───────────────\n"
            f"Species ({len(self.species)}): {', '.join(species_names)}\n"
            f"Biodiversity (H'): {self.biodiversity_score:.3f}\n"
            f"Water demand: {self.water_demand_m3:.0f} m³/yr\n"
            f"Carbon sequestration: {self.carbon_sequestration_t:.2f} t CO₂e\n"
            f"Fitness: {self.fitness:.3f}"
        )


@dataclass
class OptimizationResult:
    """Complete result of a design optimization run."""

    pareto_front: list[DesignSolution] = field(default_factory=list)
    all_solutions: list[DesignSolution] = field(default_factory=list)
    generations: int = 0
    total_evaluations: int = 0

    def best(self) -> DesignSolution | None:
        """Return the highest-fitness solution."""
        if not self.all_solutions:
            return None
        return max(self.all_solutions, key=lambda s: s.fitness)

    def summary(self) -> str:
        best = self.best()
        return (
            f"Optimization Complete\n"
            f"────────────────────\n"
            f"Generations: {self.generations}\n"
            f"Solutions evaluated: {self.total_evaluations}\n"
            f"Pareto-optimal solutions: {len(self.pareto_front)}\n"
            f"Best fitness: {best.fitness:.3f}" if best else ""
        )


@dataclass
class DesignOptimizer:
    """
    Multi-objective optimizer for ecological planting design.

    Uses a simplified evolutionary algorithm to find species palettes
    that optimize biodiversity, water use, carbon sequestration, and
    design complexity.

    Parameters
    ----------
    candidate_species : list[Species]
        Pool of species to select from
    site : Site
        The site being designed for
    objectives : list[Objective]
        Objectives to optimize. Order determines priority weighting.
    palette_size_min : int
        Minimum number of species in a palette
    palette_size_max : int
        Maximum number of species in a palette
    population_size : int
        Number of solutions per generation
    generations : int
        Number of evolutionary generations
    mutation_rate : float
        Probability of mutation per solution
    """

    candidate_species: list[Species]
    site: Site
    objectives: list[Objective] = field(default_factory=lambda: [
        Objective.MAXIMIZE_BIODIVERSITY,
        Objective.MINIMIZE_WATER,
        Objective.MAXIMIZE_CARBON,
        Objective.MINIMIZE_COST,
    ])
    palette_size_min: int = 3
    palette_size_max: int = 12
    population_size: int = 50
    generations: int = 30
    mutation_rate: float = 0.2

    def optimize(self) -> OptimizationResult:
        """
        Run the multi-objective optimization.

        Returns
        -------
        OptimizationResult
            Complete optimization results with Pareto front
        """
        if len(self.candidate_species) < self.palette_size_min:
            raise ValueError(
                f"Candidate species pool ({len(self.candidate_species)}) "
                f"is smaller than minimum palette size ({self.palette_size_min})"
            )

        # Initialize population
        population = self._initialize_population()
        all_solutions: list[DesignSolution] = []

        for generation in range(self.generations):
            # Evaluate all solutions
            for solution in population:
                self._evaluate(solution)

            all_solutions.extend(population)

            # Non-dominated sorting (simplified Pareto ranking)
            self._assign_pareto_ranks(population)

            # Select parents (tournament selection on Pareto rank)
            parents = self._tournament_selection(population, self.population_size // 2)

            # Crossover and mutate to create offspring
            offspring = []
            for i in range(0, len(parents) - 1, 2):
                child1, child2 = self._crossover(parents[i], parents[i + 1])
                offspring.append(self._mutate(child1))
                offspring.append(self._mutate(child2))

            # Elitism: keep best solutions from current population
            population.sort(key=lambda s: (s.rank, -s.fitness))
            elites = population[: self.population_size // 4]

            # New population: elites + offspring + random newcomers
            population = elites + offspring
            while len(population) < self.population_size:
                population.append(self._random_solution())

        # Final evaluation
        for solution in population:
            self._evaluate(solution)
        all_solutions.extend(population)

        # Extract Pareto front (rank 0 solutions)
        pareto_front = [s for s in all_solutions if s.rank == 0]

        return OptimizationResult(
            pareto_front=pareto_front,
            all_solutions=all_solutions,
            generations=self.generations,
            total_evaluations=len(all_solutions),
        )

    def _initialize_population(self) -> list[DesignSolution]:
        """Generate initial random population."""
        return [self._random_solution() for _ in range(self.population_size)]

    def _random_solution(self) -> DesignSolution:
        """Generate a random species palette."""
        size = random.randint(self.palette_size_min, self.palette_size_max)
        selected = random.sample(
            self.candidate_species,
            min(size, len(self.candidate_species))
        )
        return DesignSolution(species=selected)

    def _evaluate(self, solution: DesignSolution) -> None:
        """
        Evaluate all objectives for a solution and compute fitness.

        Each objective is normalized to [0, 1] and combined with weights
        based on objective priority order.
        """
        species = solution.species
        if not species:
            solution.fitness = 0.0
            return

        # Biodiversity (Shannon index, normalized by log(species_count))
        bio = BiodiversityIndex.from_equal_abundance(species)
        bio_result = bio.calculate()
        max_possible_h = math.log(len(self.candidate_species))
        biodiversity_norm = (
            bio_result.shannon_index / max_possible_h
            if max_possible_h > 0 else 0.0
        )

        # Water demand (normalized inverse — lower water = higher score)
        water = WaterBudget(site=self.site)
        water_result = water.calculate(species)
        # Normalize: assume max demand is all HIGH water species
        max_demand = 1400 / 1000 * self.site.area_hectares * 10000 / 0.85
        water_norm = 1.0 - min(1.0, water_result.net_irrigation_required_m3 / max(max_demand, 1))

        # Carbon sequestration (normalized)
        carbon = CarbonEstimator(
            species_counts={sp: 10 for sp in species},
            site_area_hectares=self.site.area_hectares,
        )
        carbon_result = carbon.calculate()
        # Normalize: assume max ~50 tCO2e for a small site
        carbon_norm = min(1.0, carbon_result.co2_equivalent_t / 50.0)

        # Cost/complexity (normalized inverse - fewer species = lower cost)
        cost_norm = 1.0 - (len(species) - self.palette_size_min) / (
            self.palette_size_max - self.palette_size_min
        ) if self.palette_size_max > self.palette_size_min else 1.0

        # Store objective values
        solution.biodiversity_score = round(biodiversity_norm, 4)
        solution.water_demand_m3 = round(water_result.net_irrigation_required_m3, 2)
        solution.carbon_sequestration_t = round(carbon_result.co2_equivalent_t, 4)
        solution.species_count = len(species)

        # Weighted fitness equal weights across objectives
        weights = {
            Objective.MAXIMIZE_BIODIVERSITY: 0.30,
            Objective.MINIMIZE_WATER: 0.30,
            Objective.MAXIMIZE_CARBON: 0.25,
            Objective.MINIMIZE_COST: 0.15,
        }

        fitness = 0.0
        total_weight = 0.0
        for obj in self.objectives:
            w = weights.get(obj, 0.25)
            total_weight += w
            if obj == Objective.MAXIMIZE_BIODIVERSITY:
                fitness += w * biodiversity_norm
            elif obj == Objective.MINIMIZE_WATER:
                fitness += w * water_norm
            elif obj == Objective.MAXIMIZE_CARBON:
                fitness += w * carbon_norm
            elif obj == Objective.MINIMIZE_COST:
                fitness += w * cost_norm

        solution.fitness = round(fitness / total_weight, 4) if total_weight > 0 else 0.0

    def _assign_pareto_ranks(self, population: list[DesignSolution]) -> None:
        """
        Simplified non-dominated sorting.
        Assigns rank 0 to solutions not dominated by any other solution.
        """
        for i, sol_a in enumerate(population):
            dominated = False
            for j, sol_b in enumerate(population):
                if i == j:
                    continue
                # Check if sol_b dominates sol_a (better or equal on all objectives)
                if (sol_b.biodiversity_score >= sol_a.biodiversity_score and
                    sol_b.water_demand_m3 <= sol_a.water_demand_m3 and
                    sol_b.carbon_sequestration_t >= sol_a.carbon_sequestration_t and
                    sol_b.species_count <= sol_a.species_count):
                    # At least one strictly better
                    if (sol_b.biodiversity_score > sol_a.biodiversity_score or
                        sol_b.water_demand_m3 < sol_a.water_demand_m3 or
                        sol_b.carbon_sequestration_t > sol_a.carbon_sequestration_t or
                        sol_b.species_count < sol_a.species_count):
                        dominated = True
                        break
            sol_a.rank = 1 if dominated else 0

    def _tournament_selection(
        self, population: list[DesignSolution], num_parents: int
    ) -> list[DesignSolution]:
        """Tournament selection based on Pareto rank and fitness."""
        selected = []
        for _ in range(num_parents):
            candidates = random.sample(population, min(3, len(population)))
            candidates.sort(key=lambda s: (s.rank, -s.fitness))
            selected.append(candidates[0])
        return selected

    def _crossover(
        self, parent1: DesignSolution, parent2: DesignSolution
    ) -> tuple[DesignSolution, DesignSolution]:
        """Crossover: combine species from both parents."""
        combined = list(set(parent1.species + parent2.species))
        random.shuffle(combined)

        split = len(combined) // 2
        child1_species = combined[:max(split, self.palette_size_min)]
        child2_species = combined[max(split, self.palette_size_min):]

        # Ensure minimum size
        if len(child1_species) < self.palette_size_min:
            remaining = [s for s in self.candidate_species if s not in child1_species]
            child1_species.extend(
                random.sample(remaining, self.palette_size_min - len(child1_species))
            )
        if len(child2_species) < self.palette_size_min:
            remaining = [s for s in self.candidate_species if s not in child2_species]
            child2_species.extend(
                random.sample(remaining, self.palette_size_min - len(child2_species))
            )

        return DesignSolution(species=child1_species), DesignSolution(species=child2_species)

    def _mutate(self, solution: DesignSolution) -> DesignSolution:
        """
        Mutate a solution by randomly adding, removing, or swapping species.
        """
        species = list(solution.species)

        if random.random() < self.mutation_rate:
            mutation_type = random.choice(["add", "remove", "swap"])

            if mutation_type == "add" and len(species) < self.palette_size_max:
                new_species = [
                    s for s in self.candidate_species if s not in species
                ]
                if new_species:
                    species.append(random.choice(new_species))

            elif mutation_type == "remove" and len(species) > self.palette_size_min:
                species.remove(random.choice(species))

            elif mutation_type == "swap" and species:
                new_species = [
                    s for s in self.candidate_species if s not in species
                ]
                if new_species:
                    species.remove(random.choice(species))
                    species.append(random.choice(new_species))

        return DesignSolution(species=species)
