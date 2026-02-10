# Machine Learning Models

> Machine learning analysis including clustering, time series forecasting, and regression modeling with comprehensive performance metrics.

## Regression Models

### Target Variable: **Property_Value**

#### Model Performance

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| Best Model | gradient_boosting | — |
| R² Score | 0.1542 | Poor fit |
| RMSE | 201,095.29 | Root Mean Square Error |
| MAE | 94,392.96 | Mean Absolute Error |
| Sample Weights | Applied | ACS weights used |


#### SHAP Feature Importance

> SHAP (SHapley Additive exPlanations) values show the contribution of each feature to predictions. Higher absolute values indicate stronger influence.


| Feature | SHAP Value | Impact |
| :--- | :--- | :--- |
| Year_Structure_Built | 49827.8357 | Positive |
| Number_of_Rooms | 25478.0363 | Positive |
| Housing_Unit_Weight | 18852.9287 | Positive |
| Building_Type | 15804.5081 | Positive |
| Number_of_Bedrooms | 11898.9650 | Positive |
| Number_of_Persons | 11080.3177 | Positive |
| Census_Division | 0.0000 | Negative |
| Census_Region | 0.0000 | Negative |
| Housing_Adjustment_Factor | 0.0000 | Negative |
| Housing_Unit_Type | 0.0000 | Negative |


#### Visualizations

![predictions HOUSING](figures/ml/regression/Property_Value/linear/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/linear/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/linear/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/linear/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/linear/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/linear/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/linear/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/linear/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Property_Value/ridge/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/ridge/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/ridge/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/ridge/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/ridge/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/ridge/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/ridge/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/ridge/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Property_Value/lasso/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/lasso/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/lasso/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/lasso/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/lasso/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/lasso/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/lasso/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/lasso/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Property_Value/random_forest/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/random_forest/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/random_forest/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/random_forest/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/random_forest/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/random_forest/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/random_forest/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/random_forest/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Property_Value/gradient_boosting/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/gradient_boosting/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/gradient_boosting/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/gradient_boosting/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/gradient_boosting/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/gradient_boosting/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/gradient_boosting/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/gradient_boosting/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/linear/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/linear/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/linear/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/linear/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/linear/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/linear/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/linear/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/linear/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/ridge/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/ridge/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/ridge/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/ridge/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/ridge/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/ridge/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/ridge/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/ridge/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/lasso/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/lasso/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/lasso/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/lasso/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/lasso/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/lasso/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/lasso/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/lasso/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/random_forest/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/random_forest/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/random_forest/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/random_forest/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/random_forest/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/random_forest/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/random_forest/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/random_forest/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/feature_target_correlation_HOUSING.png)

## Regression Models

### Target Variable: **Gross_Rent**

#### Model Performance

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| Best Model | random_forest | — |
| R² Score | 0.2325 | Poor fit |
| RMSE | 355.82 | Root Mean Square Error |
| MAE | 240.23 | Mean Absolute Error |
| Sample Weights | Applied | ACS weights used |


#### SHAP Feature Importance

> SHAP (SHapley Additive exPlanations) values show the contribution of each feature to predictions. Higher absolute values indicate stronger influence.


| Feature | SHAP Value | Impact |
| :--- | :--- | :--- |
| Year_Structure_Built | 96.6448 | Positive |
| Housing_Unit_Weight | 73.2912 | Positive |
| Number_of_Bedrooms | 59.6947 | Positive |
| Number_of_Rooms | 49.3805 | Positive |
| Number_of_Persons | 41.1697 | Positive |
| Building_Type | 37.9426 | Positive |
| Census_Division | 0.0000 | Negative |
| Census_Region | 0.0000 | Negative |
| Housing_Adjustment_Factor | 0.0000 | Negative |
| Housing_Unit_Type | 0.0000 | Negative |


#### Visualizations

