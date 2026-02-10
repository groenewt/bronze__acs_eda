"""
Classification Models Module
Provides classification modeling with multiple algorithms
"""
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')
warnings.filterwarnings('ignore', message='.*parallel.*')
warnings.filterwarnings('ignore', message='.*delayed.*')

import pandas as pd
import numpy as np
from typing import Dict, List
from .base import BaseMLModel, ModelResults, SKLEARN_AVAILABLE

try:
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
                                  AdaBoostClassifier, ExtraTreesClassifier,
                                  BaggingClassifier)
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                                 f1_score)
except ImportError:
    pass  # SKLEARN_AVAILABLE flag from base handles this


class ClassificationModeler(BaseMLModel):
    """Handles classification modeling with multiple algorithms"""

    def __init__(self, random_state: int = 42):
        super().__init__(random_state)
        self.models = {
            'logistic': LogisticRegression(random_state=random_state, max_iter=1000),
            'decision_tree': DecisionTreeClassifier(random_state=random_state),
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=random_state, n_jobs=-1),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=random_state),
            'adaboost': AdaBoostClassifier(n_estimators=100, random_state=random_state),
            'extratrees': ExtraTreesClassifier(n_estimators=100, random_state=random_state, n_jobs=-1),
            'svc': SVC(kernel='rbf', random_state=random_state),
            'knn': KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
            'gaussian_nb': GaussianNB(),
            'multinomial_nb': MultinomialNB(),
            'bernoulli_nb': BernoulliNB(),
            'mlp': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=random_state),
            'bagging': BaggingClassifier(n_estimators=100, random_state=random_state, n_jobs=-1)
        }

    def train_model(self, X: pd.DataFrame, y: pd.Series,
                   model_type: str = 'random_forest',
                   test_size: float = 0.2,
                   cv_folds: int = 5) -> ModelResults:
        """Train a classification model with evaluation"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn required for ML models")

        # Prepare data - scale for linear and distance-based models
        scale_models = {'logistic', 'svc', 'knn', 'mlp', 'gaussian_nb'}
        X_clean, y_clean = self._prepare_data(X, y, scale=(model_type in scale_models))

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_clean, y_clean, test_size=test_size, random_state=self.random_state, stratify=y_clean
        )

        # Train model
        self.model = self.models.get(model_type, self.models['random_forest'])
        self.model.fit(X_train, y_train)
        self.is_fitted = True

        # Evaluate
        train_score = accuracy_score(y_train, self.model.predict(X_train))
        test_score = accuracy_score(y_test, self.model.predict(X_test))
        y_pred = self.model.predict(X_test)

        # Cross-validation
        cv_scores = cross_val_score(self.model, X_clean, y_clean,
                                    cv=cv_folds, scoring='accuracy')

        # Feature importance
        feat_imp = self._get_feature_importance(X_clean.columns.tolist())

        # Additional metrics
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        return ModelResults(
            model_type='classification',
            model_name=model_type,
            train_score=train_score,
            test_score=test_score,
            cv_scores=cv_scores.tolist(),
            predictions=y_pred,
            feature_importance=feat_imp,
            metadata={
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'n_features': X_clean.shape[1],
                'n_samples': len(X_clean),
                'n_classes': len(np.unique(y_clean)),
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
        )

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions on new data"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before prediction")
        X_clean, _ = self._prepare_data(X, scale=True)
        return self.model.predict(X_clean)
