"""
Feature Engineering Package for Census Data Analysis.

Provides modular feature creation, selection, transformation, and encoding capabilities.
Following the same pattern as the report/ and visualizations/ packages.
"""

from .base import BaseFeatureCreator
from .orchestrator import FeatureEngineer

from .cleaning import SmartDataCleaner

from .creators import (
    FeatureCreator,
    EconomicFeatureCreator,
    DisabilityFeatureCreator,
    HealthInsuranceFeatureCreator,
    OccupationIndustryFeatureCreator,
    EducationFieldFeatureCreator,
    HouseholdCompositionFeatureCreator,
)

from .selection import FeatureSelector, AdvancedFeatureSelector

from .transformation import FeatureTransformer, CategoricalEncoder, DimensionalityReducer

__all__ = [
    # Base and orchestrator
    'BaseFeatureCreator',
    'FeatureEngineer',

    # Cleaning
    'SmartDataCleaner',

    # Creators
    'FeatureCreator',
    'EconomicFeatureCreator',
    'DisabilityFeatureCreator',
    'HealthInsuranceFeatureCreator',
    'OccupationIndustryFeatureCreator',
    'EducationFieldFeatureCreator',
    'HouseholdCompositionFeatureCreator',

    # Selection
    'FeatureSelector',
    'AdvancedFeatureSelector',

    # Transformation
    'FeatureTransformer',
    'CategoricalEncoder',
    'DimensionalityReducer',
]
