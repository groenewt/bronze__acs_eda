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


- **('Presence_And_Age_Own_Children', 23.928226905667305)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.626604808224634)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 14.270726160865092)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.732336352360225)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 11.761283526712974)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 10.507010352672353)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 10.183828901082844)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 9.494213379933633)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 8.892474519197041)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.849389347793037)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 8.579473256959057)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.462949260598325)**: 0 outliers (0.00%)

- **('Other_Income', 8.039348056707492)**: 0 outliers (0.00%)

- **('Supplemental_Security_Income', 7.439957720840103)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 6.826898275644715)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
