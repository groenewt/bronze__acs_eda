"""
Cross-variable and regional comparison analyzers for Census ACS data
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

from ..base import BaseAnalyzer
from exceptions import InsufficientRegionsError, RegionDataMismatchError


# ============================================================================
# CROSS-VARIABLE ANALYZER
# ============================================================================

class CrossVariableAnalyzer:
    """Analyzes relationships and interactions between multiple variables"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def analyze(self, variable_groups: Optional[List[List[str]]] = None) -> Dict[str, Any]:
        """Analyze cross-variable relationships"""
        if variable_groups is None:
            variable_groups = self._get_default_groups()

        results = {
            'group_correlations': {},
            'interaction_effects': {},
            'ratio_analysis': {}
        }

        for group in variable_groups:
            group_name = '_'.join(group[:2])
            results['group_correlations'][group_name] = self._analyze_group(group)
            results['interaction_effects'][group_name] = self._analyze_interactions(group)
            results['ratio_analysis'][group_name] = self._analyze_ratios(group)

        return results

    def _get_default_groups(self) -> List[List[str]]:
        """Get default variable groups for analysis"""
        groups = []

        # Income-related group
        income_vars = [c for c in self.df.columns if 'Income' in c or 'Wage' in c]
        if len(income_vars) >= 2:
            groups.append(income_vars[:3])

        # Housing-related group
        housing_vars = [c for c in self.df.columns if any(k in c for k in ['Value', 'Rent', 'Bedroom', 'Room'])]
        if len(housing_vars) >= 2:
            groups.append(housing_vars[:3])

        # Demographic group
        demo_vars = [c for c in self.df.columns if any(k in c for k in ['Age', 'Education', 'Employment'])]
        if len(demo_vars) >= 2:
            groups.append(demo_vars[:3])

        return groups if groups else [[]]

    def _analyze_group(self, variables: List[str]) -> Dict[str, Any]:
        """Analyze correlations within a variable group"""
        from ..utilities import should_exclude_zeros

        existing = [v for v in variables if v in self.df.columns]
        if len(existing) < 2:
            return {'error': 'Insufficient variables'}

        subset = self.df[existing].select_dtypes(include=[np.number])
        if subset.shape[1] < 2:
            return {'error': 'Insufficient numeric variables'}

        # Filter zeros for each column before correlation
        subset_filtered = subset.copy()
        for col in subset.columns:
            if should_exclude_zeros(col):
                numeric_col = pd.to_numeric(subset_filtered[col], errors='coerce')
                subset_filtered.loc[numeric_col <= 0, col] = np.nan
        corr_matrix = subset_filtered.corr()
        return {
            'variables': existing,
            'avg_correlation': float(corr_matrix.mean().mean()),
            'max_correlation': float(corr_matrix.max().max()),
            'min_correlation': float(corr_matrix.min().min())
        }

    def _analyze_interactions(self, variables: List[str]) -> Dict[str, Any]:
        """Analyze interaction effects between variables"""
        existing = [v for v in variables if v in self.df.columns][:2]
        if len(existing) < 2:
            return {'error': 'Insufficient variables'}

        v1, v2 = existing[0], existing[1]
        if v1 not in self.df.columns or v2 not in self.df.columns:
            return {'error': 'Variables not found'}

        n1 = pd.to_numeric(self.df[v1], errors='coerce')
        n2 = pd.to_numeric(self.df[v2], errors='coerce')

        interaction = n1 * n2
        valid_interaction = interaction.dropna()

        if len(valid_interaction) == 0:
            return {'error': 'No valid interaction data'}

        return {
            'variables': existing,
            'interaction_mean': float(valid_interaction.mean()),
            'interaction_std': float(valid_interaction.std()),
            'interaction_range': [float(valid_interaction.min()), float(valid_interaction.max())]
        }

    def _analyze_ratios(self, variables: List[str]) -> Dict[str, Any]:
        """Analyze ratios between variables"""
        existing = [v for v in variables if v in self.df.columns][:2]
        if len(existing) < 2:
            return {'error': 'Insufficient variables'}

        v1, v2 = existing[0], existing[1]
        n1 = pd.to_numeric(self.df[v1], errors='coerce')
        n2 = pd.to_numeric(self.df[v2], errors='coerce')

        ratio = n1 / n2.replace(0, np.nan)
        valid_ratio = ratio.dropna()

        if len(valid_ratio) == 0:
            return {'error': 'No valid ratio data'}

        return {
            'variables': f"{v1}/{v2}",
            'ratio_mean': float(valid_ratio.mean()),
            'ratio_median': float(valid_ratio.median()),
            'ratio_std': float(valid_ratio.std())
        }


# ============================================================================
# REGIONAL COMPARISON ANALYZER
# ============================================================================

