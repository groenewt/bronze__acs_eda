"""Correlation visualizations for relationships between variables"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

from .base import BaseVisualizer, get_key_column_keywords, _EXCLUDE_COLUMN_PATTERNS
from .formatting import tight_layout_safe
from memory_utils import adaptive_sample
from logging_config import get_logger

logger = get_logger("visualization.correlation")


class CorrelationVisualizer(BaseVisualizer):
    """Visualizes correlations and relationships"""

    def create_all(self):
        self._apply_housing_sampling()
        logger.verbose("Creating correlation heatmap...")
        self._correlation_heatmap()
        logger.verbose("Creating scatter matrix...")
        self._scatter_matrix()

    def _get_key_columns(self, limit: int = 10) -> List[str]:
        """Get key numeric columns using centralized keywords from base.py"""
        numeric = self.df.select_dtypes(include=[np.number]).columns
        # Use centralized exclude patterns from base.py
        valuable = [c for c in numeric if not any(p in c for p in _EXCLUDE_COLUMN_PATTERNS)]
        # Use centralized keywords from base.py
        keywords = get_key_column_keywords(self.survey_type)
        return [c for c in valuable if any(k in c for k in keywords)][:limit]

    def _correlation_heatmap(self):
        key_cols = self._get_key_columns()
        if len(key_cols) < 2:
            logger.verbose(f"Skipping correlation heatmap: insufficient key columns (found {len(key_cols)})")
            return

        logger.verbose(f"Creating heatmap with {len(key_cols)} columns")
        plt.figure(figsize=(12, 10))
        # corr() handles NA internally via pairwise deletion
        corr = self.df[key_cols].corr()
        # Convert to float for seaborn compatibility
        corr = corr.astype(float)
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                    center=0, square=True, linewidths=1)
        plt.title('Correlation Heatmap - Key Variables', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('correlation_heatmap.png')

    def _scatter_matrix(self):
        key_cols = self._get_key_columns(limit=8)
        if len(key_cols) < 2:
            logger.verbose(f"Skipping scatter matrix: insufficient key columns (found {len(key_cols)})")
            return

        df_subset = adaptive_sample(self.df[key_cols], survey_type=self.survey_type)
        logger.verbose(f"Creating scatter matrix with {len(key_cols)} columns, {len(df_subset)} rows")

        # scatter_matrix handles NA pairwise internally
        pd.plotting.scatter_matrix(df_subset, figsize=(12, 12), diagonal='hist', alpha=0.5)
        plt.suptitle('Scatter Matrix - Key Variables', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('scatter_matrix.png')
