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

- Training Loss: 1501247360.0000

- Validation Loss: 1486390400.0000

- Overfitting Risk: LOW (gap: -14856960.0000)

- MAE: 18235.6934

- MSE: 1467154816.0000

- RMSE: 38303.4570

- R2: 0.2234



## Task: Employment Analysis

### Model Details

- Model Type: PopulationEmploymentModel

- Task Type: multi_output

- Target Variables: Hours_Worked_Per_Week, Employment_Status_Recode, Weeks_Worked_Past_Year

- Architecture: 6 layers, 10,371 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 26.1349

- Validation Loss: 25.7661

- Overfitting Risk: LOW (gap: -0.3688)

- MAE: 1.9430

- MSE: 25.8358

- RMSE: 5.0829

- R2: 0.3282



## Task: Demographic Profile

### Model Details

- Model Type: PopulationDemographicModel

- Task Type: multi_output

- Target Variables: Educational_Attainment, Age, Sex, Marital_Status

- Architecture: 7 layers, 10,436 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 618.6898

- Validation Loss: 620.7686

- Overfitting Risk: HIGH RISK (gap: 2.0787)

- MAE: 15.0953

- MSE: 618.5122

- RMSE: 24.8699

- R2: -5.7642



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
