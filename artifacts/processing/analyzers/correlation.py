"""Correlation analysis components"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any, Optional, Tuple

from ..base import BaseAnalyzer
from ..utilities import weighted_correlation, should_exclude_zeros, get_weight_column


class CorrelationAnalyzer:
    """Analyzes correlations in census data"""

    def __init__(self, df: pd.DataFrame, weight_col: Optional[str] = None):
        self.df = df
        self.weight_col = weight_col
        self.has_weights = weight_col is not None and weight_col in df.columns

    def analyze(self, focus_vars: List[str]) -> Dict[str, Any]:
        if len(self.df) < 100:
            from exceptions import InsufficientDataError
            raise InsufficientDataError('correlation analysis', 100, len(self.df))
        numeric_df = self._get_numeric_subset(focus_vars)
        if numeric_df.shape[1] < 2:
            from exceptions import CorrelationAnalysisError
            raise CorrelationAnalysisError(focus_vars, 'Insufficient numeric variables')

        result = {
            'correlation_matrix': self._calc_correlations(numeric_df),
            'strong_correlations': self._find_strong_corr(numeric_df)
        }

        # Add weighted correlations if weights available
        if self.has_weights:
            result['weighted_correlations'] = self._calc_weighted_correlations(focus_vars)

        return result

    def _get_numeric_subset(self, focus_vars: List[str]) -> pd.DataFrame:
        available = [v for v in focus_vars if v in self.df.columns]
        return self.df[available].select_dtypes(include=[np.number])

    def _filter_zeros_for_correlation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter out zero values for columns where zeros are meaningless (DRY helper)."""
        df_filtered = df.copy()
        for col in df.columns:
            if should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan
        return df_filtered

    def _calc_correlations(self, df: pd.DataFrame) -> Dict:
        if df.empty:
            return {}
        df_filtered = self._filter_zeros_for_correlation(df)
        return df_filtered.corr().to_dict()

    def _find_strong_corr(self, df: pd.DataFrame, threshold: float = 0.7) -> List[Tuple]:
        if df.empty:
            return []
        df_filtered = self._filter_zeros_for_correlation(df)
        corr_matrix = df_filtered.corr()

        # Vectorized approach: use numpy to find strong correlations in upper triangle
        corr_values = corr_matrix.values
        upper_mask = np.triu(np.ones_like(corr_values, dtype=bool), k=1)
        strong_mask = (np.abs(corr_values) > threshold) & upper_mask
        rows, cols = np.where(strong_mask)

        columns = corr_matrix.columns
        return [(columns[r], columns[c], abs(corr_values[r, c])) for r, c in zip(rows, cols)]

    def _calc_weighted_correlations(self, focus_vars: List[str]) -> Dict[str, Any]:
        """Calculate weighted correlations PER YEAR then aggregate."""
        if not self.has_weights or 'Census_Year' not in self.df.columns:
            return {}

        available = [v for v in focus_vars if v in self.df.columns]
        numeric_cols = [c for c in available if pd.api.types.is_numeric_dtype(self.df[c])]

        if len(numeric_cols) < 2:
            return {}

        # Calculate weighted correlations per year
        yearly_corrs = {}
        for year in self.df['Census_Year'].unique():
            year_df = self.df[self.df['Census_Year'] == year]
            weights = pd.to_numeric(year_df[self.weight_col], errors='coerce').values

            year_corrs = {}
            for i, col1 in enumerate(numeric_cols):
                for col2 in numeric_cols[i+1:]:
                    x = pd.to_numeric(year_df[col1], errors='coerce').values
                    y = pd.to_numeric(year_df[col2], errors='coerce').values

                    # Filter zeros for economic columns
                    mask = ~(np.isnan(x) | np.isnan(y) | np.isnan(weights) | (weights <= 0))
                    if should_exclude_zeros(col1):
                        mask &= (x > 0)
                    if should_exclude_zeros(col2):
                        mask &= (y > 0)

                    if mask.sum() >= 10:
                        wcorr = weighted_correlation(x[mask], y[mask], weights[mask])
                        if not np.isnan(wcorr):
                            key = f"{col1}__{col2}"
                            year_corrs[key] = wcorr

            if year_corrs:
                yearly_corrs[int(year)] = year_corrs

        # Aggregate across years (average weighted correlation)
        all_pairs = set()
        for yc in yearly_corrs.values():
            all_pairs.update(yc.keys())

        aggregated = {}
        for pair in all_pairs:
            vals = [yc[pair] for yc in yearly_corrs.values() if pair in yc]
            if vals:
                aggregated[pair] = {
                    'avg_weighted_corr': float(np.mean(vals)),
                    'std_across_years': float(np.std(vals)) if len(vals) > 1 else 0,
                    'n_years': len(vals)
                }

        return {
            'by_year': yearly_corrs,
            'aggregated': aggregated
        }


