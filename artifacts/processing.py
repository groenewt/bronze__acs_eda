import pandas as pd
import numpy as np
import glob
import os
import re
import requests
import json
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

from config import Config, ProcessingStats, SurveyMetadata
from schema import (SchemaDefinition, PopulationSchema, HousingSchema,
                    Population1Year, Population5Year, Housing1Year, Housing5Year)
from exceptions import (DataError, EmptyDataError, MissingColumnsError, 
                        UnsupportedSurveyTypeError, InsufficientDataError,
                        TemporalAnalysisError, CorrelationAnalysisError,
                        StatisticalAnalysisError, OutlierDetectionError,
                        InsufficientRegionsError, RegionDataMismatchError)


# ============================================================================
# SCHEMA FACTORY
# ============================================================================

class SchemaFactory:
    """Factory for schema instantiation"""

    @staticmethod
    def create(survey_type: str, scope: str = '1-Year') -> SchemaDefinition:
        # Case-insensitive normalization: remove hyphens and 'year'/'Year', then strip
        scope_normalized = scope.replace('-', '').lower().replace('year', '').strip()
        schemas = {
            ('population', '1'): Population1Year,
            ('population', '5'): Population5Year,
            ('housing', '1'): Housing1Year,
            ('housing', '5'): Housing5Year
        }
        key = (survey_type.lower(), scope_normalized)
        schema_class = schemas.get(key)
        if not schema_class:
            raise UnsupportedSurveyTypeError(survey_type, list(set(k[0] for k in schemas.keys())))
        return schema_class()


# ============================================================================
# FILE LOADER
# ============================================================================

class FileLoader:
    """Handles CSV file loading"""

    def __init__(self, config: Config):
        self.config = config
        self.stats = ProcessingStats()

    def load(self, survey_type: str, scope: str) -> pd.DataFrame:
        print(f"[VERBOSE] Searching for {survey_type} files with scope {scope}...")
        files = self._find_files(survey_type, scope)
        print(f"[VERBOSE] Found {len(files)} file(s) to load")
        
        dfs = []
        for idx, f in enumerate(files, 1):
            print(f"[VERBOSE] Loading file {idx}/{len(files)}: {os.path.basename(f)}")
            df = self._load_file(f)
            if df is not None:
                dfs.append(df)
                print(f"[VERBOSE]   -> Loaded {len(df):,} rows")
        
        print(f"[VERBOSE] Successfully loaded {len(dfs)} dataframe(s)")
        if not dfs:
            raise EmptyDataError(f"{survey_type} ({scope})")
        combined_df = pd.concat([d for d in dfs if d is not None], ignore_index=True)
        if len(combined_df) == 0:
            raise EmptyDataError(f"{survey_type} ({scope})")
        print(f"[VERBOSE] Combined into {len(combined_df):,} total rows")
        
        # Update stats with combined data info
        self.stats.total_rows = len(combined_df)
        self.stats.columns_found = len(combined_df.columns)
        
        return combined_df

    def _find_files(self, survey_type: str, scope: str) -> List[str]:
        # Normalize scope for file path: ensure capital Y in "Year"
        # Files are stored as "1-Year" and "5-Year" with capital Y
        if 'year' in scope.lower() and not 'Year' in scope:
            scope = scope.replace('year', 'Year')
        pattern = f"{self.config.folder_base}/{survey_type}/{scope}/{self.config.state_fips}/*/*.csv"
        print(f"Pattern is:{pattern}")
        files = glob.glob(pattern)
        self.stats.files_found = len(files)
        return files

    def _load_file(self, path: str) -> Optional[pd.DataFrame]:
        df = pd.read_csv(path, low_memory=False)
        meta = self._extract_metadata(path)
        return self._add_metadata(df, meta)

    def _extract_metadata(self, path: str) -> Optional[SurveyMetadata]:
        pattern = r"/acs/([^/]+)/([^/]+)/(\d{2})/(\d{4})/"
        match = re.search(pattern, path)
        if not match:
            return None
        # Extract metadata with proper type conversion
        survey_type = match.group(1)
        survey_scope = match.group(2)
        state_fips = str(match.group(3))  # Ensure string to preserve leading zeros
        year = int(match.group(4))  # Ensure int for proper type
        return SurveyMetadata(survey_type, survey_scope, state_fips, year)

    def _add_metadata(self, df: pd.DataFrame, meta: Optional[SurveyMetadata]) -> pd.DataFrame:
        """Add metadata columns with proper type handling"""
        if meta is None:
            # Handle missing metadata gracefully
            df['year'] = pd.NA
            df['survey_type'] = pd.NA
            df['survey_scope'] = pd.NA
            df['state_fips'] = pd.NA
        else:
            # Ensure proper types for concatenation
            df['year'] = pd.Series([meta.year] * len(df), dtype='Int64')
            df['survey_type'] = meta.survey_type
            df['survey_scope'] = meta.survey_scope
            # CRITICAL FIX: Ensure state_fips is always string to preserve leading zeros
            df['state_fips'] = str(meta.state_fips)

        self.stats.files_loaded += 1
        return df


