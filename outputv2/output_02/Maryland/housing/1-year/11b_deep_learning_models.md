# Deep Learning Models

> Neural network analysis using TensorFlow/Keras for complex pattern recognition and multi-output prediction tasks.

## Deep Learning Summary

- **Total Tasks**: 5

- **Tasks**: Property Valuation, Affordability Analysis, Housing Quality, Cost Prediction, Occupancy Prediction


### Aggregate Statistics

| Metric | Value |
| :--- | :--- |
| Total Parameters | 78,283 |
| Average Validation Loss | 6240302829.4874 |
| Number of Tasks | 5 |


## Task: Property Valuation

### Model Configuration

| Property | Value |
| :--- | :--- |
| Model Type | HousingValuationModel |
| Task Type | Multi_Output |
| Target Variables | Property_Value, Gross_Rent |
| Number of Targets | 2 |
| Input Features | 10 |


### Network Architecture

| Component | Value | Notes |
| :--- | :--- | :--- |
| Total Layers | 7 | Including input and output |
| Total Parameters | 36,994 | Trainable weights |
| Parameters per Layer | 5,284 | Average |


### Performance Metrics

| Metric | Value | Assessment |
| :--- | :--- | :--- |
| Training Loss | 32734765056.0000 | Final epoch |
| Validation Loss | 31200948224.0000 | Final epoch |
| Loss Gap | -1533816832.0000 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 52378.0078 | Mean Absolute Error (lower is better) |
| MSE | 30892611584.0000 | Mean Squared Error (lower is better) |
| RMSE | 175762.9414 | Root Mean Squared Error (lower is better) |
| R2 | -0.1208 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 80790855680.0000 |
| Final Training Loss | 32734765056.0000 |
| Loss Improvement | 59.5% |
| Initial Validation Loss | 48471334912.0000 |
| Final Validation Loss | 31200948224.0000 |
| Validation Improvement | 35.6% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.20%



## Task: Affordability Analysis

### Model Configuration

| Property | Value |
| :--- | :--- |
| Model Type | HousingAffordabilityModel |
| Task Type | Multi_Output |
| Target Variables | Owner_Costs_Percentage_Income, Gross_Rent_Percentage_Income |
| Number of Targets | 2 |
| Input Features | 10 |


### Network Architecture

| Component | Value | Notes |
| :--- | :--- | :--- |
| Total Layers | 6 | Including input and output |
| Total Parameters | 10,306 | Trainable weights |
| Parameters per Layer | 1,717 | Average |


### Performance Metrics

| Metric | Value | Assessment |
| :--- | :--- | :--- |
| Training Loss | 216.8214 | Final epoch |
| Validation Loss | 217.3100 | Final epoch |
| Loss Gap | 0.4885 | MODERATE overfitting risk |



> *Some overfitting detected*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 7.3457 | Mean Absolute Error (lower is better) |
| MSE | 218.6743 | Mean Squared Error (lower is better) |
| RMSE | 14.7876 | Root Mean Squared Error (lower is better) |
| R2 | 0.0499 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 267.2301 |
| Final Training Loss | 216.8214 |
| Loss Improvement | 18.9% |
| Initial Validation Loss | 223.4315 |
| Final Validation Loss | 217.3100 |
| Validation Improvement | 2.7% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.04%



## Task: Housing Quality

### Model Configuration

| Property | Value |
| :--- | :--- |
| Model Type | HousingQualityModel |
| Task Type | Multi_Output |
| Target Variables | Year_Structure_Built, Number_of_Bedrooms, Number_of_Rooms |
| Number of Targets | 3 |
| Input Features | 10 |


### Network Architecture

| Component | Value | Notes |
| :--- | :--- | :--- |
| Total Layers | 6 | Including input and output |
| Total Parameters | 10,371 | Trainable weights |
| Parameters per Layer | 1,728 | Average |


### Performance Metrics

| Metric | Value | Assessment |
| :--- | :--- | :--- |
| Training Loss | 206.1636 | Final epoch |
| Validation Loss | 12.9191 | Final epoch |
| Loss Gap | -193.2445 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 1.4392 | Mean Absolute Error (lower is better) |
| MSE | 12.7429 | Mean Squared Error (lower is better) |
| RMSE | 3.5697 | Root Mean Squared Error (lower is better) |
| R2 | 0.8359 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 9793.5615 |
| Final Training Loss | 206.1636 |
| Loss Improvement | 97.9% |
| Initial Validation Loss | 170.8715 |
| Final Validation Loss | 12.9191 |
| Validation Improvement | 92.4% |


#### Convergence Assessment

- **Status**: Near convergence (< 5% change)

- **Last 10 epochs change**: 4.09%



## Task: Cost Prediction

### Model Configuration

| Property | Value |
| :--- | :--- |
| Model Type | HousingDefaultModel |
| Task Type | Multi_Output |
| Target Variables | Property_Taxes_Yearly, Insurance_Cost_Yearly |
| Number of Targets | 2 |
| Input Features | 10 |


