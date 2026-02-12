# Deep Learning Models

> Neural network analysis using TensorFlow/Keras for complex pattern recognition and multi-output prediction tasks.

## Deep Learning Summary

- **Total Tasks**: 3

- **Tasks**: Income Prediction, Employment Analysis, Demographic Profile


### Aggregate Statistics

| Metric | Value |
| :--- | :--- |
| Total Parameters | 57,930 |
| Average Validation Loss | 1127092964.4537 |
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
| Training Loss | 3421129216.0000 | Final epoch |
| Validation Loss | 3381278208.0000 | Final epoch |
| Loss Gap | -39851008.0000 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 26439.3906 | Mean Absolute Error (lower is better) |
| MSE | 3380765440.0000 | Mean Squared Error (lower is better) |
| RMSE | 58144.3500 | Root Mean Squared Error (lower is better) |
| R2 | 0.2517 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 4105297408.0000 |
| Final Training Loss | 3421129216.0000 |
| Loss Improvement | 16.7% |
| Initial Validation Loss | 3692422144.0000 |
| Final Validation Loss | 3381278208.0000 |
| Validation Improvement | 8.4% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.07%



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
| Training Loss | 69.5855 | Final epoch |
| Validation Loss | 68.4737 | Final epoch |
| Loss Gap | -1.1118 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 3.5421 | Mean Absolute Error (lower is better) |
| MSE | 68.8730 | Mean Squared Error (lower is better) |
| RMSE | 8.2990 | Root Mean Squared Error (lower is better) |
| R2 | 0.3342 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 83.5981 |
| Final Training Loss | 69.5855 |
| Loss Improvement | 16.8% |
| Initial Validation Loss | 70.0111 |
| Final Validation Loss | 68.4737 |
| Validation Improvement | 2.2% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.03%



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
| Training Loss | 618.5008 | Final epoch |
| Validation Loss | 616.8874 | Final epoch |
| Loss Gap | -1.6134 | NONE overfitting risk |



> *Good generalization*



#### Test Set Metrics

| Metric | Value | Description |
| :--- | :--- | :--- |
| MAE | 15.1648 | Mean Absolute Error (lower is better) |
| MSE | 619.0957 | Mean Squared Error (lower is better) |
| RMSE | 24.8816 | Root Mean Squared Error (lower is better) |
| R2 | -5.5121 | R-squared (higher is better) |


### Training Analysis

| Training Statistic | Value |
| :--- | :--- |
| Epochs Trained | 75 |
| Initial Training Loss | 618.0831 |
| Final Training Loss | 618.5008 |
| Loss Improvement | -0.1% |
| Initial Validation Loss | 616.3734 |
| Final Validation Loss | 616.8874 |
| Validation Improvement | -0.1% |


#### Convergence Assessment

- **Status**: Fully converged (< 1% change in last 10 epochs)

- **Last 10 epochs change**: 0.01%



## Cross-Task Comparison

| Task | Model Type | Parameters | Train Loss | Val Loss | Gap |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Income Prediction | PopulationIncomeModel | 37,123 | 3421129216.0000 | 3381278208.0000 | -39851008.0000 |
| Employment Analysis | PopulationEmploymentModel | 10,371 | 69.5855 | 68.4737 | -1.1118 |
| Demographic Profile | PopulationDemographicModel | 10,436 | 618.5008 | 616.8874 | -1.6134 |


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

