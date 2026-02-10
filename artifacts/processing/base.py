import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseAnalyzer(ABC):
    """Base class for all analyzers"""

    def __init__(self, df: pd.DataFrame, survey_type: str = None):
        self.df = df
        self.survey_type = survey_type

    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Execute analysis and return results dict"""
        pass

    def _validate_columns(self, required: List[str]) -> bool:
        """Check if required columns exist"""
        missing = [c for c in required if c not in self.df.columns]
        return len(missing) == 0

    def _get_numeric_columns(self) -> List[str]:
        """Get list of numeric columns"""
        return self.df.select_dtypes(include=[np.number]).columns.tolist()
