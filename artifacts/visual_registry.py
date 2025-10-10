"""
Visual Registry System
Centralized tracking and retrieval of all generated visualizations
"""
import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from exceptions import (VisualRegistrationError, VisualNotFoundError,
                        InvalidVisualMetadataError)


# ============================================================================
# VISUAL METADATA
# ============================================================================

@dataclass
class VisualMetadata:
    """Metadata for a single visualization"""
    path: str
    visual_type: str
    title: str
    category: str = None
    features: List[str] = field(default_factory=list)
    targets: List[str] = field(default_factory=list)
    model_name: str = None
    task_name: str = None
    subdirectory: str = None

    def matches(self, **filters) -> bool:
        """Check if metadata matches filters (≤10 lines)"""
        for key, value in filters.items():
            if not hasattr(self, key):
                continue
            attr_val = getattr(self, key)
            if value is None:
                continue
            if isinstance(value, list):
                if not any(v in attr_val for v in value):
                    return False
            elif attr_val != value:
                return False
        return True


# ============================================================================
# VISUAL REGISTRY
# ============================================================================

class VisualRegistry:
    """Centralized registry for all visualizations"""

    _instance = None

    def __new__(cls):
        """Singleton pattern (≤10 lines)"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize registry once (≤10 lines)"""
        if not self._initialized:
            self.visuals: List[VisualMetadata] = []
            self.output_dir: str = None
            self._initialized = True

    def reset(self):
        """Reset registry (≤10 lines)"""
        self.visuals = []
        self.output_dir = None

    def set_output_dir(self, output_dir: str):
        """Set output directory (≤10 lines)"""
        self.output_dir = output_dir

    def register(self, visual: VisualMetadata):
        """Register visualization (≤10 lines)"""
        try:
            if not isinstance(visual, VisualMetadata):
                raise InvalidVisualMetadataError('visual', type(visual),
                                                 'Must be VisualMetadata instance')
            self.visuals.append(visual)
        except Exception as e:
            raise VisualRegistrationError(visual.path, str(e))

    def register_from_dict(self, data: Dict):
        """Register from dictionary (≤10 lines)"""
        try:
            visual = VisualMetadata(**data)
            self.register(visual)
        except Exception as e:
            raise VisualRegistrationError(str(data.get('path')), str(e))

    def query(self, **filters) -> List[VisualMetadata]:
        """Query visuals by filters (≤10 lines)"""
        results = [v for v in self.visuals if v.matches(**filters)]
        return results

    def get_by_type(self, visual_type: str) -> List[VisualMetadata]:
        """Get all visuals of specific type (≤10 lines)"""
        return self.query(visual_type=visual_type)

    def get_by_category(self, category: str) -> List[VisualMetadata]:
        """Get all visuals in category (≤10 lines)"""
        return self.query(category=category)

    def get_by_target(self, target: str) -> List[VisualMetadata]:
        """Get all visuals for specific target (≤10 lines)"""
        return [v for v in self.visuals if target in v.targets]

    def get_by_subdirectory(self, subdir: str) -> List[VisualMetadata]:
        """Get all visuals in subdirectory (≤10 lines)"""
        return self.query(subdirectory=subdir)

    def get_ml_visuals(self) -> List[VisualMetadata]:
        """Get all ML visualizations (≤10 lines)"""
        ml_types = ['regression', 'clustering', 'time_series', 'deep_learning']
        return [v for v in self.visuals if v.visual_type in ml_types]

    def get_all(self) -> List[VisualMetadata]:
        """Get all registered visuals (≤10 lines)"""
        return self.visuals.copy()

    def get_relative_path(self, visual: VisualMetadata) -> str:
        """Get relative path from output dir (≤10 lines)"""
        if self.output_dir:
            try:
                return os.path.relpath(visual.path, self.output_dir)
            except ValueError:
                return visual.path
        return visual.path

    def to_markdown_links(self, visuals: List[VisualMetadata]) -> List[str]:
        """Convert visuals to markdown links (≤10 lines)"""
        links = []
        for v in visuals:
            rel_path = self.get_relative_path(v)
            links.append(f"![{v.title}]({rel_path})")
        return links

    def save_to_json(self, filepath: str):
        """Save registry to JSON (≤10 lines)"""
        try:
            data = [asdict(v) for v in self.visuals]
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise VisualRegistrationError(filepath, f"Failed to save: {e}")

    def load_from_json(self, filepath: str):
        """Load registry from JSON (≤10 lines)"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.visuals = [VisualMetadata(**item) for item in data]
        except Exception as e:
            raise VisualRegistrationError(filepath, f"Failed to load: {e}")

    def count_by_type(self) -> Dict[str, int]:
        """Count visuals by type (≤10 lines)"""
        counts = {}
        for v in self.visuals:
            counts[v.visual_type] = counts.get(v.visual_type, 0) + 1
        return counts

    def count_by_category(self) -> Dict[str, int]:
        """Count visuals by category (≤10 lines)"""
        counts = {}
        for v in self.visuals:
            cat = v.category or 'uncategorized'
            counts[cat] = counts.get(cat, 0) + 1
        return counts


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_visual_metadata(path: str, visual_type: str, title: str,
                          **kwargs) -> VisualMetadata:
    """Factory function for VisualMetadata (≤10 lines)"""
    return VisualMetadata(
        path=path,
        visual_type=visual_type,
        title=title,
        category=kwargs.get('category'),
        features=kwargs.get('features', []),
        targets=kwargs.get('targets', []),
        model_name=kwargs.get('model_name'),
        task_name=kwargs.get('task_name'),
        subdirectory=kwargs.get('subdirectory')
    )


def get_registry() -> VisualRegistry:
    """Get singleton registry instance (≤10 lines)"""
    return VisualRegistry()


def register_visual(path: str, visual_type: str, title: str, **kwargs):
    """Convenience function to register visual (≤10 lines)"""
    registry = get_registry()
    metadata = create_visual_metadata(path, visual_type, title, **kwargs)
    registry.register(metadata)
