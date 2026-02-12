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


- **('Hours_Worked_Per_Week', 34.269192983455305)**: 0 outliers (0.00%)

- **('Presence_And_Age_Own_Children', 23.63935509794551)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 16.31197758942572)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.54956760540216)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 13.787666996419375)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 13.086201645989343)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 12.453208846956281)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 11.850858460426837)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 11.33721974960231)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 10.674403764856025)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 9.16302709205397)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.345145287030476)**: 0 outliers (0.00%)

- **('Supplemental_Security_Income', 7.335438426038378)**: 0 outliers (0.00%)

- **('Other_Income', 6.941890582675921)**: 0 outliers (0.00%)

- **('Flag_Hours_Worked', 6.791833986218481)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
