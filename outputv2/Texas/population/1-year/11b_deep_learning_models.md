# Deep Learning Models

> Neural network analysis using TensorFlow/Keras for complex pattern recognition and multi-output prediction tasks.

## Deep Learning Summary

- **Total Tasks**: 3

- **Tasks**: Income Prediction, Employment Analysis, Demographic Profile


### Aggregate Statistics

| Metric | Value |
| :--- | :--- |
| Total Parameters | 57,930 |
| Average Validation Loss | 662105342.0653 |
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
| Training Loss | 2038813568.0000 | Final epoch |
| Validation Loss | 1986315392.0000 | Final epoch |
| Loss Gap | -52498176.0000 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 19736.8008 | Mean Absolute Error (lower is better) |
| MSE | 2033919616.0000 | Mean Squared Error (lower is better) |
| RMSE | 45098.9979 | Root Mean Squared Error (lower is better) |
| R2 | 0.2367 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 2267489280.0000 |
| Final Training Loss | 2038813568.0000 |
| Loss Improvement | 10.1% |
| Initial Validation Loss | 2096109568.0000 |
| Final Validation Loss | 1986315392.0000 |
| Validation Improvement | 5.2% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.11%



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
| Training Loss | 68.5246 | Final epoch |
| Validation Loss | 68.4873 | Final epoch |
| Loss Gap | -0.0373 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 3.4143 | Mean Absolute Error (lower is better) |
| MSE | 68.1111 | Mean Squared Error (lower is better) |
| RMSE | 8.2529 | Root Mean Squared Error (lower is better) |
| R2 | 0.3053 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 76.6391 |
| Final Training Loss | 68.5246 |
| Loss Improvement | 10.6% |
| Initial Validation Loss | 69.3682 |
| Final Validation Loss | 68.4873 |
| Validation Improvement | 1.3% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.02%



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
| Training Loss | 566.0463 | Final epoch |
| Validation Loss | 565.7086 | Final epoch |
| Loss Gap | -0.3376 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 14.3682 | Mean Absolute Error (lower is better) |
| MSE | 565.3602 | Mean Squared Error (lower is better) |
| RMSE | 23.7773 | Root Mean Squared Error (lower is better) |
| R2 | -5.1653 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 564.5401 |
| Final Training Loss | 566.0463 |
| Loss Improvement | -0.3% |
| Initial Validation Loss | 564.1548 |
| Final Validation Loss | 565.7086 |
| Validation Improvement | -0.3% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.03%



## Cross-Task Comparison

| Task | Model Type | Parameters | Train Loss | Val Loss | Gap |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Income Prediction | PopulationIncomeModel | 37,123 | 2038813568.0000 | 1986315392.0000 | -52498176.0000 |
| Employment Analysis | PopulationEmploymentModel | 10,371 | 68.5246 | 68.4873 | -0.0373 |
| Demographic Profile | PopulationDemographicModel | 10,436 | 566.0463 | 565.7086 | -0.3376 |


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

