"""
Economic Feature Creator Module

Provides domain-specific economic and housing features for census analysis,
including Gini coefficient, affordability indices, poverty intensity measures,
and housing quality indices.
"""
import pandas as pd
import numpy as np
from typing import List, Optional
from logging_config import get_logger


class EconomicFeatureCreator:
    """Domain-specific economic and housing features for census analysis"""

    @staticmethod
    def _validate_columns(df: pd.DataFrame, required: List[str],
                          operation: str) -> List[str]:
        """Return list of available columns from required list."""
        logger = get_logger("feature_engineering")
        available = [c for c in required if c in df.columns]
        missing = set(required) - set(available)
        if missing:
            logger.warning(f"{operation}: Missing columns {missing}")
        return available

    @staticmethod
    def create_gini_coefficient(df: pd.DataFrame,
                                income_col: str = 'Total_Person_Income',
                                group_by: Optional[str] = 'Census_Year') -> pd.DataFrame:
        """Calculate Gini coefficient for income inequality"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()

        def gini(values):
            """Calculate Gini coefficient using Lorenz curve"""
            values = np.array(values)
            values = values[~np.isnan(values)]
            values = values[values > 0]
            if len(values) < 2:
                return np.nan
            values = np.sort(values)
            n = len(values)
            cumulative = np.cumsum(values)
            return (2 * np.sum((np.arange(1, n + 1) * values)) / (n * cumulative[-1])) - (n + 1) / n

        if income_col not in df.columns:
            logger.warning(f"Gini coefficient: {income_col} not found")
            return df_enhanced

        if group_by and group_by in df.columns:
            gini_by_group = df.groupby(group_by)[income_col].apply(gini)
            gini_map = gini_by_group.to_dict()
            df_enhanced[f'{income_col}_gini'] = df_enhanced[group_by].map(gini_map)
            logger.debug(f"Created Gini coefficient by {group_by}")
        else:
            overall_gini = gini(df[income_col].dropna().values)
            df_enhanced[f'{income_col}_gini'] = overall_gini
            logger.debug(f"Created overall Gini coefficient: {overall_gini:.4f}")

        return df_enhanced

    @staticmethod
    def create_affordability_indices(df: pd.DataFrame) -> pd.DataFrame:
        """Create comprehensive housing affordability indices"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        # Rent-to-Income Ratio (monthly rent / monthly income)
        if 'Gross_Rent' in df.columns and 'Total_Person_Income' in df.columns:
            monthly_income = df['Total_Person_Income'] / 12
            mask = (monthly_income > 0) & (df['Gross_Rent'] > 0)
            df_enhanced['Rent_to_Income_Ratio'] = np.nan
            df_enhanced.loc[mask, 'Rent_to_Income_Ratio'] = df.loc[mask, 'Gross_Rent'] / monthly_income[mask]
            created.append('Rent_to_Income_Ratio')

            # Housing Cost Burden (30% threshold)
            df_enhanced['Housing_Cost_Burden'] = (df_enhanced['Rent_to_Income_Ratio'] > 0.30).fillna(False).astype(int)
            created.append('Housing_Cost_Burden')

            # Severe Cost Burden (50% threshold)
            df_enhanced['Severe_Cost_Burden'] = (df_enhanced['Rent_to_Income_Ratio'] > 0.50).fillna(False).astype(int)
            created.append('Severe_Cost_Burden')

        # Price-to-Income Ratio (property value / annual income)
        if 'Property_Value' in df.columns and 'Total_Person_Income' in df.columns:
            mask = (df['Total_Person_Income'] > 0) & (df['Property_Value'] > 0)
            df_enhanced['Price_to_Income_Ratio'] = np.nan
            df_enhanced.loc[mask, 'Price_to_Income_Ratio'] = (
                df.loc[mask, 'Property_Value'] / df.loc[mask, 'Total_Person_Income']
            )
            created.append('Price_to_Income_Ratio')

        # Housing Affordability Index (HAI)
        # HAI = (Median Income / Qualifying Income) * 100
        # Qualifying Income = (Mortgage Payment * 12) / 0.25
        if 'Property_Value' in df.columns and 'Total_Person_Income' in df.columns:
            # Estimate monthly mortgage (assume 30yr @ 7% rate, 20% down)
            principal = df['Property_Value'] * 0.80
            monthly_rate = 0.07 / 12
            n_payments = 360
            mortgage_payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)

            qualifying_income = (mortgage_payment * 12) / 0.25
            mask = qualifying_income > 0
            df_enhanced['Housing_Affordability_Index'] = np.nan
            df_enhanced.loc[mask, 'Housing_Affordability_Index'] = (
                df.loc[mask, 'Total_Person_Income'] / qualifying_income[mask]
            ) * 100
            created.append('Housing_Affordability_Index')

        logger.debug(f"Created affordability indices: {created}")
        return df_enhanced

    @staticmethod
    def create_poverty_intensity(df: pd.DataFrame,
                                 poverty_line: float = 15000,
                                 survey_type: str = 'population') -> pd.DataFrame:
        """
        Create poverty gap and severity indices.

        Note: Only applicable to population surveys (uses Total_Person_Income).
        """
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()

        # Skip for housing surveys - poverty metrics require person-level income
        if survey_type.lower() != 'population':
            logger.debug("Poverty intensity: Skipped for non-population survey")
            return df_enhanced

        if 'Total_Person_Income' not in df.columns:
            logger.warning("Poverty intensity: Total_Person_Income not found")
            return df_enhanced

        income = df['Total_Person_Income']

        # Poverty status (binary)
        df_enhanced['In_Poverty'] = (income < poverty_line).fillna(False).astype(int)

        # Poverty Gap (distance from poverty line, normalized)
        df_enhanced['Poverty_Gap'] = np.maximum(0, (poverty_line - income) / poverty_line)

        # Poverty Severity (squared poverty gap)
        df_enhanced['Poverty_Severity'] = df_enhanced['Poverty_Gap'] ** 2

        logger.debug(f"Created poverty indices with poverty line ${poverty_line:,}")
        return df_enhanced

    @staticmethod
    def create_housing_quality_index(df: pd.DataFrame,
                                     survey_type: str = 'housing') -> pd.DataFrame:
        """
        Create composite housing quality index.

        Note: Only applicable to housing surveys (uses housing-specific columns).
        """
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()

        # Skip for population surveys - quality index requires housing-specific columns
        if survey_type.lower() != 'housing':
            logger.debug("Housing quality index: Skipped for non-housing survey")
            return df_enhanced

        quality_cols = []

        # Age of structure (newer = higher quality)
        if 'Year_Structure_Built' in df.columns:
            current_year = 2024
            df_enhanced['Structure_Age'] = current_year - df['Year_Structure_Built']
            df_enhanced['Structure_Age_Score'] = 1 - (df_enhanced['Structure_Age'] / 100).clip(0, 1)
            quality_cols.append('Structure_Age_Score')

        # Rooms and bedrooms (more = higher quality)
        if 'Number_of_Rooms' in df.columns:
            df_enhanced['Rooms_Score'] = (df['Number_of_Rooms'] / 10).clip(0, 1)
            quality_cols.append('Rooms_Score')

        if 'Number_of_Bedrooms' in df.columns:
            df_enhanced['Bedrooms_Score'] = (df['Number_of_Bedrooms'] / 5).clip(0, 1)
            quality_cols.append('Bedrooms_Score')

        # Create composite index
        if quality_cols:
            df_enhanced['Housing_Quality_Index'] = df_enhanced[quality_cols].mean(axis=1)
            logger.debug(f"Created housing quality index from {len(quality_cols)} components")

        return df_enhanced
