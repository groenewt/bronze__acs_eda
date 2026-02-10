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


- **('Presence_And_Age_Own_Children', 24.995420835835898)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.249119861975705)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 13.782832056952532)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 13.41849410643584)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 12.652381142275571)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 11.909959237881896)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 11.067495895180153)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 10.49481501003015)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 10.175445288429696)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.602856031253813)**: 0 outliers (0.00%)

- **('Other_Income', 8.269388873664017)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 8.255628837843984)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.21871400501389)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 8.049781451935898)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 7.373414230557088)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
