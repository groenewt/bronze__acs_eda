# Deep Learning Models (TensorFlow CPU)

## Deep Learning Summary

- Total Tasks: 2

- Tasks: cost_prediction, occupancy_prediction


## Task: Cost Prediction

### Model Details

- Model Type: HousingDefaultModel

- Task Type: multi_output

- Target Variables: Property_Taxes_Yearly, Insurance_Cost_Yearly

- Architecture: 6 layers, 10,306 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 14558.2627

- Validation Loss: 19991.2422

- Overfitting Risk: HIGH RISK (gap: 5432.9795)

- MAE: 21.8725

- MSE: 12326.1377

- RMSE: 111.0231

- R2: 0.0326



## Task: Occupancy Prediction

### Model Details

- Model Type: HousingDefaultModel

- Task Type: multi_output

- Target Variables: Vacancy_Status, Tenure

- Architecture: 6 layers, 10,306 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 0.3728

- Validation Loss: 0.3704

- Overfitting Risk: LOW (gap: -0.0024)

- MAE: 0.3423

- MSE: 0.3786

- RMSE: 0.6153

- R2: 0.3742



## Visualizations

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
