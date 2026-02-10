"""
Disability Feature Creator Module

Provides domain-specific disability features for census analysis,
including disability severity scores, disability-employment interactions,
and disability-age features.
"""
import pandas as pd
from typing import Dict, Tuple, List
from logging_config import get_logger


class DisabilityFeatureCreator:
    """Domain-specific disability features for census analysis"""

    # Disability difficulty columns (value 1 = has difficulty, 2 = no difficulty)
    DIFFICULTY_COLS = [
        'Hearing_Difficulty', 'Vision_Difficulty', 'Cognitive_Difficulty',
        'Ambulatory_Difficulty', 'Self_Care_Difficulty', 'Independent_Living_Difficulty'
    ]

    @staticmethod
    def create_disability_severity_score(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Create disability severity score (count of difficulty types).
        Score ranges from 0 (no disabilities) to 6 (all disability types).
        """
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        available = [c for c in DisabilityFeatureCreator.DIFFICULTY_COLS if c in df.columns]

        if available:
            # For each difficulty column, 1 means "has difficulty"
            for col in available:
                df_enhanced[f'{col}_binary'] = (df_enhanced[col] == 1).fillna(False).astype(int)

            binary_cols = [f'{c}_binary' for c in available]
            df_enhanced['Disability_Count'] = df_enhanced[binary_cols].sum(axis=1)
            created.append('Disability_Count')

            # Create severity category
            df_enhanced['Disability_Severity'] = pd.cut(
                df_enhanced['Disability_Count'],
                bins=[-1, 0, 1, 2, 6],
                labels=['None', 'Single', 'Multiple', 'Severe']
            )
            created.append('Disability_Severity')

            # Multiple disability indicator
            df_enhanced['Has_Multiple_Disabilities'] = (df_enhanced['Disability_Count'] >= 2).fillna(False).astype(int)
            created.append('Has_Multiple_Disabilities')

            # Clean up temporary binary columns
            df_enhanced = df_enhanced.drop(columns=binary_cols)

            logger.debug(f"Created disability severity features: {created}")

        metadata = {
            'features': created,
            'transform': 'Disability count and severity computed' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_disability_employment_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create disability-employment interaction features"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        dis_col = 'Disability_Status'
        emp_col = 'Employment_Status_Recode'

        if dis_col in df.columns:
            # Binary disability indicator (1 = has disability, 2 = no disability)
            df_enhanced['Has_Disability'] = (df_enhanced[dis_col] == 1).fillna(False).astype(int)
            created.append('Has_Disability')

            if emp_col in df.columns:
                # ESR codes: 1,2 = employed; 3 = unemployed; 4,5,6 = not in labor force
                df_enhanced['Is_Employed'] = df_enhanced[emp_col].isin([1, 2]).fillna(False).astype(int)
                created.append('Is_Employed')

                # Interaction: disabled and employed
                df_enhanced['Disability_Employment_Interaction'] = (
                    df_enhanced['Has_Disability'] * df_enhanced['Is_Employed']
                )
                created.append('Disability_Employment_Interaction')

            logger.debug(f"Created disability-employment features: {created}")

        metadata = {
            'features': created,
            'transform': 'Disability-employment interactions created' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_disability_age_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create disability by age group interaction features"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        dis_col = 'Disability_Status'
        age_col = 'Age'

        if dis_col in df.columns and age_col in df.columns:
            has_dis = (df_enhanced[dis_col] == 1).fillna(False)

            # Disability by age group
            df_enhanced['Disability_Youth'] = (has_dis & (df_enhanced[age_col] < 18)).fillna(False).astype(int)
            df_enhanced['Disability_Working_Age'] = (
                has_dis & (df_enhanced[age_col] >= 18) & (df_enhanced[age_col] < 65)
            ).fillna(False).astype(int)
            df_enhanced['Disability_Senior'] = (has_dis & (df_enhanced[age_col] >= 65)).fillna(False).astype(int)

            created.extend(['Disability_Youth', 'Disability_Working_Age', 'Disability_Senior'])
            logger.debug(f"Created disability-age features: {created}")

        metadata = {
            'features': created,
            'transform': 'Disability by age group features created' if created else ''
        }
        return df_enhanced, metadata
