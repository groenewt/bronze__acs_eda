# Deep Learning Models (TensorFlow CPU)

## Deep Learning Summary

- Total Tasks: 3

- Tasks: income_prediction, employment_analysis, demographic_profile


## Task: Income Prediction

### Model Details

- Model Type: PopulationIncomeModel

- Task Type: multi_output

- Target Variables: Total_Person_Income, Wage_Income, Total_Person_Earnings

- Architecture: 7 layers, 37,123 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 2508335104.0000

- Validation Loss: 2310097920.0000

- Overfitting Risk: LOW (gap: -198237184.0000)

- MAE: 25616.1777

- MSE: 2531907840.0000

- RMSE: 50318.0667

- R2: 0.1933



## Task: Employment Analysis

### Model Details

- Model Type: PopulationEmploymentModel

- Task Type: multi_output

- Target Variables: Hours_Worked_Per_Week, Employment_Status_Recode, Weeks_Worked_Past_Year

- Architecture: 6 layers, 10,371 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 30.2269

- Validation Loss: 29.7533

- Overfitting Risk: LOW (gap: -0.4736)

- MAE: 2.2794

- MSE: 30.7024

- RMSE: 5.5410

- R2: 0.3223



## Task: Demographic Profile

### Model Details

- Model Type: PopulationDemographicModel

- Task Type: multi_output

- Target Variables: Educational_Attainment, Age, Sex, Marital_Status

- Architecture: 7 layers, 10,436 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 684.5654

- Validation Loss: 685.3240

- Overfitting Risk: HIGH RISK (gap: 0.7587)

- MAE: 16.0942

- MSE: 686.2633

- RMSE: 26.1966

- R2: -6.3273



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
