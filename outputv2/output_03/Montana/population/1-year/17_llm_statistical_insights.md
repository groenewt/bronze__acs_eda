# model: granite3.1-moe:3b-instruct-fp16, Engine: ROCm llama.cpp, GPU: AMD RX 9060 XT -- AI-Generated Insights: Statistical Analysis

1. **MEAN vs MEDIAN for each variable:** 
    The Mean is a measure of central tendency that considers all values in the dataset, whereas the Median represents the middle value when the data is arranged in order. In many distributions, including some income-related variables, the Median tends to be more resilient against outliers and skewness than the Mean. For instance, if a variable has a few extremely high or low values (outliers), these can significantly affect the Mean but have little impact on the Median.
    - **Income per Hour** shows that while its Mean is 24.95, the Median is slightly lower at 16.03, indicating that half of the workers earn less than this figure and half earn more. This suggests a relatively low skewness in income distribution for hourly wages.
    - **Total Annual Hours** shows that while its Mean is 332.51 hours per year (a substantial amount), the Median is around 50 hours, suggesting that many workers fall into the category of working less than or equal to 50 hours a week.

2. **SKEWNESS values:** 
    SKEWNESS measures the asymmetry of the probability distribution about its mean. High positive SKEWNESS indicates a left-skewed distribution, meaning there are more low values than high ones, and vice versa for negative skewness.
    - For example, in the **Income per Hour** data, the SKEWNESS is 41.851, indicating an extremely left-skewed distribution where the majority of workers earn far less than the mean hourly wage.

3. **KURTOSIS:** 
    KURTOSIS measures the "tailedness" or the extent to which extreme values are clustered at the tails (outliers). High positive kurtosis suggests heavy-tailed distributions, meaning there are more extreme values on one side of the distribution than would be expected in a normal distribution.
    - In our income data, **Poverty Gap** has a high positive kurtosis value (1.254), indicating that many individuals experience significant financial hardship relative to their median earnings.

4. **Variance/STD DEV:** 
    Variance is the square of the standard deviation and measures how spread out values are in a dataset, while Standard Deviation represents the actual distance between each data point and the mean. Higher variance or standard deviation indicate greater dispersion among the data points.
    - In our income-related variables (Income per Hour, Total Annual Hours), both have high variance/standard deviation. This suggests that a substantial portion of individuals fall outside their calculated mean incomes or hours worked, indicating a significant degree of variation across the dataset.

5. **Key Insights:** 
    - The data shows highly skewed distributions for many variables, particularly with respect to Income per Hour and Total Annual Hours, suggesting potential inequalities in earnings distribution and working hours.
    - There are heavy tails or outliers observed across most income-related variables (Income per Hour, Poverty Gap), indicating that extreme values significantly impact the overall distributions.
    - The high kurtosis found for **Poverty Gap** suggests a considerable amount of financial hardship among individuals in this dataset relative to their median earnings, highlighting an urgent need for targeted policies addressing poverty.
