"""Temporal analysis classes for census data."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from ..utilities.zero_exclusion import should_exclude_zeros
from exceptions import InsufficientDataError, TemporalAnalysisError


# ============================================================================
# TEMPORAL ANALYZER
# ============================================================================

class TemporalAnalyzer:
    """Analyzes temporal trends"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def analyze(self) -> Dict[str, Any]:
        if len(self.df) < 100:
            raise InsufficientDataError('temporal analysis', 100, len(self.df))
        if 'Census_Year' not in self.df.columns:
            raise TemporalAnalysisError('Missing Census_Year column')
        return {
            'year_distribution': self._year_dist(),
            'trends': self._compute_trends(),
            'growth_rates': self._growth_rates(),
            'temporal_patterns': self._patterns()
        }

    def _year_dist(self) -> Dict[int, int]:
        return self.df['Census_Year'].value_counts().sort_index().to_dict()

    def _compute_trends(self) -> Dict[str, Dict]:
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        trends = {}

        for col in numeric_cols:  # Top 10 numeric columns
            trends[col] = self._column_trend(col)

        return trends

    def _column_trend(self, col: str) -> Dict:
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly = numeric_col.groupby(df_filtered['Census_Year']).agg(['mean', 'median', 'std'])
        return yearly.to_dict('index')

    def _growth_rates(self) -> Dict[str, float]:
        years = sorted(self.df['Census_Year'].unique())
        if len(years) < 2:
            return {}

        first_year = self.df[self.df['Census_Year'] == years[0]]
        last_year = self.df[self.df['Census_Year'] == years[-1]]

        return {
            'sample_growth': (len(last_year) - len(first_year)) / len(first_year) * 100
        }

    def _patterns(self) -> Dict[str, Any]:
        return {
            'years_covered': len(self.df['Census_Year'].unique()),
            'year_range': (self.df['Census_Year'].min(), self.df['Census_Year'].max()),
            'missing_years': self._find_missing_years()
        }

    def _find_missing_years(self) -> List[int]:
        # Explicitly convert to int to avoid type errors with range()
        years = sorted([int(y) for y in self.df['Census_Year'].unique() if pd.notna(y)])
        if not years:
            return []
        full_range = range(int(years[0]), int(years[-1]) + 1)
        return [y for y in full_range if y not in years]


# ============================================================================
# ANOMALY ANALYZER
# ============================================================================

class AnomalyAnalyzer:
    """Detects temporal anomalies and unusual patterns"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def analyze(self, focus_vars: Optional[List[str]] = None) -> Dict[str, Any]:
        """Detect temporal anomalies"""
        print("[VERBOSE] Detecting temporal anomalies...")

        if 'Census_Year' not in self.df.columns:
            return {'error': 'Census_Year column not found'}

        if focus_vars is None:
            focus_vars = self._get_key_numeric_columns()

        anomaly_summary = {}
        for col in focus_vars:  # Limit to top 8
            anomaly_summary[col] = self._detect_temporal_anomalies(col)

        return {
            'anomaly_years': anomaly_summary,
            'total_anomalies': self._count_total_anomalies(anomaly_summary)
        }

    def _get_key_numeric_columns(self) -> List[str]:
        """Get key numeric columns for analysis"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Cost', 'Age', 'Hours']
        priority_cols = [c for c in numeric_cols if any(k in c for k in keywords)]
        return priority_cols if priority_cols else numeric_cols

    def _detect_temporal_anomalies(self, col: str) -> Dict[str, Any]:
        """Detect anomalies in temporal trends"""
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if should_exclude_zeros(col):
            numeric_col = numeric_col[numeric_col > 0]
        yearly_median = numeric_col.groupby(self.df['Census_Year']).median().sort_index()

        if len(yearly_median) < 3:
            return {'anomaly_years': [], 'reason': 'Insufficient years'}

        # Calculate moving average
        ma = yearly_median.rolling(window=3, center=True).mean()
        std_dev = yearly_median.std()

        # Identify anomalies (> 1.5 std devs from moving average)
        anomalies = []
        for year in yearly_median.index:
            if pd.notna(ma.loc[year]):
                deviation = abs(yearly_median.loc[year] - ma.loc[year])
                if deviation > 1.5 * std_dev:
                    anomalies.append({
                        'year': int(year),
                        'value': float(yearly_median.loc[year]),
                        'expected': float(ma.loc[year]),
                        'deviation': float(deviation)
                    })

        return {'anomaly_years': anomalies}

    def _count_total_anomalies(self, anomaly_summary: Dict) -> int:
        """Count total anomalies across all variables"""
        total = 0
        for var_anomalies in anomaly_summary.values():
            if 'anomaly_years' in var_anomalies:
                total += len(var_anomalies['anomaly_years'])
        return total


