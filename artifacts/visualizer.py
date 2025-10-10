import pandas as pd
import numpy as np
import os
import gc
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend to prevent memory leaks
import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import warnings
from config import Config
from exceptions import (VisualizationError, PlotCreationError,
                        InvalidVisualizationDataError)
from visual_registry import get_registry, register_visual
warnings.filterwarnings('ignore')

# ============================================================================
# SHARED CONFIGURATION (Module-level singleton for memory efficiency)
# ============================================================================

# Columns where zero is meaningless and should be excluded
# This is shared across ALL visualizer instances to save memory
_EXCLUDE_ZERO_COLS_RAW = [
    # POPULATION SURVEY - Income Columns (schema.py lines 142-148, 198-199)
    'Wage_Income', 'Total_Person_Earnings', 'Total_Person_Income',
    'Self_Employment_Income', 'Interest_Dividend_Rental_Income',
    'Retirement_Income', 'Social_Security_Income', 'Supplemental_Security_Income',
    'Public_Assistance_Income', 'Other_Income',
    # POPULATION SURVEY - Work/Hours Columns (schema.py lines 112, 158, 160)
    'Travel_Time_To_Work_Minutes', 'Hours_Worked_Per_Week', 'Weeks_Worked_Past_Year',
    # HOUSING SURVEY - Property Values (schema.py line 346)
    'Property_Value',
    # HOUSING SURVEY - Utility Costs (schema.py lines 355-361)
    'Condo_Fee_Monthly', 'Electricity_Cost_Monthly', 'Fuel_Cost_Monthly',
    'Gas_Cost_Monthly', 'Insurance_Cost_Yearly', 'Water_Cost_Yearly',
    # HOUSING SURVEY - Mortgage Costs (schema.py lines 366, 368, 371, 373)
    'Mobile_Home_Costs_Monthly', 'First_Mortgage_Payment_Monthly',
    'Second_Mortgage_Payment_Monthly', 'Property_Taxes_Yearly',
    # HOUSING SURVEY - Rental Costs (schema.py lines 379-382)
    'Rent_Amount_Monthly', 'Gross_Rent', 'Selected_Monthly_Owner_Costs',
    # HOUSING SURVEY - Household Income (schema.py lines 400, 403)
    'Family_Income', 'Household_Income',
    # DERIVED FEATURES (from feature_engineering.py FeatureCreator methods)
    'Income_Per_Hour', 'Income_Per_Week_Worked', 'Total_Annual_Hours',
    'Total_Monthly_Utility_Cost', 'Property_Tax_Rate', 'Annual_Rent_to_Value_Ratio'
]
# Normalize to uppercase once at module load (not per instance)
_EXCLUDE_ZERO_COLUMNS = {col.upper().strip() for col in _EXCLUDE_ZERO_COLS_RAW}

# Cache for _should_exclude_zeros results to avoid repeated lookups
_EXCLUDE_ZEROS_CACHE = {}

# Debug logging flag (set to False in production to save memory)
_DEBUG_LOGGING = False

def enable_debug_logging(enable: bool = True):
    """Enable/disable debug logging globally for all visualizers"""
    global _DEBUG_LOGGING
    _DEBUG_LOGGING = enable
    if enable:
        print("[VIZ-CONFIG] Debug logging ENABLED")
    else:
        print("[VIZ-CONFIG] Debug logging DISABLED (production mode)")

def clear_viz_cache():
    """Clear the visualization cache to free memory"""
    global _EXCLUDE_ZEROS_CACHE
    cache_size = len(_EXCLUDE_ZEROS_CACHE)
    _EXCLUDE_ZEROS_CACHE.clear()
    if _DEBUG_LOGGING:
        print(f"[VIZ-CACHE] Cleared {cache_size} cached entries")

# ============================================================================
# BASE VISUALIZER
# ============================================================================

