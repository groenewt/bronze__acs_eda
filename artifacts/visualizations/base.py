"""Base visualizer classes and utilities"""
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
# KEY COLUMN KEYWORDS (for _get_key_numeric_cols methods)
# ============================================================================

# Centralized keyword lists for column selection across all visualizers
# Each keyword matches columns containing that substring (case-sensitive)
_KEY_COLUMN_KEYWORDS = {
    'housing': [
        # Core economic
        'Value', 'Rent', 'Income', 'Cost', 'Tax', 'Mortgage',
        # Utilities (specific)
        'Electricity', 'Gas', 'Water', 'Fuel', 'Utility',
        # Other costs
        'Insurance', 'Fee', 'Payment',
        # Physical characteristics
        'Bedroom', 'Room', 'Vehicle', 'Person',
    ],
    'population': [
        # Core income/work
        'Income', 'Wage', 'Age', 'Hours', 'Earnings',
        # Time-related
        'Week', 'Travel',
        # Income types (specific)
        'Security', 'Retirement', 'Employment', 'Dividend', 'Assistance',
        # Demographics
        'Person', 'Poverty',
    ]
}

# Columns to always exclude from key column selection
_EXCLUDE_COLUMN_PATTERNS = [
    'Flag_', '_is_zero', '_is_missing', 'Specified_',
    'Adjustment_Factor', 'Weight_Replicate', 'SERIALNO', 'PUMA', 'ST'
]

def get_key_column_keywords(survey_type: str = '') -> List[str]:
    """Get keyword list for the given survey type."""
    survey = survey_type.upper() if survey_type else ''
    if survey == 'HOUSING':
        return _KEY_COLUMN_KEYWORDS['housing']
    elif survey == 'POPULATION':
        return _KEY_COLUMN_KEYWORDS['population']
    # Default: combine both for mixed/unknown survey types
    return list(set(_KEY_COLUMN_KEYWORDS['housing'] + _KEY_COLUMN_KEYWORDS['population']))

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
        """HOUSING: Apply memory-aware sampling - MUST be called first in create_all()"""
        if self.survey_type != "HOUSING":
            return

        from memory_utils import get_available_memory_gb
        available_gb = get_available_memory_gb()

        # Skip sampling if plenty of RAM available (16GB+)
        if available_gb > 16:
            return
        elif available_gb > 8:
            target = 20_000
        elif available_gb > 4:
            target = 10_000
        else:
            target = 4_000

        if len(self.df) > target:
            viz_name = self.__class__.__name__
            print(f"[HOUSING-SAMPLE] {viz_name}: {len(self.df):,} → {target} rows (RAM: {available_gb:.1f}GB)")
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
