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

- Training Loss: 2179601408.0000

- Validation Loss: 2181482240.0000

- Overfitting Risk: HIGH RISK (gap: 1880832.0000)

- MAE: 21021.9082

- MSE: 2198808576.0000

- RMSE: 46891.4553

- R2: 0.2130



## Task: Employment Analysis

### Model Details

- Model Type: PopulationEmploymentModel

- Task Type: multi_output

- Target Variables: Hours_Worked_Per_Week, Employment_Status_Recode, Weeks_Worked_Past_Year

- Architecture: 6 layers, 10,371 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 25.4279

- Validation Loss: 25.3475

- Overfitting Risk: LOW (gap: -0.0804)

- MAE: 1.8742

- MSE: 25.5595

- RMSE: 5.0556

- R2: 0.3138



## Task: Demographic Profile

### Model Details

- Model Type: PopulationDemographicModel

- Task Type: multi_output

- Target Variables: Educational_Attainment, Age, Sex, Marital_Status

- Architecture: 7 layers, 10,436 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 601.6516

- Validation Loss: 602.2299

- Overfitting Risk: HIGH RISK (gap: 0.5782)

- MAE: 15.0232

- MSE: 603.3424

- RMSE: 24.5630

- R2: -5.6848



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
