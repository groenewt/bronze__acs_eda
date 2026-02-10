from typing import Dict
from .base import PopulationSurvey
from .one_year import Population1Year


class Population5Year(PopulationSurvey):
    """5-year population survey with raw column name mappings"""

    def get_raw_to_standard_mapping(self) -> Dict[str, str]:
        """
        Maps raw 5-year column names to standardized names.
        Population data has identical structure between 1-year and 5-year.
        """
        # 5-year population uses the same raw column names as 1-year
        return Population1Year().get_raw_to_standard_mapping()
