"""
Household Composition Feature Creator Module

Provides domain-specific household composition features for census analysis,
including dependency ratios, SNAP eligibility proxies, and workers ratios.
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from logging_config import get_logger


class HouseholdCompositionFeatureCreator:
    """Domain-specific household composition features for census analysis"""

    # Federal Poverty Level approximation (2023)
    FPL_BASE = 14580  # For household of 1
    FPL_INCREMENT = 5140  # Per additional person

    @staticmethod
    def create_dependency_ratio(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create dependency ratio features"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        np_col = 'Number_of_Persons'
        r18_col = 'Persons_Under_18'
        r65_col = 'Persons_65_And_Over'

        if all(c in df.columns for c in [np_col, r18_col, r65_col]):
            # Working age = Total - Under 18 - 65 and Over
            df_enhanced['Working_Age_Persons'] = (
                df_enhanced[np_col] - df_enhanced[r18_col] - df_enhanced[r65_col]
            ).clip(lower=0)

            # Dependency ratio: (dependents) / (working age)
            mask = df_enhanced['Working_Age_Persons'] > 0
            df_enhanced['Dependency_Ratio'] = 0.0
            df_enhanced.loc[mask, 'Dependency_Ratio'] = (
                (df_enhanced.loc[mask, r18_col] + df_enhanced.loc[mask, r65_col]) /
                df_enhanced.loc[mask, 'Working_Age_Persons']
            )
            created.extend(['Working_Age_Persons', 'Dependency_Ratio'])

            # High dependency indicator
            df_enhanced['High_Dependency_Household'] = (df_enhanced['Dependency_Ratio'] > 1.0).fillna(False).astype(int)
            created.append('High_Dependency_Household')

            logger.debug(f"Created dependency ratio features")

        metadata = {
            'features': created,
            'transform': 'Dependency ratio features created' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_snap_eligibility_proxy(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create SNAP eligibility proxy based on income and household size"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        income_col = 'Household_Income'
        np_col = 'Number_of_Persons'
        snap_col = 'Food_Stamp_SNAP'

        if income_col in df.columns and np_col in df.columns:
            # Calculate FPL threshold for each household
            df_enhanced['FPL_Threshold'] = (
                HouseholdCompositionFeatureCreator.FPL_BASE +
                (df_enhanced[np_col] - 1) * HouseholdCompositionFeatureCreator.FPL_INCREMENT
            )
            created.append('FPL_Threshold')

            # Income to FPL ratio
            mask = df_enhanced['FPL_Threshold'] > 0
            df_enhanced['Income_to_FPL_Ratio'] = np.nan
            df_enhanced.loc[mask, 'Income_to_FPL_Ratio'] = (
                df_enhanced.loc[mask, income_col] / df_enhanced.loc[mask, 'FPL_Threshold']
            )
            created.append('Income_to_FPL_Ratio')

            # SNAP eligibility proxy (income < 130% FPL)
            df_enhanced['SNAP_Eligible_Proxy'] = (df_enhanced['Income_to_FPL_Ratio'] < 1.30).fillna(False).astype(int)
            created.append('SNAP_Eligible_Proxy')

            # SNAP takeup gap (eligible but not receiving)
            if snap_col in df.columns:
                # SNAP col: 1 = received, 2 = did not receive
                eligible_not_receiving = (
                    (df_enhanced['SNAP_Eligible_Proxy'] == 1) &
                    (df_enhanced[snap_col] == 2)
                )
                df_enhanced['SNAP_Takeup_Gap'] = eligible_not_receiving.fillna(False).astype(int)
                created.append('SNAP_Takeup_Gap')

            logger.debug(f"Created SNAP eligibility proxy features")

        metadata = {
            'features': created,
            'transform': 'SNAP eligibility proxy features created' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_workers_ratio(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create workers-related household features"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        wif_col = 'Workers_In_Family'
        np_col = 'Number_of_Persons'

        if wif_col in df.columns and np_col in df.columns:
            # Workers per person ratio
            mask = df_enhanced[np_col] > 0
            df_enhanced['Workers_Per_Person'] = 0.0
            df_enhanced.loc[mask, 'Workers_Per_Person'] = (
                df_enhanced.loc[mask, wif_col] / df_enhanced.loc[mask, np_col]
            )
            created.append('Workers_Per_Person')

            # No-worker household indicator
            df_enhanced['No_Worker_Household'] = (df_enhanced[wif_col] == 0).fillna(False).astype(int)
            created.append('No_Worker_Household')

            logger.debug(f"Created workers ratio features")

        metadata = {
            'features': created,
            'transform': 'Workers ratio features created' if created else ''
        }
        return df_enhanced, metadata
