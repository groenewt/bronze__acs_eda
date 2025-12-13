"""
Custom exception classes for Census ACS Pipeline
Provides comprehensive error handling with inheritance hierarchy
"""

# ============================================================================
# BASE EXCEPTIONS
# ============================================================================

class CensusError(Exception):
    """Base exception for all census-related errors"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            detail_str = ", ".join([f"{k}={v}" for k, v in self.details.items()])
            return f"{self.message} [{detail_str}]"
        return self.message


# ============================================================================
# DATA LOADING & VALIDATION EXCEPTIONS
# ============================================================================

class DataError(CensusError):
    """Base exception for data-related errors"""
    pass


class FileNotFoundError(DataError):
    """Raised when required data files are not found"""
    def __init__(self, path: str, survey_type: str = None):
        details = {'path': path}
        if survey_type:
            details['survey_type'] = survey_type
        super().__init__(f"Data file not found: {path}", details)


class EmptyDataError(DataError):
    """Raised when loaded data is empty or has no rows"""
    def __init__(self, source: str):
        super().__init__(f"No data loaded from source: {source}", {'source': source})


class InvalidDataFormatError(DataError):
    """Raised when data format is invalid or corrupted"""
    def __init__(self, reason: str, expected_format: str = None):
        details = {'reason': reason}
        if expected_format:
            details['expected_format'] = expected_format
        super().__init__(f"Invalid data format: {reason}", details)


class MissingColumnsError(DataError):
    """Raised when required columns are missing from dataset"""
    def __init__(self, missing_columns: list, dataset_name: str = None):
        details = {'missing_columns': missing_columns}
        if dataset_name:
            details['dataset'] = dataset_name
        super().__init__(
            f"Missing required columns: {', '.join(missing_columns)}", 
            details
        )


class DataValidationError(DataError):
    """Raised when data fails validation checks"""
    def __init__(self, validation_type: str, reason: str):
        super().__init__(
            f"Data validation failed ({validation_type}): {reason}",
            {'validation_type': validation_type, 'reason': reason}
        )


# ============================================================================
# SCHEMA EXCEPTIONS
# ============================================================================

class SchemaError(CensusError):
    """Base exception for schema-related errors"""
    pass


class UnsupportedSurveyTypeError(SchemaError):
    """Raised when survey type is not supported"""
    def __init__(self, survey_type: str, supported_types: list = None):
        details = {'survey_type': survey_type}
        if supported_types:
            details['supported_types'] = supported_types
        super().__init__(
            f"Unsupported survey type: {survey_type}", 
            details
        )


class SchemaMappingError(SchemaError):
    """Raised when schema mapping fails"""
    def __init__(self, column: str, reason: str):
        super().__init__(
            f"Schema mapping failed for column '{column}': {reason}",
            {'column': column, 'reason': reason}
        )


class TypeCastError(SchemaError):
    """Raised when type casting fails"""
    def __init__(self, column: str, target_type: str, value_sample: str = None):
        details = {'column': column, 'target_type': target_type}
        if value_sample:
            details['value_sample'] = value_sample
        super().__init__(
            f"Type casting failed for column '{column}' to {target_type}",
            details
        )


# ============================================================================
# ANALYSIS EXCEPTIONS
# ============================================================================

class AnalysisError(CensusError):
    """Base exception for analysis-related errors"""
    pass


class InsufficientDataError(AnalysisError):
    """Raised when insufficient data for analysis"""
    def __init__(self, analysis_type: str, required_rows: int, actual_rows: int):
        super().__init__(
            f"Insufficient data for {analysis_type}: need {required_rows}, got {actual_rows}",
            {'analysis_type': analysis_type, 'required': required_rows, 'actual': actual_rows}
        )


class TemporalAnalysisError(AnalysisError):
    """Raised when temporal analysis fails"""
    def __init__(self, reason: str, year_range: tuple = None):
        details = {'reason': reason}
        if year_range:
            details['year_range'] = year_range
        super().__init__(f"Temporal analysis failed: {reason}", details)


class CorrelationAnalysisError(AnalysisError):
    """Raised when correlation analysis fails"""
    def __init__(self, variables: list, reason: str):
        super().__init__(
            f"Correlation analysis failed: {reason}",
            {'variables': variables, 'reason': reason}
        )


class StatisticalAnalysisError(AnalysisError):
    """Raised when statistical analysis fails"""
    def __init__(self, variable: str, statistic: str, reason: str):
        super().__init__(
            f"Statistical analysis failed for '{variable}' ({statistic}): {reason}",
            {'variable': variable, 'statistic': statistic, 'reason': reason}
        )


class OutlierDetectionError(AnalysisError):
    """Raised when outlier detection fails"""
    def __init__(self, variable: str, method: str, reason: str):
        super().__init__(
            f"Outlier detection failed for '{variable}' using {method}: {reason}",
            {'variable': variable, 'method': method, 'reason': reason}
        )


class MultivariateOutlierError(OutlierDetectionError):
    """Raised when multivariate outlier detection fails"""
    def __init__(self, method: str, n_features: int, reason: str):
        super().__init__(
            variable=f"{n_features} features",
            method=method,
            reason=reason
        )
        self.details['n_features'] = n_features


class PartialCorrelationError(CorrelationAnalysisError):
    """Raised when partial correlation analysis fails"""
    def __init__(self, var1: str, var2: str, control_vars: list, reason: str):
        super().__init__(
            variables=[var1, var2],
            reason=f"controlling for {control_vars}: {reason}"
        )
        self.details['control_variables'] = control_vars


class HypothesisTestError(StatisticalAnalysisError):
    """Raised when hypothesis testing fails"""
    def __init__(self, test_name: str, variables: list, reason: str):
        super().__init__(
            variable=', '.join(variables) if isinstance(variables, list) else str(variables),
            statistic=test_name,
            reason=reason
        )
        self.details['test_name'] = test_name


# ============================================================================
# FEATURE ENGINEERING EXCEPTIONS
# ============================================================================

class FeatureEngineeringError(CensusError):
    """Base exception for feature engineering errors"""
    pass


class FeatureCreationError(FeatureEngineeringError):
    """Raised when feature creation fails"""
    def __init__(self, feature_name: str, reason: str):
        super().__init__(
            f"Feature creation failed for '{feature_name}': {reason}",
            {'feature_name': feature_name, 'reason': reason}
        )


class FeatureTransformError(FeatureEngineeringError):
    """Raised when feature transformation fails"""
    def __init__(self, transform_type: str, columns: list, reason: str):
        super().__init__(
            f"Feature transform ({transform_type}) failed: {reason}",
            {'transform_type': transform_type, 'columns': columns, 'reason': reason}
        )


class FeatureSelectionError(FeatureEngineeringError):
    """Raised when feature selection fails"""
    def __init__(self, method: str, reason: str):
        super().__init__(
            f"Feature selection ({method}) failed: {reason}",
            {'method': method, 'reason': reason}
        )


class ImputationError(FeatureEngineeringError):
    """Raised when data imputation fails"""
    def __init__(self, method: str, columns: list, reason: str):
        super().__init__(
            f"Imputation ({method}) failed for {len(columns)} columns: {reason}",
            {'method': method, 'columns': columns, 'reason': reason}
        )


# ============================================================================
# ML MODEL EXCEPTIONS
# ============================================================================

class MLError(CensusError):
    """Base exception for machine learning errors"""
    pass


class ModelTrainingError(MLError):
    """Raised when model training fails"""
    def __init__(self, model_name: str, reason: str):
        super().__init__(
            f"Model training failed for {model_name}: {reason}",
            {'model_name': model_name, 'reason': reason}
        )


class ModelPredictionError(MLError):
    """Raised when model prediction fails"""
    def __init__(self, model_name: str, reason: str):
        super().__init__(
            f"Model prediction failed for {model_name}: {reason}",
            {'model_name': model_name, 'reason': reason}
        )


class InvalidModelParametersError(MLError):
    """Raised when model parameters are invalid"""
    def __init__(self, model_name: str, parameter: str, value: any, reason: str):
        super().__init__(
            f"Invalid parameter '{parameter}' for {model_name}: {reason}",
            {'model_name': model_name, 'parameter': parameter, 'value': value, 'reason': reason}
        )


class ModelEvaluationError(MLError):
    """Raised when model evaluation fails"""
    def __init__(self, model_name: str, metric: str, reason: str):
        super().__init__(
            f"Model evaluation failed for {model_name} ({metric}): {reason}",
            {'model_name': model_name, 'metric': metric, 'reason': reason}
        )


# ============================================================================
# VISUALIZATION EXCEPTIONS
# ============================================================================

class VisualizationError(CensusError):
    """Base exception for visualization errors"""
    pass


class PlotCreationError(VisualizationError):
    """Raised when plot creation fails"""
    def __init__(self, plot_type: str, reason: str):
        super().__init__(
            f"Plot creation failed for {plot_type}: {reason}",
            {'plot_type': plot_type, 'reason': reason}
        )


class InvalidVisualizationDataError(VisualizationError):
    """Raised when data is invalid for visualization"""
    def __init__(self, plot_type: str, data_issue: str):
        super().__init__(
            f"Invalid data for {plot_type}: {data_issue}",
            {'plot_type': plot_type, 'data_issue': data_issue}
        )


# ============================================================================
# API & LLM EXCEPTIONS
# ============================================================================

class APIError(CensusError):
    """Base exception for API-related errors"""
    pass


class LLMConnectionError(APIError):
    """Raised when LLM API connection fails"""
    def __init__(self, endpoint: str, reason: str):
        super().__init__(
            f"LLM connection failed to {endpoint}: {reason}",
            {'endpoint': endpoint, 'reason': reason}
        )


class LLMTimeoutError(APIError):
    """Raised when LLM API request times out"""
    def __init__(self, endpoint: str, timeout: int):
        super().__init__(
            f"LLM request timed out after {timeout}s",
            {'endpoint': endpoint, 'timeout': timeout}
        )


class LLMResponseError(APIError):
    """Raised when LLM API returns invalid response"""
    def __init__(self, status_code: int, reason: str):
        super().__init__(
            f"LLM API error (status {status_code}): {reason}",
            {'status_code': status_code, 'reason': reason}
        )


class LLMParsingError(APIError):
    """Raised when LLM response cannot be parsed"""
    def __init__(self, response_sample: str, reason: str):
        super().__init__(
            f"Failed to parse LLM response: {reason}",
            {'response_sample': response_sample[:100], 'reason': reason}
        )


# ============================================================================
# REPORT GENERATION EXCEPTIONS
# ============================================================================

class ReportError(CensusError):
    """Base exception for report generation errors"""
    pass


class ReportGenerationError(ReportError):
    """Raised when report generation fails"""
    def __init__(self, section: str, reason: str):
        super().__init__(
            f"Report generation failed for section '{section}': {reason}",
            {'section': section, 'reason': reason}
        )


class ReportSaveError(ReportError):
    """Raised when saving report fails"""
    def __init__(self, path: str, reason: str):
        super().__init__(
            f"Failed to save report to {path}: {reason}",
            {'path': path, 'reason': reason}
        )


# ============================================================================
# CONFIGURATION EXCEPTIONS
# ============================================================================

class ConfigurationError(CensusError):
    """Base exception for configuration errors"""
    pass


class InvalidConfigurationError(ConfigurationError):
    """Raised when configuration is invalid"""
    def __init__(self, parameter: str, value: any, reason: str):
        super().__init__(
            f"Invalid configuration for '{parameter}': {reason}",
            {'parameter': parameter, 'value': value, 'reason': reason}
        )


class MissingConfigurationError(ConfigurationError):
    """Raised when required configuration is missing"""
    def __init__(self, parameter: str):
        super().__init__(
            f"Missing required configuration: {parameter}",
            {'parameter': parameter}
        )


# ============================================================================
# REGIONAL COMPARISON EXCEPTIONS
# ============================================================================

class RegionalComparisonError(CensusError):
    """Base exception for regional comparison errors"""
    pass


class InsufficientRegionsError(RegionalComparisonError):
    """Raised when insufficient regions for comparison"""
    def __init__(self, required: int, actual: int):
        super().__init__(
            f"Insufficient regions for comparison: need {required}, got {actual}",
            {'required': required, 'actual': actual}
        )


class RegionDataMismatchError(RegionalComparisonError):
    """Raised when regional data structures don't match"""
    def __init__(self, region1: str, region2: str, mismatch_detail: str):
        super().__init__(
            f"Data mismatch between {region1} and {region2}: {mismatch_detail}",
            {'region1': region1, 'region2': region2, 'detail': mismatch_detail}
        )


