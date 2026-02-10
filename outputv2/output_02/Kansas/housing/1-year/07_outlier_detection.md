# Outlier Detection

> Statistical outlier detection using IQR (Interquartile Range) method. Outliers are values falling outside Q1 - 1.5×IQR or Q3 + 1.5×IQR bounds.

## Detection Methodology

| Parameter | Value | Description |
| :--- | :--- | :--- |
| Method | IQR | Outlier detection algorithm |
| Lower Bound | Q1 - 1.5 × IQR | Values below are outliers |
| Upper Bound | Q3 + 1.5 × IQR | Values above are outliers |
| IQR Definition | Q3 - Q1 | Interquartile Range |



> **Note**: The IQR method is robust to extreme values and works well for approximately symmetric distributions.


## Outlier Summary

_No outlier summary available._
## High Outlier Rate Variables

> Variables with outlier rate > 5% may indicate data quality issues, non-normal distributions, or genuinely extreme values.


- **('Specified_Rent_Unit', 24.44617893292501)**: 0 outliers (0.00%)

- **('Flag_Selected_Monthly_Owner_Costs', 22.906152321414957)**: 0 outliers (0.00%)

- **('Flag_Family_Income', 18.85986842105263)**: 0 outliers (0.00%)

- **('Property_Tax_Rate', 17.732219764870212)**: 0 outliers (0.00%)

- **('Fuel_Cost_Monthly', 11.10923207010531)**: 0 outliers (0.00%)

- **('Flag_Property_Taxes', 10.809503561177847)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 9.344547045225232)**: 0 outliers (0.00%)

- **('Gross_Rent_Percentage_Income', 9.309547715226376)**: 0 outliers (0.00%)

- **('Working_Age_Persons', 9.170034526135481)**: 0 outliers (0.00%)

- **('Structure_Age', 8.8996846792909)**: 0 outliers (0.00%)

- **('Property_Taxes_Yearly', 8.632132974709263)**: 0 outliers (0.00%)

- **('Flag_Water_Cost', 8.533210332103321)**: 0 outliers (0.00%)

- **('Structure_Age_Score', 7.417164166338802)**: 0 outliers (0.00%)

- **('Flag_Gross_Rent', 7.291537475712101)**: 0 outliers (0.00%)

- **('Owner_Costs_Percentage_Income', 7.003640416585245)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 HOUSING](figures/box_plots_1_HOUSING.png)

![figures - box plots 2 HOUSING](figures/box_plots_2_HOUSING.png)

![figures - box plots 3 HOUSING](figures/box_plots_3_HOUSING.png)

![figures - box plots 4 HOUSING](figures/box_plots_4_HOUSING.png)

![figures - outlier detection 1 HOUSING](figures/outlier_detection_1_HOUSING.png)

![figures - outlier detection 2 HOUSING](figures/outlier_detection_2_HOUSING.png)

![figures - outlier detection 3 HOUSING](figures/outlier_detection_3_HOUSING.png)
