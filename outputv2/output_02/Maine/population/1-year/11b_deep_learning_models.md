# Deep Learning Models

> Neural network analysis using TensorFlow/Keras for complex pattern recognition and multi-output prediction tasks.

## Deep Learning Summary

- **Total Tasks**: 3

- **Tasks**: Income Prediction, Employment Analysis, Demographic Profile


### Aggregate Statistics

| Metric | Value |
| :--- | :--- |
| Total Parameters | 57,930 |
| Average Validation Loss | 425732607.0653 |
| Number of Tasks | 3 |


## Task: Income Prediction

### Model Configuration

| Property | Value |
| :--- | :--- |
| Model Type | PopulationIncomeModel |
| Task Type | Multi_Output |
| Target Variables | Total_Person_Income, Wage_Income, Total_Person_Earnings |
| Number of Targets | 3 |
| Input Features | 10 |


### Network Architecture

| Component | Value | Notes |
| :--- | :--- | :--- |
| Total Layers | 7 | Including input and output |
| Total Parameters | 37,123 | Trainable weights |
| Parameters per Layer | 5,303 | Average |


### Performance Metrics

| Metric | Value | Assessment |
| :--- | :--- | :--- |
| Training Loss | 1219155200.0000 | Final epoch |
| Validation Loss | 1277197056.0000 | Final epoch |
| Loss Gap | 58041856.0000 | HIGH overfitting risk |



> *Model may be overfitting significantly*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 16997.4922 | Mean Absolute Error (lower is better) |
| MSE | 1238232704.0000 | Mean Squared Error (lower is better) |
| RMSE | 35188.5309 | Root Mean Squared Error (lower is better) |
| R2 | 0.1997 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 1912197888.0000 |
| Final Training Loss | 1219155200.0000 |
| Loss Improvement | 36.2% |
| Initial Validation Loss | 1578100352.0000 |
| Final Validation Loss | 1277197056.0000 |
| Validation Improvement | 19.1% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.17%



## Task: Employment Analysis

### Model Configuration

| Property | Value |
| :--- | :--- |
| Model Type | PopulationEmploymentModel |
| Task Type | Multi_Output |
| Target Variables | Hours_Worked_Per_Week, Employment_Status_Recode, Weeks_Worked_Past_Year |
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
| Training Loss | 72.5529 | Final epoch |
| Validation Loss | 70.7001 | Final epoch |
| Loss Gap | -1.8529 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 3.7899 | Mean Absolute Error (lower is better) |
| MSE | 72.6128 | Mean Squared Error (lower is better) |
| RMSE | 8.5213 | Root Mean Squared Error (lower is better) |
| R2 | 0.3139 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 133.2054 |
| Final Training Loss | 72.5529 |
| Loss Improvement | 45.5% |
| Initial Validation Loss | 76.6873 |
| Final Validation Loss | 70.7001 |
| Validation Improvement | 7.8% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.07%



## Task: Demographic Profile

### Model Configuration

| Property | Value |
| :--- | :--- |
| Model Type | PopulationDemographicModel |
| Task Type | Multi_Output |
| Target Variables | Educational_Attainment, Age, Sex, Marital_Status |
| Number of Targets | 4 |
| Input Features | 10 |


### Network Architecture

| Component | Value | Notes |
| :--- | :--- | :--- |
| Total Layers | 7 | Including input and output |
| Total Parameters | 10,436 | Trainable weights |
| Parameters per Layer | 1,490 | Average |


### Performance Metrics

| Metric | Value | Assessment |
| :--- | :--- | :--- |
| Training Loss | 693.4257 | Final epoch |
| Validation Loss | 694.4957 | Final epoch |
| Loss Gap | 1.0701 | HIGH overfitting risk |



> *Model may be overfitting significantly*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 16.0269 | Mean Absolute Error (lower is better) |
| MSE | 695.0637 | Mean Squared Error (lower is better) |
| RMSE | 26.3641 | Root Mean Squared Error (lower is better) |
| R2 | -5.9829 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 694.2396 |
| Final Training Loss | 693.4257 |
| Loss Improvement | 0.1% |
| Initial Validation Loss | 694.6808 |
| Final Validation Loss | 694.4957 |
| Validation Improvement | 0.0% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.00%



## Cross-Task Comparison

| Task | Model Type | Parameters | Train Loss | Val Loss | Gap |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Income Prediction | PopulationIncomeModel | 37,123 | 1219155200.0000 | 1277197056.0000 | 58041856.0000 |
| Employment Analysis | PopulationEmploymentModel | 10,371 | 72.5529 | 70.7001 | -1.8529 |
| Demographic Profile | PopulationDemographicModel | 10,436 | 693.4257 | 694.4957 | 1.0701 |