![predictions HOUSING](figures/ml/regression/Property_Value/linear/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/linear/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/linear/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/linear/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/linear/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/linear/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/linear/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/linear/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Property_Value/ridge/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/ridge/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/ridge/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/ridge/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/ridge/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/ridge/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/ridge/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/ridge/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Property_Value/lasso/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/lasso/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/lasso/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/lasso/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/lasso/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/lasso/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/lasso/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/lasso/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Property_Value/random_forest/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/random_forest/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/random_forest/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/random_forest/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/random_forest/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/random_forest/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/random_forest/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/random_forest/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Property_Value/gradient_boosting/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Property_Value/gradient_boosting/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Property_Value/gradient_boosting/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Property_Value/gradient_boosting/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Property_Value/gradient_boosting/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Property_Value/gradient_boosting/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Property_Value/gradient_boosting/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Property_Value/gradient_boosting/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/linear/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/linear/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/linear/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/linear/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/linear/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/linear/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/linear/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/linear/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/ridge/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/ridge/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/ridge/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/ridge/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/ridge/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/ridge/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/ridge/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/ridge/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/lasso/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/lasso/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/lasso/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/lasso/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/lasso/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/lasso/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/lasso/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/lasso/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/random_forest/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/random_forest/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/random_forest/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/random_forest/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/random_forest/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/random_forest/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/random_forest/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/random_forest/feature_target_correlation_HOUSING.png)
![predictions HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/predictions_HOUSING.png)
![residuals HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/residuals_HOUSING.png)
![cv scores HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/cv_scores_HOUSING.png)
![features HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/features_HOUSING.png)
![error distribution HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/error_distribution_HOUSING.png)
![distribution comparison HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/distribution_comparison_HOUSING.png)
![variance comparison HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/variance_comparison_HOUSING.png)
![feature target correlation HOUSING](figures/ml/regression/Gross_Rent/gradient_boosting/feature_target_correlation_HOUSING.png)

## Clustering Analysis

### Clustering Configuration

| Parameter | Value | Description |
| :--- | :--- | :--- |
| Method | Kmeans | Clustering algorithm used |
| Number of Clusters | 5 | Optimal or specified K |
| Silhouette Score | 0.2843 | Weak structure |


### Cluster Size Distribution

| Cluster | Size | Percentage | Description |
| :--- | :--- | :--- | :--- |
| Cluster 0 | 10,857 | 31.1% | Major cluster |
| Cluster 1 | 2,345 | 6.7% | Minor cluster |
| Cluster 2 | 3,605 | 10.3% | Moderate cluster |
| Cluster 3 | 16,252 | 46.6% | Dominant cluster |
| Cluster 4 | 1,828 | 5.2% | Minor cluster |



> *Cluster distribution is imbalanced (CV: 81.2%).*



### Visualizations

![sizes HOUSING](figures/ml/clustering/kmeans/sizes_HOUSING.png)
![scatter HOUSING](figures/ml/clustering/kmeans/scatter_HOUSING.png)
![silhouette HOUSING](figures/ml/clustering/kmeans/silhouette_HOUSING.png)
![feature distributions HOUSING](figures/ml/clustering/kmeans/feature_distributions_HOUSING.png)
![variance by cluster HOUSING](figures/ml/clustering/kmeans/variance_by_cluster_HOUSING.png)
![sizes HOUSING](figures/ml/clustering/hierarchical/sizes_HOUSING.png)

## Time Series Forecasting

### Target Variable: **Property_Value**

#### Best Model Summary

| Metric | Value |
| :--- | :--- |
| Best Model | polynomial_degree_3 |
| R² Score | 0.9921 |
| Forecast Periods | 3 |


#### All Models Performance Comparison

| Model | R² | MAE | RMSE | MAPE | Rank |
| :--- | :--- | :--- | :--- | :--- | :--- |
| polynomial_degree_3 | 0.9921 | — | — | — | 1 |
| polynomial_degree_2 | 0.9326 | — | — | — | 2 |
| polynomial_degree_1 | 0.9170 | — | — | — | 3 |
| holt_winters | 0.7814 | — | — | — | 4 |
| sma | 0.6814 | — | — | — | 5 |
| wma | 0.6745 | — | — | — | 6 |
| arima | 0.5467 | — | — | — | 7 |
| ewma | 0.4227 | — | — | — | 8 |



