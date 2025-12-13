"""Main visualizer orchestrator that coordinates all visualization types"""
import pandas as pd
import numpy as np
import os
import gc
import matplotlib
import matplotlib.pyplot as plt
from config import Config
from exceptions import VisualizationError, PlotCreationError

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
                    print(f"[MEMORY-ORCHESTRATOR] Sampling {len(df):,} → {sample_rows:,} rows (RAM: {available_gb:.1f}GB)")
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
        print("[VERBOSE] Creating temporal visualizations...")
        try:
            TemporalVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Temporal visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating economic visualizations...")
        try:
            EconomicVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Economic visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating correlation visualizations...")
        try:
            CorrelationVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Correlation visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating statistical distribution visualizations...")
        try:
            StatisticalVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Statistical visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating advanced visualizations (violin, ridge, radar)...")
        try:
            AdvancedVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Advanced visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating year-over-year change visualizations...")
        try:
            YoYChangeVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Year-over-year visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating outlier and anomaly detection visualizations...")
        try:
            OutlierVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Outlier visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating demographics visualizations...")
        try:
            DemographicsVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Demographics visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating transportation visualizations...")
        try:
            TransportationVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Transportation visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating income composition visualizations...")
        try:
            IncomeCompositionVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Income composition visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating housing characteristics visualizations...")
        try:
            HousingCharacteristicsVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Housing characteristics visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating household composition visualizations...")
        try:
            HouseholdCompositionVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Household composition visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating technology adoption visualizations...")
        try:
            TechnologyAdoptionVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Technology adoption visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating cost burden visualizations...")
        try:
            CostBurdenVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Cost burden visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating race & ethnicity visualizations...")
        try:
            RaceEthnicityVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Race & ethnicity visualizations failed: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating multi-variable interaction visualizations...")
        try:
            MultiVariableVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except (VisualizationError, PlotCreationError) as e:
            print(f"[WARNING] Multi-variable visualizations failed: {e}")
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Multi-variable visualizations failed unexpectedly: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating distribution comparison visualizations...")
        try:
            DistributionComparisonVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except (VisualizationError, PlotCreationError) as e:
            print(f"[WARNING] Distribution comparison visualizations failed: {e}")
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Distribution comparison visualizations failed unexpectedly: {e}")
            self._cleanup_memory()

        print("[VERBOSE] Creating enhanced feature interaction visualizations...")
        try:
            EnhancedFeatureInteractionVisualizer(self.df, self.config, self.survey_type).create_all()
            self._cleanup_memory()
        except (VisualizationError, PlotCreationError) as e:
            print(f"[WARNING] Enhanced feature interaction visualizations failed: {e}")
            self._cleanup_memory()
        except Exception as e:
            print(f"[WARNING] Enhanced feature interaction visualizations failed unexpectedly: {e}")
            self._cleanup_memory()

        # New inequality visualizations
        if HAS_INEQUALITY:
            print("[VERBOSE] Creating inequality visualizations...")
            try:
                InequalityVisualizer(self.df, self.config, self.survey_type).create_all()
                self._cleanup_memory()
            except (VisualizationError, PlotCreationError) as e:
                print(f"[VIZ-WARNING] InequalityVisualizer failed: {e}")
                self._cleanup_memory()
            except Exception as e:
                print(f"[VIZ-WARNING] InequalityVisualizer failed unexpectedly: {e}")
                self._cleanup_memory()

        print("[VERBOSE] All visualizations complete!")
        self._cleanup_memory()  # Final cleanup

        print("[VERBOSE] Creating missing data analysis...")
        try:
            self._missing_data_analysis()
        except Exception as e:
            print(f"[WARNING] Missing data analysis failed: {e}")

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
