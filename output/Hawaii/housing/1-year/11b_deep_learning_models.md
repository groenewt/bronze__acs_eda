# Deep Learning Models (TensorFlow CPU)

## Deep Learning Summary

- Total Tasks: 5

- Tasks: property_valuation, affordability_analysis, housing_quality, cost_prediction, occupancy_prediction


## Task: Property Valuation

### Model Details

- Model Type: HousingValuationModel

- Task Type: multi_output

- Target Variables: Property_Value, Gross_Rent

- Architecture: 7 layers, 36,994 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 147889520640.0000

- Validation Loss: 160155844608.0000

- Overfitting Risk: HIGH RISK (gap: 12266323968.0000)

- MAE: 109360.9141

- MSE: 129321295872.0000

- RMSE: 359612.7026

- R2: -0.1553



## Task: Affordability Analysis

### Model Details

- Model Type: HousingAffordabilityModel

- Task Type: multi_output

- Target Variables: Owner_Costs_Percentage_Income, Gross_Rent_Percentage_Income

- Architecture: 6 layers, 10,306 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 232.4762

- Validation Loss: 222.4762

- Overfitting Risk: LOW (gap: -10.0000)

- MAE: 8.0073

- MSE: 245.6810

- RMSE: 15.6742

- R2: 0.0533



## Task: Housing Quality

### Model Details

- Model Type: HousingQualityModel

- Task Type: multi_output

- Target Variables: Year_Structure_Built, Number_of_Bedrooms, Number_of_Rooms

- Architecture: 6 layers, 10,371 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 0.0694

- Validation Loss: 0.0239

- Overfitting Risk: LOW (gap: -0.0455)

- MAE: 0.0924

- MSE: 0.0221

- RMSE: 0.1487

- R2: 0.9934



## Task: Cost Prediction

### Model Details

- Model Type: HousingDefaultModel

- Task Type: multi_output

- Target Variables: Property_Taxes_Yearly, Insurance_Cost_Yearly

- Architecture: 6 layers, 10,306 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 452514.0625

- Validation Loss: 450546.1562

- Overfitting Risk: LOW (gap: -1967.9062)

- MAE: 258.9522

- MSE: 447613.5625

- RMSE: 669.0393

- R2: 0.0526



## Task: Occupancy Prediction

### Model Details

- Model Type: HousingDefaultModel

- Task Type: multi_output

- Target Variables: Vacancy_Status, Tenure

- Architecture: 6 layers, 10,306 parameters

- Input Features: 10 features

- Training Epochs: 75


### Performance Metrics

- Training Loss: 0.4438

- Validation Loss: 0.4548

- Overfitting Risk: LOW (gap: 0.0111)

- MAE: 0.3612

- MSE: 0.4209

- RMSE: 0.6487

- R2: 0.1670



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
