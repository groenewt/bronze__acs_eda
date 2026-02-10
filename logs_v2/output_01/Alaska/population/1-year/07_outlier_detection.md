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


- **('Hours_Worked_Per_Week', 17.79900675955304)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 14.357132354485685)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 13.072813907605257)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.54569944198576)**: 0 outliers (0.00%)

- **('Other_Income', 11.239839045072781)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 10.291106726724491)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.642403808012693)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 8.33116182109221)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 7.918884711312958)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 7.794177865465509)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 7.783701447067784)**: 0 outliers (0.00%)

- **('Presence_And_Age_Own_Children', 7.1865691849444895)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 7.017086699177306)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 6.8894752272060975)**: 0 outliers (0.00%)

- **('Flag_Hours_Worked', 6.617838662844805)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
