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


- **('Hours_Worked_Per_Week', 16.741636418359175)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.86719219389725)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.472157553639967)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 10.91365754285403)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 10.400351250508855)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 9.883155619359918)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 9.400531888688853)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 9.100449741348053)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 9.00157215717423)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 8.884244864672002)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 8.523356343814093)**: 0 outliers (0.00%)

- **('Supplemental_Security_Income', 8.434162298506285)**: 0 outliers (0.00%)

- **('Other_Income', 8.215111903899217)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.040900907021776)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 6.718978438681296)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
