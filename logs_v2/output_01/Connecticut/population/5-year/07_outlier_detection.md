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


- **('Total_Annual_Hours', 17.698113097503327)**: 0 outliers (0.00%)

- **('Flag_Wage_Income', 13.415410541732836)**: 0 outliers (0.00%)

- **('Interest_Dividend_Rental_Income', 12.844424069874053)**: 0 outliers (0.00%)

- **('Flag_Interest_Dividend_Income', 11.994497172992029)**: 0 outliers (0.00%)

- **('Flag_Social_Security_Income', 11.23701435244429)**: 0 outliers (0.00%)

- **('Flag_Retirement_Income', 10.322377575417205)**: 0 outliers (0.00%)

- **('Flag_Other_Income', 9.795317194758733)**: 0 outliers (0.00%)

- **('Flag_Supplemental_Security_Income', 9.499392055415434)**: 0 outliers (0.00%)

- **('Other_Income', 8.390176369640772)**: 0 outliers (0.00%)

- **('Public_Assistance_Income', 8.368404408008368)**: 0 outliers (0.00%)

- **('Self_Employment_Income', 8.069824635661064)**: 0 outliers (0.00%)

- **('Flag_Self_Employment_Income', 7.532547826161988)**: 0 outliers (0.00%)

- **('Income_Per_Hour', 6.966458499354775)**: 0 outliers (0.00%)

- **('Income_Adjustment_Factor', 6.501649384983675)**: 0 outliers (0.00%)

- **('Supplemental_Security_Income', 6.443639067001208)**: 0 outliers (0.00%)



> *Consider investigating these variables for data entry errors, applying transformations, or using robust statistical methods.*


## Visualizations

![figures - box plots 1 POPULATION](figures/box_plots_1_POPULATION.png)

![figures - box plots 2 POPULATION](figures/box_plots_2_POPULATION.png)

![figures - box plots 3 POPULATION](figures/box_plots_3_POPULATION.png)

![figures - box plots 4 POPULATION](figures/box_plots_4_POPULATION.png)

![figures - outlier detection 1 POPULATION](figures/outlier_detection_1_POPULATION.png)

![figures - outlier detection 2 POPULATION](figures/outlier_detection_2_POPULATION.png)

![figures - outlier detection 3 POPULATION](figures/outlier_detection_3_POPULATION.png)