class AdvancedCorrelationAnalyzer:
    """Enhanced correlation analysis with multiple methods and partial correlations"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        from logging_config import get_logger
        self.logger = get_logger("processing.advanced_correlation")

    def analyze(self, focus_vars: List[str],
                methods: List[str] = ['pearson', 'spearman', 'kendall']) -> Dict[str, Any]:
        """Compute correlations using multiple methods"""
        self.logger.debug(f"Computing correlations with methods: {methods}")
        numeric_df = self._get_numeric_subset(focus_vars)
        if numeric_df.shape[1] < 2:
            return {'error': 'Insufficient numeric variables'}

        results = {}
        if 'pearson' in methods:
            results['pearson'] = self._calc_correlation(numeric_df, method='pearson')
        if 'spearman' in methods:
            results['spearman'] = self._calc_correlation(numeric_df, method='spearman')
        if 'kendall' in methods:
            results['kendall'] = self._calc_correlation(numeric_df, method='kendall')

        # Find correlations that differ significantly between methods
        results['method_comparison'] = self._compare_methods(results)
        return results

    def _get_numeric_subset(self, focus_vars: List[str]) -> pd.DataFrame:
        available = [v for v in focus_vars if v in self.df.columns]
        df = self.df[available].select_dtypes(include=[np.number])
        # Filter zeros for economic columns
        for col in df.columns:
            if should_exclude_zeros(col):
                df = df[df[col] > 0]
        return df

    def _calc_correlation(self, df: pd.DataFrame, method: str = 'pearson') -> Dict:
        """Calculate correlation matrix using specified method"""
        if df.empty:
            return {}
        try:
            corr_matrix = df.corr(method=method)
            return corr_matrix.to_dict()
        except Exception as e:
            self.logger.warning(f"Correlation calculation failed ({method}): {e}")
            return {}

    def _compare_methods(self, results: Dict[str, Dict]) -> List[Dict]:
        """Find correlations that differ significantly between methods"""
        differences = []
        if 'pearson' not in results or 'spearman' not in results:
            return differences

        pearson = results.get('pearson', {})
        spearman = results.get('spearman', {})

        for col1 in pearson:
            for col2 in pearson.get(col1, {}):
                p_val = pearson.get(col1, {}).get(col2, 0)
                s_val = spearman.get(col1, {}).get(col2, 0)
                if p_val and s_val:
                    diff = abs(p_val - s_val)
                    if diff > 0.2:  # Significant difference threshold
                        differences.append({
                            'var1': col1, 'var2': col2,
                            'pearson': p_val, 'spearman': s_val,
                            'difference': diff,
                            'interpretation': 'Non-linear relationship likely' if s_val > p_val else 'Outliers affecting Pearson'
                        })
        return differences

    def calc_partial_correlation(self, var1: str, var2: str,
                                  control_vars: List[str]) -> Optional[float]:
        """Calculate partial correlation controlling for other variables"""
        try:
            from scipy import stats
            import numpy as np

            # Get relevant columns
            all_vars = [var1, var2] + control_vars
            df = self.df[all_vars].dropna()

            if len(df) < 10:
                return None

            # Regress var1 on control variables
            X = df[control_vars].values
            y1 = df[var1].values
            y2 = df[var2].values

            # Add constant for regression
            X_with_const = np.column_stack([np.ones(len(X)), X])

            # Get residuals for var1
            beta1, _, _, _ = np.linalg.lstsq(X_with_const, y1, rcond=None)
            resid1 = y1 - X_with_const @ beta1

            # Get residuals for var2
            beta2, _, _, _ = np.linalg.lstsq(X_with_const, y2, rcond=None)
            resid2 = y2 - X_with_const @ beta2

            # Correlation of residuals is partial correlation
            partial_corr, _ = stats.pearsonr(resid1, resid2)
            return float(partial_corr)
        except Exception as e:
            self.logger.warning(f"Partial correlation failed: {e}")
            return None
