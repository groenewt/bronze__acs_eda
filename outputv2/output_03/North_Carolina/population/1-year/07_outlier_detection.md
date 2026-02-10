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


- **('Presence_And_Age_Own_Children', 24.265792383058212)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 19.67546947847032)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 16.035038618247604)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 13.233755203275358)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.972800800846349)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 11.297581210643903)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 11.225327011457093)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 10.325445217067058)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 9.797568969489394)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 9.409932409994557)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.99442449434668)**: 0 outliers (0.00%)

- **('Other_Income', 8.751953815787973)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.625374878560468)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 7.92995335321557)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 7.751664012324018)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