# ============================================================================
# SCHEMA APPLIER
# ============================================================================

class SchemaApplier:
    """Applies schema to raw data"""

    def __init__(self, schema: SchemaDefinition):
        self.schema = schema
        self.stats = {'found': 0, 'missing': 0}

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        cols_map = self._build_column_map(df)
        raw_to_std = self.schema.get_raw_to_standard_mapping()
        result = pd.DataFrame()

        for std_name, dtype, alias in self.schema.get_all_columns():
            # Find raw column name from mapping, or use std_name if not in mapping
            raw_name = None
            for raw, std in raw_to_std.items():
                if std == std_name:
                    raw_name = raw
                    break
            if raw_name is None:
                raw_name = std_name
            
            result[alias] = self._process_column(df, cols_map, raw_name, dtype)

        return result

    def _build_column_map(self, df: pd.DataFrame) -> Dict[str, str]:
        return {col.upper(): col for col in df.columns}

    def _process_column(self, df: pd.DataFrame, cols_map: Dict,
                        raw_name: str, dtype: str) -> pd.Series:
        col_upper = raw_name.upper()

        if col_upper in cols_map:
            self.stats['found'] += 1
            return self._cast_column(df[cols_map[col_upper]], dtype)
        else:
            self.stats['missing'] += 1
            return pd.Series([pd.NA] * len(df))

    def _cast_column(self, series: pd.Series, dtype: str) -> pd.Series:
        """Cast column to specified dtype with robust error handling"""
        try:
            dtype_lower = dtype.lower() if dtype else ''
            if 'int' in dtype_lower or 'bigint' in dtype_lower:
                numeric_series = pd.to_numeric(series, errors='coerce')
                return numeric_series.astype('Int64')
            elif 'float' in dtype_lower or 'decimal' in dtype_lower:
                return pd.to_numeric(series, errors='coerce').astype('float64')
            else:
                return series.astype(str)
        except Exception as e:
            dtype_lower = dtype.lower() if dtype else ''
            if 'int' in dtype_lower or 'float' in dtype_lower or 'decimal' in dtype_lower:
                return pd.to_numeric(series, errors='coerce')
            return series


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
# ECONOMIC ANALYZER BASE
# ============================================================================

# Survey-specific zero-exclusion columns (zeros are meaningless for economic analysis)

# Population survey columns where zero should be excluded
_POP_ZERO_EXCLUDE = [
    # Income columns (schema.py _income_cols)
    'Wage_Income', 'Total_Person_Earnings', 'Total_Person_Income',
    'Self_Employment_Income', 'Interest_Dividend_Rental_Income',
    'Retirement_Income', 'Social_Security_Income', 'Supplemental_Security_Income',
    'Public_Assistance_Income', 'Other_Income',
    # Work/Hours columns (schema.py _work_travel_demographics, _education_work_cols)
    'Travel_Time_To_Work_Minutes', 'Hours_Worked_Per_Week', 'Weeks_Worked_Past_Year',
    # Derived population features
    'Income_Per_Hour', 'Income_Per_Week_Worked', 'Total_Annual_Hours',
]

