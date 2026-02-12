# Deep Learning Models

> Neural network analysis using TensorFlow/Keras for complex pattern recognition and multi-output prediction tasks.

## Deep Learning Summary

- **Total Tasks**: 5

- **Tasks**: Property Valuation, Affordability Analysis, Housing Quality, Cost Prediction, Occupancy Prediction


### Aggregate Statistics

| Metric | Value |
| :--- | :--- |
| Total Parameters | 78,283 |
| Average Validation Loss | 7150984485.6888 |
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
| Training Loss | 36671234048.0000 | Final epoch |
| Validation Loss | 35753676800.0000 | Final epoch |
| Loss Gap | -917557248.0000 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 53129.3477 | Mean Absolute Error (lower is better) |
| MSE | 35709923328.0000 | Mean Squared Error (lower is better) |
| RMSE | 188970.6944 | Root Mean Squared Error (lower is better) |
| R2 | 0.0486 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 78328037376.0000 |
| Final Training Loss | 36671234048.0000 |
| Loss Improvement | 53.2% |
| Initial Validation Loss | 45487890432.0000 |
| Final Validation Loss | 35753676800.0000 |
| Validation Improvement | 21.4% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.01%



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
| Training Loss | 250.7652 | Final epoch |
| Validation Loss | 249.5413 | Final epoch |
| Loss Gap | -1.2239 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 8.1944 | Mean Absolute Error (lower is better) |
| MSE | 251.7357 | Mean Squared Error (lower is better) |
| RMSE | 15.8662 | Root Mean Squared Error (lower is better) |
| R2 | 0.0662 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 301.3932 |
| Final Training Loss | 250.7652 |
| Loss Improvement | 16.8% |
| Initial Validation Loss | 255.0121 |
| Final Validation Loss | 249.5413 |
| Validation Improvement | 2.1% |


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
| Training Loss | 112.2518 | Final epoch |
| Validation Loss | 112.0846 | Final epoch |
| Loss Gap | -0.1672 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 1.9051 | Mean Absolute Error (lower is better) |
| MSE | 112.4700 | Mean Squared Error (lower is better) |
| RMSE | 10.6052 | Root Mean Squared Error (lower is better) |
| R2 | 0.9100 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 6750.8018 |
| Final Training Loss | 112.2518 |
| Loss Improvement | 98.3% |
| Initial Validation Loss | 32.7364 |
| Final Validation Loss | 112.0846 |
| Validation Improvement | -242.4% |


#### Convergence Assessment

- **Status**: Still improving (> 5% change)

- **Last 10 epochs change**: 32.72%



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
| Training Loss | 1349079.7500 | Final epoch |
| Validation Loss | 1245266.5000 | Final epoch |
| Loss Gap | -103813.2500 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 343.8009 | Mean Absolute Error (lower is better) |
| MSE | 1238420.1250 | Mean Squared Error (lower is better) |
| RMSE | 1112.8433 | Root Mean Squared Error (lower is better) |
| R2 | 0.3738 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 1945408.7500 |
| Final Training Loss | 1349079.7500 |
| Loss Improvement | 30.7% |
| Initial Validation Loss | 1406949.7500 |
| Final Validation Loss | 1245266.5000 |
| Validation Improvement | 11.5% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.29%



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
| Training Loss | 0.3159 | Final epoch |
| Validation Loss | 0.3180 | Final epoch |
| Loss Gap | 0.0020 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 0.2958 | Mean Absolute Error (lower is better) |
| MSE | 0.3180 | Mean Squared Error (lower is better) |
| RMSE | 0.5639 | Root Mean Squared Error (lower is better) |
| R2 | 0.2654 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 0.6754 |
| Final Training Loss | 0.3159 |
| Loss Improvement | 53.2% |
| Initial Validation Loss | 0.3511 |
| Final Validation Loss | 0.3180 |
| Validation Improvement | 9.4% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.01%



## Cross-Task Comparison

| Task | Model Type | Parameters | Train Loss | Val Loss | Gap |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Property Valuation | HousingValuationModel | 36,994 | 36671234048.0000 | 35753676800.0000 | -917557248.0000 |
| Affordability Analysis | HousingAffordabilityModel | 10,306 | 250.7652 | 249.5413 | -1.2239 |
| Housing Quality | HousingQualityModel | 10,371 | 112.2518 | 112.0846 | -0.1672 |
| Cost Prediction | HousingDefaultModel | 10,306 | 1349079.7500 | 1245266.5000 | -103813.2500 |
| Occupancy Prediction | HousingDefaultModel | 10,306 | 0.3159 | 0.3180 | 0.0020 |


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

