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


- **('Presence_And_Age_Own_Children', 22.556553272319118)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 16.87325701735675)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 15.07507863968188)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.066827069259547)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 13.4933823965814)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 12.818564899994064)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 12.005309526103385)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 11.813757493026293)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 11.5227434257285)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 11.2095673333729)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 10.957920351356163)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 8.723366371891506)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.1739833019122)**: 0 outliers (0.00%)

- **('Supplemental_Security_Income', 7.792207792207792)**: 0 outliers (0.00%)

- **('Other_Income', 7.690677966101695)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
