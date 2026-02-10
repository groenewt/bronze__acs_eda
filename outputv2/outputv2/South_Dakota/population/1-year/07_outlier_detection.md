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


- **('Total_Annual_Hours', 15.962802629469298)**: 0 outliers (0.00%)

- **('Hours_Worked_Per_Week', 14.038792935902253)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.06447963800905)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 11.117437209469928)**: 0 outliers (0.00%)

- **('Other_Income', 10.76154806491885)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 10.27134157327664)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 9.677489099491911)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.880075868609364)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.788715349998109)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 8.436452740441785)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 8.086915786818492)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 7.67395769521819)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 7.159173502232374)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 6.877589996756874)**: 0 outliers (0.00%)

- **('Supplemental_Security_Income', 6.33587786259542)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
