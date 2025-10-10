# Deep Learning Models (TensorFlow CPU)

## Deep Learning Summary

- Total Tasks: 3

- Tasks: affordability_analysis, cost_prediction, occupancy_prediction


## Task: Affordability Analysis

### Model Details

- Model Type: HousingAffordabilityModel

- Task Type: multi_output

- Target Variables: Owner_Costs_Percentage_Income, Gross_Rent_Percentage_Income

- Architecture: 6 layers, 10,306 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 192.3811

- Validation Loss: 195.3496

- Overfitting Risk: HIGH RISK (gap: 2.9685)

- MAE: 6.8172

- MSE: 197.6771

- RMSE: 14.0598

- R2: 0.0399



## Task: Cost Prediction

### Model Details

- Model Type: HousingDefaultModel

- Task Type: multi_output

- Target Variables: Property_Taxes_Yearly, Insurance_Cost_Yearly

- Architecture: 6 layers, 10,306 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 18101.6484

- Validation Loss: 16530.0098

- Overfitting Risk: LOW (gap: -1571.6387)

- MAE: 23.6075

- MSE: 14654.3066

- RMSE: 121.0550

- R2: 0.0078



## Task: Occupancy Prediction

### Model Details

- Model Type: HousingDefaultModel

- Task Type: multi_output

- Target Variables: Vacancy_Status, Tenure

- Architecture: 6 layers, 10,306 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 0.3916

- Validation Loss: 0.3922

- Overfitting Risk: LOW (gap: 0.0006)

- MAE: 0.3270

- MSE: 0.3818

- RMSE: 0.6179

- R2: 0.2352



## Visualizations

![affordability analysis/training history housing](figures/ml/deep_learning/affordability_analysis/training_history_housing.png)
![affordability analysis/predictions vs actual housing](figures/ml/deep_learning/affordability_analysis/predictions_vs_actual_housing.png)
![affordability analysis/residual analysis housing](figures/ml/deep_learning/affordability_analysis/residual_analysis_housing.png)
![affordability analysis/error distribution housing](figures/ml/deep_learning/affordability_analysis/error_distribution_housing.png)
![affordability analysis/architecture summary housing](figures/ml/deep_learning/affordability_analysis/architecture_summary_housing.png)
![affordability analysis/Owner Costs Percentage Income detailed analysis housing](figures/ml/deep_learning/affordability_analysis/Owner_Costs_Percentage_Income_detailed_analysis_housing.png)
![affordability analysis/Gross Rent Percentage Income detailed analysis housing](figures/ml/deep_learning/affordability_analysis/Gross_Rent_Percentage_Income_detailed_analysis_housing.png)
![affordability analysis/affordability analysis convergence diagnostics housing](figures/ml/deep_learning/affordability_analysis/affordability_analysis_convergence_diagnostics_housing.png)
![affordability analysis/affordability analysis error evolution housing](figures/ml/deep_learning/affordability_analysis/affordability_analysis_error_evolution_housing.png)
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