### Network Architecture

| Component | Value | Notes |
| :--- | :--- | :--- |
| Total Layers | 6 | Including input and output |
| Total Parameters | 10,306 | Trainable weights |
| Parameters per Layer | 1,717 | Average |


### Performance Metrics

| Metric | Value | Assessment |
| :--- | :--- | :--- |
| Training Loss | 591294.3125 | Final epoch |
| Validation Loss | 565692.8750 | Final epoch |
| Loss Gap | -25601.4375 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 245.5844 | Mean Absolute Error (lower is better) |
| MSE | 560812.5625 | Mean Squared Error (lower is better) |
| RMSE | 748.8742 | Root Mean Squared Error (lower is better) |
| R2 | 0.3489 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 825591.1875 |
| Final Training Loss | 591294.3125 |
| Loss Improvement | 28.4% |
| Initial Validation Loss | 626095.1875 |
| Final Validation Loss | 565692.8750 |
| Validation Improvement | 9.6% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.02%



## Task: Occupancy Prediction

### Model Configuration

| Property | Value |
| :--- | :--- |
| Model Type | HousingDefaultModel |
| Task Type | Multi_Output |
| Target Variables | Vacancy_Status, Tenure |
| Number of Targets | 2 |
| Input Features | 10 |


### Network Architecture

| Component | Value | Notes |
| :--- | :--- | :--- |
| Total Layers | 6 | Including input and output |
| Total Parameters | 10,306 | Trainable weights |
| Parameters per Layer | 1,717 | Average |


### Performance Metrics

| Metric | Value | Assessment |
| :--- | :--- | :--- |
| Training Loss | 0.3363 | Final epoch |
| Validation Loss | 0.3329 | Final epoch |
| Loss Gap | -0.0034 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 0.3018 | Mean Absolute Error (lower is better) |
| MSE | 0.3343 | Mean Squared Error (lower is better) |
| RMSE | 0.5782 | Root Mean Squared Error (lower is better) |
| R2 | 0.2720 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 0.9075 |
| Final Training Loss | 0.3363 |
| Loss Improvement | 62.9% |
| Initial Validation Loss | 0.3675 |
| Final Validation Loss | 0.3329 |
| Validation Improvement | 9.4% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.18%



## Cross-Task Comparison

| Task | Model Type | Parameters | Train Loss | Val Loss | Gap |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Property Valuation | HousingValuationModel | 36,994 | 32734765056.0000 | 31200948224.0000 | -1533816832.0000 |
| Affordability Analysis | HousingAffordabilityModel | 10,306 | 216.8214 | 217.3100 | 0.4885 |
| Housing Quality | HousingQualityModel | 10,371 | 206.1636 | 12.9191 | -193.2445 |
| Cost Prediction | HousingDefaultModel | 10,306 | 591294.3125 | 565692.8750 | -25601.4375 |
| Occupancy Prediction | HousingDefaultModel | 10,306 | 0.3363 | 0.3329 | -0.0034 |


## Visualizations

![property valuation/training history housing](figures/ml/deep_learning/property_valuation/training_history_housing.png)

![property valuation/predictions vs actual housing](figures/ml/deep_learning/property_valuation/predictions_vs_actual_housing.png)

![property valuation/residual analysis housing](figures/ml/deep_learning/property_valuation/residual_analysis_housing.png)

![property valuation/error distribution housing](figures/ml/deep_learning/property_valuation/error_distribution_housing.png)

![property valuation/architecture summary housing](figures/ml/deep_learning/property_valuation/architecture_summary_housing.png)

![property valuation/Property Value detailed analysis housing](figures/ml/deep_learning/property_valuation/Property_Value_detailed_analysis_housing.png)

![property valuation/Gross Rent detailed analysis housing](figures/ml/deep_learning/property_valuation/Gross_Rent_detailed_analysis_housing.png)

![property valuation/property valuation convergence diagnostics housing](figures/ml/deep_learning/property_valuation/property_valuation_convergence_diagnostics_housing.png)

![property valuation/property valuation error evolution housing](figures/ml/deep_learning/property_valuation/property_valuation_error_evolution_housing.png)

![affordability analysis/training history housing](figures/ml/deep_learning/affordability_analysis/training_history_housing.png)

![affordability analysis/predictions vs actual housing](figures/ml/deep_learning/affordability_analysis/predictions_vs_actual_housing.png)

![affordability analysis/residual analysis housing](figures/ml/deep_learning/affordability_analysis/residual_analysis_housing.png)

![affordability analysis/error distribution housing](figures/ml/deep_learning/affordability_analysis/error_distribution_housing.png)

![affordability analysis/architecture summary housing](figures/ml/deep_learning/affordability_analysis/architecture_summary_housing.png)

![affordability analysis/Owner Costs Percentage Income detailed analysis housing](figures/ml/deep_learning/affordability_analysis/Owner_Costs_Percentage_Income_detailed_analysis_housing.png)

