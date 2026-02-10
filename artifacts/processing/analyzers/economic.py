"""Economic analysis classes for census data."""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from ..utilities.zero_exclusion import get_zero_exclusion_columns, should_exclude_zeros
from ..utilities.weights import get_weight_column


# ============================================================================
# ECONOMIC ANALYZER BASE
# ============================================================================

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
