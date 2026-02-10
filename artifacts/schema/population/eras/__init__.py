"""
Year-range specific population schema classes.

This module provides era-specific schema classes that handle the differences
in column naming and availability across different ACS survey periods.

Available eras:
- 2007-2011: Population1Year_2007_2011
- 2012-2016: Population1Year_2012_2016
- 2017-2022: Population1Year_2017_2022
- 2023+: Population1Year_2023_Plus
"""

from .era_2007_2011 import Population1Year_2007_2011
from .era_2012_2016 import Population1Year_2012_2016
from .era_2017_2022 import Population1Year_2017_2022
from .era_2023_plus import Population1Year_2023_Plus

__all__ = [
    'Population1Year_2007_2011',
    'Population1Year_2012_2016',
    'Population1Year_2017_2022',
    'Population1Year_2023_Plus',
]
