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


- **('First_Mortgage_Includes_Taxes', 18.249210906601764)**: 0 outliers (0.00%)

- **('Working_Age_Persons', 10.896767493388234)**: 0 outliers (0.00%)

- **('Flag_Property_Taxes', 10.323065350441842)**: 0 outliers (0.00%)

- **('Fuel_Cost_Monthly', 9.804035426331932)**: 0 outliers (0.00%)

- **('Property_Tax_Rate', 9.294410709147902)**: 0 outliers (0.00%)

- **('Gross_Rent_Percentage_Income', 9.03996573192271)**: 0 outliers (0.00%)

- **('Flag_Property_Value', 7.560635949494908)**: 0 outliers (0.00%)

- **('Owner_Costs_Percentage_Income', 7.522942375582453)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 6.909864494958941)**: 0 outliers (0.00%)

- **('Property_Value', 6.779924092640978)**: 0 outliers (0.00%)

- **('Flag_Water_Cost', 6.6193152419707)**: 0 outliers (0.00%)

- **('Insurance_Cost_Yearly', 6.3044316193016074)**: 0 outliers (0.00%)

- **('Income_to_FPL_Ratio', 5.763001833768014)**: 0 outliers (0.00%)

- **('Family_Income', 5.629989180501162)**: 0 outliers (0.00%)

- **('Household_Income', 5.556832364554505)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 HOUSING](figures/box_plots_1_HOUSING.png)

![figures - box plots 2 HOUSING](figures/box_plots_2_HOUSING.png)

![figures - box plots 3 HOUSING](figures/box_plots_3_HOUSING.png)

![figures - box plots 4 HOUSING](figures/box_plots_4_HOUSING.png)

![figures - outlier detection 1 HOUSING](figures/outlier_detection_1_HOUSING.png)

![figures - outlier detection 2 HOUSING](figures/outlier_detection_2_HOUSING.png)

![figures - outlier detection 3 HOUSING](figures/outlier_detection_3_HOUSING.png)
