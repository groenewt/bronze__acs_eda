"""
Health Insurance Feature Creator Module

Provides domain-specific health insurance features for census analysis,
including coverage type features, uninsured indicators, and coverage
comprehensiveness scores.
"""
import pandas as pd
from typing import Dict, Tuple, List
from logging_config import get_logger


class HealthInsuranceFeatureCreator:
    """Domain-specific health insurance features for census analysis"""

    # Insurance type columns (value 1 = has coverage, 2 = no coverage)
    INSURANCE_TYPE_COLS = [
        'Health_Insurance_Employer', 'Health_Insurance_Direct',
        'Health_Insurance_Medicare', 'Health_Insurance_Medicaid',
        'Health_Insurance_Tricare', 'Health_Insurance_VA', 'Health_Insurance_IHS'
    ]

    PRIVATE_TYPES = ['Health_Insurance_Employer', 'Health_Insurance_Direct']
    PUBLIC_TYPES = ['Health_Insurance_Medicare', 'Health_Insurance_Medicaid',
                    'Health_Insurance_Tricare', 'Health_Insurance_VA', 'Health_Insurance_IHS']

    @staticmethod
    def create_coverage_type_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create health insurance coverage type features"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        available = [c for c in HealthInsuranceFeatureCreator.INSURANCE_TYPE_COLS if c in df.columns]

        if available:
            # Count coverage types (1 = has coverage)
            for col in available:
                df_enhanced[f'{col}_binary'] = (df_enhanced[col] == 1).fillna(False).astype(int)

            binary_cols = [f'{c}_binary' for c in available]
            df_enhanced['Insurance_Coverage_Count'] = df_enhanced[binary_cols].sum(axis=1)
            created.append('Insurance_Coverage_Count')

            # Count public vs private
            private_avail = [c for c in HealthInsuranceFeatureCreator.PRIVATE_TYPES if c in df.columns]
            public_avail = [c for c in HealthInsuranceFeatureCreator.PUBLIC_TYPES if c in df.columns]

            if private_avail:
                private_binary = [f'{c}_binary' for c in private_avail]
                df_enhanced['Private_Insurance_Count'] = df_enhanced[private_binary].sum(axis=1)
                created.append('Private_Insurance_Count')

            if public_avail:
                public_binary = [f'{c}_binary' for c in public_avail]
                df_enhanced['Public_Insurance_Count'] = df_enhanced[public_binary].sum(axis=1)
                created.append('Public_Insurance_Count')

            # Clean up temporary columns
            df_enhanced = df_enhanced.drop(columns=binary_cols)

            logger.debug(f"Created insurance coverage features: {created}")

        metadata = {
            'features': created,
            'transform': 'Insurance coverage type features created' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_uninsured_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create uninsured and coverage gap features"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        cov_col = 'Health_Insurance_Coverage'
        age_col = 'Age'
        income_col = 'Total_Person_Income'

        if cov_col in df.columns:
            # Uninsured indicator (2 = not covered)
            df_enhanced['Is_Uninsured'] = (df_enhanced[cov_col] == 2).fillna(False).astype(int)
            created.append('Is_Uninsured')

            # Vulnerable uninsured: working age, low income, no coverage
            if age_col in df.columns and income_col in df.columns:
                working_age = (df_enhanced[age_col] >= 18) & (df_enhanced[age_col] < 65)
                income_threshold = df_enhanced[income_col].quantile(0.25)
                low_income = df_enhanced[income_col] < income_threshold

                df_enhanced['Vulnerable_Uninsured'] = (
                    working_age & low_income & (df_enhanced[cov_col] == 2)
                ).fillna(False).astype(int)
                created.append('Vulnerable_Uninsured')

            logger.debug(f"Created uninsured features: {created}")

        metadata = {
            'features': created,
            'transform': 'Uninsured and vulnerability features created' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_coverage_comprehensiveness(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create composite coverage comprehensiveness score"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        # Weights for different insurance types
        weights = {
            'Health_Insurance_Employer': 1.0,  # Typically most comprehensive
            'Health_Insurance_Medicare': 0.9,
            'Health_Insurance_Medicaid': 0.8,
            'Health_Insurance_Direct': 0.7,
            'Health_Insurance_Tricare': 0.6,
            'Health_Insurance_VA': 0.6,
            'Health_Insurance_IHS': 0.5,
        }

        available = {k: v for k, v in weights.items() if k in df.columns}

        if available:
            df_enhanced['Coverage_Score'] = 0.0
            for col, weight in available.items():
                df_enhanced['Coverage_Score'] += (df_enhanced[col] == 1).astype(float) * weight

            created.append('Coverage_Score')
            logger.debug(f"Created coverage comprehensiveness score")

        metadata = {
            'features': created,
            'transform': 'Coverage comprehensiveness score created' if created else ''
        }
        return df_enhanced, metadata
