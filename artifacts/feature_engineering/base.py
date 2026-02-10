"""Base classes for feature engineering."""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from abc import ABC, abstractmethod

from logging_config import get_logger


class BaseFeatureCreator(ABC):
    """Abstract base class for feature creators."""

    def __init__(self, survey_type: str = ""):
        self.survey_type = survey_type.upper() if survey_type else ""
        self.logger = get_logger("feature_engineering")

    @abstractmethod
    def create_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Create features. Must be implemented by subclasses.

        Returns:
            Tuple of (enhanced_df, metadata_dict)
        """
        pass

    def _validate_columns(self, df: pd.DataFrame, required: List[str],
                          operation: str) -> List[str]:
        """Return list of available columns from required list."""
        available = [c for c in required if c in df.columns]
        missing = set(required) - set(available)
        if missing:
            self.logger.warning(f"{operation}: Missing columns {missing}")
        return available

    def _log_created_features(self, created: List[str], operation: str) -> None:
        """Log the created features."""
        if created:
            self.logger.debug(f"{operation}: Created {len(created)} features: {created}")
