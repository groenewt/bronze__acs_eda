"""
Basic Feature Creator Module

Provides fundamental feature engineering operations including ratios,
income features, housing features, age groups, temporal features,
interactions, and polynomial features.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class FeatureCreator:
    """Create new features from existing census data"""

    @staticmethod
    def create_ratio_features(df: pd.DataFrame, numerators: List[str],
                             denominators: List[str]) -> pd.DataFrame:
        """Create ratio features from pairs of columns"""
        df_enhanced = df.copy()

        for num in numerators:
            for denom in denominators:
                if num in df_enhanced.columns and denom in df_enhanced.columns:
                    # Avoid division by zero
                    mask = df_enhanced[denom] != 0
                    feature_name = f'{num}_to_{denom}_ratio'
                    df_enhanced[feature_name] = np.nan
                    df_enhanced.loc[mask, feature_name] = (
                        df_enhanced.loc[mask, num] / df_enhanced.loc[mask, denom]
                    )

        return df_enhanced

    @staticmethod
    def create_income_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create income-related derived features.

        Returns:
            Tuple of (enhanced_df, metadata_dict)
        """
        df_enhanced = df.copy()
        created = []

        # Income per hour worked
        if 'Total_Person_Income' in df_enhanced.columns and 'Hours_Worked_Per_Week' in df_enhanced.columns:
            mask = (df_enhanced['Hours_Worked_Per_Week'] > 0) & (df_enhanced['Total_Person_Income'] > 0)
            df_enhanced['Income_Per_Hour'] = np.nan
            # Assuming 52 weeks per year
            df_enhanced.loc[mask, 'Income_Per_Hour'] = (
                df_enhanced.loc[mask, 'Total_Person_Income'] /
                (df_enhanced.loc[mask, 'Hours_Worked_Per_Week'] * 52)
            )
            created.append('Income_Per_Hour')

        # Income per week worked
        if 'Total_Person_Income' in df_enhanced.columns and 'Weeks_Worked_Past_Year' in df_enhanced.columns:
            mask = (df_enhanced['Weeks_Worked_Past_Year'] > 0) & (df_enhanced['Total_Person_Income'] > 0)
            df_enhanced['Income_Per_Week_Worked'] = np.nan
            df_enhanced.loc[mask, 'Income_Per_Week_Worked'] = (
                df_enhanced.loc[mask, 'Total_Person_Income'] /
                df_enhanced.loc[mask, 'Weeks_Worked_Past_Year']
            )
            created.append('Income_Per_Week_Worked')

        # Total annual hours worked
        if 'Hours_Worked_Per_Week' in df_enhanced.columns and 'Weeks_Worked_Past_Year' in df_enhanced.columns:
            mask = (df_enhanced['Hours_Worked_Per_Week'] > 0) & (df_enhanced['Weeks_Worked_Past_Year'] > 0)
            df_enhanced['Total_Annual_Hours'] = np.nan
            df_enhanced.loc[mask, 'Total_Annual_Hours'] = (
                df_enhanced.loc[mask, 'Hours_Worked_Per_Week'] * df_enhanced.loc[mask, 'Weeks_Worked_Past_Year']
            )
            created.append('Total_Annual_Hours')

        metadata = {
            'features': created,
            'transform': 'Income ratios derived from work metrics' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_housing_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create housing-related derived features.

        Returns:
            Tuple of (enhanced_df, metadata_dict)
        """
        df_enhanced = df.copy()
        created = []

        # Rent to property value ratio
        if 'Gross_Rent' in df_enhanced.columns and 'Property_Value' in df_enhanced.columns:
            mask = df_enhanced['Property_Value'] > 0
            df_enhanced['Annual_Rent_to_Value_Ratio'] = np.nan
            df_enhanced.loc[mask, 'Annual_Rent_to_Value_Ratio'] = (
                (df_enhanced.loc[mask, 'Gross_Rent'] * 12) /
                df_enhanced.loc[mask, 'Property_Value']
            )
            created.append('Annual_Rent_to_Value_Ratio')

        # Total monthly housing cost
        cost_cols = ['Electricity_Cost_Monthly', 'Gas_Cost_Monthly']
        available_cost_cols = [col for col in cost_cols if col in df_enhanced.columns]
        if available_cost_cols:
            df_enhanced['Total_Monthly_Utility_Cost'] = df_enhanced[available_cost_cols].sum(axis=1)
            created.append('Total_Monthly_Utility_Cost')

        # Property tax as percentage of value
        if 'Property_Taxes_Yearly' in df_enhanced.columns and 'Property_Value' in df_enhanced.columns:
            mask = df_enhanced['Property_Value'] > 0
            df_enhanced['Property_Tax_Rate'] = np.nan
            df_enhanced.loc[mask, 'Property_Tax_Rate'] = (
                df_enhanced.loc[mask, 'Property_Taxes_Yearly'] /
                df_enhanced.loc[mask, 'Property_Value'] * 100
            )
            created.append('Property_Tax_Rate')

        metadata = {
            'features': created,
            'transform': 'Housing cost ratios calculated' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_age_groups(df: pd.DataFrame, age_col: str = 'Age') -> Tuple[pd.DataFrame, Dict]:
        """Create age group categories.

        Returns:
            Tuple of (enhanced_df, metadata_dict)
        """
        df_enhanced = df.copy()
        created = []

        if age_col not in df_enhanced.columns:
            return df_enhanced, {'features': [], 'transform': ''}

        # Filter out NA values before pd.cut to avoid "boolean value of NA is ambiguous" error
        valid_age_mask = df_enhanced[age_col].notna()

        bins = [0, 18, 25, 35, 45, 55, 65, 100]
        labels = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']

        # Initialize Age_Group column with NaN
        df_enhanced['Age_Group'] = pd.NA

        # Apply pd.cut only to valid (non-NA) age values
        if valid_age_mask.any():
            df_enhanced.loc[valid_age_mask, 'Age_Group'] = pd.cut(
                df_enhanced.loc[valid_age_mask, age_col],
                bins=bins,
                labels=labels,
                right=False
            )
            created.append('Age_Group')

        metadata = {
            'features': created,
            'transform': 'Age binned into demographic groups' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_temporal_features(df: pd.DataFrame, year_col: str = 'Census_Year') -> Tuple[pd.DataFrame, Dict]:
        """Create temporal features from year.

        Returns:
            Tuple of (enhanced_df, metadata_dict)
        """
        df_enhanced = df.copy()
        created = []

        if year_col not in df_enhanced.columns:
            return df_enhanced, {'features': [], 'transform': ''}

        # Years since earliest year in dataset
        min_year = df_enhanced[year_col].min()
        df_enhanced['Years_Since_Start'] = df_enhanced[year_col] - min_year
        created.append('Years_Since_Start')

        # Decade
        df_enhanced['Decade'] = (df_enhanced[year_col] // 10) * 10
        created.append('Decade')

        metadata = {
            'features': created,
            'transform': 'Temporal features extracted from year' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_interaction_features(df: pd.DataFrame,
                                   col_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
        """Create interaction features (products) between column pairs"""
        df_enhanced = df.copy()

        for col1, col2 in col_pairs:
            if col1 in df_enhanced.columns and col2 in df_enhanced.columns:
                feature_name = f'{col1}_x_{col2}'
                df_enhanced[feature_name] = df_enhanced[col1] * df_enhanced[col2]

        return df_enhanced

    @staticmethod
    def create_polynomial_features(df: pd.DataFrame, cols: List[str],
                                  degree: int = 2) -> pd.DataFrame:
        """Create polynomial features (squared, cubed, etc.)"""
        df_enhanced = df.copy()

        for col in cols:
            if col not in df_enhanced.columns:
                continue
            for d in range(2, degree + 1):
                df_enhanced[f'{col}_power_{d}'] = df_enhanced[col] ** d

        return df_enhanced
