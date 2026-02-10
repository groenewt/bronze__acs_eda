from .base import HousingSurvey
from .one_year import Housing1Year
from .five_year import Housing5Year
from .eras import (
    Housing1Year_2007_2011,
    Housing1Year_2012_2016,
    Housing1Year_2017_2022,
    Housing1Year_2023_Plus,
)


def get_housing_schema(year: int, scope: str = '1-Year') -> HousingSurvey:
    """
    Factory function to get the correct housing schema for a given year.

    Args:
        year: Census data year (2007-2024+)
        scope: '1-Year' or '5-Year'

    Returns:
        Appropriate HousingSurvey subclass instance
    """
    if scope.lower().replace('-', '').replace('year', '') == '5':
        return Housing5Year()

    # 1-Year era-specific schemas
    if year <= 2011:
        return Housing1Year_2007_2011()
    elif year <= 2016:
        return Housing1Year_2012_2016()
    elif year <= 2022:
        return Housing1Year_2017_2022()
    else:
        return Housing1Year_2023_Plus()


__all__ = [
    'HousingSurvey',
    'Housing1Year', 'Housing5Year',
    'Housing1Year_2007_2011', 'Housing1Year_2012_2016',
    'Housing1Year_2017_2022', 'Housing1Year_2023_Plus',
    'get_housing_schema',
]