class RegionalComparisonAnalyzer:
    """Compares census data across different regions/states"""

    def __init__(self, regional_data: Dict[str, pd.DataFrame]):
        """Initialize with dictionary of region_name: dataframe"""
        self.regional_data = regional_data
        self.regions = list(regional_data.keys())

    def compare_all(self, focus_vars: Optional[List[str]] = None) -> Dict[str, Any]:
        """Comprehensive regional comparison"""
        if len(self.regions) < 2:
            return {'error': 'Need at least 2 regions for comparison'}

        if focus_vars is None:
            focus_vars = self._get_common_variables()

        return {
            'regions_compared': self.regions,
            'variable_comparison': self._compare_variables(focus_vars),
            'economic_comparison': self._compare_economics(),
            'demographic_comparison': self._compare_demographics(),
            'temporal_comparison': self._compare_temporal_trends(focus_vars),
            'rankings': self._compute_rankings(focus_vars)
        }

    def _get_common_variables(self) -> List[str]:
        """Get variables common to all regions"""
        if not self.regional_data:
            return []

        common = set(self.regional_data[self.regions[0]].columns)
        for region in self.regions[1:]:
            common &= set(self.regional_data[region].columns)

        numeric_common = []
        first_df = self.regional_data[self.regions[0]]
        for col in common:
            if pd.api.types.is_numeric_dtype(first_df[col]):
                numeric_common.append(col)

        return numeric_common

    def _compare_variables(self, variables: List[str]) -> Dict[str, Any]:
        """Compare specific variables across regions"""
        from ..utilities import should_exclude_zeros

        comparisons = {}

        for var in variables:
            var_data = {}
            for region, df in self.regional_data.items():
                if var in df.columns:
                    numeric_col = pd.to_numeric(df[var], errors='coerce')
                    if should_exclude_zeros(var):
                        numeric_col = numeric_col[numeric_col > 0]
                    var_data[region] = {
                        'mean': float(numeric_col.mean()),
                        'median': float(numeric_col.median()),
                        'std': float(numeric_col.std()),
                        'count': int(numeric_col.count())
                    }

            if len(var_data) >= 2:
                comparisons[var] = {
                    'by_region': var_data,
                    'variance_across_regions': self._calc_regional_variance(var_data)
                }

        return comparisons

    def _calc_regional_variance(self, var_data: Dict) -> float:
        """Calculate variance in means across regions"""
        means = [data['mean'] for data in var_data.values()]
        return float(np.var(means)) if means else 0.0

    def _compare_economics(self) -> Dict[str, Any]:
        """Compare economic indicators across regions"""
        economic_vars = ['Total_Person_Income', 'Wage_Income', 'Property_Value', 'Gross_Rent']
        comparisons = {}

        for var in economic_vars:
            regional_stats = {}
            for region, df in self.regional_data.items():
                if var in df.columns:
                    numeric_col = pd.to_numeric(df[var], errors='coerce').dropna()
                    if len(numeric_col) > 0:
                        regional_stats[region] = {
                            'median': float(numeric_col.median()),
                            'mean': float(numeric_col.mean())
                        }

            if regional_stats:
                comparisons[var] = regional_stats

        return comparisons

    def _compare_demographics(self) -> Dict[str, Any]:
        """Compare demographic indicators across regions"""
        demo_vars = ['Age', 'Hours_Worked_Per_Week']
        comparisons = {}

        for var in demo_vars:
            regional_stats = {}
            for region, df in self.regional_data.items():
                if var in df.columns:
                    numeric_col = pd.to_numeric(df[var], errors='coerce')
                    regional_stats[region] = {
                        'mean': float(numeric_col.mean()),
                        'median': float(numeric_col.median())
                    }

            if regional_stats:
                comparisons[var] = regional_stats

        return comparisons

    def _compare_temporal_trends(self, variables: List[str]) -> Dict[str, Any]:
        """Compare temporal trends across regions"""
        trend_comparisons = {}

        for var in variables:
            regional_trends = {}
            for region, df in self.regional_data.items():
                if var in df.columns and 'Census_Year' in df.columns:
                    numeric_col = pd.to_numeric(df[var], errors='coerce')
                    yearly = numeric_col.groupby(df['Census_Year']).median()

                    if len(yearly) >= 2:
                        pct_change = ((yearly.iloc[-1] - yearly.iloc[0]) / yearly.iloc[0] * 100) if yearly.iloc[0] != 0 else 0
                        regional_trends[region] = float(pct_change)

            if regional_trends:
                trend_comparisons[var] = regional_trends

        return trend_comparisons

    def _compute_rankings(self, variables: List[str]) -> Dict[str, Any]:
        """Rank regions by various metrics"""
        rankings = {}

        for var in variables:
            regional_medians = {}
            for region, df in self.regional_data.items():
                if var in df.columns:
                    numeric_col = pd.to_numeric(df[var], errors='coerce')
                    regional_medians[region] = numeric_col.median()

            if regional_medians:
                sorted_regions = sorted(regional_medians.items(), key=lambda x: x[1], reverse=True)
                rankings[var] = [{'rank': i+1, 'region': r, 'value': float(v)}
                               for i, (r, v) in enumerate(sorted_regions)]

        return rankings
