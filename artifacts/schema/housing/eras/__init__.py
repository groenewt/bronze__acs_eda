"""
Housing schema era-specific classes for ACS data.

Each era represents a distinct period with different column names and availability:
- 2007-2011: Early ACS format (BDS, RMS, VAL, no adjustment factors)
- 2012-2016: Standardized codes introduced (BDSP, RMSP, VALP, adjustment factors)
- 2017-2022: Technology columns added (ACCESS, BROADBND, etc.)
- 2023+: Column renames (ACCESSINET, YRBLT, TYPEHUGQ, TAXAMT)
"""

from .era_2007_2011 import Housing1Year_2007_2011
from .era_2012_2016 import Housing1Year_2012_2016
from .era_2017_2022 import Housing1Year_2017_2022
from .era_2023_plus import Housing1Year_2023_Plus

__all__ = [
    'Housing1Year_2007_2011',
    'Housing1Year_2012_2016',
    'Housing1Year_2017_2022',
    'Housing1Year_2023_Plus',
]
