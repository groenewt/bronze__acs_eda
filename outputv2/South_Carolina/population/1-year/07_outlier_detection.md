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


- **('Presence_And_Age_Own_Children', 23.161671773562105)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 22.340676153911872)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.809658080412865)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 14.377910060706075)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.741267787839586)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 12.206431410333614)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 12.146852842218014)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 11.281233904177162)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 10.712226547184944)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 10.21266345668446)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 9.18002771595347)**: 0 outliers (0.00%)

- **('Other_Income', 8.78289260308331)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 8.729139922978177)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 8.432353340627971)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.373910616257792)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