# Housing survey columns where zero should be excluded
_HOUSING_ZERO_EXCLUDE = [
    # Property values (schema.py _unit_status_cols)
    'Property_Value',
    # Utility costs (schema.py _utility_costs)
    'Condo_Fee_Monthly', 'Electricity_Cost_Monthly', 'Fuel_Cost_Monthly',
    'Gas_Cost_Monthly', 'Insurance_Cost_Yearly', 'Water_Cost_Yearly',
    # Mortgage costs (schema.py _mortgage_costs)
    'Mobile_Home_Costs_Monthly', 'First_Mortgage_Payment_Monthly',
    'Second_Mortgage_Payment_Monthly', 'Property_Taxes_Yearly',
    # Rental costs (schema.py _rental_costs)
    'Rent_Amount_Monthly', 'Gross_Rent', 'Selected_Monthly_Owner_Costs',
    # Household income (schema.py _household_family_cols)
    'Family_Income', 'Household_Income',
    # Derived housing features
    'Total_Monthly_Utility_Cost', 'Property_Tax_Rate', 'Annual_Rent_to_Value_Ratio',
]

# Combined list for backward compatibility
_EXCLUDE_ZERO_RAW = _POP_ZERO_EXCLUDE + _HOUSING_ZERO_EXCLUDE

# NORMALIZE TO UPPERCASE for robust case-insensitive matching
EXCLUDE_ZERO_COLUMNS = {col.upper().strip() for col in _EXCLUDE_ZERO_RAW}
_POP_ZERO_EXCLUDE_SET = {col.upper().strip() for col in _POP_ZERO_EXCLUDE}
_HOUSING_ZERO_EXCLUDE_SET = {col.upper().strip() for col in _HOUSING_ZERO_EXCLUDE}


def get_zero_exclusion_columns(survey_type: str) -> List[str]:
    """Get appropriate zero-exclusion columns for survey type."""
    if survey_type == 'population':
        return _POP_ZERO_EXCLUDE.copy()
    elif survey_type == 'housing':
        return _HOUSING_ZERO_EXCLUDE.copy()
    return _EXCLUDE_ZERO_RAW.copy()


def should_exclude_zeros(col: str, survey_type: str = None) -> bool:
    """
    Check if zeros should be excluded for this column - CASE INSENSITIVE.

    Args:
        col: Column name to check
        survey_type: Optional survey type ('population' or 'housing') for targeted check
    """
    col_upper = col.upper().strip()
    if survey_type == 'population':
        return col_upper in _POP_ZERO_EXCLUDE_SET
    elif survey_type == 'housing':
        return col_upper in _HOUSING_ZERO_EXCLUDE_SET
    return col_upper in EXCLUDE_ZERO_COLUMNS


# ============================================================================
# WEIGHTED STATISTICS HELPERS (ACS Sample Weights)
# ============================================================================

def get_weight_column(survey_type: str) -> str:
    """Get appropriate weight column name for survey type."""
    if survey_type == 'population':
        return 'Person_Weight'
    elif survey_type == 'housing':
        return 'Housing_Unit_Weight'
    return 'Person_Weight'  # Default


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted mean."""
    mask = ~(np.isnan(values) | np.isnan(weights) | (weights <= 0))
    if mask.sum() == 0:
        return np.nan
    return float(np.average(values[mask], weights=weights[mask]))


def weighted_std(values: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted standard deviation."""
    mask = ~(np.isnan(values) | np.isnan(weights) | (weights <= 0))
    if mask.sum() == 0:
        return np.nan
    v, w = values[mask], weights[mask]
    avg = np.average(v, weights=w)
    variance = np.average((v - avg) ** 2, weights=w)
    return float(np.sqrt(variance))


def weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted median (50th percentile)."""
    mask = ~(np.isnan(values) | np.isnan(weights) | (weights <= 0))
    if mask.sum() == 0:
        return np.nan
    v, w = values[mask], weights[mask]
    sorted_idx = np.argsort(v)
    v_sorted, w_sorted = v[sorted_idx], w[sorted_idx]
    cumsum = np.cumsum(w_sorted)
    cutoff = cumsum[-1] / 2.0
    return float(v_sorted[np.searchsorted(cumsum, cutoff)])


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    """Calculate weighted quantile."""
    mask = ~(np.isnan(values) | np.isnan(weights) | (weights <= 0))
    if mask.sum() == 0:
        return np.nan
    v, w = values[mask], weights[mask]
    sorted_idx = np.argsort(v)
    v_sorted, w_sorted = v[sorted_idx], w[sorted_idx]
    cumsum = np.cumsum(w_sorted)
    cutoff = cumsum[-1] * q
    return float(v_sorted[np.searchsorted(cumsum, cutoff)])


def weighted_correlation(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted Pearson correlation coefficient."""
    mask = ~(np.isnan(x) | np.isnan(y) | np.isnan(weights) | (weights <= 0))
    if mask.sum() < 3:
        return np.nan
    x_m, y_m, w = x[mask], y[mask], weights[mask]
    x_mean = np.average(x_m, weights=w)
    y_mean = np.average(y_m, weights=w)
    cov = np.average((x_m - x_mean) * (y_m - y_mean), weights=w)
    x_std = np.sqrt(np.average((x_m - x_mean) ** 2, weights=w))
    y_std = np.sqrt(np.average((y_m - y_mean) ** 2, weights=w))
    if x_std == 0 or y_std == 0:
        return np.nan
    return float(cov / (x_std * y_std))


def calc_weighted_stats_by_year(df: pd.DataFrame, col: str, weight_col: str) -> Dict[int, Dict]:
    """
    Calculate weighted statistics PER YEAR.

    ACS weights are calibrated to each survey year's population totals,
    so weights must be applied within each year, not across years.
    """
    if col not in df.columns or weight_col not in df.columns:
        return {}
    if 'Census_Year' not in df.columns:
        return {}

    results = {}
    numeric_col = pd.to_numeric(df[col], errors='coerce')
    numeric_weight = pd.to_numeric(df[weight_col], errors='coerce')

    # Filter zeros for economic columns
    if should_exclude_zeros(col):
        valid_mask = (numeric_col > 0) & numeric_col.notna() & numeric_weight.notna() & (numeric_weight > 0)
    else:
        valid_mask = numeric_col.notna() & numeric_weight.notna() & (numeric_weight > 0)

    df_valid = df[valid_mask].copy()
    df_valid['_val'] = numeric_col[valid_mask].values
    df_valid['_wgt'] = numeric_weight[valid_mask].values

    for year, group in df_valid.groupby('Census_Year'):
        v = group['_val'].values
        w = group['_wgt'].values
        if len(v) < 10:
            continue
        results[int(year)] = {
            'weighted_mean': weighted_mean(v, w),
            'weighted_median': weighted_median(v, w),
            'weighted_std': weighted_std(v, w),
            'weighted_q25': weighted_quantile(v, w, 0.25),
            'weighted_q75': weighted_quantile(v, w, 0.75),
            'unweighted_mean': float(np.mean(v)),
            'unweighted_median': float(np.median(v)),
            'n_obs': len(v),
            'sum_weights': float(np.sum(w))
        }

    return results


