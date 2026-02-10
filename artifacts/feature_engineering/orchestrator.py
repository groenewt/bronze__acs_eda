"""Feature Engineering Orchestrator - coordinates all feature creation."""
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from config import Config
from logging_config import get_logger

logger = get_logger("feature_engineering")

from .cleaning import SmartDataCleaner
from .creators import (
    FeatureCreator, EconomicFeatureCreator, DisabilityFeatureCreator,
    HealthInsuranceFeatureCreator, OccupationIndustryFeatureCreator,
    EducationFieldFeatureCreator, HouseholdCompositionFeatureCreator
)
from .selection import FeatureSelector, AdvancedFeatureSelector
from .transformation import FeatureTransformer, CategoricalEncoder, DimensionalityReducer


class FeatureEngineer:
    """Main orchestrator for feature engineering operations.

    Args:
        df: Input DataFrame
        config: Configuration object
        survey_type: Type of survey ('POPULATION' or 'HOUSING')
        copy: If True (default), creates a defensive copy of the DataFrame.
              Set to False to avoid memory overhead when the original
              DataFrame is not needed after feature engineering.
    """

    def __init__(self, df: pd.DataFrame, config: Config = None, survey_type: str = "", copy: bool = True):
        self.df = df.copy() if copy else df
        self.config = config
        self.survey_type = survey_type.upper() if survey_type else ""
        self.metadata = {'created_features': [], 'transforms_applied': []}

    def create_all_features(self) -> Tuple[pd.DataFrame, Dict]:
        """Run all feature creators and return enhanced dataframe."""
        logger.info("[FE] Creating all engineered features...")

        # Basic features
        self.df, meta = FeatureCreator.create_income_features(self.df)
        self._track_metadata(meta)

        self.df, meta = FeatureCreator.create_housing_features(self.df)
        self._track_metadata(meta)

        self.df, meta = FeatureCreator.create_age_groups(self.df)
        self._track_metadata(meta)

        self.df, meta = FeatureCreator.create_temporal_features(self.df)
        self._track_metadata(meta)

        # Economic features
        self.df = EconomicFeatureCreator.create_affordability_indices(self.df)
        self.df = EconomicFeatureCreator.create_poverty_intensity(
            self.df, survey_type=self.survey_type
        )
        self.df = EconomicFeatureCreator.create_housing_quality_index(
            self.df, survey_type=self.survey_type
        )

        # Domain-specific features based on survey type
        if self.survey_type == "POPULATION":
            self._create_population_features()
        elif self.survey_type == "HOUSING":
            self._create_housing_specific_features()

        logger.info(f"[FE] Feature engineering complete. Created {len(self.metadata['created_features'])} features.")
        return self.df, self.metadata

    def _create_population_features(self):
        """Create population survey-specific features."""
        self.df, meta = DisabilityFeatureCreator.create_disability_severity_score(self.df)
        self._track_metadata(meta)

        self.df, meta = DisabilityFeatureCreator.create_disability_employment_features(self.df)
        self._track_metadata(meta)

        self.df, meta = HealthInsuranceFeatureCreator.create_coverage_type_features(self.df)
        self._track_metadata(meta)

        self.df, meta = HealthInsuranceFeatureCreator.create_uninsured_features(self.df)
        self._track_metadata(meta)

        self.df, meta = OccupationIndustryFeatureCreator.create_industry_sector(self.df)
        self._track_metadata(meta)

        self.df, meta = OccupationIndustryFeatureCreator.create_occupation_skill_level(self.df)
        self._track_metadata(meta)

        self.df, meta = EducationFieldFeatureCreator.create_stem_category(self.df)
        self._track_metadata(meta)

    def _create_housing_specific_features(self):
        """Create housing survey-specific features."""
        self.df, meta = HouseholdCompositionFeatureCreator.create_dependency_ratio(self.df)
        self._track_metadata(meta)

        self.df, meta = HouseholdCompositionFeatureCreator.create_snap_eligibility_proxy(self.df)
        self._track_metadata(meta)

        self.df, meta = HouseholdCompositionFeatureCreator.create_workers_ratio(self.df)
        self._track_metadata(meta)

    def _track_metadata(self, meta: Dict):
        """Track created features from metadata."""
        if meta and meta.get('features'):
            self.metadata['created_features'].extend(meta['features'])
        if meta and meta.get('transform'):
            self.metadata['transforms_applied'].append(meta['transform'])

    def clean_data(self, strategy: str = 'median') -> pd.DataFrame:
        """Apply data cleaning."""
        self.df = SmartDataCleaner.impute_missing(self.df, strategy=strategy)
        return self.df

    def select_features(self, target_col: str, method: str = 'correlation',
                       **kwargs) -> List[str]:
        """Select features using specified method."""
        if method == 'correlation':
            return FeatureSelector.select_by_correlation(self.df, target_col, **kwargs)
        elif method == 'mutual_info':
            return FeatureSelector.select_by_mutual_information(self.df, target_col, **kwargs)
        elif method == 'rfe':
            return AdvancedFeatureSelector.select_by_rfe(self.df, target_col, **kwargs)
        elif method == 'permutation':
            return AdvancedFeatureSelector.select_by_permutation_importance(self.df, target_col, **kwargs)
        else:
            return FeatureSelector.select_by_variance(self.df, **kwargs)
