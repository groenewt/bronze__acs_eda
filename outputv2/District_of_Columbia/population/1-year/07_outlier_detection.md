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


- **('Hours_Worked_Per_Week', 29.648784990213084)**: 0 outliers (0.00%)

- **('Presence_And_Age_Own_Children', 17.678197426868284)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 17.009290665093644)**: 0 outliers (0.00%)

- **('Total_Annual_Hours', 15.475279042591772)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 15.165904733815072)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 14.42953350046699)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 14.188664405446591)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 13.64498844811483)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 13.370692621540577)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.628496666874339)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 10.958069114683184)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 9.94618667656337)**: 0 outliers (0.00%)

- **('Other_Income', 9.386845039018953)**: 0 outliers (0.00%)

- **('Flag_Hours_Worked', 8.673253699061103)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 8.557961783439492)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
