"""Statistical analysis components"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple

from ..base import BaseAnalyzer
from ..utilities import (
    get_zero_exclusion_columns, should_exclude_zeros,
    get_weight_column, weighted_mean, weighted_std, weighted_median,
    calc_weighted_stats_by_year
)


class StatisticalAnalyzer:
    """Computes comprehensive summary statistics for census data"""

    def __init__(self, df: pd.DataFrame, weight_col: Optional[str] = None):
        self.df = df
        self.weight_col = weight_col
        self.has_weights = weight_col is not None and weight_col in df.columns

    def analyze(self, focus_vars: Optional[List[str]] = None) -> Dict[str, Any]:
        """Compute comprehensive statistics for key variables"""
        print("[VERBOSE] Computing comprehensive summary statistics...")
        if self.has_weights:
            print(f"[VERBOSE] Using sample weights from '{self.weight_col}' column")

        # Get numeric columns to analyze
        if focus_vars:
            # Filter to columns that exist and are numeric
            available_cols = []
            for c in focus_vars:
                if c in self.df.columns:
                    try:
                        # Try to convert to numeric to test if it's numeric
                        pd.to_numeric(self.df[c], errors='coerce')
                        available_cols.append(c)
                    except:
                        pass
            numeric_cols = available_cols
        else:
            numeric_cols = self._get_key_numeric_columns()

        print(f"[VERBOSE] Analyzing {len(numeric_cols)} numeric variables")

        stats_summary = {}
        for col in numeric_cols:
            stats_summary[col] = self._compute_column_statistics(col)

        return {
            'summary_statistics': stats_summary,
            'overall_metrics': self._compute_overall_metrics(numeric_cols),
            'distribution_analysis': self._analyze_distributions(numeric_cols)
        }

    def _get_key_numeric_columns(self) -> List[str]:
        """Identify key numeric columns for analysis"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()

        # Prioritize columns with meaningful keywords
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Cost', 'Tax',
                   'Age', 'Hours', 'Poverty', 'Earnings', 'Payment']

        priority_cols = [c for c in numeric_cols if any(k in c for k in keywords)]

        # Return top priority columns (limit to avoid overwhelming output)
        return priority_cols if priority_cols else numeric_cols

    def _compute_column_statistics(self, col: str) -> Dict[str, Any]:
        """Compute comprehensive statistics for a single column"""
        series = pd.to_numeric(self.df[col], errors='coerce').dropna()
        if should_exclude_zeros(col):
            series = series[series > 0]

        if len(series) == 0:
            return {'error': 'No valid numeric data'}

        try:
            from scipy import stats as scipy_stats

            result = {
                'count': int(len(series)),
                'mean': float(series.mean()),
                'median': float(series.median()),
                'std_dev': float(series.std()),
                'variance': float(series.var()),
                'min': float(series.min()),
                'max': float(series.max()),
                'q25': float(series.quantile(0.25)),
                'q75': float(series.quantile(0.75)),
                'skewness': float(scipy_stats.skew(series)),
                'kurtosis': float(scipy_stats.kurtosis(series)),
                'range': float(series.max() - series.min()),
                'cv': float(series.std() / series.mean() * 100) if series.mean() != 0 else 0
            }

            # Add weighted statistics if weights available
            if self.has_weights:
                weighted_by_year = calc_weighted_stats_by_year(self.df, col, self.weight_col)
                if weighted_by_year:
                    # Aggregate weighted stats across years
                    all_wmeans = [y['weighted_mean'] for y in weighted_by_year.values() if not np.isnan(y['weighted_mean'])]
                    all_wmedians = [y['weighted_median'] for y in weighted_by_year.values() if not np.isnan(y['weighted_median'])]
                    result['weighted_mean_avg'] = float(np.mean(all_wmeans)) if all_wmeans else None
                    result['weighted_median_avg'] = float(np.mean(all_wmedians)) if all_wmedians else None
                    result['weighted_by_year'] = weighted_by_year

            return result
        except ImportError:
            # Fallback if scipy not available
            return {
                'count': int(len(series)),
                'mean': float(series.mean()),
                'median': float(series.median()),
                'std_dev': float(series.std()),
                'variance': float(series.var()),
                'min': float(series.min()),
                'max': float(series.max()),
                'q25': float(series.quantile(0.25)),
                'q75': float(series.quantile(0.75)),
                'skewness': float(series.skew()),
                'kurtosis': float(series.kurtosis()),
                'range': float(series.max() - series.min()),
                'cv': float(series.std() / series.mean() * 100) if series.mean() != 0 else 0
            }
        except Exception as e:
            return {'error': str(e)}

    def _compute_overall_metrics(self, numeric_cols: List[str]) -> Dict[str, Any]:
        """Compute dataset-wide statistical metrics"""
        try:
            numeric_df = self.df[numeric_cols].select_dtypes(include=[np.number])

            # Convert all columns to numeric
            for col in numeric_df.columns:
                numeric_df[col] = pd.to_numeric(numeric_df[col], errors='coerce')

            return {
                'total_variables': len(numeric_cols),
                'total_observations': len(self.df),
                'avg_missing_rate': float(numeric_df.isna().mean().mean() * 100),
                'highly_variable_vars': self._find_high_variance_vars(numeric_df),
                'skewed_distributions': self._find_skewed_distributions(numeric_df)
            }
        except Exception as e:
            return {'error': str(e)}

    def _find_high_variance_vars(self, df: pd.DataFrame) -> List[Tuple[str, float]]:
        """Find variables with high coefficient of variation"""
        cv_values = []
        for col in df.columns:
            series = df[col].dropna()
            if should_exclude_zeros(col):
                series = series[series > 0]
            if len(series) > 0 and series.mean() != 0:
                cv = series.std() / series.mean() * 100
                if cv > 100:  # CV > 100% indicates high variability
                    cv_values.append((col, float(cv)))
        return sorted(cv_values, key=lambda x: x[1], reverse=True)

    def _find_skewed_distributions(self, df: pd.DataFrame) -> List[Tuple[str, float]]:
        """Find highly skewed distributions"""
        skewed = []
        for col in df.columns:
            series = df[col].dropna()
            if should_exclude_zeros(col):
                series = series[series > 0]
            if len(series) > 0:
                try:
                    skew_val = series.skew()
                    if abs(skew_val) > 1.0:  # Highly skewed if |skewness| > 1
                        skewed.append((col, float(skew_val)))
                except:
                    pass
        return sorted(skewed, key=lambda x: abs(x[1]), reverse=True)

    def _analyze_distributions(self, numeric_cols: List[str]) -> Dict[str, Any]:
        """Analyze distribution characteristics"""
        analysis = {
            'normal_distributions': [],
            'skewed_right': [],
            'skewed_left': [],
            'heavy_tailed': []
        }

        for col in numeric_cols:  # Analyze top 10 to avoid overwhelming
            series = pd.to_numeric(self.df[col], errors='coerce').dropna()
            if should_exclude_zeros(col):
                series = series[series > 0]
            if len(series) < 30:  # Need sufficient data
                continue

            try:
                skew = series.skew()
                kurt = series.kurtosis()

                # Classify distribution
                if abs(skew) < 0.5 and abs(kurt) < 0.5:
                    analysis['normal_distributions'].append(col)
                elif skew > 1.0:
                    analysis['skewed_right'].append(col)
                elif skew < -1.0:
                    analysis['skewed_left'].append(col)

                if kurt > 3.0:
                    analysis['heavy_tailed'].append(col)
            except:
                pass

        return analysis


