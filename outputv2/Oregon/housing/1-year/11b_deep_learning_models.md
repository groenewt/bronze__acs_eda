# Deep Learning Models

> Neural network analysis using TensorFlow/Keras for complex pattern recognition and multi-output prediction tasks.

## Deep Learning Summary

- **Total Tasks**: 5

- **Tasks**: Property Valuation, Affordability Analysis, Housing Quality, Cost Prediction, Occupancy Prediction


### Aggregate Statistics

| Metric | Value |
| :--- | :--- |
| Total Parameters | 78,283 |
| Average Validation Loss | 5369167559.7307 |
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
| Training Loss | 25103452160.0000 | Final epoch |
| Validation Loss | 26845380608.0000 | Final epoch |
| Loss Gap | 1741928448.0000 | HIGH overfitting risk |



> *Model may be overfitting significantly*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 48258.2891 | Mean Absolute Error (lower is better) |
| MSE | 25351936000.0000 | Mean Squared Error (lower is better) |
| RMSE | 159222.9129 | Root Mean Squared Error (lower is better) |
| R2 | -0.1191 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 73621241856.0000 |
| Final Training Loss | 25103452160.0000 |
| Loss Improvement | 65.9% |
| Initial Validation Loss | 58361806848.0000 |
| Final Validation Loss | 26845380608.0000 |
| Validation Improvement | 54.0% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.09%



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
| Training Loss | 229.1559 | Final epoch |
| Validation Loss | 225.2091 | Final epoch |
| Loss Gap | -3.9468 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 7.6017 | Mean Absolute Error (lower is better) |
| MSE | 227.9213 | Mean Squared Error (lower is better) |
| RMSE | 15.0971 | Root Mean Squared Error (lower is better) |
| R2 | 0.0576 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 306.1670 |
| Final Training Loss | 229.1559 |
| Loss Improvement | 25.2% |
| Initial Validation Loss | 232.8119 |
| Final Validation Loss | 225.2091 |
| Validation Improvement | 3.3% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.03%



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
| Training Loss | 239.6061 | Final epoch |
| Validation Loss | 16.3531 | Final epoch |
| Loss Gap | -223.2529 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 1.0757 | Mean Absolute Error (lower is better) |
| MSE | 17.3149 | Mean Squared Error (lower is better) |
| RMSE | 4.1611 | Root Mean Squared Error (lower is better) |
| R2 | 0.8842 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 14819.0020 |
| Final Training Loss | 239.6061 |
| Loss Improvement | 98.4% |
| Initial Validation Loss | 172.6721 |
| Final Validation Loss | 16.3531 |
| Validation Improvement | 90.5% |


#### Convergence Assessment

- **Status**: Still improving (> 5% change)

- **Last 10 epochs change**: 6.94%



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
| Training Loss | 482939.4688 | Final epoch |
| Validation Loss | 456948.7812 | Final epoch |
| Loss Gap | -25990.6875 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 204.1451 | Mean Absolute Error (lower is better) |
| MSE | 480585.0625 | Mean Squared Error (lower is better) |
| RMSE | 693.2424 | Root Mean Squared Error (lower is better) |
| R2 | 0.3020 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 684016.3750 |
| Final Training Loss | 482939.4688 |
| Loss Improvement | 29.4% |
| Initial Validation Loss | 519719.3125 |
| Final Validation Loss | 456948.7812 |
| Validation Improvement | 12.1% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.48%



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
| Training Loss | 0.3086 | Final epoch |
| Validation Loss | 0.3102 | Final epoch |
| Loss Gap | 0.0016 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 0.2949 | Mean Absolute Error (lower is better) |
| MSE | 0.3131 | Mean Squared Error (lower is better) |
| RMSE | 0.5596 | Root Mean Squared Error (lower is better) |
| R2 | 0.2341 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 0.9653 |
| Final Training Loss | 0.3086 |
| Loss Improvement | 68.0% |
| Initial Validation Loss | 0.3586 |
| Final Validation Loss | 0.3102 |
| Validation Improvement | 13.5% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.27%



## Cross-Task Comparison

| Task | Model Type | Parameters | Train Loss | Val Loss | Gap |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Property Valuation | HousingValuationModel | 36,994 | 25103452160.0000 | 26845380608.0000 | 1741928448.0000 |
| Affordability Analysis | HousingAffordabilityModel | 10,306 | 229.1559 | 225.2091 | -3.9468 |
| Housing Quality | HousingQualityModel | 10,371 | 239.6061 | 16.3531 | -223.2529 |
| Cost Prediction | HousingDefaultModel | 10,306 | 482939.4688 | 456948.7812 | -25990.6875 |
| Occupancy Prediction | HousingDefaultModel | 10,306 | 0.3086 | 0.3102 | 0.0016 |


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

