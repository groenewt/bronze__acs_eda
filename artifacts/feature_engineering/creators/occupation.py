"""
Occupation and Industry Feature Creator Module

Provides domain-specific occupation and industry features for census analysis,
including industry sector mapping and occupation skill level classification.
"""
import pandas as pd
from typing import Dict, Tuple
from logging_config import get_logger


class OccupationIndustryFeatureCreator:
    """Domain-specific occupation and industry features for census analysis"""

    # Industry sector groupings (based on NAICS-based INDP codes)
    INDUSTRY_SECTORS = {
        'Agriculture': range(170, 291),
        'Mining': range(370, 491),
        'Construction': range(770, 771),
        'Manufacturing': range(1070, 3991),
        'Wholesale': range(4070, 4591),
        'Retail': range(4670, 5791),
        'Transportation': range(6070, 6391),
        'Information': range(6470, 6781),
        'Finance': range(6870, 7191),
        'Professional': range(7270, 7791),
        'Education_Health': range(7860, 8471),
        'Entertainment': range(8560, 8691),
        'Other_Services': range(8770, 9091),
        'Public_Admin': range(9170, 9291),
    }

    # SOC-based occupation skill levels
    HIGH_SKILL_OCCS = range(10, 3000)  # Management through Science
    MEDIUM_SKILL_OCCS = range(3000, 6000)  # Healthcare Support through Personal Care
    LOW_SKILL_OCCS = range(6000, 10000)  # Sales through Transportation

    @staticmethod
    def create_industry_sector(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Map detailed industry codes to broad sectors for ALL available columns"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        industry_cols = ['Industry_Code_2007', 'Industry_Code_2002', 'Industry_Code', 'INDP']
        available = [c for c in industry_cols if c in df.columns]

        def map_to_sector(code):
            if pd.isna(code) or code == '' or str(code).strip() == '':
                return 'Not_In_Labor_Force'
            code_str = str(code).strip()
            # Handle ACS special codes (N=not applicable, b=blank)
            if code_str in ('N', 'b', 'bb', 'bbb', 'bbbb'):
                return 'Not_In_Labor_Force'
            try:
                code_int = int(float(code_str))  # Handle "170.0" string floats
            except (ValueError, TypeError):
                return 'Unknown'
            if code_int == 0:
                return 'Not_In_Labor_Force'
            for sector, code_range in OccupationIndustryFeatureCreator.INDUSTRY_SECTORS.items():
                if code_int in code_range:
                    return sector
            return 'Other'

        for ind_col in available:
            # Determine suffix based on column name
            if ind_col == 'Industry_Code':
                suffix = ''
            elif ind_col == 'INDP':
                suffix = 'INDP'
            else:
                suffix = ind_col.replace('Industry_Code_', '')
            col_name = f'Industry_Sector_{suffix}' if suffix else 'Industry_Sector'
            df_enhanced[col_name] = df_enhanced[ind_col].apply(map_to_sector)
            created.append(col_name)
            logger.debug(f"Created {col_name} from {ind_col}")

        # Binary sector indicators (use first available)
        if available:
            first_sector_col = created[0]
            df_enhanced['Is_Goods_Producing'] = df_enhanced[first_sector_col].isin(
                ['Agriculture', 'Mining', 'Construction', 'Manufacturing']
            ).fillna(False).astype(int)
            df_enhanced['Is_Service_Sector'] = (~df_enhanced[first_sector_col].isin(
                ['Agriculture', 'Mining', 'Construction', 'Manufacturing', 'Unknown', 'Other']
            )).fillna(False).astype(int)
            created.extend(['Is_Goods_Producing', 'Is_Service_Sector'])

        metadata = {
            'features': created,
            'transform': f'Industry codes mapped to sectors from {len(available)} columns' if created else ''
        }
        return df_enhanced, metadata

    @staticmethod
    def create_occupation_skill_level(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Classify occupation by skill level for ALL available columns"""
        logger = get_logger("feature_engineering")

        df_enhanced = df.copy()
        created = []

        occ_cols = ['Occupation_Code_2010', 'Occupation_Code_2002', 'Occupation_Code', 'OCCP']
        available = [c for c in occ_cols if c in df.columns]

        def get_skill_level(code):
            if pd.isna(code) or code == '' or str(code).strip() == '':
                return 'Not_In_Labor_Force'
            code_str = str(code).strip()
            # Handle ACS special codes (N=not applicable, b=blank)
            if code_str in ('N', 'b', 'bb', 'bbb', 'bbbb'):
                return 'Not_In_Labor_Force'
            try:
                code_int = int(float(code_str))  # Handle "170.0" string floats
            except (ValueError, TypeError):
                return 'Unknown'
            if code_int == 0:
                return 'Not_In_Labor_Force'
            if code_int in OccupationIndustryFeatureCreator.HIGH_SKILL_OCCS:
                return 'High'
            elif code_int in OccupationIndustryFeatureCreator.MEDIUM_SKILL_OCCS:
                return 'Medium'
            elif code_int in OccupationIndustryFeatureCreator.LOW_SKILL_OCCS:
                return 'Low'
            return 'Unknown'

        for occ_col in available:
            # Determine suffix based on column name
            if occ_col == 'Occupation_Code':
                suffix = ''
            elif occ_col == 'OCCP':
                suffix = 'OCCP'
            else:
                suffix = occ_col.replace('Occupation_Code_', '')
            col_name = f'Occupation_Skill_Level_{suffix}' if suffix else 'Occupation_Skill_Level'
            df_enhanced[col_name] = df_enhanced[occ_col].apply(get_skill_level)
            created.append(col_name)
            logger.debug(f"Created {col_name} from {occ_col}")

        # Numeric skill level (use first available)
        if available:
            first_skill_col = created[0]
            skill_map = {'High': 3, 'Medium': 2, 'Low': 1, 'Unknown': 0}
            df_enhanced['Skill_Level_Numeric'] = df_enhanced[first_skill_col].map(skill_map)
            created.append('Skill_Level_Numeric')

        metadata = {
            'features': created,
            'transform': f'Occupation skill levels from {len(available)} columns' if created else ''
        }
        return df_enhanced, metadata
