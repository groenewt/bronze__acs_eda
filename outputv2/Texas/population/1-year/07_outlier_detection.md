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


- **('Hours_Worked_Per_Week', 19.551619732825504)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 16.20837027343547)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 13.630945053414212)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.798070242950008)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 10.97582181896366)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 10.767829144175444)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 10.052237602125007)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 9.703922427438973)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 9.373262444915195)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 9.232655065606226)**: 0 outliers (0.00%)

- **('Other_Income', 8.973062287202083)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 8.730542395823262)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.50430210788736)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 7.934146616938681)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 7.207439628880112)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
