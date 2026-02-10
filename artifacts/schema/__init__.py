"""
Schema Module for ACS Survey Data
Provides schema definitions for Population and Housing surveys.

Era-aware schemas handle year-over-year Census Bureau changes:
- 2007-2011: Original field codes (BDS, RMS, VAL), lowercase weights
- 2012-2016: Standardized codes (BDSP, RMSP, VALP), adjustment factors
- 2017-2022: Technology columns (ACCESS, BROADBND, etc.), uppercase weights
- 2023+: Nomenclature refinements (ACCESSINET, YRBLT, TYPEHUGQ, etc.)
"""
from .base import (
    SchemaDefinition,
    ERA_2007_2011, ERA_2012_2016, ERA_2017_2022, ERA_2023_PLUS,
    ERA_INDICATORS,
)
from .population import (
    PopulationSurvey, Population1Year, Population5Year,
    Population1Year_2007_2011, Population1Year_2012_2016,
    Population1Year_2017_2022, Population1Year_2023_Plus,
    get_population_schema,
)
from .housing import (
    HousingSurvey, Housing1Year, Housing5Year,
    Housing1Year_2007_2011, Housing1Year_2012_2016,
    Housing1Year_2017_2022, Housing1Year_2023_Plus,
    get_housing_schema,
)


def get_schema(survey_type: str, year: int, scope: str = '1-Year'):
    """
    Factory function to get the correct schema for a given survey type and year.

    Args:
        survey_type: 'population' or 'housing'
        year: Census data year (2007-2024+)
        scope: '1-Year' or '5-Year'

    Returns:
        Appropriate schema instance

    Example:
        >>> schema = get_schema('housing', 2023)
        >>> mapping = schema.get_raw_to_standard_mapping()
    """
    survey = survey_type.lower()
    if survey == 'population':
        return get_population_schema(year, scope)
    elif survey == 'housing':
        return get_housing_schema(year, scope)
    else:
        raise ValueError(f"Unknown survey type: {survey_type}. Use 'population' or 'housing'.")


__all__ = [
    # Base
    'SchemaDefinition',
    # Era constants
    'ERA_2007_2011', 'ERA_2012_2016', 'ERA_2017_2022', 'ERA_2023_PLUS',
    'ERA_INDICATORS',
    # Population
    'PopulationSurvey', 'Population1Year', 'Population5Year',
    'Population1Year_2007_2011', 'Population1Year_2012_2016',
    'Population1Year_2017_2022', 'Population1Year_2023_Plus',
    'get_population_schema',
    # Housing
    'HousingSurvey', 'Housing1Year', 'Housing5Year',
    'Housing1Year_2007_2011', 'Housing1Year_2012_2016',
    'Housing1Year_2017_2022', 'Housing1Year_2023_Plus',
    'get_housing_schema',
    # Unified factory
    'get_schema',
]