![affordability analysis/Gross Rent Percentage Income detailed analysis housing](figures/ml/deep_learning/affordability_analysis/Gross_Rent_Percentage_Income_detailed_analysis_housing.png)

![affordability analysis/affordability analysis convergence diagnostics housing](figures/ml/deep_learning/affordability_analysis/affordability_analysis_convergence_diagnostics_housing.png)

![affordability analysis/affordability analysis error evolution housing](figures/ml/deep_learning/affordability_analysis/affordability_analysis_error_evolution_housing.png)

![housing quality/training history housing](figures/ml/deep_learning/housing_quality/training_history_housing.png)

![housing quality/predictions vs actual housing](figures/ml/deep_learning/housing_quality/predictions_vs_actual_housing.png)

![housing quality/residual analysis housing](figures/ml/deep_learning/housing_quality/residual_analysis_housing.png)

![housing quality/error distribution housing](figures/ml/deep_learning/housing_quality/error_distribution_housing.png)

![housing quality/architecture summary housing](figures/ml/deep_learning/housing_quality/architecture_summary_housing.png)

![housing quality/Year Structure Built detailed analysis housing](figures/ml/deep_learning/housing_quality/Year_Structure_Built_detailed_analysis_housing.png)

![housing quality/Number of Bedrooms detailed analysis housing](figures/ml/deep_learning/housing_quality/Number_of_Bedrooms_detailed_analysis_housing.png)

![housing quality/Number of Rooms detailed analysis housing](figures/ml/deep_learning/housing_quality/Number_of_Rooms_detailed_analysis_housing.png)

![housing quality/housing quality convergence diagnostics housing](figures/ml/deep_learning/housing_quality/housing_quality_convergence_diagnostics_housing.png)

![housing quality/housing quality error evolution housing](figures/ml/deep_learning/housing_quality/housing_quality_error_evolution_housing.png)

![cost prediction/training history housing](figures/ml/deep_learning/cost_prediction/training_history_housing.png)

![cost prediction/predictions vs actual housing](figures/ml/deep_learning/cost_prediction/predictions_vs_actual_housing.png)

![cost prediction/residual analysis housing](figures/ml/deep_learning/cost_prediction/residual_analysis_housing.png)

![cost prediction/error distribution housing](figures/ml/deep_learning/cost_prediction/error_distribution_housing.png)

![cost prediction/architecture summary housing](figures/ml/deep_learning/cost_prediction/architecture_summary_housing.png)

![cost prediction/Property Taxes Yearly detailed analysis housing](figures/ml/deep_learning/cost_prediction/Property_Taxes_Yearly_detailed_analysis_housing.png)

![cost prediction/Insurance Cost Yearly detailed analysis housing](figures/ml/deep_learning/cost_prediction/Insurance_Cost_Yearly_detailed_analysis_housing.png)

![cost prediction/cost prediction convergence diagnostics housing](figures/ml/deep_learning/cost_prediction/cost_prediction_convergence_diagnostics_housing.png)

![cost prediction/cost prediction error evolution housing](figures/ml/deep_learning/cost_prediction/cost_prediction_error_evolution_housing.png)

![occupancy prediction/training history housing](figures/ml/deep_learning/occupancy_prediction/training_history_housing.png)

![occupancy prediction/predictions vs actual housing](figures/ml/deep_learning/occupancy_prediction/predictions_vs_actual_housing.png)

![occupancy prediction/residual analysis housing](figures/ml/deep_learning/occupancy_prediction/residual_analysis_housing.png)

![occupancy prediction/error distribution housing](figures/ml/deep_learning/occupancy_prediction/error_distribution_housing.png)

![occupancy prediction/architecture summary housing](figures/ml/deep_learning/occupancy_prediction/architecture_summary_housing.png)

![occupancy prediction/Vacancy Status detailed analysis housing](figures/ml/deep_learning/occupancy_prediction/Vacancy_Status_detailed_analysis_housing.png)

![occupancy prediction/Tenure detailed analysis housing](figures/ml/deep_learning/occupancy_prediction/Tenure_detailed_analysis_housing.png)

![occupancy prediction/occupancy prediction convergence diagnostics housing](figures/ml/deep_learning/occupancy_prediction/occupancy_prediction_convergence_diagnostics_housing.png)

![occupancy prediction/occupancy prediction error evolution housing](figures/ml/deep_learning/occupancy_prediction/occupancy_prediction_error_evolution_housing.png)

![learning curves comparison housing](figures/ml/deep_learning/learning_curves_comparison_housing.png)

![model comparison housing](figures/ml/deep_learning/model_comparison_housing.png)

![comprehensive performance dashboard housing](figures/ml/deep_learning/comprehensive_performance_dashboard_housing.png)

![comprehensive performance dashboard housing](figures/ml/deep_learning/comprehensive_performance_dashboard_housing.png)

