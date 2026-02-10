"""
Feature Transformation Subpackage
Provides transformation, encoding, and dimensionality reduction capabilities
"""
from .transformers import FeatureTransformer
from .encoders import CategoricalEncoder
from .dimensionality import DimensionalityReducer

__all__ = ['FeatureTransformer', 'CategoricalEncoder', 'DimensionalityReducer']