class BaseVisualizer(ABC):
    """Abstract base for all visualizers with optimized memory usage"""

    def __init__(self, df: pd.DataFrame, config: Config, survey_type: str = ""):
        self.df = df
        self.config = config
        self.survey_type = survey_type.upper() if survey_type else ""
        os.makedirs(config.figure_dir, exist_ok=True)

        # Use shared module-level set (no per-instance duplication)
        self.exclude_zero_columns = _EXCLUDE_ZERO_COLUMNS

        # Only print initialization debug info once per visualizer type
        if _DEBUG_LOGGING:
            viz_type = self.__class__.__name__
            if not hasattr(BaseVisualizer, '_init_logged'):
                BaseVisualizer._init_logged = set()
            if viz_type not in BaseVisualizer._init_logged:
                print(f"[INIT-DEBUG] {viz_type} initialized with {len(self.exclude_zero_columns)} exclude cols")
                BaseVisualizer._init_logged.add(viz_type)

    def _apply_housing_sampling(self):
        """HOUSING: Apply aggressive sampling - MUST be called first in create_all()"""
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            target = 4000  # Fixed 4k rows for housing
            if len(self.df) > target:
                viz_name = self.__class__.__name__
                print(f"[HOUSING-SAMPLE] {viz_name}: {len(self.df):,} → {target} rows")
                self.df = self.df.sample(n=target, random_state=42)

    def _should_exclude_zeros(self, col: str) -> bool:
        """Check if zeros should be excluded - OPTIMIZED with caching"""
        if col in _EXCLUDE_ZEROS_CACHE:
            return _EXCLUDE_ZEROS_CACHE[col]
        col_normalized = col.upper().strip()
        result = col_normalized in self.exclude_zero_columns
        _EXCLUDE_ZEROS_CACHE[col] = result
        if _DEBUG_LOGGING:
            if not col.startswith('Flag_') and not col.startswith('Weight'):
                print(f"[DEBUG] _should_exclude_zeros(col='{col}') = {result}")
        return result
    
    @abstractmethod
    def create_all(self):
        pass
    
    def _save_fig(self, filename: str):
        """Save figure and close to prevent memory leaks (≤10 lines)"""
        if '.' not in filename:
            filename = f"{filename}.png"
        if self.survey_type:
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{self.survey_type}.{ext}"
        path = f"{self.config.figure_dir}/{filename}"
        plt.savefig(path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close('all')  # Close ALL figures to prevent memory leaks
        gc.collect()  # Force garbage collection

    def _chunk_plot(self, cols: List[str], plot_func, base_name: str,
                    chunk_size: int = 4, figsize=(15, 10)):
        """Create multiple 2x2 subplot figures for all columns (≤10 lines)"""
        total = len(cols)
        for chunk_idx in range(0, total, chunk_size):
            chunk = cols[chunk_idx:chunk_idx + chunk_size]
            fig, axes = plt.subplots(2, 2, figsize=figsize)
            for idx, col in enumerate(chunk):
                plot_func(axes[idx // 2, idx % 2], col)
            for idx in range(len(chunk), chunk_size):
                axes[idx // 2, idx % 2].axis('off')
            plt.tight_layout()
            file_num = (chunk_idx // chunk_size) + 1
            self._save_fig(f'{base_name}_{file_num}.png')
            # Explicitly delete figure objects to prevent memory leaks
            del fig, axes
            plt.clf()  # Clear current figure state
            gc.collect()  # Force immediate garbage collection

# ============================================================================
# TEMPORAL VISUALIZER
# ============================================================================

class TemporalVisualizer(BaseVisualizer):
    """Visualizes temporal trends"""

    def create_all(self):
        self._apply_housing_sampling()
        try:
            self._sample_size_trend()
        except Exception as e:
            print(f"[VIZ-WARNING] Sample size trend plot failed: {e}")
        try:
            self._year_distribution()
        except Exception as e:
            print(f"[VIZ-WARNING] Year distribution plot failed: {e}")
        try:
            self._temporal_comparison()
        except Exception as e:
            print(f"[VIZ-WARNING] Temporal comparison plot failed: {e}")
    
    def _sample_size_trend(self):
        plt.figure(figsize=(10, 6))
        self._plot_sample_counts()
        plt.tight_layout()
        self._save_fig('sample_size_trend.png')
    
    def _plot_sample_counts(self):
        print(f"[VIZ-VERBOSE] _plot_sample_counts: df.shape={self.df.shape}")
        print(f"[VIZ-VERBOSE] 'Census_Year' in columns: {'Census_Year' in self.df.columns}")
        if 'Census_Year' not in self.df.columns:
            print("[VIZ-WARNING] Census_Year column missing - skipping plot")
            return
        counts = self.df['Census_Year'].value_counts().sort_index()
        print(f"[VIZ-VERBOSE] Census_Year counts: {len(counts)} unique years, total records: {counts.sum()}")
        print(f"[VIZ-VERBOSE] Year range: {counts.index.min() if len(counts) > 0 else 'N/A'} to {counts.index.max() if len(counts) > 0 else 'N/A'}")
        plt.plot(counts.index, counts.values, marker='o', linewidth=2, color='steelblue')
        plt.title('Sample Size Over Time', fontweight='bold', fontsize=14)
        plt.xlabel('Year')
        plt.ylabel('Records')
        plt.grid(alpha=0.3)
    
    def _year_distribution(self):
        print(f"[VIZ-VERBOSE] _year_distribution: df.shape={self.df.shape}")
        if 'Census_Year' not in self.df.columns:
            print("[VIZ-WARNING] Census_Year column missing - skipping plot")
            return
        plt.figure(figsize=(12, 6))
        counts = self.df['Census_Year'].value_counts().sort_index()
        print(f"[VIZ-VERBOSE] Year distribution: {dict(counts)}")
        plt.bar(counts.index, counts.values, color='steelblue', edgecolor='black')
        plt.title('Records by Census Year', fontweight='bold', fontsize=14)
        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        self._save_fig('year_distribution.png')
    
    def _temporal_comparison(self):
        print(f"[VIZ-VERBOSE] _temporal_comparison: df.shape={self.df.shape}")
        numeric_cols = self._get_key_numeric_cols()
        print(f"[VIZ-VERBOSE] Key numeric columns found: {numeric_cols}")
        if not numeric_cols:
            print("[VIZ-WARNING] No key numeric columns found - skipping plot")
            return
        self._chunk_plot(numeric_cols, self._plot_metric_trend, 'temporal_comparison')
    
    def _get_key_numeric_cols(self) -> List[str]:
        numeric = self.df.select_dtypes(include=[np.number]).columns
        print(f"[VIZ-VERBOSE] _get_key_numeric_cols: {len(numeric)} numeric columns total")
        print(f"[VIZ-VERBOSE] Numeric columns: {list(numeric)[:20]}...")  # Show first 20
        keywords = ['Age', 'Income', 'Poverty', 'Hours', 'Value', 'Rent']
        matched = [c for c in numeric if any(k in c for k in keywords)][:8]
        print(f"[VIZ-VERBOSE] Matched key columns: {matched}")
        return matched
    
    def _plot_metric_trend(self, ax, col: str):
        print(f"[VIZ-VERBOSE] _plot_metric_trend for column '{col}'")
        # Ensure numeric type before aggregation
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        # Filter zeros if needed
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        non_null = numeric_col.notna().sum()
        print(f"[VIZ-VERBOSE] Column '{col}': {non_null} non-null values (zeros excluded if needed)")
        if non_null > 0:
            print(f"[VIZ-VERBOSE] Value range: {numeric_col.min():.2f} to {numeric_col.max():.2f}")
        yearly = numeric_col.groupby(df_filtered['Census_Year']).agg(['mean', 'median'])
        yearly.plot(ax=ax, marker='o')
        ax.set_title(f'{col} Over Time', fontweight='bold')
        ax.set_xlabel('Year')
        ax.legend(['Mean', 'Median'])
        ax.grid(alpha=0.3)

# ============================================================================
# ECONOMIC VISUALIZER
# ============================================================================

class EconomicVisualizer(BaseVisualizer):
    """Visualizes economic metrics"""

    def create_all(self):
        self._apply_housing_sampling()
        try:
            self._income_distribution()
        except Exception as e:
            print(f"[VIZ-WARNING] Income distribution plot failed: {e}")
        try:
            self._economic_trends()
        except Exception as e:
            print(f"[VIZ-WARNING] Economic trends plot failed: {e}")
        try:
            self._cost_analysis()
        except Exception as e:
            print(f"[VIZ-WARNING] Cost analysis plot failed: {e}")
    
    def _income_distribution(self):
        income_cols = self._find_income_cols()
        if not income_cols:
            return
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        self._plot_income_hist(axes[0], income_cols[0])
        self._plot_income_by_year(axes[1], income_cols[0])
        plt.tight_layout()
        self._save_fig('income_distribution.png')
    
    def _find_income_cols(self) -> List[str]:
        return [c for c in self.df.columns if 'Income' in c and 
                self.df[c].dtype in [np.float64, np.int64]]
    
    def _plot_income_hist(self, ax, col: str):
        data = self.df[col].dropna()
        if self._should_exclude_zeros(col):
            data = data[data > 0]
        if len(data) > 0:
            ax.hist(data, bins=50, edgecolor='black', alpha=0.7)
            ax.set_title(f'{col} Distribution', fontweight='bold')
            ax.set_xlabel('Income ($)')
            ax.set_ylabel('Frequency')
    
    def _plot_income_by_year(self, ax, col: str):
        # Ensure numeric type before aggregation
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        # Filter zeros if needed
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='green')
        ax.set_title(f'Median {col} Over Time', fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Median Income ($)')
        ax.grid(alpha=0.3)
    
    def _economic_trends(self):
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        self._plot_property_values(axes[0, 0])
        self._plot_rents(axes[0, 1])
        self._plot_wages(axes[1, 0])
        self._plot_employment(axes[1, 1])
        plt.tight_layout()
        self._save_fig('economic_trends.png')
    
    def _plot_property_values(self, ax):
        if 'Property_Value' in self.df.columns:
            # Ensure numeric type before aggregation
            numeric_col = pd.to_numeric(self.df['Property_Value'], errors='coerce')
            if self._should_exclude_zeros('Property_Value'):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
            ax.plot(yearly.index, yearly.values, marker='s', color='coral', linewidth=2)
            ax.set_title('Median Property Value', fontweight='bold')
            ax.set_ylabel('Value ($)')
            ax.grid(alpha=0.3)
    
    def _plot_rents(self, ax):
        if 'Gross_Rent' in self.df.columns:
            # Ensure numeric type before aggregation
            numeric_col = pd.to_numeric(self.df['Gross_Rent'], errors='coerce')
            if self._should_exclude_zeros('Gross_Rent'):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
            ax.plot(yearly.index, yearly.values, marker='^', color='purple', linewidth=2)
            ax.set_title('Median Gross Rent', fontweight='bold')
            ax.set_ylabel('Rent ($)')
            ax.grid(alpha=0.3)
    
    def _plot_wages(self, ax):
        if 'Wage_Income' in self.df.columns:
            # Ensure numeric type before aggregation
            numeric_col = pd.to_numeric(self.df['Wage_Income'], errors='coerce')
            if self._should_exclude_zeros('Wage_Income'):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
            ax.plot(yearly.index, yearly.values, marker='o', color='green', linewidth=2)
            ax.set_title('Median Wage Income', fontweight='bold')
            ax.set_ylabel('Wages ($)')
            ax.grid(alpha=0.3)
    
    def _plot_employment(self, ax):
        if 'Hours_Worked_Per_Week' in self.df.columns:
            # Ensure numeric type before aggregation
            numeric_col = pd.to_numeric(self.df['Hours_Worked_Per_Week'], errors='coerce')
            if self._should_exclude_zeros('Hours_Worked_Per_Week'):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly = numeric_col.groupby(df_filtered['Census_Year']).mean()
            ax.plot(yearly.index, yearly.values, marker='d', color='orange', linewidth=2)
            ax.set_title('Avg Hours Worked Per Week', fontweight='bold')
            ax.set_ylabel('Hours')
            ax.grid(alpha=0.3)
    
    def _cost_analysis(self):
        cost_cols = self._find_cost_cols()
        if not cost_cols:
            return
        self._chunk_plot(cost_cols, self._plot_cost_trend, 'cost_analysis')
    
    def _find_cost_cols(self) -> List[str]:
        keywords = ['Cost', 'Tax', 'Fee', 'Payment']
        return [c for c in self.df.columns if any(k in c for k in keywords)]
    
    def _plot_cost_trend(self, ax, col: str):
        # Ensure numeric type before aggregation
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly = numeric_col.groupby(df_filtered['Census_Year']).median()
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2)
        ax.set_title(f'{col}', fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Cost ($)')
        ax.grid(alpha=0.3)

# ============================================================================
# CORRELATION VISUALIZER
# ============================================================================

class CorrelationVisualizer(BaseVisualizer):
    """Visualizes correlations and relationships"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] CorrelationVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        print("[VERBOSE] Creating correlation heatmap...")
        self._correlation_heatmap()
        print("[VERBOSE] Creating scatter matrix...")
        self._scatter_matrix()
    
    def _correlation_heatmap(self):
        key_cols = self._get_key_columns()
        if len(key_cols) < 2:
            return
        plt.figure(figsize=(12, 10))
        # Filter zeros for each column before correlation
        df_filtered = self.df[key_cols].copy()
        for col in key_cols:
            if self._should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan
        corr = df_filtered.corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                    center=0, square=True, linewidths=1)
        plt.title('Correlation Heatmap - Key Variables', fontweight='bold', fontsize=14)
        plt.tight_layout()
        self._save_fig('correlation_heatmap.png')
    
    def _get_key_columns(self) -> List[str]:
        numeric = self.df.select_dtypes(include=[np.number]).columns
        keywords = ['Income', 'Value', 'Rent', 'Age', 'Hours', 'Wage']
        return [c for c in numeric if any(k in c for k in keywords)][:8]
    
    def _scatter_matrix(self):
        key_cols = self._get_key_columns()[:8]
        if len(key_cols) < 2:
            print(f"[VERBOSE] Skipping scatter matrix: insufficient key columns (found {len(key_cols)})")
            return
        
        # Validate data exists and is not empty
        df_subset = self.df[key_cols].dropna()
        if len(df_subset) == 0:
            print(f"[VERBOSE] Skipping scatter matrix: no valid data after removing NaN values")
            return
        
        # Check if columns have any variance
        for col in key_cols:
            if df_subset[col].nunique() <= 1:
                print(f"[VERBOSE] Skipping scatter matrix: column '{col}' has no variance")
                return
        
        print(f"[VERBOSE] Creating scatter matrix with columns: {key_cols}")
        pd.plotting.scatter_matrix(df_subset, figsize=(12, 12), 
                                  diagonal='hist', alpha=0.5)
        plt.suptitle('Scatter Matrix - Key Variables', fontweight='bold', fontsize=14)
        plt.tight_layout()
        self._save_fig('scatter_matrix.png')

# ============================================================================
# STATISTICAL VISUALIZER
# ============================================================================

class StatisticalVisualizer(BaseVisualizer):
    """Creates statistical distribution visualizations (memory optimized)"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] StatisticalVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._box_plots()
        self._distribution_with_stats()
    
    def _box_plots(self):
        """Create box plots for key variables showing quartiles and outliers"""
        print(f"[VIZ-VERBOSE] _box_plots: df.shape={self.df.shape}")
        key_cols = self._get_key_numeric_cols()
        print(f"[VIZ-VERBOSE] Key columns for box plots: {key_cols}")
        if not key_cols:
            print("[VIZ-WARNING] No key columns found - skipping box plots")
            return
        self._chunk_plot(key_cols, self._plot_box, 'box_plots')

    def _plot_box(self, ax, col: str):
        data = pd.to_numeric(self.df[col], errors='coerce').dropna()
        if self._should_exclude_zeros(col):
            data = data[data > 0]
        print(f"[VIZ-VERBOSE] Box plot for '{col}': {len(data)} non-null values")
        if len(data) > 0:
            print(f"[VIZ-VERBOSE] Data range: {data.min():.2f} to {data.max():.2f}")
            ax.boxplot(data, vert=True)
            ax.set_title(f'Distribution of {col}', fontweight='bold')
            ax.set_ylabel(col)
            ax.grid(alpha=0.3, axis='y')
            mean_val, median_val = data.mean(), data.median()
            ax.text(0.98, 0.98, f'Mean: {mean_val:,.0f}\nMedian: {median_val:,.0f}',
                   transform=ax.transAxes, verticalalignment='top',
                   horizontalalignment='right', bbox=dict(boxstyle='round',
                   facecolor='wheat', alpha=0.5), fontsize=9)
        else:
            print(f"[VIZ-WARNING] No data for column '{col}' - skipping")
    
    def _distribution_with_stats(self):
        """Create histograms with mean, median, and std dev overlay"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols:
            return
        self._chunk_plot(key_cols, self._plot_dist_stats, 'distribution_statistics')

    def _plot_dist_stats(self, ax, col: str):
        """Plot histogram with stats overlay (memory optimized, ≤10 lines)"""
        data = self.df[col].dropna()  # Avoid pd.to_numeric copy for numeric cols
        if _DEBUG_LOGGING:
            print(f"[DEBUG] _plot_dist_stats: col='{col}', before_filter={len(data)}")
        if self._should_exclude_zeros(col):
            data = data[data > 0]
            if _DEBUG_LOGGING:
                print(f"[DEBUG]   -> After filter: {len(data)} rows")
        if len(data) > 0:
            ax.hist(data, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
            mean_val, median_val = data.mean(), data.median()
            std_val, skew_val = data.std(), data.skew()
            kurt_val = data.kurtosis()
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:,.0f}')
            ax.axvline(median_val, color='green', linestyle='-', linewidth=2, label=f'Median: {median_val:,.0f}')
            ax.axvline(mean_val - std_val, color='orange', linestyle=':', linewidth=1.5, alpha=0.7)
            ax.axvline(mean_val + std_val, color='orange', linestyle=':', linewidth=1.5, alpha=0.7,
                      label=f'±1 SD: {std_val:,.0f}')
            ax.set_title(f'{col} Distribution', fontweight='bold')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            ax.legend(loc='upper right', fontsize=8)
            stats_text = f'Skewness: {skew_val:.2f}\nKurtosis: {kurt_val:.2f}'
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                   verticalalignment='top', bbox=dict(boxstyle='round',
                   facecolor='lightyellow', alpha=0.8), fontsize=8)
    
    def _get_key_numeric_cols(self) -> List[str]:
        """Get key columns with smart exclusions (≤10 lines)"""
        numeric = self.df.select_dtypes(include=[np.number]).columns
        exclude = ['Flag_', '_is_zero', '_is_missing', 'Specified_', 'Adjustment_Factor', 'Weight_Replicate']
        valuable = [c for c in numeric if not any(p in c for p in exclude)]
        if self.survey_type == "HOUSING":
            keywords = ['Value', 'Rent', 'Income', 'Cost', 'Tax', 'Mortgage', 'Utility']
            selected = [c for c in valuable if any(k in c for k in keywords)][:12]
            print(f"[MEMORY] Housing: {len(selected)}/{len(numeric)} columns (excluded flags/binary)")
            return selected
        keywords = ['Income', 'Wage', 'Age', 'Hours', 'Earnings']
        return [c for c in valuable if any(k in c for k in keywords)]

# ============================================================================
# ADVANCED VISUALIZER
# ============================================================================

class AdvancedVisualizer(BaseVisualizer):
    """Creates advanced statistical visualizations"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] AdvancedVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._violin_plots()
        self._ridge_plots()
        self._radar_chart()
    
    def _violin_plots(self):
        """Create violin plots showing full distribution shape by year"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return
        self._chunk_plot(key_cols, self._plot_violin, 'violin_plots', figsize=(16, 12))

    def _plot_violin(self, ax, col: str):
        data_by_year = []
        years = sorted(self.df['Census_Year'].dropna().unique())
        for year in years[-5:]:
            year_data = pd.to_numeric(self.df[self.df['Census_Year'] == year][col],
                                     errors='coerce').dropna()
            if self._should_exclude_zeros(col):
                year_data = year_data[year_data > 0]
            if len(year_data) > 10:
                data_by_year.append(year_data)
        if data_by_year:
            parts = ax.violinplot(data_by_year, positions=range(len(data_by_year)),
                                 showmeans=True, showmedians=True)
            ax.set_xticks(range(len(data_by_year)))
            ax.set_xticklabels([str(int(y)) for y in years[-len(data_by_year):]], rotation=45)
            ax.set_title(f'{col} Distribution by Year (Violin Plot)', fontweight='bold')
            ax.set_ylabel(col)
            ax.grid(alpha=0.3, axis='y')
    
    def _ridge_plots(self):
        """Create ridge plots (joyplots) for temporal density visualization"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return
        
        col = key_cols[0]  # Use first key column
        years = sorted(self.df['Census_Year'].dropna().unique())[-8:]  # Last 8 years
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(years)))
        
        for idx, year in enumerate(years):
            year_data = pd.to_numeric(self.df[self.df['Census_Year'] == year][col],
                                     errors='coerce').dropna()
            if self._should_exclude_zeros(col):
                year_data = year_data[year_data > 0]
            if len(year_data) > 30:
                # Calculate density
                density, bins = np.histogram(year_data, bins=50, density=True)
                bin_centers = (bins[:-1] + bins[1:]) / 2
                
                # Offset each year's distribution vertically
                offset = idx * 0.15
                ax.fill_between(bin_centers, offset, offset + density * 0.1, 
                               alpha=0.7, color=colors[idx], label=str(int(year)))
                ax.plot(bin_centers, offset + density * 0.1, color='black', 
                       linewidth=0.5, alpha=0.8)
        
        ax.set_xlabel(col, fontsize=12)
        ax.set_ylabel('Year (stacked)', fontsize=12)
        ax.set_title(f'{col} Distribution Over Time (Ridge Plot)', 
                    fontweight='bold', fontsize=14)
        ax.legend(loc='upper right', fontsize=9, ncol=2)
        ax.set_yticks([])
        plt.tight_layout()
        self._save_fig('ridge_plot.png')
    
    def _radar_chart(self):
        """Create radar chart for multi-dimensional comparison across years"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return
        
        years = sorted(self.df['Census_Year'].dropna().unique())
        if len(years) < 2:
            return
        
        # Compare first and last year
        compare_years = [years[0], years[-1]]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        angles = np.linspace(0, 2 * np.pi, len(key_cols), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        for year in compare_years:
            values = []
            year_df = self.df[self.df['Census_Year'] == year]
            
            for col in key_cols:
                col_data = pd.to_numeric(year_df[col], errors='coerce').dropna()
                if len(col_data) > 0:
                    # Normalize to 0-100 scale for comparison
                    all_data = pd.to_numeric(self.df[col], errors='coerce').dropna()
                    if all_data.max() > all_data.min():
                        normalized = (col_data.median() - all_data.min()) / (all_data.max() - all_data.min()) * 100
                        values.append(normalized)
                    else:
                        values.append(0)
                else:
                    values.append(0)
            
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, label=f'Year {int(year)}')
            ax.fill(angles, values, alpha=0.15)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([col.replace('_', ' ') for col in key_cols], fontsize=9)
        ax.set_ylim(0, 100)
        ax.set_title('Multi-Dimensional Comparison (Radar Chart)', 
                    fontweight='bold', fontsize=14, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)
        
        plt.tight_layout()
        self._save_fig('radar_chart.png')
    
    def _get_key_numeric_cols(self) -> List[str]:
        """Get key numeric columns for visualization"""
        numeric = self.df.select_dtypes(include=[np.number]).columns
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Age', 'Hours']
        cols = [c for c in numeric if any(k in c for k in keywords)]
        return cols[:6] if len(cols) >= 6 else cols

# ============================================================================
# YEAR-OVER-YEAR CHANGE VISUALIZER
# ============================================================================

class YoYChangeVisualizer(BaseVisualizer):
    """Visualizes year-over-year changes and trends"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] YoYChangeVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._yoy_change_plot()
        self._growth_rate_heatmap()
    
    def _yoy_change_plot(self):
        """Create year-over-year percentage change visualization"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return
        self._chunk_plot(key_cols, self._plot_yoy, 'yoy_change')

    def _plot_yoy(self, ax, col: str):
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly_median = numeric_col.groupby(df_filtered['Census_Year']).median().sort_index()
        if len(yearly_median) > 1:
            yoy_change = yearly_median.pct_change() * 100
            yoy_change_clean = yoy_change.dropna()
            if len(yoy_change_clean) > 0:
                colors = ['green' if x > 0 else 'red' for x in yoy_change_clean.values]
                ax.bar(yoy_change_clean.index, yoy_change_clean.values, color=colors, alpha=0.7, edgecolor='black')
            ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
            ax.set_title(f'{col} - Year-over-Year % Change', fontweight='bold')
            ax.set_xlabel('Year')
            ax.set_ylabel('% Change')
            ax.grid(alpha=0.3, axis='y')
            ax.tick_params(axis='x', rotation=45)
    
    def _growth_rate_heatmap(self):
        """Create heatmap of growth rates across variables and years"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return
        
        # Calculate YoY changes for all key columns
        growth_matrix = []
        years = sorted(self.df['Census_Year'].dropna().unique())
        
        for col in key_cols:  # key_cols[:8] <<removed
            numeric_col = pd.to_numeric(self.df[col], errors='coerce')
            if self._should_exclude_zeros(col):
                df_filtered = self.df[numeric_col > 0].copy()
                numeric_col = numeric_col[numeric_col > 0]
            else:
                df_filtered = self.df.copy()
            yearly_median = numeric_col.groupby(df_filtered['Census_Year']).median().sort_index()
            yoy_change = yearly_median.pct_change() * 100
            growth_matrix.append(yoy_change.values)
        
        if growth_matrix:
            growth_df = pd.DataFrame(growth_matrix, 
                                    index=[c.replace('_', ' ')[:20] for c in key_cols[:len(growth_matrix)]],
                                    columns=[str(int(y)) for y in years])
            
            # Replace pandas NA with numpy nan for seaborn compatibility
            growth_df = growth_df.fillna(np.nan)
            
            # Check if dataframe has valid data before plotting
            if growth_df.empty or growth_df.shape[0] == 0 or growth_df.shape[1] == 0:
                print("[VERBOSE] Skipping growth rate heatmap: no valid data")
                return
            
            plt.figure(figsize=(12, 8))
            sns.heatmap(growth_df, annot=True, fmt='.1f', cmap='RdYlGn',
                       center=0, cbar_kws={'label': '% Change'}, linewidths=0.5)
            plt.title('Year-over-Year Growth Rate Heatmap (%)', fontweight='bold', fontsize=14)
            plt.xlabel('Year')
            plt.ylabel('Variable')
            plt.tight_layout()
            self._save_fig('growth_rate_heatmap.png')
    
    def _get_key_numeric_cols(self) -> List[str]:
        """Get key numeric columns for visualization"""
        numeric = self.df.select_dtypes(include=[np.number]).columns
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Age', 'Hours', 'Earnings', 'Cost']
        return [c for c in numeric if any(k in c for k in keywords)][:8]

# ============================================================================
# OUTLIER VISUALIZER
# ============================================================================

class OutlierVisualizer(BaseVisualizer):
    """Visualizes outliers and anomalies"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] OutlierVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._outlier_detection_plot()
        self._temporal_anomalies()
    
    def _outlier_detection_plot(self):
        """Create visualization of outliers using IQR method"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols:
            return
        self._chunk_plot(key_cols, self._plot_outlier, 'outlier_detection')

    def _plot_outlier(self, ax, col: str):
        data = pd.to_numeric(self.df[col], errors='coerce').dropna()
        if self._should_exclude_zeros(col):
            data = data[data > 0]
        if len(data) > 0:
            Q1, Q3 = data.quantile(0.25), data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound, upper_bound = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            normal = data[(data >= lower_bound) & (data <= upper_bound)]
            ax.scatter(range(len(normal)), sorted(normal.values),
                      alpha=0.5, s=10, color='steelblue', label='Normal')
            if len(outliers) > 0:
                ax.scatter(range(len(normal), len(normal) + len(outliers)),
                          sorted(outliers.values),
                          alpha=0.7, s=30, color='red', marker='x', label='Outliers')
            ax.axhline(y=lower_bound, color='orange', linestyle='--',
                      linewidth=1, label=f'Lower bound: {lower_bound:,.0f}')
            ax.axhline(y=upper_bound, color='orange', linestyle='--',
                      linewidth=1, label=f'Upper bound: {upper_bound:,.0f}')
            ax.set_title(f'{col} - Outlier Detection (IQR Method)', fontweight='bold')
            ax.set_xlabel('Index (sorted)')
            ax.set_ylabel(col)
            ax.legend(fontsize=8, loc='upper left')
            ax.grid(alpha=0.3)
            outlier_pct = len(outliers) / len(data) * 100
            ax.text(0.98, 0.5, f'Outliers: {len(outliers):,}\n({outlier_pct:.1f}%)',
                   transform=ax.transAxes, verticalalignment='center',
                   horizontalalignment='right', bbox=dict(boxstyle='round',
                   facecolor='lightyellow', alpha=0.8), fontsize=9)
    
    def _temporal_anomalies(self):
        """Detect and visualize temporal anomalies"""
        key_cols = self._get_key_numeric_cols()
        if not key_cols or 'Census_Year' not in self.df.columns:
            return
        self._chunk_plot(key_cols, self._plot_anomaly, 'temporal_anomalies')

    def _plot_anomaly(self, ax, col: str):
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            numeric_col = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly_stats = numeric_col.groupby(df_filtered['Census_Year']).agg(['median', 'std']).sort_index()
        if len(yearly_stats) > 2:
            ma = yearly_stats['median'].rolling(window=3, center=True).mean()
            std_dev = yearly_stats['median'].std()
            anomalies = []
            for year in yearly_stats.index:
                if pd.notna(ma.loc[year]):
                    if abs(yearly_stats.loc[year, 'median'] - ma.loc[year]) > 1.5 * std_dev:
                        anomalies.append(year)
            ax.plot(yearly_stats.index, yearly_stats['median'],
                   marker='o', linewidth=2, label='Actual', color='steelblue')
            ax.plot(ma.index, ma.values, linestyle='--', linewidth=2,
                   label='Moving Avg', color='green', alpha=0.7)
            if anomalies:
                anomaly_vals = [yearly_stats.loc[y, 'median'] for y in anomalies]
                ax.scatter(anomalies, anomaly_vals, color='red', s=100,
                         marker='X', label='Anomalies', zorder=5)
            ax.set_title(f'{col} - Temporal Anomaly Detection', fontweight='bold')
            ax.set_xlabel('Year')
            ax.set_ylabel('Median Value')
            ax.legend(fontsize=9)
            ax.grid(alpha=0.3)
    
    def _get_key_numeric_cols(self) -> List[str]:
        """Get key numeric columns for visualization"""
        numeric = self.df.select_dtypes(include=[np.number]).columns
        keywords = ['Income', 'Wage', 'Value', 'Rent', 'Cost', 'Tax']
        return [c for c in numeric if any(k in c for k in keywords)][:8]

# ============================================================================
# DEMOGRAPHICS VISUALIZER
# ============================================================================

class DemographicsVisualizer(BaseVisualizer):
    """Visualizes demographic distributions and trends"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] DemographicsVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._age_pyramid()
        self._education_distribution()
        self._marital_status_trends()
        self._citizenship_patterns()
    
    def _age_pyramid(self):
        if 'Age' not in self.df.columns or 'Sex' not in self.df.columns:
            return
        # Get 3 most recent years if Census_Year available
        if 'Census_Year' in self.df.columns:
            recent_years = sorted(self.df['Census_Year'].dropna().unique())[-3:]
            fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
            self._plot_pyramids_by_year(axes, recent_years)
        else:
            # Fallback to single pyramid if no year data
            fig, ax = plt.subplots(figsize=(10, 8))
            self._plot_single_pyramid(ax, self.df, 'All Years')
        plt.tight_layout()
        self._save_fig('age_pyramid.png')

    def _plot_pyramids_by_year(self, axes, years):
        """Plot age pyramids for multiple years (≤10 lines)"""
        age_bins = [0, 18, 30, 45, 60, 75, 100]
        labels = ['0-17', '18-29', '30-44', '45-59', '60-74', '75+']
        for idx, year in enumerate(years):
            df_year = self.df[self.df['Census_Year'] == year]
            self._plot_single_pyramid(axes[idx], df_year, str(int(year)), labels, age_bins)
            if idx == 0:
                axes[idx].set_ylabel('Age Group', fontweight='bold')

    def _plot_single_pyramid(self, ax, df, title, labels=None, age_bins=None):
        """Plot single age pyramid (≤10 lines)"""
        if labels is None:
            labels = ['0-17', '18-29', '30-44', '45-59', '60-74', '75+']
        if age_bins is None:
            age_bins = [0, 18, 30, 45, 60, 75, 100]
        df_clean = df[df['Age'].notna() & df['Sex'].notna()].copy()
        df_clean['Age_Group'] = pd.cut(df_clean['Age'], bins=age_bins, labels=labels)
        male = df_clean[df_clean['Sex'] == 1].groupby('Age_Group').size()
        female = df_clean[df_clean['Sex'] == 2].groupby('Age_Group').size()
        y_pos = np.arange(len(labels))
        ax.barh(y_pos, -male.reindex(labels, fill_value=0), color='steelblue', label='Male')
        ax.barh(y_pos, female.reindex(labels, fill_value=0), color='coral', label='Female')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.set_xlabel('Population Count', fontweight='bold')
        ax.set_title(f'Age Pyramid - {title}', fontweight='bold', fontsize=12)
        ax.legend(loc='upper right')
        ax.grid(alpha=0.3, axis='x')
        ax.axvline(0, color='black', linewidth=0.8)
    
    def _education_distribution(self):
        if 'Educational_Attainment' not in self.df.columns:
            return
        plt.figure(figsize=(12, 6))
        edu_counts = self.df['Educational_Attainment'].value_counts().sort_index()
        plt.bar(edu_counts.index, edu_counts.values, color='teal', edgecolor='black')
        plt.title('Educational Attainment Distribution', fontweight='bold', fontsize=14)
        plt.xlabel('Education Level Code')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save_fig('education_distribution.png')
    
    def _marital_status_trends(self):
        if 'Marital_Status' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot = pd.crosstab(self.df['Census_Year'], self.df['Marital_Status'], normalize='index') * 100
        pivot.plot(kind='line', marker='o', ax=ax, linewidth=2)
        ax.set_title('Marital Status Trends Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage')
        ax.legend(title='Status', bbox_to_anchor=(1.05, 1))
        ax.grid(alpha=0.3)
        plt.tight_layout()
        self._save_fig('marital_status_trends.png')
    
    def _citizenship_patterns(self):
        if 'Citizenship_Status' not in self.df.columns:
            return
        plt.figure(figsize=(10, 6))
        cit_counts = self.df['Citizenship_Status'].value_counts()
        plt.pie(cit_counts.values, labels=cit_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Citizenship Status Distribution', fontweight='bold', fontsize=14)
        plt.tight_layout()
        self._save_fig('citizenship_distribution.png')

# ============================================================================
# TRANSPORTATION VISUALIZER
# ============================================================================

class TransportationVisualizer(BaseVisualizer):
    """Visualizes commute and transportation patterns"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] TransportationVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._travel_time_distribution()
        self._transportation_mode()
        self._commute_trends()
    
    def _travel_time_distribution(self):
        if 'Travel_Time_To_Work_Minutes' not in self.df.columns:
            return
        plt.figure(figsize=(12, 6))
        travel = self.df['Travel_Time_To_Work_Minutes'].dropna()
        if self._should_exclude_zeros('Travel_Time_To_Work_Minutes'):
            travel = travel[travel > 0]
        plt.hist(travel[travel < 120], bins=30, color='skyblue', edgecolor='black')
        plt.title('Travel Time to Work Distribution', fontweight='bold', fontsize=14)
        plt.xlabel('Minutes')
        plt.ylabel('Frequency')
        plt.axvline(travel.median(), color='red', linestyle='--', label=f'Median: {travel.median():.0f} min')
        plt.legend()
        plt.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save_fig('travel_time_distribution.png')
    
    def _transportation_mode(self):
        if 'Transportation_To_Work' not in self.df.columns:
            return
        plt.figure(figsize=(10, 8))
        mode_counts = self.df['Transportation_To_Work'].value_counts()
        plt.barh(range(len(mode_counts)), mode_counts.values, color='teal')
        plt.yticks(range(len(mode_counts)), mode_counts.index)
        plt.title('Transportation Mode to Work', fontweight='bold', fontsize=14)
        plt.xlabel('Count')
        plt.grid(alpha=0.3, axis='x')
        plt.tight_layout()
        self._save_fig('transportation_mode.png')
    
    def _commute_trends(self):
        if 'Travel_Time_To_Work_Minutes' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        col = 'Travel_Time_To_Work_Minutes'
        numeric_col = pd.to_numeric(self.df[col], errors='coerce')
        if self._should_exclude_zeros(col):
            df_filtered = self.df[numeric_col > 0].copy()
            df_filtered[col] = numeric_col[numeric_col > 0]
        else:
            df_filtered = self.df.copy()
        yearly = df_filtered.groupby('Census_Year')[col].agg(['mean', 'median'])
        yearly.plot(kind='line', marker='o', ax=ax, linewidth=2)
        ax.set_title('Commute Time Trends', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Minutes')
        ax.legend(['Mean', 'Median'])
        ax.grid(alpha=0.3)
        plt.tight_layout()
        self._save_fig('commute_trends.png')

# ============================================================================
# INCOME COMPOSITION VISUALIZER
# ============================================================================

class IncomeCompositionVisualizer(BaseVisualizer):
    """Visualizes income sources and composition"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] IncomeCompositionVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._income_sources_stacked()
        self._income_by_source()
    
    def _income_sources_stacked(self):
        income_cols = ['Wage_Income', 'Self_Employment_Income', 'Interest_Dividend_Rental_Income',
                      'Social_Security_Income', 'Retirement_Income', 'Public_Assistance_Income', 'Other_Income']
        available = [c for c in income_cols if c in self.df.columns]
        if not available or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(14, 7))
        # Filter zeros for each income column
        df_filtered = self.df.copy()
        for col in available:
            if self._should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan
        yearly_income = df_filtered.groupby('Census_Year')[available].mean()
        yearly_income.plot(kind='area', stacked=True, ax=ax, alpha=0.7)
        ax.set_title('Income Sources Over Time (Stacked)', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Average Income ($)')
        ax.legend(title='Income Type', bbox_to_anchor=(1.05, 1), fontsize=9)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        self._save_fig('income_sources_stacked.png')
    
    def _income_by_source(self):
        income_cols = ['Wage_Income', 'Self_Employment_Income', 'Social_Security_Income', 
                      'Retirement_Income', 'Public_Assistance_Income']
        available = [c for c in income_cols if c in self.df.columns]
        if not available:
            return
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        for idx, col in enumerate(available[:6]):
            ax = axes[idx]
            data = self.df[col].dropna()
            if self._should_exclude_zeros(col):
                data = data[data > 0]
            if len(data) > 0:
                ax.hist(data, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
                ax.set_title(col.replace('_', ' '), fontweight='bold')
                ax.set_xlabel('Amount ($)')
                ax.set_ylabel('Frequency')
                ax.grid(alpha=0.3, axis='y')
        for idx in range(len(available), 6):
            axes[idx].axis('off')
        plt.tight_layout()
        self._save_fig('income_by_source.png')

# ============================================================================
# HOUSING CHARACTERISTICS VISUALIZER
# ============================================================================

class HousingCharacteristicsVisualizer(BaseVisualizer):
    """Visualizes housing unit characteristics"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] HousingCharacteristicsVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._bedrooms_rooms_distribution()
        self._building_type_trends()
        self._year_built_distribution()
        self._vehicles_available()
    
    def _bedrooms_rooms_distribution(self):
        has_bed = 'Number_of_Bedrooms' in self.df.columns
        has_rooms = 'Number_of_Rooms' in self.df.columns
        if not (has_bed or has_rooms):
            return
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        if has_bed:
            bed_counts = self.df['Number_of_Bedrooms'].value_counts().sort_index()
            axes[0].bar(bed_counts.index, bed_counts.values, color='coral', edgecolor='black')
            axes[0].set_title('Number of Bedrooms', fontweight='bold', fontsize=12)
            axes[0].set_xlabel('Bedrooms')
            axes[0].set_ylabel('Count')
            axes[0].grid(alpha=0.3, axis='y')
        if has_rooms:
            room_counts = self.df['Number_of_Rooms'].value_counts().sort_index()
            axes[1].bar(room_counts.index, room_counts.values, color='teal', edgecolor='black')
            axes[1].set_title('Total Number of Rooms', fontweight='bold', fontsize=12)
            axes[1].set_xlabel('Rooms')
            axes[1].set_ylabel('Count')
            axes[1].grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save_fig('bedrooms_rooms_distribution.png')
    
    def _building_type_trends(self):
        if 'Building_Type' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot = pd.crosstab(self.df['Census_Year'], self.df['Building_Type'], normalize='index') * 100
        pivot.plot(kind='line', marker='o', ax=ax, linewidth=2)
        ax.set_title('Building Type Trends', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage')
        ax.legend(title='Type', bbox_to_anchor=(1.05, 1))
        ax.grid(alpha=0.3)
        plt.tight_layout()
        self._save_fig('building_type_trends.png')
    
    def _year_built_distribution(self):
        if 'Year_Structure_Built' not in self.df.columns:
            return
        plt.figure(figsize=(12, 6))
        years = self.df['Year_Structure_Built'].dropna()
        plt.hist(years, bins=30, color='steelblue', edgecolor='black')
        plt.title('Year Structure Built Distribution', fontweight='bold', fontsize=14)
        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save_fig('year_built_distribution.png')
    
    def _vehicles_available(self):
        if 'Vehicles_Available' not in self.df.columns:
            return
        plt.figure(figsize=(10, 6))
        veh_counts = self.df['Vehicles_Available'].value_counts().sort_index()
        plt.bar(veh_counts.index, veh_counts.values, color='darkgreen', edgecolor='black')
        plt.title('Vehicles Available per Household', fontweight='bold', fontsize=14)
        plt.xlabel('Number of Vehicles')
        plt.ylabel('Count')
        plt.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save_fig('vehicles_available.png')

# ============================================================================
# HOUSEHOLD COMPOSITION VISUALIZER
# ============================================================================

class HouseholdCompositionVisualizer(BaseVisualizer):
    """Visualizes household composition and family structure"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] HouseholdCompositionVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._family_type_distribution()
        self._household_size()
        self._children_presence()
        self._multigenerational_trends()
    
    def _family_type_distribution(self):
        if 'Household_Family_Type' not in self.df.columns:
            return
        plt.figure(figsize=(10, 6))
        fam_counts = self.df['Household_Family_Type'].value_counts()
        plt.pie(fam_counts.values, labels=fam_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Household Family Type Distribution', fontweight='bold', fontsize=14)
        plt.tight_layout()
        self._save_fig('family_type_distribution.png')
    
    def _household_size(self):
        if 'Number_of_Persons' not in self.df.columns:
            return
        plt.figure(figsize=(10, 6))
        size_counts = self.df['Number_of_Persons'].value_counts().sort_index()
        plt.bar(size_counts.index, size_counts.values, color='purple', edgecolor='black')
        plt.title('Household Size Distribution', fontweight='bold', fontsize=14)
        plt.xlabel('Number of Persons')
        plt.ylabel('Count')
        plt.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save_fig('household_size.png')
    
    def _children_presence(self):
        child_cols = ['Household_Own_Children_Present', 'Household_Related_Children_Present']
        available = [c for c in child_cols if c in self.df.columns]
        if not available or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        for col in available:
            yearly = self.df.groupby('Census_Year')[col].mean() * 100
            ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, label=col.replace('_', ' '))
        ax.set_title('Children Presence in Households Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        self._save_fig('children_presence.png')
    
    def _multigenerational_trends(self):
        if 'Multigenerational_Household' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        yearly = self.df.groupby('Census_Year')['Multigenerational_Household'].mean() * 100
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='darkred')
        ax.set_title('Multigenerational Households Trend', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage')
        ax.grid(alpha=0.3)
        plt.tight_layout()
        self._save_fig('multigenerational_trends.png')

# ============================================================================
# TECHNOLOGY ADOPTION VISUALIZER
# ============================================================================

class TechnologyAdoptionVisualizer(BaseVisualizer):
    """Visualizes technology adoption trends"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] TechnologyAdoptionVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._technology_adoption_trends()
        self._device_ownership()
    
    def _technology_adoption_trends(self):
        tech_cols = ['Smartphone', 'Tablet_Computer', 'Satellite_Internet']
        available = [c for c in tech_cols if c in self.df.columns]
        if not available or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        for col in available:
            yearly = self.df.groupby('Census_Year')[col].mean() * 100
            ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, label=col.replace('_', ' '))
        ax.set_title('Technology Adoption Over Time', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Adoption Rate (%)')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        self._save_fig('technology_adoption_trends.png')
    
    def _device_ownership(self):
        tech_cols = ['Smartphone', 'Tablet_Computer']
        available = [c for c in tech_cols if c in self.df.columns]
        if not available:
            return
        fig, axes = plt.subplots(1, len(available), figsize=(12, 5))
        if len(available) == 1:
            axes = [axes]
        for idx, col in enumerate(available):
            counts = self.df[col].value_counts()
            axes[idx].pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=90)
            axes[idx].set_title(col.replace('_', ' '), fontweight='bold')
        plt.tight_layout()
        self._save_fig('device_ownership.png')

# ============================================================================
# COST BURDEN VISUALIZER
# ============================================================================

class CostBurdenVisualizer(BaseVisualizer):
    """Visualizes housing cost burden and affordability"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] CostBurdenVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._rent_burden()
        self._owner_cost_burden()
        self._utility_costs_comparison()
    
    def _rent_burden(self):
        if 'Gross_Rent_Percentage_Income' not in self.df.columns:
            return
        plt.figure(figsize=(12, 6))
        burden = self.df['Gross_Rent_Percentage_Income'].dropna()
        plt.hist(burden[burden < 100], bins=30, color='coral', edgecolor='black')
        plt.axvline(30, color='red', linestyle='--', linewidth=2, label='30% Threshold')
        plt.title('Gross Rent as Percentage of Income', fontweight='bold', fontsize=14)
        plt.xlabel('Percentage (%)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save_fig('rent_burden.png')
    
    def _owner_cost_burden(self):
        if 'Owner_Costs_Percentage_Income' not in self.df.columns:
            return
        plt.figure(figsize=(12, 6))
        burden = self.df['Owner_Costs_Percentage_Income'].dropna()
        plt.hist(burden[burden < 100], bins=30, color='steelblue', edgecolor='black')
        plt.axvline(30, color='red', linestyle='--', linewidth=2, label='30% Threshold')
        plt.title('Owner Costs as Percentage of Income', fontweight='bold', fontsize=14)
        plt.xlabel('Percentage (%)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save_fig('owner_cost_burden.png')
    
    def _utility_costs_comparison(self):
        util_cols = ['Electricity_Cost_Monthly', 'Gas_Cost_Monthly', 'Fuel_Cost_Monthly', 'Water_Cost_Yearly']
        available = [c for c in util_cols if c in self.df.columns]
        if not available:
            return
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        for idx, col in enumerate(available[:8]):
            ax = axes[idx]
            data = self.df[col].dropna()
            if self._should_exclude_zeros(col):
                data = data[data > 0]
            if len(data) > 0:
                data_filtered = data[data < data.quantile(0.95)]
                ax.hist(data_filtered, bins=30, color='teal', edgecolor='black', alpha=0.7)
                ax.set_title(col.replace('_', ' '), fontweight='bold')
                ax.set_xlabel('Cost ($)')
                ax.set_ylabel('Frequency')
                ax.grid(alpha=0.3, axis='y')
        for idx in range(len(available), 4):
            axes[idx].axis('off')
        plt.tight_layout()
        self._save_fig('utility_costs_comparison.png')

# ============================================================================
# RACE & ETHNICITY VISUALIZER
# ============================================================================

class RaceEthnicityVisualizer(BaseVisualizer):
    """Visualizes race and ethnicity distributions"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] RaceEthnicityVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        self._race_distribution()
        self._hispanic_origin_trends()
        self._diversity_trends()
    
    def _race_distribution(self):
        race_cols = ['Race_White', 'Race_Black', 'Race_Asian', 
                    'Race_American_Indian_Alaska_Native', 'Race_Native_Hawaiian_Pacific_Islander']
        available = [c for c in race_cols if c in self.df.columns]
        if not available:
            return
        fig, ax = plt.subplots(figsize=(10, 6))
        race_counts = {col.replace('Race_', ''): self.df[col].sum() for col in available}
        ax.bar(race_counts.keys(), race_counts.values(), color='skyblue', edgecolor='black')
        ax.set_title('Race Distribution', fontweight='bold', fontsize=14)
        ax.set_xlabel('Race')
        ax.set_ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        ax.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save_fig('race_distribution.png')
    
    def _hispanic_origin_trends(self):
        if 'Hispanic_Origin' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        yearly = self.df.groupby('Census_Year')['Hispanic_Origin'].apply(lambda x: (x > 1).sum())
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='orange')
        ax.set_title('Hispanic/Latino Population Trend', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Count')
        ax.grid(alpha=0.3)
        plt.tight_layout()
        self._save_fig('hispanic_origin_trends.png')
    
    def _diversity_trends(self):
        if 'Number_Of_Races' not in self.df.columns or 'Census_Year' not in self.df.columns:
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        yearly = self.df.groupby('Census_Year')['Number_Of_Races'].mean()
        ax.plot(yearly.index, yearly.values, marker='o', linewidth=2, color='purple')
        ax.set_title('Average Number of Races per Person', fontweight='bold', fontsize=14)
        ax.set_xlabel('Year')
        ax.set_ylabel('Avg Number of Races')
        ax.grid(alpha=0.3)
        plt.tight_layout()
        self._save_fig('diversity_trends.png')

# ============================================================================
# MULTI-VARIABLE AND DISTRIBUTION VISUALIZERS
# ============================================================================

class MultiVariableVisualizer(BaseVisualizer):
    """Visualizations for multi-variable interactions"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] MultiVariableVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        # Sample large datasets for performance
      #  if len(self.df) > 50000:
      #      print(f"[VERBOSE] Sampling {len(self.df)} records to 50,000 for multi-variable viz")
      #      self.df = self.df.sample(n=50000, random_state=42)
        self._pairwise_interactions()
        self._three_way_interactions()
    
    def _pairwise_interactions(self):
        try:
            numeric_cols = self._get_key_numeric_cols()
            if len(numeric_cols) < 2:
                return
            # Create more diverse pairs for better coverage
            pairs = []
            for i in range(min(6, len(numeric_cols))):
                for j in range(i+1, min(i+3, len(numeric_cols))):
                    if len(pairs) < 6:
                        pairs.append((numeric_cols[i], numeric_cols[j]))
            
            if not pairs:
                return
            
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            axes = axes.flatten()
            for idx, (col1, col2) in enumerate(pairs):
                data1 = self.df[col1].dropna()
                data2 = self.df[col2].dropna()
                if len(data1) > 0 and len(data2) > 0:
                    # Align data
                    common_idx = data1.index.intersection(data2.index)
                    axes[idx].scatter(data1[common_idx], data2[common_idx], 
                                    alpha=0.3, s=5)
                    axes[idx].set_xlabel(col1)
                    axes[idx].set_ylabel(col2)
                    axes[idx].set_title(f'{col1} vs {col2}')
            # Hide unused subplots
            for idx in range(len(pairs), 6):
                axes[idx].axis('off')
            plt.tight_layout()
            self._save_fig('pairwise_interactions')
        except Exception as e:
            print(f"[WARNING] Pairwise interactions failed: {e}")
    
    def _three_way_interactions(self):
        try:
            numeric_cols = self._get_key_numeric_cols()[:5]
            if len(numeric_cols) < 3:
                return
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.df[numeric_cols[0]], self.df[numeric_cols[1]], 
                      self.df[numeric_cols[2]], alpha=0.3, s=5)
            ax.set_xlabel(numeric_cols[0])
            ax.set_ylabel(numeric_cols[1])
            ax.set_zlabel(numeric_cols[2])
            self._save_fig('three_way_interaction')
        except Exception as e:
            raise PlotCreationError('three_way_interaction', str(e))
    
    def _get_key_numeric_cols(self):
        numeric = self.df.select_dtypes(include=[np.number]).columns
        return [c for c in numeric if c not in ['SERIALNO', 'PUMA', 'ST']][:15]


class DistributionComparisonVisualizer(BaseVisualizer):
    """Compare distributions across different dimensions"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] DistributionComparisonVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        # Sample large datasets for performance
        if len(self.df) > 50000:
            print(f"[VERBOSE] Sampling {len(self.df)} records to 50,000 for distribution viz")
            self.df = self.df.sample(n=50000, random_state=42)
        self._temporal_distributions()
        self._density_overlays()
    
    def _temporal_distributions(self):
        try:
            if 'Census_Year' not in self.df.columns:
                return
            numeric_cols = self._get_key_numeric_cols()[:3]
            if not numeric_cols:
                return
            years = sorted(self.df['Census_Year'].unique())
            if len(years) == 0:
                return
            
            # Use up to 3 years
            years_to_plot = years[:min(3, len(years))]
            num_cols = len(numeric_cols)
            
            fig, axes = plt.subplots(1, num_cols, figsize=(15, 5))
            # Handle single subplot case
            if num_cols == 1:
                axes = [axes]
            
            for idx, col in enumerate(numeric_cols):
                for year in years_to_plot:
                    data = self.df[self.df['Census_Year'] == year][col].dropna()
                    # Filter zeros if needed
                    if self._should_exclude_zeros(col):
                        data = data[data > 0]
                    if len(data) > 10:  # Need enough data for histogram
                        axes[idx].hist(data, alpha=0.5, bins=20, label=str(year))
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Frequency')
                axes[idx].legend()
                axes[idx].grid(alpha=0.3)
            
            plt.tight_layout()
            self._save_fig('temporal_distributions')
        except Exception as e:
            print(f"[WARNING] Temporal distributions failed: {e}")
    
    def _density_overlays(self):
        try:
            numeric_cols = self._get_key_numeric_cols()[:8]
            if not numeric_cols:
                return
            
            plt.figure(figsize=(12, 6))
            plotted = False
            for col in numeric_cols:
                data = self.df[col].dropna()
                if self._should_exclude_zeros(col):
                    data = data[data > 0]
                if len(data) > 10:  # Need enough data for density plot
                    try:
                        data.plot(kind='density', alpha=0.6, label=col)
                        plotted = True
                    except Exception:
                        continue
            
            if plotted:
                plt.xlabel('Value')
                plt.ylabel('Density')
                plt.title('Density Overlays', fontweight='bold')
                plt.legend()
                plt.grid(alpha=0.3)
                plt.tight_layout()
                self._save_fig('density_overlays')
            else:
                plt.close()
        except Exception as e:
            print(f"[WARNING] Density overlays failed: {e}")
    
    def _get_key_numeric_cols(self):
        numeric = self.df.select_dtypes(include=[np.number]).columns
        return [c for c in numeric if c not in ['SERIALNO', 'PUMA', 'ST']][:15]


class EnhancedFeatureInteractionVisualizer(BaseVisualizer):
    """Enhanced feature interactions and ratio analysis"""

    def _apply_housing_sampling(self):
        if self.survey_type == "HOUSING" and len(self.df) > 4000:
            print(f"[HOUSING-SAMPLE] EnhancedFeatureInteractionVisualizer: {len(self.df):,} → 4000 rows")
            self.df = self.df.sample(n=4000, random_state=42)

    def create_all(self):
        self._apply_housing_sampling()
        # Sample large datasets for performance
        if len(self.df) > 50000:
            print(f"[VERBOSE] Sampling {len(self.df)} records to 50,000 for feature interaction viz")
            self.df = self.df.sample(n=50000, random_state=42)
        self._feature_ratios()
        self._quadrant_analysis()
    
    def _feature_ratios(self):
        try:
            pairs = [('Total_Person_Income', 'Hours_Worked_Per_Week'),
                    ('Property_Value', 'Household_Income'),
                    ('Gross_Rent', 'Household_Income')]
            for num, denom in pairs:
                if num in self.df.columns and denom in self.df.columns:
                    data = self.df[[num, denom]].dropna()
                    data = data[(data[denom] > 0) & (data[num] > 0)]
                    if len(data) > 10:
                        data['ratio'] = data[num] / data[denom]
                        plt.figure(figsize=(10, 6))
                        plt.hist(data['ratio'], bins=30, alpha=0.7, edgecolor='black')
                        plt.xlabel(f'{num} / {denom}')
                        plt.ylabel('Frequency')
                        plt.title(f'Ratio: {num}/{denom}', fontweight='bold')
                        self._save_fig(f'ratio_{num}_{denom}')
        except Exception as e:
            raise PlotCreationError('feature_ratios', str(e))
    
    def _quadrant_analysis(self):
        try:
            pairs = [('Age', 'Total_Person_Income'),
                    ('Property_Value', 'Gross_Rent'),
                    ('Hours_Worked_Per_Week', 'Wage_Income')]
            for x_col, y_col in pairs:
                if x_col in self.df.columns and y_col in self.df.columns:
                    data = self.df[[x_col, y_col]].dropna()
                    if len(data) > 10:
                        x_med = data[x_col].median()
                        y_med = data[y_col].median()
                        plt.figure(figsize=(10, 8))
                        plt.scatter(data[x_col], data[y_col], alpha=0.4, s=10)
                        plt.axvline(x_med, color='red', linestyle='--', alpha=0.7)
                        plt.axhline(y_med, color='red', linestyle='--', alpha=0.7)
                        plt.xlabel(x_col)
                        plt.ylabel(y_col)
                        plt.title(f'Quadrant: {x_col} vs {y_col}', fontweight='bold')
                        self._save_fig(f'quadrant_{x_col}_{y_col}')
        except Exception as e:
            raise PlotCreationError('quadrant_analysis', str(e))


# ============================================================================
# MAIN VISUALIZER (Orchestrator)
# ============================================================================

class Visualizer:
    """Orchestrates all visualization types"""

    def __init__(self, df: pd.DataFrame, config: Config, survey_type: str = ""):
        self.config = config
        self.survey_type = survey_type.upper() if survey_type else ""
        # HOUSING: Apply aggressive sampling at orchestrator level for ALL visualizers
        if self.survey_type == "HOUSING":
            target_cells = 1_000_000
            sample_rows = min(len(df), int(target_cells / len(df.columns)))
            if len(df) > sample_rows:
                print(f"[MEMORY-ORCHESTRATOR] Sampling {len(df):,} → {sample_rows:,} rows for all visualizers")
                self.df = df.sample(n=sample_rows, random_state=42)
            else:
                self.df = df
        else:
            self.df = df
        os.makedirs(config.figure_dir, exist_ok=True)
        matplotlib.rcParams['figure.max_open_warning'] = 0
        plt.ioff()

    def _cleanup_memory(self):
        """Force memory cleanup between visualizers (≤10 lines)"""
        plt.close('all')
        gc.collect()
        # Periodically clear the cache to prevent unbounded growth
        # Clear every 5 visualizer calls (reduces memory footprint)
        if not hasattr(self, '_cleanup_count'):
            self._cleanup_count = 0
        self._cleanup_count += 1
        if self._cleanup_count % 5 == 0:
            clear_viz_cache()

    def create_all(self):
        print("[VERBOSE] Creating temporal visualizations...")
        try:
            TemporalVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Temporal visualizations failed: {e}")
            self._cleanup_memory()
        
        print("[VERBOSE] Creating economic visualizations...")
        try:
            EconomicVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Economic visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating correlation visualizations...")
        try:
            CorrelationVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Correlation visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating statistical distribution visualizations...")
        try:
            StatisticalVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Statistical visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating advanced visualizations (violin, ridge, radar)...")
        try:
            AdvancedVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Advanced visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating year-over-year change visualizations...")
        try:
            YoYChangeVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Year-over-year visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating outlier and anomaly detection visualizations...")
        try:
            OutlierVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Outlier visualizations failed: {e}")
            self._cleanup_memory()
        
        print("[VERBOSE] Creating demographics visualizations...")
        try:
            DemographicsVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Demographics visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating transportation visualizations...")
        try:
            TransportationVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Transportation visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating income composition visualizations...")
        try:
            IncomeCompositionVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Income composition visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating housing characteristics visualizations...")
        try:
            HousingCharacteristicsVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Housing characteristics visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating household composition visualizations...")
        try:
            HouseholdCompositionVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Household composition visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating technology adoption visualizations...")
        try:
            TechnologyAdoptionVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Technology adoption visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating cost burden visualizations...")
        try:
            CostBurdenVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Cost burden visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating race & ethnicity visualizations...")
        try:
            RaceEthnicityVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Race & ethnicity visualizations failed: {e}")
            self._cleanup_memory()
        
        print("[VERBOSE] Creating multi-variable interaction visualizations...")
        try:
            MultiVariableVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except (VisualizationError, PlotCreationError) as e:
            print(f"[WARNING] Multi-variable visualizations failed: {e}")
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Multi-variable visualizations failed unexpectedly: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating distribution comparison visualizations...")
        try:
            DistributionComparisonVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except (VisualizationError, PlotCreationError) as e:
            print(f"[WARNING] Distribution comparison visualizations failed: {e}")
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Distribution comparison visualizations failed unexpectedly: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating enhanced feature interaction visualizations...")
        try:
            EnhancedFeatureInteractionVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except (VisualizationError, PlotCreationError) as e:
            print(f"[WARNING] Enhanced feature interaction visualizations failed: {e}")
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Enhanced feature interaction visualizations failed unexpectedly: {e}")
            self._cleanup_memory()

        print("[VERBOSE] All visualizations complete!")
        self._cleanup_memory()  # Final cleanup
        
        print("[VERBOSE] Creating missing data analysis...")
        try:
            self._missing_data_analysis()
        except Exception as e:
            print(f"[WARNING] Missing data analysis failed: {e}")

        # Force cleanup to prevent memory leaks
        plt.close('all')
        gc.collect()
    
    def _missing_data_analysis(self):
        plt.figure(figsize=(12, 8))
        missing_pct = self.df.isna().sum() / len(self.df) * 100
        top_missing = missing_pct.nlargest(15)
        plt.barh(range(len(top_missing)), top_missing.values, color='coral')
        plt.yticks(range(len(top_missing)), top_missing.index, fontsize=9)
        plt.xlabel('Missing %')
        plt.title('Top 15 Variables with Missing Data', fontweight='bold', fontsize=14)
        plt.tight_layout()
        self._save_fig('missing_data.png')
    
    def _save_fig(self, filename: str):
        if self.survey_type:
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{self.survey_type}.{ext}"
        path = f"{self.config.figure_dir}/{filename}"
        plt.savefig(path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close()

# ============================================================================
# ML VISUALIZER
# ============================================================================

class MLVisualizer:
    """Visualizes ML model results with comprehensive plots"""

    def __init__(self, config: Config, survey_type: str = ""):
        self.config = config
        self.survey_type = survey_type.upper() if survey_type else ""
        self.current_target = None  # Track current target for supervised learning

    def _dir(self, model_type: str, model_name: str = None) -> str:
        """Build directory path with optional target subdirectory for supervised learning"""
        # For supervised learning (regression/classification/timeseries), add target subdirectory
        supervised_types = ['regression', 'classification', 'timeseries', 'time_series']
        if self.current_target and model_type in supervised_types:
            if model_name:
                path = os.path.join(self.config.figure_dir, 'ml', model_type,
                                  self.current_target, model_name)
            else:
                path = os.path.join(self.config.figure_dir, 'ml', model_type,
                                  self.current_target)
        else:
            # Unsupervised learning (clustering) - no target subdirectory
            if model_name:
                path = os.path.join(self.config.figure_dir, 'ml', model_type, model_name)
            else:
                path = os.path.join(self.config.figure_dir, 'ml', model_type)
        os.makedirs(path, exist_ok=True)
        return path

    def _save(self, filename: str, model_type: str, model_name: str = None):
        """Save visualization and register in registry (≤10 lines)"""
        if self.survey_type:
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{self.survey_type}.{ext}"
        path = os.path.join(self._dir(model_type, model_name), filename)
        plt.savefig(path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close()
        self._register_visual(path, model_type, filename, model_name)

    def _register_visual(self, path, model_type, filename, model_name):
        """Register visual in global registry (≤10 lines)"""
        try:
            title = filename.replace('_', ' ').replace('.png', '')
            register_visual(path=path, visual_type=model_type, title=title,
                          category='ml', model_name=model_name,
                          targets=getattr(self, 'current_target', None) and [self.current_target] or [],
                          features=getattr(self, 'feature_names', '').split(', ') if hasattr(self, 'feature_names') else [],
                          subdirectory=self.current_target)
        except Exception as e:
            print(f"[WARNING] Failed to register visual {path}: {e}")
    
    def viz_regression(self, result, X, y, target_name: str = None):
        self.target_name = target_name or 'Target'
        self.current_target = target_name  # Set for directory path
        self.model_name = getattr(result, 'model_name', 'unknown')
        self.feature_names = ', '.join(X.columns[:3].tolist())  # First 3 features for titles
        self._pred_actual(result)
        self._residuals(result)
        self._cv(result)
        self._features(result)
        self._learning_curve(result)
        self._feature_correlations(result, X, y)
    
    def _pred_actual(self, r):
        if r.metadata.get('y_test') is None:
            return
        y_test = r.metadata['y_test']
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, r.predictions, alpha=0.5, s=20)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel(f'Actual {self.target_name}')
        plt.ylabel(f'Predicted {self.target_name}')
        title = f'{r.model_name.upper()} - Target: {self.target_name}\nFeatures: {self.feature_names} (R²={r.test_score:.3f})'
        plt.title(title, fontweight='bold')
        plt.grid(alpha=0.3)
        self._save('predictions.png', 'regression', self.model_name)
    
    def _residuals(self, r):
        if r.metadata.get('y_test') is None:
            return
        y_test = r.metadata['y_test']
        res = y_test - r.predictions
        plt.figure(figsize=(10, 6))
        plt.scatter(r.predictions, res, alpha=0.5, s=20)
        plt.axhline(y=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Predicted')
        plt.ylabel('Residuals')
        title = f'{r.model_name.upper()} Residuals - Target: {self.target_name}\nFeatures: {self.feature_names}'
        plt.title(title, fontweight='bold')
        plt.grid(alpha=0.3)
        self._save('residuals.png', 'regression', self.model_name)
    
    def _cv(self, r):
        if not r.cv_scores:
            return
        plt.figure(figsize=(10, 6))
        plt.bar(range(1, len(r.cv_scores) + 1), r.cv_scores, color='steelblue')
        mean = r.metadata.get('cv_mean', 0)
        plt.axhline(y=mean, color='r', linestyle='--', label=f'Mean: {mean:.3f}')
        plt.xlabel('Fold')
        plt.ylabel('R²')
        title = f'{r.model_name.upper()} Cross-Validation - Target: {self.target_name}\nFeatures: {self.feature_names}'
        plt.title(title, fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        self._save('cv_scores.png', 'regression', self.model_name)
    
    def _features(self, r):
        if not r.feature_importance:
            return
        plt.figure(figsize=(10, 6))
        items = sorted(r.feature_importance.items(), key=lambda x: x[1], reverse=True)[:10]
        names, vals = zip(*items)
        plt.barh(range(len(names)), vals, color='teal')
        plt.yticks(range(len(names)), names)
        plt.xlabel('Importance')
        title = f'{r.model_name.upper()} Top Features - Target: {self.target_name}'
        plt.title(title, fontweight='bold')
        plt.tight_layout()
        self._save('features.png', 'regression', self.model_name)
    
    def _learning_curve(self, r):
        if r.metadata.get('y_test') is None:
            return
        y_test = r.metadata['y_test']
        res = y_test - r.predictions
        
        # Error distribution
        plt.figure(figsize=(10, 6))
        plt.hist(res, bins=30, edgecolor='black', alpha=0.7, color='coral')
        plt.axvline(x=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Error')
        plt.ylabel('Frequency')
        title = f'{r.model_name.upper()} Error Distribution - Target: {self.target_name}\nFeatures: {self.feature_names}'
        plt.title(title, fontweight='bold')
        plt.grid(alpha=0.3)
        self._save('error_distribution.png', 'regression', self.model_name)
        
        # Actual vs Predicted distribution comparison
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.hist(y_test, bins=30, alpha=0.7, color='blue', edgecolor='black', label='Actual')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Actual Distribution')
        plt.legend()
        plt.grid(alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.hist(r.predictions, bins=30, alpha=0.7, color='green', edgecolor='black', label='Predicted')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title('Predicted Distribution')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        self._save('distribution_comparison.png', 'regression', self.model_name)
        
        # Variance analysis
        actual_var = np.var(y_test)
        pred_var = np.var(r.predictions)
        plt.figure(figsize=(8, 6))
        plt.bar(['Actual', 'Predicted'], [actual_var, pred_var],
                color=['blue', 'green'], alpha=0.7, edgecolor='black')
        plt.ylabel('Variance')
        title = f'{r.model_name.upper()} Variance - Target: {self.target_name}\nFeatures: {self.feature_names}'
        plt.title(title, fontweight='bold')
        plt.grid(alpha=0.3, axis='y')
        for i, v in enumerate([actual_var, pred_var]):
            plt.text(i, v + actual_var * 0.02, f'{v:.2f}', ha='center', fontweight='bold')
        self._save('variance_comparison.png', 'regression', self.model_name)
    
    def _feature_correlations(self, r, X, y):
        """Visualize top feature correlations with target"""
        if not r.feature_importance or len(X) == 0:
            return
        
        top_features = sorted(r.feature_importance.items(), 
                            key=lambda x: x[1], reverse=True)[:5]
        if not top_features:
            return
        
        fig, axes = plt.subplots(1, min(3, len(top_features)), 
                                figsize=(15, 4))
        if len(top_features) == 1:
            axes = [axes]
        
        for idx, (feat_name, _) in enumerate(top_features[:3]):
            if feat_name in X.columns:
                ax = axes[idx] if len(top_features) > 1 else axes[0]
                ax.scatter(X[feat_name], y, alpha=0.3, s=10)
                ax.set_xlabel(feat_name)
                ax.set_ylabel(self.target_name)
                ax.set_title(f'{feat_name} vs {self.target_name}')
                ax.grid(alpha=0.3)
        
        plt.tight_layout()
        self._save('feature_target_correlation.png', 'regression', self.model_name)
    
    def viz_clustering(self, result, X):
        self.cluster_method = getattr(result, 'method', 'kmeans')
        self._sizes(result)
        self._scatter(result, X)
        self._silhouette(result)
        self._cluster_distributions(result, X)
        self._cluster_variance(result, X)
    
    def _sizes(self, r):
        plt.figure(figsize=(10, 6))
        sizes = [r.cluster_sizes.get(i, 0) for i in range(r.n_clusters)]
        plt.bar(range(r.n_clusters), sizes, color='steelblue')
        plt.xlabel('Cluster')
        plt.ylabel('Size')
        plt.title(f'Cluster Sizes (Silhouette={r.silhouette_score:.3f})', fontweight='bold')
        plt.grid(alpha=0.3)
        self._save('sizes.png', 'clustering', self.cluster_method)
    
    def _scatter(self, r, X):
        if X.shape[1] < 2:
            return
        plt.figure(figsize=(10, 8))
        cols = X.columns[:2]
        plt.scatter(X[cols[0]], X[cols[1]], c=r.labels, cmap='viridis', alpha=0.6, s=30)
        plt.xlabel(cols[0])
        plt.ylabel(cols[1])
        plt.title('Clusters (2D)', fontweight='bold')
        plt.colorbar(label='Cluster')
        self._save('scatter.png', 'clustering', self.cluster_method)
    
    def _silhouette(self, r):
        plt.figure(figsize=(10, 6))
        plt.bar([0], [r.silhouette_score], color='teal', width=0.5)
        plt.ylim(0, 1)
        plt.ylabel('Score')
        plt.title(f'Silhouette: {r.silhouette_score:.3f}', fontweight='bold')
        plt.xticks([])
        plt.grid(alpha=0.3)
        self._save('silhouette.png', 'clustering', self.cluster_method)
    
    def _cluster_distributions(self, r, X):
        """Visualize feature distributions across clusters"""
        if X.shape[1] == 0:
            return
        
        # Select up to 4 features for visualization
        n_features = min(4, X.shape[1])
        features = X.columns[:n_features]
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        for idx, feature in enumerate(features):
            if idx >= 4:
                break
            ax = axes[idx]
            for cluster_id in range(r.n_clusters):
                cluster_data = X[r.labels == cluster_id][feature]
                ax.hist(cluster_data, alpha=0.5, label=f'Cluster {cluster_id}', bins=20)
            ax.set_xlabel(feature)
            ax.set_ylabel('Frequency')
            ax.set_title(f'{feature} Distribution by Cluster', fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)
        
        plt.tight_layout()
        self._save('feature_distributions.png', 'clustering', self.cluster_method)
    
    def _cluster_variance(self, r, X):
        """Visualize variance of features across clusters"""
        if X.shape[1] == 0:
            return
        
        # Calculate variance for each feature in each cluster
        variances = []
        for cluster_id in range(r.n_clusters):
            cluster_data = X[r.labels == cluster_id]
            cluster_var = cluster_data.var().values
            variances.append(cluster_var)
        
        # Plot variance comparison
        features = X.columns[:min(6, X.shape[1])]  # Limit to 6 features for readability
        x = np.arange(len(features))
        width = 0.15
        
        fig, ax = plt.subplots(figsize=(12, 6))
        for cluster_id in range(r.n_clusters):
            offset = width * (cluster_id - r.n_clusters / 2)
            cluster_vars = [variances[cluster_id][i] for i in range(len(features))]
            ax.bar(x + offset, cluster_vars, width, label=f'Cluster {cluster_id}', alpha=0.8)
        
        ax.set_xlabel('Features')
        ax.set_ylabel('Variance')
        ax.set_title('Feature Variance by Cluster', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(features, rotation=45, ha='right')
        ax.legend()
        ax.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save('variance_by_cluster.png', 'clustering', self.cluster_method)
    
    def viz_timeseries(self, result, df, target_col):
        """Generate all time series visualizations (≤10 lines)"""
        self.target_name = target_col
        self.current_target = target_col  # Set for directory path (supervised learning)
        self.ts_method = result.get('model_name', result.get('method', 'polynomial'))
        self._forecast(result, df, target_col)
        self._ts_residuals(result, df, target_col)
        self._ts_trend_decomposition(df, target_col)
        self._ts_accuracy_metrics(result, df, target_col)
        self._ts_confidence_intervals(result, df, target_col)
    
    def _prep_forecast_data(self, df, col):
        """Prepare aggregated time series data (≤10 lines)"""
        if 'Census_Year' not in df.columns or col not in df.columns:
            return None
        df_agg = df.groupby('Census_Year')[col].mean().reset_index()
        df_agg = df_agg.sort_values('Census_Year')
        return df_agg if len(df_agg) > 0 else None
    
    def _plot_forecast_lines(self, df_agg, col, forecast_vals, ci_lower=None, ci_upper=None):
        """Plot historical and forecast lines with CI bands (≤10 lines)"""
        # Calculate historical std for uncertainty band
        hist_mean = df_agg[col].mean()
        hist_std = df_agg[col].std()
        hist_upper = df_agg[col] + hist_std
        hist_lower = df_agg[col] - hist_std

        # Plot historical std band (light blue)
        plt.fill_between(df_agg['Census_Year'], hist_lower, hist_upper,
                        alpha=0.15, color='#87CEEB', label='Historical ±1σ')

        # Plot historical data line (EXPLICIT BLUE)
        plt.plot(df_agg['Census_Year'], df_agg[col], marker='o', label='Historical Data',
                linewidth=2.5, color='#1f77b4', markersize=6, markerfacecolor='#1f77b4', markeredgecolor='darkblue')
        print(f"[DEBUG-VIZ] Forecast values: {forecast_vals}, CI_lower: {ci_lower}, CI_upper: {ci_upper}")

        if forecast_vals and len(forecast_vals) > 0:
            # Get last historical point for seamless connection
            max_yr = df_agg['Census_Year'].max()
            last_val = df_agg[df_agg['Census_Year'] == max_yr][col].iloc[0]

            # Create forecast years and prepend last historical year for connection
            forecast_yrs = list(range(int(max_yr) + 1, int(max_yr) + len(forecast_vals) + 1))
            forecast_yrs_connected = [int(max_yr)] + forecast_yrs
            forecast_vals_connected = [last_val] + list(forecast_vals)

            # Plot forecast connected to last historical point (EXPLICIT ORANGE/RED)
            plt.plot(forecast_yrs_connected, forecast_vals_connected, marker='s',
                    label='Forecast', linewidth=2.5, linestyle='--', color='#ff7f0e',
                    markersize=7, markerfacecolor='#ff7f0e', markeredgecolor='darkorange')

            # Plot forecast CI bands if available (orange/red to contrast with blue historical)
            if ci_lower and ci_upper and len(ci_lower) == len(forecast_vals) and len(ci_upper) == len(forecast_vals):
                ci_lower_connected = [last_val] + list(ci_lower)
                ci_upper_connected = [last_val] + list(ci_upper)
                plt.fill_between(forecast_yrs_connected, ci_lower_connected, ci_upper_connected,
                                alpha=0.25, color='#ff7f0e', label='Forecast 95% CI')
                print(f"[DEBUG-VIZ] Plotted CI bands: lower={ci_lower_connected}, upper={ci_upper_connected}")
            else:
                print(f"[DEBUG-VIZ] CI not plotted - ci_lower len: {len(ci_lower) if ci_lower else 0}, ci_upper len: {len(ci_upper) if ci_upper else 0}, forecast len: {len(forecast_vals)}")

    def _finalize_forecast_plot(self, col, model_name=''):
        """Finalize forecast plot (≤10 lines)"""
        plt.xlabel('Year')
        plt.ylabel(f'{col}')
        # Include target name and model name in title
        title = f'Time Series Forecast - {col}'
        if model_name:
            title += f' ({model_name})'
        plt.title(title, fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()

    def _forecast(self, r, df, col):
        """Visualize forecast with historical data and CI (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            if df_agg is None:
                return
            plt.figure(figsize=(12, 6))
            forecast_vals = r.get('forecast_values', [])
            ci_lower = r.get('ci_lower', [])
            ci_upper = r.get('ci_upper', [])
            model_name = r.get('model_name', r.get('best_model', ''))
            self._plot_forecast_lines(df_agg, col, forecast_vals, ci_lower, ci_upper)
            self._finalize_forecast_plot(col, model_name)
            self._save('forecast.png', 'time_series', self.ts_method)
        except Exception as e:
            print(f"[WARNING] Time series forecast visualization failed: {e}")
    
    def _calc_ts_residuals(self, df_sorted, col):
        """Calculate time series residuals (≤10 lines)"""
        window = min(3, len(df_sorted))
        ma = df_sorted[col].rolling(window=window, center=True).mean()
        return df_sorted[col] - ma
    
    def _plot_residuals_scatter(self, df_agg, residuals, col):
        """Plot residuals scatter (≤10 lines)"""
        plt.scatter(df_agg['Census_Year'], residuals, alpha=0.6, s=50)
        plt.axhline(y=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Year')
        plt.ylabel('Residuals')
        plt.title(f'Time Series Residuals - {col}', fontweight='bold')
        plt.grid(alpha=0.3)
    
    def _ts_residuals(self, r, df, col):
        """Visualize time series residuals (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            if df_agg is None or len(df_agg) < 3:
                return
            residuals = self._calc_ts_residuals(df_agg, col)
            plt.figure(figsize=(12, 6))
            self._plot_residuals_scatter(df_agg, residuals, col)
            self._save('residuals.png', 'time_series', self.ts_method)
        except Exception as e:
            raise PlotCreationError('ts_residuals', str(e))
    
    def _plot_decomp_original(self, ax, df_sorted, col):
        """Plot original series (≤10 lines)"""
        ax.plot(df_sorted['Census_Year'], df_sorted[col], marker='o', linewidth=2)
        ax.set_ylabel(col)
        ax.set_title(f'Original Series - {col}', fontweight='bold')
        ax.grid(alpha=0.3)
    
    def _plot_decomp_trend(self, ax, df_sorted, col):
        """Plot trend component (≤10 lines)"""
        window = min(3, len(df_sorted))
        trend = df_sorted[col].rolling(window=window, center=True).mean()
        ax.plot(df_sorted['Census_Year'], trend, marker='o', linewidth=2, color='orange')
        ax.set_ylabel('Trend')
        ax.set_title('Trend Component', fontweight='bold')
        ax.grid(alpha=0.3)
        return trend
    
    def _plot_decomp_residual(self, ax, df_sorted, col, trend):
        """Plot residual component (≤10 lines)"""
        residual = df_sorted[col] - trend
        ax.plot(df_sorted['Census_Year'], residual, marker='o', linewidth=2, color='green')
        ax.axhline(y=0, color='r', linestyle='--', lw=2)
        ax.set_xlabel('Year')
        ax.set_ylabel('Residual')
        ax.set_title('Residual Component', fontweight='bold')
        ax.grid(alpha=0.3)
    
    def _plot_all_decomp(self, axes, df_agg, col):
        """Plot all decomposition components (≤10 lines)"""
        self._plot_decomp_original(axes[0], df_agg, col)
        trend = self._plot_decomp_trend(axes[1], df_agg, col)
        self._plot_decomp_residual(axes[2], df_agg, col, trend)
    
    def _ts_trend_decomposition(self, df, col):
        """Visualize trend decomposition (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            if df_agg is None or len(df_agg) < 4:
                return
            fig, axes = plt.subplots(3, 1, figsize=(12, 10))
            self._plot_all_decomp(axes, df_agg, col)
            plt.tight_layout()
            self._save('trend_decomposition.png', 'time_series', self.ts_method)
        except Exception as e:
            raise PlotCreationError('ts_trend_decomposition', str(e))
    
    def _plot_yoy_change(self, ax, df_sorted, col):
        """Plot year-over-year change (≤10 lines)"""
        yoy_change = df_sorted[col].pct_change() * 100
        ax.plot(df_sorted['Census_Year'].iloc[1:], yoy_change.iloc[1:], 
                marker='o', linewidth=2, color='purple')
        ax.axhline(y=0, color='r', linestyle='--', lw=2)
        ax.set_xlabel('Year')
        ax.set_ylabel('YoY Change (%)')
        ax.set_title(f'Year-over-Year Change - {col}', fontweight='bold')
        ax.grid(alpha=0.3)
    
    def _plot_forecast_bars(self, ax, df_sorted, col, forecast_vals):
        """Plot forecast values as bars (≤10 lines)"""
        if len(forecast_vals) == 0:
            return False
        max_yr = df_sorted['Census_Year'].max()
        forecast_yrs = list(range(int(max_yr) + 1, int(max_yr) + len(forecast_vals) + 1))
        ax.bar(forecast_yrs, forecast_vals, alpha=0.7, color='coral', edgecolor='black')
        ax.set_xlabel('Forecast Year')
        ax.set_ylabel(col)
        ax.set_title(f'Forecasted Values - {col}', fontweight='bold')
        ax.grid(alpha=0.3, axis='y')
        return True
    
    def _ts_accuracy_metrics(self, r, df, col):
        """Visualize forecast accuracy metrics (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            if df_agg is None or len(df_agg) < 2:
                return
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            self._plot_yoy_change(axes[0], df_agg, col)
            self._plot_forecast_bars(axes[1], df_agg, col, r.get('forecast_values', []))
            plt.tight_layout()
            self._save('accuracy_metrics.png', 'time_series', self.ts_method)
        except Exception as e:
            raise PlotCreationError('ts_accuracy_metrics', str(e))
    
    def _get_ci_data(self, r):
        """Extract confidence interval data from result (≤10 lines)"""
        forecast_vals = r.get('forecast_values', [])
        ci_lower = r.get('ci_lower', [])
        ci_upper = r.get('ci_upper', [])
        if not forecast_vals or not ci_lower or not ci_upper:
            return None, None, None
        return forecast_vals, ci_lower, ci_upper
    
    def _plot_ci_bands(self, df_agg, col, forecast_vals, ci_lower, ci_upper):
        """Plot confidence interval bands (≤10 lines)"""
        # Plot historical data
        plt.plot(df_agg['Census_Year'], df_agg[col], marker='o', label='Historical', linewidth=2)

        # Get last historical point for connection
        max_yr = df_agg['Census_Year'].max()
        last_val = df_agg[df_agg['Census_Year'] == max_yr][col].iloc[0]

        # Create forecast years and prepend last historical year for connection
        forecast_yrs = list(range(int(max_yr) + 1, int(max_yr) + len(forecast_vals) + 1))
        forecast_yrs_connected = [int(max_yr)] + forecast_yrs
        forecast_vals_connected = [last_val] + list(forecast_vals)
        ci_lower_connected = [last_val] + list(ci_lower)
        ci_upper_connected = [last_val] + list(ci_upper)

        # Plot forecast line connected to last historical point
        plt.plot(forecast_yrs_connected, forecast_vals_connected, marker='s',
                label='Forecast', linewidth=2, linestyle='--', color='red')

        # Fill confidence interval connected to last historical point
        plt.fill_between(forecast_yrs_connected, ci_lower_connected, ci_upper_connected,
                        alpha=0.2, color='red', label='95% CI')
    
    def _finalize_ci_plot(self, col):
        """Finalize confidence interval plot (≤10 lines)"""
        plt.xlabel('Year')
        plt.ylabel(col)
        plt.title(f'Forecast with Confidence Intervals - {col}', fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
    
    def _ts_confidence_intervals(self, r, df, col):
        """Visualize forecast with confidence intervals (≤10 lines)"""
        try:
            df_agg = self._prep_forecast_data(df, col)
            forecast_vals, ci_lower, ci_upper = self._get_ci_data(r)
            if df_agg is None or forecast_vals is None:
                return
            plt.figure(figsize=(12, 6))
            self._plot_ci_bands(df_agg, col, forecast_vals, ci_lower, ci_upper)
            self._finalize_ci_plot(col)
            self._save('confidence_intervals.png', 'time_series', self.ts_method)
        except Exception as e:
            print(f"[WARNING] Confidence interval visualization failed: {e}")
    
    def viz_model_comparison(self, model_results_dict, target_name: str = None):
        """Compare performance across multiple models"""
        self.target_name = target_name or 'Target'
        self.current_target = target_name  # Set for directory path
        self._compare_scores(model_results_dict)
        self._compare_cv_scores(model_results_dict)
        self._compare_metrics(model_results_dict)
    
    def _compare_scores(self, results_dict):
        """Compare R² scores across models"""
        if not results_dict:
            return
        
        models = []
        train_scores = []
        test_scores = []
        
        for model_name, result in results_dict.items():
            if hasattr(result, 'train_score') and hasattr(result, 'test_score'):
                models.append(model_name.replace('_', ' ').title())
                train_scores.append(result.train_score)
                test_scores.append(result.test_score or 0)
        
        if not models:
            return
        
        x = np.arange(len(models))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(x - width/2, train_scores, width, label='Train R²', alpha=0.8, color='steelblue')
        ax.bar(x + width/2, test_scores, width, label='Test R²', alpha=0.8, color='coral')
        
        ax.set_xlabel('Model')
        ax.set_ylabel('R² Score')
        ax.set_title(f'Model Comparison - {self.target_name}', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.legend()
        ax.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save('model_comparison_scores.png', 'model_comparison')
    
    def _compare_cv_scores(self, results_dict):
        """Compare cross-validation scores across models"""
        if not results_dict:
            return
        
        models_with_cv = {}
        for model_name, result in results_dict.items():
            if hasattr(result, 'metadata') and result.metadata.get('cv_mean') is not None:
                models_with_cv[model_name] = {
                    'mean': result.metadata['cv_mean'],
                    'std': result.metadata.get('cv_std', 0)
                }
        
        if not models_with_cv:
            return
        
        models = [m.replace('_', ' ').title() for m in models_with_cv.keys()]
        means = [v['mean'] for v in models_with_cv.values()]
        stds = [v['std'] for v in models_with_cv.values()]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(range(len(models)), means, yerr=stds, alpha=0.8, 
              color='teal', capsize=5, edgecolor='black')
        ax.set_xlabel('Model')
        ax.set_ylabel('CV R² (Mean ± Std)')
        ax.set_title(f'Cross-Validation Comparison - {self.target_name}', fontweight='bold')
        ax.set_xticks(range(len(models)))
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.grid(alpha=0.3, axis='y')
        plt.tight_layout()
        self._save('model_comparison_cv.png', 'model_comparison')
    
    def _compare_metrics(self, results_dict):
        """Compare additional metrics (RMSE, MAE) across models"""
        if not results_dict:
            return
        
        models_with_metrics = {}
        for model_name, result in results_dict.items():
            if hasattr(result, 'metadata'):
                rmse = result.metadata.get('rmse')
                mae = result.metadata.get('mae')
                if rmse is not None and mae is not None:
                    models_with_metrics[model_name] = {'rmse': rmse, 'mae': mae}
        
        if not models_with_metrics:
            return
        
        models = [m.replace('_', ' ').title() for m in models_with_metrics.keys()]
        rmse_vals = [v['rmse'] for v in models_with_metrics.values()]
        mae_vals = [v['mae'] for v in models_with_metrics.values()]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # RMSE comparison
        axes[0].bar(range(len(models)), rmse_vals, alpha=0.8, color='purple', edgecolor='black')
        axes[0].set_xlabel('Model')
        axes[0].set_ylabel('RMSE')
        axes[0].set_title('Root Mean Squared Error', fontweight='bold')
        axes[0].set_xticks(range(len(models)))
        axes[0].set_xticklabels(models, rotation=45, ha='right')
        axes[0].grid(alpha=0.3, axis='y')
        
        # MAE comparison
        axes[1].bar(range(len(models)), mae_vals, alpha=0.8, color='orange', edgecolor='black')
        axes[1].set_xlabel('Model')
        axes[1].set_ylabel('MAE')
        axes[1].set_title('Mean Absolute Error', fontweight='bold')
        axes[1].set_xticks(range(len(models)))
        axes[1].set_xticklabels(models, rotation=45, ha='right')
        axes[1].grid(alpha=0.3, axis='y')
        
        plt.tight_layout()
        self._save('model_comparison_metrics.png', 'model_comparison')