class OutlierAnalyzer:
    """Detects and quantifies outliers using IQR method"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def analyze(self, focus_vars: Optional[List[str]] = None) -> Dict[str, Any]:
        """Detect outliers across key variables"""
        print("[VERBOSE] Detecting outliers using IQR method...")

        if focus_vars is None:
            focus_vars = self._get_key_numeric_columns()

        outlier_summary = {}
        for col in focus_vars:  # Limit to top 10
            outlier_summary[col] = self._detect_outliers(col)

        return {
            'outlier_counts': outlier_summary,
            'high_outlier_vars': self._find_high_outlier_vars(outlier_summary),
            'outlier_statistics': self._compute_outlier_stats(outlier_summary)
        }

    def _get_key_numeric_columns(self) -> List[str]:
        """Get key numeric columns for analysis"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Cost', 'Tax', 'Age', 'Hours']
        priority_cols = [c for c in numeric_cols if any(k in c for k in keywords)]
        return priority_cols if priority_cols else numeric_cols

    def _detect_outliers(self, col: str) -> Dict[str, Any]:
        """Detect outliers for a single column using IQR method"""
        series = pd.to_numeric(self.df[col], errors='coerce').dropna()
        if should_exclude_zeros(col):
            series = series[series > 0]
        if len(series) == 0:
            return {'error': 'No valid data'}

        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = series[(series < lower_bound) | (series > upper_bound)]

        return {
            'total_count': int(len(series)),
            'outlier_count': int(len(outliers)),
            'outlier_percentage': float(len(outliers) / len(series) * 100),
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'min_outlier': float(outliers.min()) if len(outliers) > 0 else None,
            'max_outlier': float(outliers.max()) if len(outliers) > 0 else None
        }

    def _find_high_outlier_vars(self, outlier_summary: Dict) -> List[Tuple[str, float]]:
        """Find variables with highest outlier percentages"""
        high_outliers = []
        for var, stats in outlier_summary.items():
            if 'error' not in stats and stats['outlier_percentage'] > 5.0:
                high_outliers.append((var, stats['outlier_percentage']))
        return sorted(high_outliers, key=lambda x: x[1], reverse=True)

    def _compute_outlier_stats(self, outlier_summary: Dict) -> Dict[str, Any]:
        """Compute overall outlier statistics"""
        valid_vars = [s for s in outlier_summary.values() if 'error' not in s]
        if not valid_vars:
            return {}

        outlier_pcts = [s['outlier_percentage'] for s in valid_vars]

        return {
            'avg_outlier_percentage': float(np.mean(outlier_pcts)),
            'max_outlier_percentage': float(np.max(outlier_pcts)),
            'vars_with_outliers': sum(1 for p in outlier_pcts if p > 0),
            'total_vars_analyzed': len(valid_vars)
        }
