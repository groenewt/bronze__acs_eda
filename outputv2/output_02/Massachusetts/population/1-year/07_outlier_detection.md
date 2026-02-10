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


- **('Presence_And_Age_Own_Children', 24.20924736935973)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.31102479832686)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 15.196387475541712)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 14.065115063947598)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 13.482016750923224)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 12.570449397534622)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.439147328862829)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 12.081873244151101)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 11.793499016225699)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 9.186610509739321)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 9.045666421336698)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.724559784431966)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 8.109184172740093)**: 0 outliers (0.00%)

- **('Other_Income', 7.491969630603008)**: 0 outliers (0.00%)

- **('Flag_Hours_Worked', 7.314491190480295)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
