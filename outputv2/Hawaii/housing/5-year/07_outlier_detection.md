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


- **('First_Mortgage_Includes_Taxes', 21.903785017525745)**: 0 outliers (0.00%)

- **('Gas_Cost_Monthly', 21.793317675581484)**: 0 outliers (0.00%)

- **('Mobile_Home_Costs_Monthly', 16.608996539792386)**: 0 outliers (0.00%)

- **('Flag_Property_Taxes', 11.851920574304248)**: 0 outliers (0.00%)

- **('Property_Value', 7.5374335678214655)**: 0 outliers (0.00%)

- **('Owner_Costs_Percentage_Income', 7.483416884072805)**: 0 outliers (0.00%)

- **('Flag_Property_Value', 6.244029156521979)**: 0 outliers (0.00%)

- **('Flag_Water_Cost', 6.0339056149122525)**: 0 outliers (0.00%)

- **('Income_to_FPL_Ratio', 5.4298108584978815)**: 0 outliers (0.00%)

- **('Family_Income', 5.3466486658195675)**: 0 outliers (0.00%)

- **('Fuel_Cost_Monthly', 5.251613328375281)**: 0 outliers (0.00%)

- **('Household_Income', 5.24973704409131)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 HOUSING](figures/box_plots_1_HOUSING.png)

![figures - box plots 2 HOUSING](figures/box_plots_2_HOUSING.png)

![figures - box plots 3 HOUSING](figures/box_plots_3_HOUSING.png)

![figures - box plots 4 HOUSING](figures/box_plots_4_HOUSING.png)

![figures - outlier detection 1 HOUSING](figures/outlier_detection_1_HOUSING.png)

![figures - outlier detection 2 HOUSING](figures/outlier_detection_2_HOUSING.png)

![figures - outlier detection 3 HOUSING](figures/outlier_detection_3_HOUSING.png)
