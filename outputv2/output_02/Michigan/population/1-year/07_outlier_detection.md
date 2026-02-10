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


- **('Presence_And_Age_Own_Children', 23.533403569657906)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.460236926012987)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.90232493192767)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 12.237336705862278)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 11.163158634326523)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 10.946478668252558)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 10.22950260216705)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 9.614593213789227)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 9.289134133305229)**: 0 outliers (0.00%)

- **('Other_Income', 9.202559759845034)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.490869839060577)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.05452837940952)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 8.0)**: 0 outliers (0.00%)

- **('Supplemental_Security_Income', 7.8557487579843865)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 7.654941816200353)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
