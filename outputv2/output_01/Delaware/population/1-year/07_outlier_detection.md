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


- **('Presence_And_Age_Own_Children', 21.36625757799793)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 16.191720311363696)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.655234536598387)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 14.501575879284859)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.821789573270925)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 12.766714082503555)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 12.314171756896215)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 11.64477170669121)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 10.81081081081081)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 10.483083702897943)**: 0 outliers (0.00%)

- **('Other_Income', 9.052126383148913)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 8.898847631241997)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.832637056581648)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 8.417705631327923)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.327053504144686)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