class EconomicAnalyzer(ABC):
    """Base class for economic analysis"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        pass

    def _calc_median_by_year(self, col: str, exclude_zeros: bool = False) -> Dict:
        """Calculate median by year with type safety"""
        if col not in self.df.columns:
            return {}
        # Ensure column is numeric before aggregation
        try:
            numeric_col = pd.to_numeric(self.df[col], errors='coerce')
            # Auto-detect if we should exclude zeros based on column type
            if exclude_zeros or should_exclude_zeros(col):
                numeric_col = numeric_col[numeric_col > 0]
            return numeric_col.groupby(self.df.loc[numeric_col.index, 'Census_Year']).median().to_dict()
        except Exception:
            return {}

    def _calc_mean_by_year(self, col: str, exclude_zeros: bool = False) -> Dict:
        """Calculate mean by year with type safety"""
        if col not in self.df.columns:
            return {}
        # Ensure column is numeric before aggregation
        try:
            numeric_col = pd.to_numeric(self.df[col], errors='coerce')
            # Auto-detect if we should exclude zeros based on column type
            if exclude_zeros or should_exclude_zeros(col):
                numeric_col = numeric_col[numeric_col > 0]
            return numeric_col.groupby(self.df.loc[numeric_col.index, 'Census_Year']).mean().to_dict()
        except Exception:
            return {}


# ============================================================================
# HOUSING ECONOMIC ANALYZER
# ============================================================================

class HousingEconomicAnalyzer(EconomicAnalyzer):
    """Analyzes housing economics"""

    def analyze(self) -> Dict[str, Any]:
        return {
            'property_values': self._property_analysis(),
            'rental_market': self._rental_analysis(),
            'costs': self._cost_analysis(),
            'affordability': self._affordability_analysis()
        }

    def _property_analysis(self) -> Dict:
        return {
            'median_value_trend': self._calc_median_by_year('Property_Value'),
            'value_distribution': self._value_percentiles()
        }

    def _value_percentiles(self) -> Dict:
        col = 'Property_Value'
        if col not in self.df.columns:
            return {}
        return self.df[col].quantile([0.25, 0.5, 0.75]).to_dict()

    def _rental_analysis(self) -> Dict:
        return {
            'median_rent_trend': self._calc_median_by_year('Gross_Rent'),
            'rent_burden': self._calc_mean_by_year('Gross_Rent_Percentage_Income')
        }

    def _cost_analysis(self) -> Dict:
        cost_cols = ['Electricity_Cost_Monthly', 'Gas_Cost_Monthly',
                     'Property_Taxes_Yearly']
        return {col: self._calc_median_by_year(col) for col in cost_cols}

    def _affordability_analysis(self) -> Dict:
        return {
            'owner_cost_burden': self._calc_mean_by_year('Owner_Costs_Percentage_Income'),
            'renter_cost_burden': self._calc_mean_by_year('Gross_Rent_Percentage_Income')
        }


# ============================================================================
# POPULATION ECONOMIC ANALYZER
# ============================================================================

class PopulationEconomicAnalyzer(EconomicAnalyzer):
    """Analyzes population economics"""

    def analyze(self) -> Dict[str, Any]:
        return {
            'income': self._income_analysis(),
            'employment': self._employment_analysis(),
            'poverty': self._poverty_analysis(),
            'wages': self._wage_analysis()
        }

    def _income_analysis(self) -> Dict:
        return {
            'median_person_income': self._calc_median_by_year('Total_Person_Income'),
            'income_sources': self._income_sources()
        }

    def _income_sources(self) -> Dict:
        sources = ['Wage_Income', 'Self_Employment_Income',
                   'Retirement_Income', 'Social_Security_Income']
        return {s: self._calc_median_by_year(s) for s in sources}

    def _employment_analysis(self) -> Dict:
        return {
            'avg_hours_worked': self._calc_mean_by_year('Hours_Worked_Per_Week'),
            'weeks_worked': self._calc_mean_by_year('Weeks_Worked_Past_Year')
        }

    def _poverty_analysis(self) -> Dict:
        return {
            'poverty_rate_trend': self._calc_mean_by_year('Poverty_Status')
        }

    def _wage_analysis(self) -> Dict:
        return {
            'median_wage_trend': self._calc_median_by_year('Wage_Income'),
            'earnings_trend': self._calc_median_by_year('Total_Person_Earnings')
        }


# ============================================================================
# CORRELATION ANALYZER
# ============================================================================

class CorrelationAnalyzer:
    """Analyzes correlations in census data"""

    def __init__(self, df: pd.DataFrame, weight_col: Optional[str] = None):
        self.df = df
        self.weight_col = weight_col
        self.has_weights = weight_col is not None and weight_col in df.columns

    def analyze(self, focus_vars: List[str]) -> Dict[str, Any]:
        if len(self.df) < 100:
            raise InsufficientDataError('correlation analysis', 100, len(self.df))
        numeric_df = self._get_numeric_subset(focus_vars)
        if numeric_df.shape[1] < 2:
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

    def _calc_correlations(self, df: pd.DataFrame) -> Dict:
        if df.empty:
            return {}
        # Filter zeros for each column before correlation
        df_filtered = df.copy()
        for col in df.columns:
            if should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan
        return df_filtered.corr().to_dict()

    def _find_strong_corr(self, df: pd.DataFrame, threshold: float = 0.7) -> List[Tuple]:
        if df.empty:
            return []
        # Filter zeros for each column before correlation
        df_filtered = df.copy()
        for col in df.columns:
            if should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan
        corr_matrix = df_filtered.corr()
        strong = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                val = abs(corr_matrix.iloc[i, j])
                if val > threshold:
                    strong.append((corr_matrix.columns[i],
                                   corr_matrix.columns[j], val))
        return strong

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


# ============================================================================
# ADVANCED CORRELATION ANALYZER
# ============================================================================

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


# ============================================================================
# MULTIVARIATE OUTLIER DETECTOR
# ============================================================================

class MultivariateOutlierDetector:
    """Multivariate outlier detection using multiple algorithms"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        from logging_config import get_logger
        self.logger = get_logger("processing.outlier_detector")

    def analyze(self, focus_vars: Optional[List[str]] = None,
                methods: List[str] = ['isolation_forest', 'mahalanobis']) -> Dict[str, Any]:
        """Detect outliers using multiple multivariate methods"""
        self.logger.debug(f"Detecting outliers with methods: {methods}")

        # Prepare data
        if focus_vars:
            available = [v for v in focus_vars if v in self.df.columns]
            df = self.df[available].select_dtypes(include=[np.number]).dropna()
        else:
            df = self.df.select_dtypes(include=[np.number]).dropna()

        if len(df) < 10 or df.shape[1] < 2:
            return {'error': 'Insufficient data for multivariate outlier detection'}

        results = {}

        if 'isolation_forest' in methods:
            results['isolation_forest'] = self._isolation_forest(df)

        if 'mahalanobis' in methods:
            results['mahalanobis'] = self._mahalanobis_distance(df)

        if 'lof' in methods:
            results['lof'] = self._local_outlier_factor(df)

        # Ensemble results
        results['ensemble'] = self._ensemble_outliers(results, len(df))
        return results

    def _isolation_forest(self, df: pd.DataFrame, contamination: float = 0.1) -> Dict:
        """Isolation Forest outlier detection"""
        try:
            from sklearn.ensemble import IsolationForest

            X = df.values
            clf = IsolationForest(contamination=contamination, random_state=42, n_jobs=-1)
            predictions = clf.fit_predict(X)

            outlier_mask = predictions == -1
            outlier_indices = df.index[outlier_mask].tolist()

            return {
                'n_outliers': int(sum(outlier_mask)),
                'outlier_percentage': float(sum(outlier_mask) / len(df) * 100),
                'outlier_indices': outlier_indices[:100],  # Limit for memory
                'method': 'Isolation Forest',
                'contamination': contamination
            }
        except ImportError:
            return {'error': 'sklearn not available'}
        except Exception as e:
            self.logger.warning(f"Isolation Forest failed: {e}")
            return {'error': str(e)}

    def _mahalanobis_distance(self, df: pd.DataFrame, threshold: float = 3.0) -> Dict:
        """Mahalanobis distance outlier detection"""
        try:
            from scipy.spatial.distance import mahalanobis
            from scipy import stats

            X = df.values
            mean = np.mean(X, axis=0)
            cov = np.cov(X.T)

            # Handle singular covariance matrix
            try:
                cov_inv = np.linalg.inv(cov)
            except np.linalg.LinAlgError:
                cov_inv = np.linalg.pinv(cov)

            # Calculate Mahalanobis distance for each point
            distances = []
            for i in range(len(X)):
                d = mahalanobis(X[i], mean, cov_inv)
                distances.append(d)

            distances = np.array(distances)

            # Chi-squared threshold for multivariate outliers
            chi2_threshold = stats.chi2.ppf(0.975, df=X.shape[1])
            outlier_mask = distances > chi2_threshold

            outlier_indices = df.index[outlier_mask].tolist()

            return {
                'n_outliers': int(sum(outlier_mask)),
                'outlier_percentage': float(sum(outlier_mask) / len(df) * 100),
                'outlier_indices': outlier_indices[:100],
                'method': 'Mahalanobis Distance',
                'threshold': float(chi2_threshold),
                'mean_distance': float(np.mean(distances)),
                'max_distance': float(np.max(distances))
            }
        except Exception as e:
            self.logger.warning(f"Mahalanobis distance failed: {e}")
            return {'error': str(e)}

    def _local_outlier_factor(self, df: pd.DataFrame, n_neighbors: int = 20) -> Dict:
        """Local Outlier Factor detection"""
        try:
            from sklearn.neighbors import LocalOutlierFactor

            X = df.values
            clf = LocalOutlierFactor(n_neighbors=min(n_neighbors, len(X) - 1))
            predictions = clf.fit_predict(X)

            outlier_mask = predictions == -1
            outlier_indices = df.index[outlier_mask].tolist()

            return {
                'n_outliers': int(sum(outlier_mask)),
                'outlier_percentage': float(sum(outlier_mask) / len(df) * 100),
                'outlier_indices': outlier_indices[:100],
                'method': 'Local Outlier Factor',
                'n_neighbors': n_neighbors
            }
        except ImportError:
            return {'error': 'sklearn not available'}
        except Exception as e:
            self.logger.warning(f"LOF failed: {e}")
            return {'error': str(e)}

    def _ensemble_outliers(self, results: Dict, n_samples: int) -> Dict:
        """Combine multiple methods for robust outlier identification"""
        all_indices = set()
        method_counts = {}

        for method, result in results.items():
            if method == 'ensemble' or 'error' in result:
                continue
            indices = result.get('outlier_indices', [])
            for idx in indices:
                all_indices.add(idx)
                method_counts[idx] = method_counts.get(idx, 0) + 1

        # Points flagged by multiple methods are more likely outliers
        consensus_outliers = [idx for idx, count in method_counts.items() if count >= 2]

        return {
            'all_flagged': len(all_indices),
            'consensus_outliers': len(consensus_outliers),
            'consensus_percentage': float(len(consensus_outliers) / n_samples * 100) if n_samples > 0 else 0,
            'consensus_indices': consensus_outliers[:100]
        }


