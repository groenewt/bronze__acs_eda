# Machine Learning Models

> Machine learning analysis including clustering, time series forecasting, and regression modeling with comprehensive performance metrics.

## Regression Models

### Target Variable: **Property_Value**

#### Model Performance

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| Best Model | gradient_boosting | — |
| R² Score | 0.2488 | Poor fit |
| RMSE | 249,124.13 | Root Mean Square Error |
| MAE | 124,371.24 | Mean Absolute Error |
| Sample Weights | Applied | ACS weights used |


#### SHAP Feature Importance

> SHAP (SHapley Additive exPlanations) values show the contribution of each feature to predictions. Higher absolute values indicate stronger influence.


| Feature | SHAP Value | Impact |
| :--- | :--- | :--- |
| Number_of_Rooms | 44119.5763 | Positive |
| Number_of_Bedrooms | 40079.4646 | Positive |
| Year_Structure_Built | 30930.3490 | Positive |
| Housing_Unit_Weight | 25003.4466 | Positive |
| Building_Type | 18062.0375 | Positive |
| Number_of_Persons | 9969.4922 | Positive |
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
| Best Model | gradient_boosting | — |
| R² Score | 0.2586 | Poor fit |
| RMSE | 521.74 | Root Mean Square Error |
| MAE | 369.39 | Mean Absolute Error |
| Sample Weights | Applied | ACS weights used |


#### SHAP Feature Importance

> SHAP (SHapley Additive exPlanations) values show the contribution of each feature to predictions. Higher absolute values indicate stronger influence.


| Feature | SHAP Value | Impact |
| :--- | :--- | :--- |
| Year_Structure_Built | 112.3935 | Positive |
| Number_of_Bedrooms | 103.8711 | Positive |
| Number_of_Persons | 85.8001 | Positive |
| Building_Type | 79.9852 | Positive |
| Housing_Unit_Weight | 49.0961 | Positive |
| Number_of_Rooms | 38.9503 | Positive |
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
| Method | Hierarchical | Clustering algorithm used |
| Number of Clusters | 5 | Optimal or specified K |
| Silhouette Score | 0.3342 | Weak structure |


### Cluster Size Distribution

| Cluster | Size | Percentage | Description |
| :--- | :--- | :--- | :--- |
| Cluster 0 | 9,449 | 63.0% | Dominant cluster |
| Cluster 1 | 1,139 | 7.6% | Minor cluster |
| Cluster 2 | 568 | 3.8% | Minor cluster |
| Cluster 3 | 1,461 | 9.7% | Minor cluster |
| Cluster 4 | 2,383 | 15.9% | Moderate cluster |



> *Cluster distribution is imbalanced (CV: 109.3%).*



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
| R² Score | 0.9954 |
| Forecast Periods | 3 |


#### All Models Performance Comparison

| Model | R² | MAE | RMSE | MAPE | Rank |
| :--- | :--- | :--- | :--- | :--- | :--- |
| polynomial_degree_3 | 0.9954 | — | — | — | 1 |
| polynomial_degree_2 | 0.9387 | — | — | — | 2 |
| polynomial_degree_1 | 0.7791 | — | — | — | 3 |
| holt_winters | 0.5904 | — | — | — | 4 |
| sma | 0.5312 | — | — | — | 5 |
| wma | 0.4821 | — | — | — | 6 |
| arima | 0.3193 | — | — | — | 7 |
| ewma | 0.2217 | — | — | — | 8 |



> *The polynomial_degree_3 model achieved the best fit with R² = 0.9954. Models are ranked by R² score.*



#### Forecasted Values

| Period | Forecast | Lower CI | Upper CI |
| :--- | :--- | :--- | :--- |
| Period 1 | 327643.58 | — | — |
| Period 2 | 362493.77 | — | — |
| Period 3 | 406322.97 | — | — |


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
| R² Score | 0.9937 |
| Forecast Periods | 3 |


#### All Models Performance Comparison

| Model | R² | MAE | RMSE | MAPE | Rank |
| :--- | :--- | :--- | :--- | :--- | :--- |
| polynomial_degree_3 | 0.9937 | — | — | — | 1 |
| polynomial_degree_2 | 0.9866 | — | — | — | 2 |
| holt_winters | 0.9781 | — | — | — | 3 |
| wma | 0.9633 | — | — | — | 4 |
| polynomial_degree_1 | 0.9354 | — | — | — | 5 |
| sma | 0.9267 | — | — | — | 6 |
| ewma | 0.7910 | — | — | — | 7 |
| arima | -0.9735 | — | — | — | 8 |



> *The polynomial_degree_3 model achieved the best fit with R² = 0.9937. Models are ranked by R² score.*



#### Forecasted Values

| Period | Forecast | Lower CI | Upper CI |
| :--- | :--- | :--- | :--- |
| Period 1 | 1425.10 | — | — |
| Period 2 | 1514.64 | — | — |
| Period 3 | 1615.49 | — | — |


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

