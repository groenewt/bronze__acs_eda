"""Main visualizer orchestrator that coordinates all visualization types"""
import pandas as pd
import numpy as np
import os
import gc
import matplotlib
import matplotlib.pyplot as plt
from config import Config
from exceptions import VisualizationError, PlotCreationError
from logging_config import get_logger

logger = get_logger("visualization.orchestrator")

from .base import BaseVisualizer, clear_viz_cache
from .formatting import tight_layout_safe
from .temporal import TemporalVisualizer
from .economic import EconomicVisualizer
from .correlation import CorrelationVisualizer
from .statistical import StatisticalVisualizer, AdvancedVisualizer
from .outlier import YoYChangeVisualizer, OutlierVisualizer
from .demographics import DemographicsVisualizer, RaceEthnicityVisualizer
from .housing import HousingCharacteristicsVisualizer, HouseholdCompositionVisualizer, CostBurdenVisualizer
from .transport import TransportationVisualizer
from .income import IncomeCompositionVisualizer
from .technology import TechnologyAdoptionVisualizer
from .interactions import MultiVariableVisualizer, EnhancedFeatureInteractionVisualizer
from .distributions import DistributionComparisonVisualizer

# Import new visualizers (conditional - may not exist yet)
try:
    from .inequality import InequalityVisualizer
    HAS_INEQUALITY = True
except ImportError:
    HAS_INEQUALITY = False

# New visualizers for extended column coverage
try:
    from .occupation_industry import OccupationIndustryVisualizer
    HAS_OCCUPATION = True
except ImportError:
    HAS_OCCUPATION = False

try:
    from .health_insurance import HealthInsuranceVisualizer
    HAS_HEALTH_INSURANCE = True
except ImportError:
    HAS_HEALTH_INSURANCE = False

try:
    from .disability import DisabilityVisualizer
    HAS_DISABILITY = True
except ImportError:
    HAS_DISABILITY = False

try:
    from .education_field import EducationFieldVisualizer
    HAS_EDUCATION_FIELD = True
except ImportError:
    HAS_EDUCATION_FIELD = False