# ============================================================================
# HYPOTHESIS TESTING ANALYZER
# ============================================================================

class HypothesisTestingAnalyzer:
    """Statistical hypothesis testing with multiple comparison corrections"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        from logging_config import get_logger
        self.logger = get_logger("processing.hypothesis_testing")

    def test_group_differences(self, value_col: str, group_col: str,
                               correction: str = 'bonferroni') -> Dict[str, Any]:
        """Test differences between groups with correction for multiple comparisons"""
        self.logger.debug(f"Testing group differences: {value_col} by {group_col}")

        if value_col not in self.df.columns or group_col not in self.df.columns:
            return {'error': 'Columns not found'}

        try:
            from scipy import stats

            # Get groups
            groups = self.df.groupby(group_col)[value_col].apply(
                lambda x: x.dropna().tolist()
            ).to_dict()

            if len(groups) < 2:
                return {'error': 'Need at least 2 groups for comparison'}

            # Perform pairwise tests
            group_names = list(groups.keys())
            p_values = []
            comparisons = []

            for i in range(len(group_names)):
                for j in range(i + 1, len(group_names)):
                    g1, g2 = groups[group_names[i]], groups[group_names[j]]
                    if len(g1) > 1 and len(g2) > 1:
                        _, p_val = stats.mannwhitneyu(g1, g2, alternative='two-sided')
                        p_values.append(p_val)
                        comparisons.append((group_names[i], group_names[j]))

            # Apply correction
            if correction == 'bonferroni':
                corrected = self._bonferroni_correction(p_values)
            elif correction == 'fdr' or correction == 'bh':
                corrected = self._fdr_correction(p_values)
            elif correction == 'holm':
                corrected = self._holm_bonferroni(p_values)
            else:
                corrected = [(p, p < 0.05) for p in p_values]

            results = []
            for (g1, g2), (adj_p, significant) in zip(comparisons, corrected):
                results.append({
                    'group1': str(g1), 'group2': str(g2),
                    'adjusted_p': float(adj_p),
                    'significant': bool(significant)
                })

            return {
                'comparisons': results,
                'correction_method': correction,
                'n_comparisons': len(comparisons),
                'n_significant': sum(1 for _, sig in corrected if sig)
            }
        except Exception as e:
            self.logger.warning(f"Group difference test failed: {e}")
            return {'error': str(e)}

    def _bonferroni_correction(self, p_values: List[float],
                                alpha: float = 0.05) -> List[Tuple[float, bool]]:
        """Bonferroni correction - conservative"""
        n = len(p_values)
        return [(min(p * n, 1.0), p * n < alpha) for p in p_values]

    def _holm_bonferroni(self, p_values: List[float],
                         alpha: float = 0.05) -> List[Tuple[float, bool]]:
        """Holm-Bonferroni step-down procedure"""
        n = len(p_values)
        sorted_indices = np.argsort(p_values)
        adjusted = [0.0] * n
        significant = [False] * n

        for rank, idx in enumerate(sorted_indices):
            adj_p = min(p_values[idx] * (n - rank), 1.0)
            adjusted[idx] = adj_p
            significant[idx] = adj_p < alpha

        return list(zip(adjusted, significant))

    def _fdr_correction(self, p_values: List[float],
                        alpha: float = 0.05) -> List[Tuple[float, bool]]:
        """Benjamini-Hochberg FDR correction"""
        n = len(p_values)
        sorted_indices = np.argsort(p_values)
        adjusted = [0.0] * n

        # Calculate adjusted p-values
        prev_adj = 1.0
        for rank in range(n - 1, -1, -1):
            idx = sorted_indices[rank]
            adj_p = min(p_values[idx] * n / (rank + 1), prev_adj)
            adjusted[idx] = adj_p
            prev_adj = adj_p

        return [(adj, adj < alpha) for adj in adjusted]

    def normality_tests(self, cols: List[str]) -> Dict[str, Dict]:
        """Test normality with Shapiro-Wilk and other tests"""
        results = {}
        try:
            from scipy import stats

            for col in cols:
                if col not in self.df.columns:
                    continue

                series = pd.to_numeric(self.df[col], errors='coerce').dropna()
                if should_exclude_zeros(col):
                    series = series[series > 0]

                if len(series) < 8:
                    results[col] = {'error': 'Insufficient data'}
                    continue

                # Limit sample size for Shapiro-Wilk
                sample = series.sample(n=min(5000, len(series)), random_state=42)

                try:
                    shapiro_stat, shapiro_p = stats.shapiro(sample)
                    results[col] = {
                        'shapiro_statistic': float(shapiro_stat),
                        'shapiro_p_value': float(shapiro_p),
                        'is_normal': shapiro_p > 0.05,
                        'n_samples': len(sample)
                    }
                except Exception:
                    results[col] = {'error': 'Test failed'}

            return results
        except ImportError:
            return {'error': 'scipy not available'}


# ============================================================================
# STATISTICAL ANALYZER
# ============================================================================

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


# ============================================================================
# OUTLIER ANALYZER
# ============================================================================

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
    
    def _find_strong_trends(self, trend_summary: Dict) -> List[Tuple[str, float, str]]:
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