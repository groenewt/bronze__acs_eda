"""
Deep Learning Module for Census Data Analysis
Provides specialized neural network architectures for Population and Housing surveys
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings('ignore')

from exceptions import (DeepLearningError, NeuralNetworkArchitectureError,
                        ModelCompilationError, GPUMemoryError, TensorShapeError,
                        EarlyStoppingError, InsufficientDataError, ModelTrainingError)

# Try importing TensorFlow/Keras (support both TF 2.x and standalone Keras)
try:
    import os
    import gc
    # Force CPU-only mode for TensorFlow (avoid GPU conflict with LLM)
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TF logging
    # Limit memory allocator behavior
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

    import tensorflow as tf
    # Configure TensorFlow for CPU with optimizations (USE ALL CORES)
    tf.config.threading.set_intra_op_parallelism_threads(24)  # ALL 24 cores
    tf.config.threading.set_inter_op_parallelism_threads(24)

    from tensorflow import keras
    from tensorflow.keras import layers, models, callbacks, regularizers
    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import (Dense, Dropout, BatchNormalization, Input,
                                          Concatenate, Embedding, Flatten, LSTM,
                                          Conv1D, GlobalAveragePooling1D, Attention)
    from tensorflow.keras.optimizers import Adam, RMSprop, SGD
    from tensorflow.keras.callbacks import (EarlyStopping, ReduceLROnPlateau,
                                             ModelCheckpoint, TensorBoard)
    TF_AVAILABLE = True
    print(f"[DL-INFO] TensorFlow {tf.__version__} configured for CPU-only mode")
    print(f"[DL-INFO] Using {tf.config.threading.get_intra_op_parallelism_threads()} cores")
except ImportError:
    try:
        import keras
        from keras import layers, models, callbacks, regularizers
        from keras.models import Sequential, Model
        from keras.layers import (Dense, Dropout, BatchNormalization, Input,
                                   Concatenate, Embedding, Flatten, LSTM,
                                   Conv1D, GlobalAveragePooling1D, Attention)
        from keras.optimizers import Adam, RMSprop, SGD
        from keras.callbacks import (EarlyStopping, ReduceLROnPlateau,
                                     ModelCheckpoint, TensorBoard)
        TF_AVAILABLE = True
        print("[DL-INFO] Standalone Keras configured")
    except ImportError:
        TF_AVAILABLE = False
        print("[WARNING] TensorFlow/Keras not available. Deep learning disabled.")

# Scikit-learn for preprocessing
try:
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder
    from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                                 accuracy_score, precision_recall_fscore_support,
                                 confusion_matrix, classification_report)
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class DLResults:
    """Container for deep learning results"""
    model_type: str
    task_type: str  # 'regression', 'classification', 'multi_output'
    targets: List[str]
    train_loss: float
    val_loss: float
    test_metrics: Dict[str, float]
    predictions: np.ndarray
    history: Dict[str, List[float]]
    architecture: Dict[str, Any]
    feature_importance: Optional[Dict[str, float]]
    metadata: Dict[str, Any]
    X_test: np.ndarray = None  # Store test features for visualization
    y_test: np.ndarray = None  # Store test targets for visualization


@dataclass
class TrainingConfig:
    """Configuration for deep learning training (CPU-only, 24 cores via threading)"""
    epochs: int = 75
    batch_size: int = 256  # Balanced: Fast but not memory-exploding
    validation_split: float = 0.2
    learning_rate: float = 0.001
    early_stopping_patience: int = 15  # More patience for CPU training
    reduce_lr_patience: int = 7
    dropout_rate: float = 0.3
    l1_reg: float = 0.0001
    l2_reg: float = 0.0001
    optimizer: str = 'adam'
    loss: str = 'mse'  # or 'categorical_crossentropy'
    verbose: int = 1  # Show progress bars for CPU training
    use_multiprocessing: bool = False  # Avoid memory duplication (threading handles cores)
    workers: int = 1  # Threading already uses all 24 cores


# ============================================================================
# BASE DEEP LEARNING MODEL
# ============================================================================

class BaseDeepLearningModel(ABC):
    """Abstract base class for deep learning models"""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        self.is_fitted = False
        self.history = None
        np.random.seed(random_state)
        if TF_AVAILABLE:
            tf.random.set_seed(random_state)

    @abstractmethod
    def build_architecture(self, input_shape: tuple, output_shape: int,
                          config: TrainingConfig) -> Model:
        """Build neural network architecture"""
        pass

    @abstractmethod
    def get_target_columns(self, survey_type: str) -> List[str]:
        """Get target columns for specific survey type"""
        pass

    def _check_dependencies(self):
        """Check if required libraries available (≤10 lines)"""
        if not TF_AVAILABLE:
            raise ImportError("TensorFlow/Keras required for deep learning")
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn required for preprocessing")

    def _prepare_features(self, df: pd.DataFrame, features: List[str]):
        """Prepare and scale features (≤10 lines)"""
        X = df[features].copy()
        # Filter to numeric columns only (TensorFlow requires numeric input)
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        X = X[numeric_cols]
        X = X.fillna(X.median())
        if self.scaler is None:
            self.scaler = RobustScaler()
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        return X_scaled, numeric_cols

    def _prepare_targets(self, df: pd.DataFrame, targets: List[str],
                        task_type: str):
        """Prepare target variables (≤10 lines)"""
        y = df[targets].copy()
        if task_type == 'classification':
            y_encoded = self._encode_labels(y, targets)
            return y_encoded
        else:  # regression or multi_output
            # Ensure numeric dtype for regression targets
            y = y.apply(pd.to_numeric, errors='coerce')
            y = y.fillna(y.median())
            return y.values.astype(np.float32)

    def _encode_labels(self, y: pd.DataFrame, targets: List[str]):
        """Encode categorical labels (≤10 lines)"""
        y_encoded = y.copy()
        for col in targets:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                y_encoded[col] = self.label_encoders[col].fit_transform(y[col])
            else:
                y_encoded[col] = self.label_encoders[col].transform(y[col])
        return y_encoded.values

    def _split_data(self, X: np.ndarray, y: np.ndarray,
                   test_size: float = 0.2):
        """Split data into train/test sets (≤10 lines)"""
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=self.random_state
            )
            return X_train, X_test, y_train, y_test
        except Exception as e:
            raise InsufficientDataError('train_test_split', 10, len(X))

    def _create_callbacks(self, config: TrainingConfig):
        """Create training callbacks (≤10 lines)"""
        early_stop = EarlyStopping(monitor='val_loss',
                                    patience=config.early_stopping_patience,
                                    restore_best_weights=True, verbose=0)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                       factor=0.5, patience=config.reduce_lr_patience,
                                       min_lr=1e-7, verbose=0)
        return [early_stop, reduce_lr]

    def _compile_model(self, model: Model, config: TrainingConfig):
        """Compile model with optimizer and loss (≤10 lines)"""
        try:
            optimizer = self._get_optimizer(config)
            model.compile(optimizer=optimizer, loss=config.loss,
                         metrics=['mae', 'mse'] if config.loss == 'mse' else ['accuracy'])
            return model
        except Exception as e:
            raise ModelCompilationError(model.name, str(e))

    def _get_optimizer(self, config: TrainingConfig):
        """Get optimizer instance (≤10 lines)"""
        lr = config.learning_rate
        if config.optimizer == 'adam':
            return Adam(learning_rate=lr)
        elif config.optimizer == 'rmsprop':
            return RMSprop(learning_rate=lr)
        elif config.optimizer == 'sgd':
            return SGD(learning_rate=lr, momentum=0.9)
        return Adam(learning_rate=lr)

    def _calculate_metrics(self, y_true, y_pred, task_type: str):
        """Calculate evaluation metrics (≤10 lines)"""
        if task_type == 'regression' or task_type == 'multi_output':
            return {'mae': float(mean_absolute_error(y_true, y_pred)),
                    'mse': float(mean_squared_error(y_true, y_pred)),
                    'rmse': float(np.sqrt(mean_squared_error(y_true, y_pred))),
                    'r2': float(r2_score(y_true, y_pred))}
        else:  # classification
            acc = accuracy_score(y_true.argmax(axis=1), y_pred.argmax(axis=1))
            return {'accuracy': float(acc)}


# ============================================================================
# POPULATION SURVEY DEEP LEARNING
# ============================================================================

class PopulationDLModel(BaseDeepLearningModel):
    """Specialized deep learning for Population surveys"""

    def get_target_columns(self, survey_type: str = 'population') -> Dict[str, List[str]]:
        """Get target configurations from schema (≤10 lines)"""
        # Extracted from PopulationSurvey schema: _income_cols() and _person_income_recodes()
        return {
            'income_prediction': ['Total_Person_Income', 'Wage_Income', 'Total_Person_Earnings'],
            'employment_analysis': ['Hours_Worked_Per_Week', 'Employment_Status_Recode', 'Weeks_Worked_Past_Year'],
            'demographic_profile': ['Educational_Attainment', 'Age', 'Sex', 'Marital_Status']
        }

    def build_architecture(self, input_shape: tuple, output_shape: int,
                          config: TrainingConfig, task_name: str = 'default') -> Model:
        """Build specialized architecture (≤10 lines)"""
        if task_name == 'income_prediction':
            return self._build_income_model(input_shape, output_shape, config)
        elif task_name == 'employment_analysis':
            return self._build_employment_model(input_shape, output_shape, config)
        elif task_name == 'demographic_profile':
            return self._build_demographic_model(input_shape, output_shape, config)
        return self._build_default_model(input_shape, output_shape, config)

    def _build_income_model(self, input_shape: tuple, output_shape: int,
                           config: TrainingConfig) -> Model:
        """Deep multi-output regression for income (≤10 lines)"""
        inputs = Input(shape=(input_shape[1],))
        x = Dense(256, activation='relu',
                 kernel_regularizer=regularizers.l2(config.l2_reg))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(config.dropout_rate)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(config.dropout_rate / 2)(x)
        outputs = Dense(output_shape, activation='linear', name='income_output')(x)
        return Model(inputs=inputs, outputs=outputs, name='PopulationIncomeModel')

    def _build_employment_model(self, input_shape: tuple, output_shape: int,
                                config: TrainingConfig) -> Model:
        """Deep model for employment prediction (≤10 lines)"""
        inputs = Input(shape=(input_shape[1],))
        x = Dense(128, activation='relu',
                 kernel_regularizer=regularizers.l1_l2(config.l1_reg, config.l2_reg))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(config.dropout_rate)(x)
        x = Dense(64, activation='relu')(x)
        outputs = Dense(output_shape, activation='linear', name='employment_output')(x)
        return Model(inputs=inputs, outputs=outputs, name='PopulationEmploymentModel')

    def _build_demographic_model(self, input_shape: tuple, output_shape: int,
                                config: TrainingConfig) -> Model:
        """Deep classifier for demographics (≤10 lines)"""
        inputs = Input(shape=(input_shape[1],))
        x = Dense(128, activation='relu',
                 kernel_regularizer=regularizers.l2(config.l2_reg))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(config.dropout_rate)(x)
        x = Dense(64, activation='relu')(x)
        x = Dropout(config.dropout_rate / 2)(x)
        outputs = Dense(output_shape, activation='softmax', name='demo_output')(x)
        return Model(inputs=inputs, outputs=outputs, name='PopulationDemographicModel')

    def _build_default_model(self, input_shape: tuple, output_shape: int,
                            config: TrainingConfig) -> Model:
        """Default deep architecture (≤10 lines)"""
        inputs = Input(shape=(input_shape[1],))
        x = Dense(128, activation='relu')(inputs)
        x = BatchNormalization()(x)
        x = Dropout(config.dropout_rate)(x)
        x = Dense(64, activation='relu')(x)
        outputs = Dense(output_shape, activation='linear')(x)
        return Model(inputs=inputs, outputs=outputs, name='PopulationDefaultModel')


# ============================================================================
# HOUSING SURVEY DEEP LEARNING
# ============================================================================

class HousingDLModel(BaseDeepLearningModel):
    """Specialized deep learning for Housing surveys"""

    def get_target_columns(self, survey_type: str = 'housing') -> Dict[str, List[str]]:
        """Get target configurations from schema (≤10 lines)"""
        # Extracted from HousingSurvey schema: _rental_costs() and _unit_status_cols()
        return {
            'property_valuation': ['Property_Value', 'Gross_Rent'],
            'affordability_analysis': ['Owner_Costs_Percentage_Income',
                                      'Gross_Rent_Percentage_Income'],
            'housing_quality': ['Year_Structure_Built', 'Number_of_Bedrooms', 'Number_of_Rooms'],
            'cost_prediction': ['Property_Taxes_Yearly', 'Insurance_Cost_Yearly'],
            'occupancy_prediction': ['Vacancy_Status', 'Tenure']
        }

    def build_architecture(self, input_shape: tuple, output_shape: int,
                          config: TrainingConfig, task_name: str = 'default') -> Model:
        """Build specialized architecture (≤10 lines)"""
        if task_name == 'property_valuation':
            return self._build_valuation_model(input_shape, output_shape, config)
        elif task_name == 'affordability_analysis':
            return self._build_affordability_model(input_shape, output_shape, config)
        elif task_name == 'housing_quality':
            return self._build_quality_model(input_shape, output_shape, config)
        return self._build_default_model(input_shape, output_shape, config)

    def _build_valuation_model(self, input_shape: tuple, output_shape: int,
                               config: TrainingConfig) -> Model:
        """Deep regression for property valuation (≤10 lines)"""
        inputs = Input(shape=(input_shape[1],))
        x = Dense(256, activation='relu',
                 kernel_regularizer=regularizers.l2(config.l2_reg))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(config.dropout_rate)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(config.dropout_rate / 2)(x)
        outputs = Dense(output_shape, activation='linear', name='value_output')(x)
        return Model(inputs=inputs, outputs=outputs, name='HousingValuationModel')

    def _build_affordability_model(self, input_shape: tuple, output_shape: int,
                                   config: TrainingConfig) -> Model:
        """Deep model for affordability metrics (≤10 lines)"""
        inputs = Input(shape=(input_shape[1],))
        x = Dense(128, activation='relu',
                 kernel_regularizer=regularizers.l1_l2(config.l1_reg, config.l2_reg))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(config.dropout_rate)(x)
        x = Dense(64, activation='relu')(x)
        outputs = Dense(output_shape, activation='linear', name='afford_output')(x)
        return Model(inputs=inputs, outputs=outputs, name='HousingAffordabilityModel')

    def _build_quality_model(self, input_shape: tuple, output_shape: int,
                            config: TrainingConfig) -> Model:
        """Deep model for housing quality (≤10 lines)"""
        inputs = Input(shape=(input_shape[1],))
        x = Dense(128, activation='relu',
                 kernel_regularizer=regularizers.l2(config.l2_reg))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(config.dropout_rate)(x)
        x = Dense(64, activation='relu')(x)
        outputs = Dense(output_shape, activation='linear', name='quality_output')(x)
        return Model(inputs=inputs, outputs=outputs, name='HousingQualityModel')

    def _build_default_model(self, input_shape: tuple, output_shape: int,
                            config: TrainingConfig) -> Model:
        """Default deep architecture (≤10 lines)"""
        inputs = Input(shape=(input_shape[1],))
        x = Dense(128, activation='relu')(inputs)
        x = BatchNormalization()(x)
        x = Dropout(config.dropout_rate)(x)
        x = Dense(64, activation='relu')(x)
        outputs = Dense(output_shape, activation='linear')(x)
        return Model(inputs=inputs, outputs=outputs, name='HousingDefaultModel')


# ============================================================================
# DEEP LEARNING TRAINER
# ============================================================================

class DeepLearningTrainer:
    """Orchestrates deep learning training for census data"""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {
            'population': PopulationDLModel(random_state),
            'housing': HousingDLModel(random_state)
        }

    def train_model(self, df: pd.DataFrame, survey_type: str,
                   task_name: str, features: List[str],
                   config: TrainingConfig = None) -> DLResults:
        """Train deep learning model (≤10 lines)"""
        config = config or TrainingConfig()
        model_class = self.models.get(survey_type)
        if not model_class:
            raise ValueError(f"Unsupported survey type: {survey_type}")
        model_class._check_dependencies()
        targets_dict = model_class.get_target_columns(survey_type)
        targets = targets_dict.get(task_name, list(targets_dict.values())[0])
        return self._execute_training(df, model_class, task_name, features, targets, config)

    def _execute_training(self, df, model_class, task_name, features,
                         targets, config):
        """Execute training pipeline (≤10 lines)"""
        X_scaled, feature_names = model_class._prepare_features(df, features)
        task_type = self._infer_task_type(df, targets)
        y = model_class._prepare_targets(df, targets, task_type)
        X_train, X_test, y_train, y_test = model_class._split_data(X_scaled, y)
        model = self._build_and_compile(model_class, X_train.shape, y_train.shape[1],
                                       config, task_name, task_type)
        history = self._fit_model(model, X_train, y_train, config)
        return self._evaluate_and_package(model, X_test, y_test, history, task_name,
                                         task_type, targets, feature_names)

    def _infer_task_type(self, df: pd.DataFrame, targets: List[str]) -> str:
        """Infer task type from targets (≤10 lines)"""
        target_data = df[targets]
        if len(targets) > 1:
            return 'multi_output'
        if target_data[targets[0]].dtype == 'object' or target_data[targets[0]].nunique() < 20:
            return 'classification'
        return 'regression'

    def _build_and_compile(self, model_class, input_shape, output_shape,
                          config, task_name, task_type):
        """Build and compile model (≤10 lines)"""
        try:
            model = model_class.build_architecture(input_shape, output_shape,
                                                   config, task_name)
            if task_type == 'classification':
                config.loss = 'sparse_categorical_crossentropy'
            return model_class._compile_model(model, config)
        except Exception as e:
            raise NeuralNetworkArchitectureError(task_name, str(e))

    def _fit_model(self, model, X_train, y_train, config):
        """Fit model with callbacks (≤10 lines)"""
        try:
            cbs = model._create_callbacks(config) if hasattr(model, '_create_callbacks') else []
            # Note: use_multiprocessing/workers only valid for generators, not arrays
            history = model.fit(X_train, y_train, epochs=config.epochs,
                               batch_size=config.batch_size,
                               validation_split=config.validation_split,
                               callbacks=cbs, verbose=config.verbose)
            return history.history
        except Exception as e:
            raise ModelTrainingError(model.name, str(e))

    def _evaluate_and_package(self, model, X_test, y_test, history,
                             task_name, task_type, targets, features):
        """Evaluate and package results (≤10 lines)"""
        y_pred = model.predict(X_test, verbose=0)
        metrics = self._calculate_test_metrics(y_test, y_pred, task_type)
        return DLResults(model_type=model.name, task_type=task_type, targets=targets,
                        train_loss=history['loss'][-1], val_loss=history['val_loss'][-1],
                        test_metrics=metrics, predictions=y_pred, history=history,
                        architecture={'layers': len(model.layers), 'params': model.count_params()},
                        feature_importance=None, metadata={'features': features},
                        X_test=X_test, y_test=y_test)

    def _calculate_test_metrics(self, y_true, y_pred, task_type):
        """Calculate test metrics (≤10 lines)"""
        if task_type == 'regression' or task_type == 'multi_output':
            return {'mae': float(mean_absolute_error(y_true, y_pred)),
                    'mse': float(mean_squared_error(y_true, y_pred)),
                    'rmse': float(np.sqrt(mean_squared_error(y_true, y_pred))),
                    'r2': float(r2_score(y_true, y_pred))}
        else:
            return {'accuracy': float(accuracy_score(y_true, y_pred.argmax(axis=1)))}


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def train_population_dl(df: pd.DataFrame, task_name: str = 'income_prediction',
                        features: List[str] = None, config: TrainingConfig = None) -> DLResults:
    """Train population survey deep learning model (≤10 lines)"""
    if not TF_AVAILABLE:
        raise ImportError("TensorFlow/Keras required for deep learning")
    features = features or _get_default_population_features(df)
    trainer = DeepLearningTrainer()
    return trainer.train_model(df, 'population', task_name, features, config)


def train_housing_dl(df: pd.DataFrame, task_name: str = 'property_valuation',
                     features: List[str] = None, config: TrainingConfig = None) -> DLResults:
    """Train housing survey deep learning model (≤10 lines)"""
    if not TF_AVAILABLE:
        raise ImportError("TensorFlow/Keras required for deep learning")
    features = features or _get_default_housing_features(df)
    trainer = DeepLearningTrainer()
    return trainer.train_model(df, 'housing', task_name, features, config)


def _get_default_population_features(df: pd.DataFrame) -> List[str]:
    """Get default features for population (≤10 lines)"""
    candidate_features = ['Age', 'Sex', 'Educational_Attainment', 'Hours_Worked_Per_Week',
                          'Weeks_Worked_Past_Year', 'Travel_Time_To_Work_Minutes',
                          'Citizenship_Status', 'Marital_Status', 'Race_Recode',
                          'Hispanic_Origin', 'Employment_Status_Recode']
    return [f for f in candidate_features if f in df.columns]


def _get_default_housing_features(df: pd.DataFrame) -> List[str]:
    """Get default features for housing (≤10 lines)"""
    candidate_features = ['Number_of_Bedrooms', 'Number_of_Rooms', 'Year_Structure_Built',
                          'Building_Type', 'Number_of_Persons', 'Tenure', 'Vehicles_Available',
                          'Electricity_Cost_Monthly', 'Gas_Cost_Monthly', 'Property_Taxes_Yearly']
    return [f for f in candidate_features if f in df.columns]
