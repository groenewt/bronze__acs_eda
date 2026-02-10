"""
Education Field Feature Creator Module

Provides domain-specific education field features for census analysis,
including STEM field categorization and field income premium calculations.
"""
import pandas as pd
from typing import Dict, Tuple, List
from logging_config import get_logger


class EducationFieldFeatureCreator:
    """Domain-specific education field features for census analysis"""

    # STEM field codes (FOD1P ranges)
    STEM_RANGES = [
        (2100, 2199),  # Computer Science
        (2400, 2599),  # Engineering
        (3600, 3699),  # Biology
        (3700, 3799),  # Mathematics
        (4000, 4099),  # Physical Sciences
        (5000, 5099),  # Physical Sciences continued
    ]

    STEM_RELATED_RANGES = [
        (1300, 1399),  # Environmental Science
        (4100, 4199),  # Psychology
        (5500, 5599),  # Social Sciences
        (6000, 6199),  # Medical/Health
    ]

    @staticmethod
    def create_stem_category(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Create STEM field category features"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        fod_col = 'Field_Of_Degree_1' if 'Field_Of_Degree_1' in df.columns else 'FOD1P'

        if fod_col in df.columns:
            def get_stem_category(code):
                if pd.isna(code):
                    return 'No_Degree'
                try:
                    code = int(code)
                except (ValueError, TypeError):
                    return 'Unknown'

                for start, end in EducationFieldFeatureCreator.STEM_RANGES:
                    if start <= code <= end:
                        return 'STEM'
                for start, end in EducationFieldFeatureCreator.STEM_RELATED_RANGES:
                    if start <= code <= end:
                        return 'STEM_Related'
                return 'Non_STEM'

            df_enhanced['STEM_Category'] = df_enhanced[fod_col].apply(get_stem_category)
            created.append('STEM_Category')

            # Binary STEM indicator
            df_enhanced['Is_STEM'] = (df_enhanced['STEM_Category'] == 'STEM').fillna(False).astype(int)
            df_enhanced['Is_STEM_Related'] = (df_enhanced['STEM_Category'] == 'STEM_Related').fillna(False).astype(int)
            created.extend(['Is_STEM', 'Is_STEM_Related'])

            logger.debug(f"Created STEM category features from {fod_col}")

        metadata = {
            'features': created,
            'transform': 'STEM field categories created' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_field_income_premium(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Calculate income premium for each field of degree"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        fod_col = 'Field_Of_Degree_1' if 'Field_Of_Degree_1' in df.columns else 'FOD1P'
        income_col = 'Total_Person_Income'

        if fod_col in df.columns and income_col in df.columns:
            # Calculate median income by field (for positive incomes)
            df_positive = df_enhanced[df_enhanced[income_col] > 0]
            overall_median = df_positive[income_col].median()

            if overall_median > 0:
                field_medians = df_positive.groupby(fod_col)[income_col].median()
                premium_map = ((field_medians - overall_median) / overall_median * 100).to_dict()
                df_enhanced['Field_Income_Premium'] = df_enhanced[fod_col].map(premium_map)
                created.append('Field_Income_Premium')

                logger.debug("Created field income premium feature")

        metadata = {
            'features': created,
            'transform': 'Field-based income premium calculated' if created else ''
        }
        return df_enhanced, metadata