# ============================================================================
# TIME SERIES FORECASTING EXCEPTIONS
# ============================================================================

class TimeSeriesError(CensusError):
    """Base exception for time series forecasting errors"""
    pass


class TimeSeriesForecastError(TimeSeriesError):
    """Raised when time series forecasting fails"""
    def __init__(self, model_type: str, reason: str):
        super().__init__(
            f"Time series forecast failed for {model_type}: {reason}",
            {'model_type': model_type, 'reason': reason}
        )


class ConfidenceIntervalError(TimeSeriesError):
    """Raised when confidence interval calculation fails"""
    def __init__(self, reason: str):
        super().__init__(
            f"Confidence interval calculation failed: {reason}",
            {'reason': reason}
        )


# ============================================================================
# DEEP LEARNING EXCEPTIONS
# ============================================================================

class DeepLearningError(CensusError):
    """Base exception for deep learning errors"""
    pass


class NeuralNetworkArchitectureError(DeepLearningError):
    """Raised when neural network architecture is invalid"""
    def __init__(self, layer_info: str, reason: str):
        super().__init__(
            f"Invalid neural network architecture ({layer_info}): {reason}",
            {'layer_info': layer_info, 'reason': reason}
        )


class ModelCompilationError(DeepLearningError):
    """Raised when deep learning model compilation fails"""
    def __init__(self, model_name: str, reason: str):
        super().__init__(
            f"Model compilation failed for {model_name}: {reason}",
            {'model_name': model_name, 'reason': reason}
        )


