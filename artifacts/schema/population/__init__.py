from .base import PopulationSurvey
from .one_year import Population1Year
from .five_year import Population5Year
from .eras import (
    Population1Year_2007_2011,
    Population1Year_2012_2016,
    Population1Year_2017_2022,
    Population1Year_2023_Plus,
)


def get_population_schema(year: int, scope: str = '1-Year') -> PopulationSurvey:
    """
    Factory function to get the correct population schema for a given year.

    Args:
        year: Census data year (2007-2024+)
        scope: '1-Year' or '5-Year'

    Returns:
        Appropriate PopulationSurvey subclass instance
    """
    if scope.lower().replace('-', '').replace('year', '') == '5':
        return Population5Year()

    # 1-Year era-specific schemas
    if year <= 2011:
        return Population1Year_2007_2011()
    elif year <= 2016:
        return Population1Year_2012_2016()
    elif year <= 2022:
        return Population1Year_2017_2022()
    else:
        return Population1Year_2023_Plus()


__all__ = [
    'PopulationSurvey',
    'Population1Year', 'Population5Year',
    'Population1Year_2007_2011', 'Population1Year_2012_2016',
    'Population1Year_2017_2022', 'Population1Year_2023_Plus',
    'get_population_schema',
]
