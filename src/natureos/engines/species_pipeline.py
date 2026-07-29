"""
Species Data Pipeline - fetches and enriches species data from global
biodiversity databases for any location on Earth.

Tier 1 (Free): Automated via GBIF, WorldClim, SoilGrids APIs.
Tier 2 (Free): Community-contributed corrections and vernacular names.
Tier 3 (Paid): Certified, expert-validated datasets with audit trail.

The pipeline produces NatureOS Species objects ready for all engines.
"""

from dataclasses import dataclass, field
from natureos.species import Species, GrowthForm, WaterRegime, SalinityTolerance, ThermalTolerance, EcosystemType
from typing import Optional
import json


@dataclass
class SpeciesPipeline:
    """
    Fetches and enriches species data for a geographic location.

    Parameters
    ----------
    latitude : float
        Decimal degrees
    longitude : float
        Decimal degrees
    radius_km : float
        Search radius around the point
    max_species : int
        Maximum species to return
    """

    latitude: float
    longitude: float
    radius_km: float = 50.0
    max_species: int = 50

    def fetch(self) -> list[Species]:
        """
        Fetch species from global databases for this location.

        Currently returns the curated MENA dataset as the base layer.
        External API integration (GBIF, TRY) planned for v0.4.

        Returns
        -------
        list[Species]
            Species occurring in the region around this point
        """
        # For now, return the curated MENA dataset
        # GBIF integration: v0.4
        # TRY Plant Trait Database: v0.4
        # WorldClim climate matching: v0.5

        from natureos.data.mena_species import ALL_SPECIES

        return ALL_SPECIES

    def enrich_with_traits(self, species_list: list[Species]) -> list[Species]:
        """
        Enrich species with functional traits from global databases.

        Currently returns species as-is with existing parameters.
        TRY database integration planned for v0.4.

        Parameters
        ----------
        species_list : list[Species]
            Species to enrich

        Returns
        -------
        list[Species]
            Enriched species with additional trait data
        """
        return species_list

    def to_geojson(self, species_list: list[Species]) -> dict:
        """
        Export species as a GeoJSON FeatureCollection for GIS integration.

        Parameters
        ----------
        species_list : list[Species]
            Species to export

        Returns
        -------
        dict
            GeoJSON FeatureCollection
        """
        features = []
        for sp in species_list:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [self.longitude, self.latitude]
                },
                "properties": {
                    "scientific_name": sp.scientific_name,
                    "common_names": sp.common_names,
                    "growth_form": sp.growth_form.value,
                    "water_regime": sp.water_regime.value,
                    "is_native": sp.is_native,
                    "wildlife_value": sp.wildlife_value,
                }
            })

        return {
            "type": "FeatureCollection",
            "features": features,
            "metadata": {
                "source": "NatureOS Species Pipeline v0.1",
                "location": [self.longitude, self.latitude],
                "radius_km": self.radius_km,
                "species_count": len(species_list),
            }
        }
