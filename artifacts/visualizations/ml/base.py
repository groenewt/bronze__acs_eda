"""Base ML Visualizer"""
import os
import matplotlib.pyplot as plt
from config import Config
from visual_registry import register_visual


class BaseMLVisualizer:
    def __init__(self, config: Config, survey_type: str = ""):
        self.config = config
        self.survey_type = survey_type.upper() if survey_type else ""
        self.current_target = None

    def _dir(self, model_type: str, model_name: str = None) -> str:
        supervised = ['regression', 'classification', 'timeseries', 'time_series']
        if self.current_target and model_type in supervised:
            path = os.path.join(self.config.figure_dir, 'ml', model_type, self.current_target, model_name) if model_name else os.path.join(self.config.figure_dir, 'ml', model_type, self.current_target)
        else:
            path = os.path.join(self.config.figure_dir, 'ml', model_type, model_name) if model_name else os.path.join(self.config.figure_dir, 'ml', model_type)
        os.makedirs(path, exist_ok=True)
        return path

    def _save(self, filename: str, model_type: str, model_name: str = None):
        if self.survey_type:
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{self.survey_type}.{ext}"
        path = os.path.join(self._dir(model_type, model_name), filename)
        plt.savefig(path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close()
        self._register_visual(path, model_type, filename, model_name)

    def _register_visual(self, path, model_type, filename, model_name):
        try:
            register_visual(path=path, visual_type=model_type, title=filename.replace('_', ' ').replace('.png', ''),
                          category='ml', model_name=model_name, targets=[self.current_target] if self.current_target else [])
        except Exception as e:
            print(f"[WARNING] Failed to register: {e}")
