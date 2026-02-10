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


- **('Hours_Worked_Per_Week', 34.21087643439215)**: 0 outliers (0.00%)

- **('Presence_And_Age_Own_Children', 23.385564002828854)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 16.78879510249513)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 16.494427200902933)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 14.132600874717832)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 13.408225169300225)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 12.83022361738149)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 12.238554599322798)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 11.714341139954854)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 10.7329107204197)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 9.580011992099323)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.704409963487336)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.064247669773634)**: 0 outliers (0.00%)

- **('Flag_Hours_Worked', 7.089006066591422)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 6.587150312544218)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