# ============================================================================
# TREND ANALYZER
# ============================================================================

class TrendAnalyzer:
    """Analyzes trend strength and significance"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def analyze(self, focus_vars: Optional[List[str]] = None) -> Dict[str, Any]:
        """Analyze trend strength for key variables"""
        print("[VERBOSE] Analyzing trend strength and significance...")

        if 'Census_Year' not in self.df.columns:
            return {'error': 'Census_Year column not found'}

        if focus_vars is None:
            focus_vars = self._get_key_numeric_columns()

        trend_summary = {}
        for col in focus_vars:
            trend_summary[col] = self._analyze_trend(col)

        return {
            'trend_analysis': trend_summary,
            'strong_trends': self._find_strong_trends(trend_summary),
            'trend_directions': self._categorize_trends(trend_summary)
        }

    def _get_key_numeric_columns(self) -> List[str]:
        """Get key numeric columns for analysis"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Cost', 'Age', 'Hours', 'Earnings']
        priority_cols = [c for c in numeric_cols if any(k in c for k in keywords)]
        return priority_cols if priority_cols else numeric_cols

    def _analyze_trend(self, col: str) -> Dict[str, Any]:
        """Analyze trend for a single variable"""
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if should_exclude_zeros(col):
            numeric_col = numeric_col[numeric_col > 0]
        yearly_median = numeric_col.groupby(self.df['Census_Year']).median().sort_index()

        if len(yearly_median) < 3:
            return {'error': 'Insufficient data'}

        # Calculate linear regression
        years = np.array(yearly_median.index)
        values = np.array(yearly_median.values)

        # Remove NaN values
        mask = ~np.isnan(values)
        years = years[mask]
        values = values[mask]

        if len(years) < 3:
            return {'error': 'Insufficient valid data'}

        # Linear regression
        A = np.vstack([years, np.ones(len(years))]).T
        slope, intercept = np.linalg.lstsq(A, values, rcond=None)[0]

        # Calculate R-squared
        predicted = slope * years + intercept
        ss_res = np.sum((values - predicted) ** 2)
        ss_tot = np.sum((values - np.mean(values)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Overall change
        pct_change = ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0

        return {
            'slope': float(slope),
            'r_squared': float(r_squared),
            'direction': 'increasing' if slope > 0 else 'decreasing',
            'trend_strength': 'strong' if r_squared > 0.7 else 'moderate' if r_squared > 0.4 else 'weak',
            'percent_change': float(pct_change),
            'years_analyzed': int(len(years))
        }

    def _find_strong_trends(self, trend_summary: Dict) -> List[tuple]:
        """Find variables with strong trends"""
        strong = []
        for var, trend in trend_summary.items():
            if 'error' not in trend and trend['r_squared'] > 0.7:
                strong.append((var, trend['r_squared'], trend['direction']))
        return sorted(strong, key=lambda x: x[1], reverse=True)

    def _categorize_trends(self, trend_summary: Dict) -> Dict[str, List[str]]:
        """Categorize trends by direction and strength"""
        categories = {
            'strong_increasing': [],
            'strong_decreasing': [],
            'moderate_increasing': [],
            'moderate_decreasing': [],
            'weak_or_flat': []
        }

        for var, trend in trend_summary.items():
            if 'error' in trend:
                continue

            strength = trend['trend_strength']
            direction = trend['direction']

            if strength == 'strong':
                if direction == 'increasing':
                    categories['strong_increasing'].append(var)
                else:
                    categories['strong_decreasing'].append(var)
            elif strength == 'moderate':
                if direction == 'increasing':
                    categories['moderate_increasing'].append(var)
                else:
                    categories['moderate_decreasing'].append(var)
            else:
                categories['weak_or_flat'].append(var)

        return categories