class GPUMemoryError(DeepLearningError):
    """Raised when GPU memory is insufficient"""
    def __init__(self, required_mb: int, available_mb: int):
        super().__init__(
            f"Insufficient GPU memory: need {required_mb}MB, got {available_mb}MB",
            {'required_mb': required_mb, 'available_mb': available_mb}
        )


class EarlyStoppingError(DeepLearningError):
    """Raised when early stopping triggers abnormally"""
    def __init__(self, epoch: int, reason: str):
        super().__init__(
            f"Early stopping triggered at epoch {epoch}: {reason}",
            {'epoch': epoch, 'reason': reason}
        )


class TensorShapeError(DeepLearningError):
    """Raised when tensor shapes are incompatible"""
    def __init__(self, expected_shape: tuple, actual_shape: tuple, operation: str):
        super().__init__(
            f"Tensor shape mismatch in {operation}: expected {expected_shape}, got {actual_shape}",
            {'expected': expected_shape, 'actual': actual_shape, 'operation': operation}
        )


class PredictionShapeMismatchError(DeepLearningError):
    """Raised when predictions and targets have mismatched shapes"""
    def __init__(self, predictions_shape: tuple, targets_shape: tuple, task_name: str):
        super().__init__(
            f"Shape mismatch in {task_name}: predictions {predictions_shape} vs targets {targets_shape}",
            {'predictions_shape': predictions_shape, 'targets_shape': targets_shape, 'task_name': task_name}
        )


# ============================================================================
# VISUAL REGISTRY EXCEPTIONS
# ============================================================================

class VisualRegistryError(VisualizationError):
    """Base exception for visual registry errors"""
    pass


class VisualRegistrationError(VisualRegistryError):
    """Raised when visual registration fails"""
    def __init__(self, visual_path: str, reason: str):
        super().__init__(
            f"Failed to register visualization '{visual_path}': {reason}",
            {'visual_path': visual_path, 'reason': reason}
        )


class VisualNotFoundError(VisualRegistryError):
    """Raised when requested visual not found in registry"""
    def __init__(self, visual_type: str, filters: dict):
        super().__init__(
            f"No visualizations found for type '{visual_type}' with filters {filters}",
            {'visual_type': visual_type, 'filters': filters}
        )


class InvalidVisualMetadataError(VisualRegistryError):
    """Raised when visual metadata is invalid"""
    def __init__(self, field: str, value: any, reason: str):
        super().__init__(
            f"Invalid visual metadata for '{field}': {reason}",
            {'field': field, 'value': value, 'reason': reason}
        )
