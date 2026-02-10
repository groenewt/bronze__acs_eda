# Deep Learning Models

> Neural network analysis using TensorFlow/Keras for complex pattern recognition and multi-output prediction tasks.

## Deep Learning Summary

- **Total Tasks**: 5

- **Tasks**: Property Valuation, Affordability Analysis, Housing Quality, Cost Prediction, Occupancy Prediction


### Aggregate Statistics

| Metric | Value |
| :--- | :--- |
| Total Parameters | 78,283 |
| Average Validation Loss | 42232.6101 |
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
| Training Loss | 13887.5693 | Final epoch |
| Validation Loss | 13117.8467 | Final epoch |
| Loss Gap | -769.7227 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 30.9912 | Mean Absolute Error (lower is better) |
| MSE | 13365.5254 | Mean Squared Error (lower is better) |
| RMSE | 115.6094 | Root Mean Squared Error (lower is better) |
| R2 | 0.0776 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 22520.7324 |
| Final Training Loss | 13887.5693 |
| Loss Improvement | 38.3% |
| Initial Validation Loss | 13471.5723 |
| Final Validation Loss | 13117.8467 |
| Validation Improvement | 2.6% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.07%



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
| Training Loss | 191.8063 | Final epoch |
| Validation Loss | 191.5497 | Final epoch |
| Loss Gap | -0.2566 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 6.3546 | Mean Absolute Error (lower is better) |
| MSE | 191.3441 | Mean Squared Error (lower is better) |
| RMSE | 13.8327 | Root Mean Squared Error (lower is better) |
| R2 | 0.0478 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 208.4925 |
| Final Training Loss | 191.8063 |
| Loss Improvement | 8.0% |
| Initial Validation Loss | 193.5274 |
| Final Validation Loss | 191.5497 |
| Validation Improvement | 1.0% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.01%



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
| Training Loss | 0.0052 | Final epoch |
| Validation Loss | 0.0299 | Final epoch |
| Loss Gap | 0.0248 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 0.0434 | Mean Absolute Error (lower is better) |
| MSE | 0.0300 | Mean Squared Error (lower is better) |
| RMSE | 0.1732 | Root Mean Squared Error (lower is better) |
| R2 | 0.9895 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 0.3072 |
| Final Training Loss | 0.0052 |
| Loss Improvement | 98.3% |
| Initial Validation Loss | 0.0527 |
| Final Validation Loss | 0.0299 |
| Validation Improvement | 43.2% |


#### Convergence Assessment

- **Status**: Still improving (> 5% change)

- **Last 10 epochs change**: 6.91%



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
| Training Loss | 198492.9219 | Final epoch |
| Validation Loss | 197853.2031 | Final epoch |
| Loss Gap | -639.7188 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 181.3310 | Mean Absolute Error (lower is better) |
| MSE | 198963.9375 | Mean Squared Error (lower is better) |
| RMSE | 446.0537 | Root Mean Squared Error (lower is better) |
| R2 | 0.1198 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 226884.3906 |
| Final Training Loss | 198492.9219 |
| Loss Improvement | 12.5% |
| Initial Validation Loss | 201447.2031 |
| Final Validation Loss | 197853.2031 |
| Validation Improvement | 1.8% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.01%



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
| Training Loss | 0.4229 | Final epoch |
| Validation Loss | 0.4211 | Final epoch |
| Loss Gap | -0.0018 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 0.3234 | Mean Absolute Error (lower is better) |
| MSE | 0.4201 | Mean Squared Error (lower is better) |
| RMSE | 0.6481 | Root Mean Squared Error (lower is better) |
| R2 | 0.2241 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 0.5891 |
| Final Training Loss | 0.4229 |
| Loss Improvement | 28.2% |
| Initial Validation Loss | 0.4509 |
| Final Validation Loss | 0.4211 |
| Validation Improvement | 6.6% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.07%



## Cross-Task Comparison

| Task | Model Type | Parameters | Train Loss | Val Loss | Gap |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Property Valuation | HousingValuationModel | 36,994 | 13887.5693 | 13117.8467 | -769.7227 |
| Affordability Analysis | HousingAffordabilityModel | 10,306 | 191.8063 | 191.5497 | -0.2566 |
| Housing Quality | HousingQualityModel | 10,371 | 0.0052 | 0.0299 | 0.0248 |
| Cost Prediction | HousingDefaultModel | 10,306 | 198492.9219 | 197853.2031 | -639.7188 |
| Occupancy Prediction | HousingDefaultModel | 10,306 | 0.4229 | 0.4211 | -0.0018 |


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

