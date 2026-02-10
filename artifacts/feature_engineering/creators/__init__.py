"""
Feature Creators Module

Provides specialized feature creator classes for different domains of census data analysis.
Each creator focuses on a specific aspect of feature engineering:

- basic: Fundamental feature operations (ratios, interactions, polynomials)
- economic: Economic and housing features (Gini, affordability, poverty)
- disability: Disability-related features and interactions
- health_insurance: Health insurance coverage features
- occupation: Occupation and industry classification features
- education: Education field and STEM categorization features
- household: Household composition and demographic features
"""

from .basic import FeatureCreator
from .economic import EconomicFeatureCreator
from .disability import DisabilityFeatureCreator
from .health_insurance import HealthInsuranceFeatureCreator
from .occupation import OccupationIndustryFeatureCreator
from .education import EducationFieldFeatureCreator
from .household import HouseholdCompositionFeatureCreator

__all__ = [
    'FeatureCreator',
    'EconomicFeatureCreator',
    'DisabilityFeatureCreator',
    'HealthInsuranceFeatureCreator',
    'OccupationIndustryFeatureCreator',
    'EducationFieldFeatureCreator',
    'HouseholdCompositionFeatureCreator',
]