## Visualizations

![income prediction/training history population](figures/ml/deep_learning/income_prediction/training_history_population.png)

![income prediction/predictions vs actual population](figures/ml/deep_learning/income_prediction/predictions_vs_actual_population.png)

![income prediction/residual analysis population](figures/ml/deep_learning/income_prediction/residual_analysis_population.png)

![income prediction/error distribution population](figures/ml/deep_learning/income_prediction/error_distribution_population.png)

![income prediction/architecture summary population](figures/ml/deep_learning/income_prediction/architecture_summary_population.png)

![income prediction/Total Person Income detailed analysis population](figures/ml/deep_learning/income_prediction/Total_Person_Income_detailed_analysis_population.png)

![income prediction/Wage Income detailed analysis population](figures/ml/deep_learning/income_prediction/Wage_Income_detailed_analysis_population.png)

![income prediction/Total Person Earnings detailed analysis population](figures/ml/deep_learning/income_prediction/Total_Person_Earnings_detailed_analysis_population.png)

![income prediction/income prediction convergence diagnostics population](figures/ml/deep_learning/income_prediction/income_prediction_convergence_diagnostics_population.png)

![income prediction/income prediction error evolution population](figures/ml/deep_learning/income_prediction/income_prediction_error_evolution_population.png)

![employment analysis/training history population](figures/ml/deep_learning/employment_analysis/training_history_population.png)

![employment analysis/predictions vs actual population](figures/ml/deep_learning/employment_analysis/predictions_vs_actual_population.png)

![employment analysis/residual analysis population](figures/ml/deep_learning/employment_analysis/residual_analysis_population.png)

![employment analysis/error distribution population](figures/ml/deep_learning/employment_analysis/error_distribution_population.png)

![employment analysis/architecture summary population](figures/ml/deep_learning/employment_analysis/architecture_summary_population.png)

![employment analysis/Hours Worked Per Week detailed analysis population](figures/ml/deep_learning/employment_analysis/Hours_Worked_Per_Week_detailed_analysis_population.png)

![employment analysis/Employment Status Recode detailed analysis population](figures/ml/deep_learning/employment_analysis/Employment_Status_Recode_detailed_analysis_population.png)

![employment analysis/Weeks Worked Past Year detailed analysis population](figures/ml/deep_learning/employment_analysis/Weeks_Worked_Past_Year_detailed_analysis_population.png)

![employment analysis/employment analysis convergence diagnostics population](figures/ml/deep_learning/employment_analysis/employment_analysis_convergence_diagnostics_population.png)

![employment analysis/employment analysis error evolution population](figures/ml/deep_learning/employment_analysis/employment_analysis_error_evolution_population.png)

![demographic profile/training history population](figures/ml/deep_learning/demographic_profile/training_history_population.png)

![demographic profile/predictions vs actual population](figures/ml/deep_learning/demographic_profile/predictions_vs_actual_population.png)

![demographic profile/residual analysis population](figures/ml/deep_learning/demographic_profile/residual_analysis_population.png)

![demographic profile/error distribution population](figures/ml/deep_learning/demographic_profile/error_distribution_population.png)

![demographic profile/architecture summary population](figures/ml/deep_learning/demographic_profile/architecture_summary_population.png)

![demographic profile/Educational Attainment detailed analysis population](figures/ml/deep_learning/demographic_profile/Educational_Attainment_detailed_analysis_population.png)

![demographic profile/Age detailed analysis population](figures/ml/deep_learning/demographic_profile/Age_detailed_analysis_population.png)

![demographic profile/Sex detailed analysis population](figures/ml/deep_learning/demographic_profile/Sex_detailed_analysis_population.png)

![demographic profile/Marital Status detailed analysis population](figures/ml/deep_learning/demographic_profile/Marital_Status_detailed_analysis_population.png)

![demographic profile/demographic profile convergence diagnostics population](figures/ml/deep_learning/demographic_profile/demographic_profile_convergence_diagnostics_population.png)

![demographic profile/demographic profile error evolution population](figures/ml/deep_learning/demographic_profile/demographic_profile_error_evolution_population.png)

![learning curves comparison population](figures/ml/deep_learning/learning_curves_comparison_population.png)

![model comparison population](figures/ml/deep_learning/model_comparison_population.png)

![comprehensive performance dashboard population](figures/ml/deep_learning/comprehensive_performance_dashboard_population.png)

![comprehensive performance dashboard population](figures/ml/deep_learning/comprehensive_performance_dashboard_population.png)