class Visualizer:
    """Orchestrates all visualization types"""

    def __init__(self, df: pd.DataFrame, config: Config, survey_type: str = ""):
        self.config = config
        self.survey_type = survey_type.upper() if survey_type else ""
        # HOUSING: Apply memory-aware sampling at orchestrator level
        if self.survey_type == "HOUSING":
            from memory_utils import get_available_memory_gb
            available_gb = get_available_memory_gb()

            if available_gb > 16:
                # Plenty of RAM - no sampling needed
                self.df = df
            else:
                # Memory constrained - apply sampling based on available RAM
                target_cells = 5_000_000 if available_gb > 8 else 1_000_000
                sample_rows = min(len(df), int(target_cells / len(df.columns)))
                if len(df) > sample_rows:
                    logger.info(f"[MEMORY-ORCHESTRATOR] Sampling {len(df):,} → {sample_rows:,} rows (RAM: {available_gb:.1f}GB)")
                    self.df = df.sample(n=sample_rows, random_state=42)
                else:
                    self.df = df
        else:
            self.df = df
        os.makedirs(config.figure_dir, exist_ok=True)
        matplotlib.rcParams['figure.max_open_warning'] = 0
        plt.ioff()

    def _cleanup_memory(self):
        """Force memory cleanup between visualizers (≤10 lines)"""
        plt.close('all')
        gc.collect()
        # Periodically clear the cache to prevent unbounded growth
        # Clear every 5 visualizer calls (reduces memory footprint)
        if not hasattr(self, '_cleanup_count'):
            self._cleanup_count = 0
        self._cleanup_count += 1
        if self._cleanup_count % 5 == 0:
            clear_viz_cache()

    def create_all(self):
        logger.verbose("Creating temporal visualizations...")
        try:
            TemporalVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Temporal visualizations failed: {e}")
            self._cleanup_memory()

        logger.verbose("Creating economic visualizations...")
        try:
            EconomicVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Economic visualizations failed: {e}")
            self._cleanup_memory()

        logger.verbose("Creating correlation visualizations...")
        try:
            CorrelationVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Correlation visualizations failed: {e}")
            self._cleanup_memory()

        logger.verbose("Creating statistical distribution visualizations...")
        try:
            StatisticalVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Statistical visualizations failed: {e}")
            self._cleanup_memory()

        logger.verbose("Creating advanced visualizations (violin, ridge, radar)...")
        try:
            AdvancedVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Advanced visualizations failed: {e}")
            self._cleanup_memory()

        logger.verbose("Creating year-over-year change visualizations...")
        try:
            YoYChangeVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Year-over-year visualizations failed: {e}")
            self._cleanup_memory()

        logger.verbose("Creating outlier and anomaly detection visualizations...")
        try:
            OutlierVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Outlier visualizations failed: {e}")
            self._cleanup_memory()

        # Population-specific visualizers (only for POPULATION survey)
        if self.survey_type == "POPULATION":
            logger.verbose("Creating demographics visualizations...")
            try:
                DemographicsVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except Exception as e:
                logger.warning(f"Demographics visualizations failed: {e}")
                self._cleanup_memory()

            logger.verbose("Creating transportation visualizations...")
            try:
                TransportationVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except Exception as e:
                logger.warning(f"Transportation visualizations failed: {e}")
                self._cleanup_memory()

            logger.verbose("Creating income composition visualizations...")
            try:
                IncomeCompositionVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except Exception as e:
                logger.warning(f"Income composition visualizations failed: {e}")
                self._cleanup_memory()

        # Housing-specific visualizers (only for HOUSING survey)
        if self.survey_type == "HOUSING":
            logger.verbose("Creating housing characteristics visualizations...")
            try:
                HousingCharacteristicsVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except Exception as e:
                logger.warning(f"Housing characteristics visualizations failed: {e}")
                self._cleanup_memory()

            logger.verbose("Creating household composition visualizations...")
            try:
                HouseholdCompositionVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except Exception as e:
                logger.warning(f"Household composition visualizations failed: {e}")
                self._cleanup_memory()

            logger.verbose("Creating cost burden visualizations...")
            try:
                CostBurdenVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except Exception as e:
                logger.warning(f"Cost burden visualizations failed: {e}")
                self._cleanup_memory()

            logger.verbose("Creating technology adoption visualizations...")
            try:
                TechnologyAdoptionVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except Exception as e:
                logger.warning(f"Technology adoption visualizations failed: {e}")
                self._cleanup_memory()

        # Population-specific: Race & Ethnicity
        if self.survey_type == "POPULATION":
            logger.verbose("Creating race & ethnicity visualizations...")
            try:
                RaceEthnicityVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except Exception as e:
                logger.warning(f"Race & ethnicity visualizations failed: {e}")
                self._cleanup_memory()

        logger.verbose("Creating multi-variable interaction visualizations...")
        try:
            MultiVariableVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except (VisualizationError, PlotCreationError) as e:
            logger.warning(f"Multi-variable visualizations failed: {e}")
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Multi-variable visualizations failed unexpectedly: {e}")
            self._cleanup_memory()

        logger.verbose("Creating distribution comparison visualizations...")
        try:
            DistributionComparisonVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except (VisualizationError, PlotCreationError) as e:
            logger.warning(f"Distribution comparison visualizations failed: {e}")
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Distribution comparison visualizations failed unexpectedly: {e}")
            self._cleanup_memory()

        logger.verbose("Creating enhanced feature interaction visualizations...")
        try:
            EnhancedFeatureInteractionVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except (VisualizationError, PlotCreationError) as e:
            logger.warning(f"Enhanced feature interaction visualizations failed: {e}")
            self._cleanup_memory()
        except Exception as e:
            logger.warning(f"Enhanced feature interaction visualizations failed unexpectedly: {e}")
            self._cleanup_memory()

        # New inequality visualizations
        if HAS_INEQUALITY:
            logger.verbose("Creating inequality visualizations...")
            try:
                InequalityVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except (VisualizationError, PlotCreationError) as e:
                logger.warning(f"InequalityVisualizer failed: {e}")
                self._cleanup_memory()
            except Exception as e:
                logger.warning(f"InequalityVisualizer failed unexpectedly: {e}")
                self._cleanup_memory()

        # Population-specific extended column visualizers
        if self.survey_type == "POPULATION":
            if HAS_OCCUPATION:
                logger.verbose("Creating occupation/industry visualizations...")
                try:
                    OccupationIndustryVisualizer(self.df, self.config, self.survey_type).create_all()
                    self._cleanup_memory()
                except (VisualizationError, PlotCreationError) as e:
                    logger.warning(f"OccupationIndustryVisualizer failed: {e}")
                    self._cleanup_memory()
                except Exception as e:
                    logger.warning(f"OccupationIndustryVisualizer failed unexpectedly: {e}")
                    self._cleanup_memory()

            if HAS_HEALTH_INSURANCE:
                logger.verbose("Creating health insurance visualizations...")
                try:
                    HealthInsuranceVisualizer(self.df, self.config, self.survey_type).create_all()
                    self._cleanup_memory()
                except (VisualizationError, PlotCreationError) as e:
                    logger.warning(f"HealthInsuranceVisualizer failed: {e}")
                    self._cleanup_memory()
                except Exception as e:
                    logger.warning(f"HealthInsuranceVisualizer failed unexpectedly: {e}")
                    self._cleanup_memory()

            if HAS_DISABILITY:
                logger.verbose("Creating disability visualizations...")
                try:
                    DisabilityVisualizer(self.df, self.config, self.survey_type).create_all()
                    self._cleanup_memory()
                except (VisualizationError, PlotCreationError) as e:
                    logger.warning(f"DisabilityVisualizer failed: {e}")
                    self._cleanup_memory()
                except Exception as e:
                    logger.warning(f"DisabilityVisualizer failed unexpectedly: {e}")
                    self._cleanup_memory()

            if HAS_EDUCATION_FIELD:
                logger.verbose("Creating education field visualizations...")
                try:
                    EducationFieldVisualizer(self.df, self.config, self.survey_type).create_all()
                    self._cleanup_memory()
                except (VisualizationError, PlotCreationError) as e:
                    logger.warning(f"EducationFieldVisualizer failed: {e}")
                    self._cleanup_memory()
                except Exception as e:
                    logger.warning(f"EducationFieldVisualizer failed unexpectedly: {e}")
                    self._cleanup_memory()

        logger.verbose("All visualizations complete!")
        self._cleanup_memory()  # Final cleanup

        logger.verbose("Creating missing data analysis...")
        try:
            self._missing_data_analysis()
        except Exception as e:
            logger.warning(f"Missing data analysis failed: {e}")

        # Force cleanup to prevent memory leaks
        plt.close('all')
        gc.collect()

    def _missing_data_analysis(self):
        plt.figure(figsize=(12, 8))
        missing_pct = self.df.isna().sum() / len(self.df) * 100
        top_missing = missing_pct.nlargest(15)
        plt.barh(range(len(top_missing)), top_missing.values, color='coral')
        plt.yticks(range(len(top_missing)), top_missing.index, fontsize=9)
        plt.xlabel('Missing %')
        plt.title('Top 15 Variables with Missing Data', fontweight='bold', fontsize=14)
        tight_layout_safe()
        self._save_fig('missing_data.png')

    def _save_fig(self, filename: str):
        if self.survey_type:
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{self.survey_type}.{ext}"
        path = f"{self.config.figure_dir}/{filename}"
        plt.savefig(path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close()
