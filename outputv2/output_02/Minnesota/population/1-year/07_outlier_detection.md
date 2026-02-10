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


- **('Total_Annual_Hours', 15.528709141823407)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.32928773846014)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 11.451158422041328)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 11.035761607419136)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 10.514259418152719)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 10.065184940023281)**: 0 outliers (0.00%)

- **('Other_Income', 9.788118595237227)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 9.141986650178689)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.829384978788758)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 8.79537641440892)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 8.410682123956798)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 7.674026630709591)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 6.678353450147559)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 6.664256187808795)**: 0 outliers (0.00%)

- **('Supplemental_Security_Income', 6.049237983587339)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