> *The polynomial_degree_3 model achieved the best fit with R² = 0.9921. Models are ranked by R² score.*



#### Forecasted Values

| Period | Forecast | Lower CI | Upper CI |
| :--- | :--- | :--- | :--- |
| Period 1 | 318354.39 | — | — |
| Period 2 | 366213.92 | — | — |
| Period 3 | 424097.79 | — | — |


#### Visualizations

![forecast HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/sma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/sma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/sma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/sma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/sma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/ewma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/ewma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/ewma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/ewma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/ewma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/wma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/wma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/wma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/wma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/wma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/arima/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/arima/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/arima/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/arima/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/arima/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/holt_winters/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/holt_winters/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/holt_winters/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/holt_winters/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/holt_winters/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/sma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/sma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/sma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/sma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/sma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/ewma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/ewma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/ewma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/ewma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/ewma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/wma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/wma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/wma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/wma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/wma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/arima/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/arima/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/arima/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/arima/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/arima/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/confidence_intervals_HOUSING.png)

## Time Series Forecasting

### Target Variable: **Gross_Rent**

#### Best Model Summary

| Metric | Value |
| :--- | :--- |
| Best Model | polynomial_degree_3 |
| R² Score | 0.9830 |
| Forecast Periods | 3 |


#### All Models Performance Comparison

| Model | R² | MAE | RMSE | MAPE | Rank |
| :--- | :--- | :--- | :--- | :--- | :--- |
| polynomial_degree_3 | 0.9830 | — | — | — | 1 |
| polynomial_degree_2 | 0.9781 | — | — | — | 2 |
| wma | 0.9613 | — | — | — | 3 |
| holt_winters | 0.9502 | — | — | — | 4 |
| polynomial_degree_1 | 0.9354 | — | — | — | 5 |
| sma | 0.9225 | — | — | — | 6 |
| ewma | 0.7930 | — | — | — | 7 |
| arima | -0.6194 | — | — | — | 8 |



> *The polynomial_degree_3 model achieved the best fit with R² = 0.9830. Models are ranked by R² score.*



#### Forecasted Values

| Period | Forecast | Lower CI | Upper CI |
| :--- | :--- | :--- | :--- |
| Period 1 | 985.10 | — | — |
| Period 2 | 1046.20 | — | — |
| Period 3 | 1114.53 | — | — |


#### Visualizations

![forecast HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_1/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_2/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/polynomial_degree_3/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/sma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/sma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/sma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/sma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/sma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/ewma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/ewma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/ewma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/ewma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/ewma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/wma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/wma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/wma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/wma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/wma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/arima/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/arima/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/arima/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/arima/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/arima/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Property_Value/holt_winters/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Property_Value/holt_winters/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Property_Value/holt_winters/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Property_Value/holt_winters/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Property_Value/holt_winters/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_1/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_2/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/polynomial_degree_3/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/sma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/sma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/sma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/sma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/sma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/ewma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/ewma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/ewma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/ewma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/ewma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/wma/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/wma/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/wma/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/wma/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/wma/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/arima/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/arima/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/arima/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/arima/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/arima/confidence_intervals_HOUSING.png)
![forecast HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/forecast_HOUSING.png)
![residuals HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/residuals_HOUSING.png)
![trend decomposition HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/trend_decomposition_HOUSING.png)
![accuracy metrics HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/accuracy_metrics_HOUSING.png)
![confidence intervals HOUSING](figures/ml/time_series/Gross_Rent/holt_winters/confidence_intervals_HOUSING.png)

## Model Comparison

![model comparison cv HOUSING](figures/ml/model_comparison/model_comparison_cv_HOUSING.png)

![model comparison metrics HOUSING](figures/ml/model_comparison/model_comparison_metrics_HOUSING.png)

![model comparison scores HOUSING](figures/ml/model_comparison/model_comparison_scores_HOUSING.png)

