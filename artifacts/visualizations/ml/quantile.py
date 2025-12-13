"""Quantile Regression Visualizations"""
import numpy as np
import matplotlib.pyplot as plt
from .base import BaseMLVisualizer


class QuantileRegressionVisualizer(BaseMLVisualizer):
    """Visualizes quantile regression results showing how relationships differ across distribution"""

    def __init__(self, config, survey_type=""):
        super().__init__(config, survey_type)
        self.quantiles = [0.10, 0.25, 0.50, 0.75, 0.90]
        self.quantile_colors = {
            0.10: '#d62728',  # red
            0.25: '#ff7f0e',  # orange
            0.50: '#2ca02c',  # green
            0.75: '#1f77b4',  # blue
            0.90: '#9467bd',  # purple
        }

    def viz_quantile_regression(self, X, y, feature_name, target_name):
        """
        Create quantile regression plot showing how relationships differ across distribution.

        Args:
            X: Feature data (can be DataFrame or array)
            y: Target data (can be Series or array)
            feature_name: Name of the feature being visualized
            target_name: Name of the target variable
        """
        try:
            self.current_target = target_name

            # Convert to numpy arrays
            if hasattr(X, 'values'):
                X_arr = X.values.flatten() if len(X.shape) > 1 else X.values
            else:
                X_arr = np.array(X).flatten()

            if hasattr(y, 'values'):
                y_arr = y.values.flatten()
            else:
                y_arr = np.array(y).flatten()

            # Remove NaN values
            mask = ~(np.isnan(X_arr) | np.isnan(y_arr))
            X_arr = X_arr[mask]
            y_arr = y_arr[mask]

            if len(X_arr) < 50:
                print(f"[WARNING] Not enough data for quantile regression ({len(X_arr)} points)")
                return

            # Create plot
            plt.figure(figsize=(12, 8))

            # Scatter plot (sample if too many points)
            if len(X_arr) > 1000:
                sample_idx = np.random.choice(len(X_arr), 1000, replace=False)
                plt.scatter(X_arr[sample_idx], y_arr[sample_idx], alpha=0.3, s=20, color='gray', label='Data')
            else:
                plt.scatter(X_arr, y_arr, alpha=0.3, s=20, color='gray', label='Data')

            # Try statsmodels quantile regression first
            try:
                import statsmodels.api as sm
                from statsmodels.regression.quantile_regression import QuantReg

                X_with_const = sm.add_constant(X_arr)

                for q in self.quantiles:
                    model = QuantReg(y_arr, X_with_const)
                    result = model.fit(q=q)

                    # Get predictions for plotting
                    X_sorted = np.sort(X_arr)
                    X_sorted_const = sm.add_constant(X_sorted)
                    y_pred = result.predict(X_sorted_const)

                    label = f'Q{int(q*100)}' if q != 0.50 else 'Median (Q50)'
                    plt.plot(X_sorted, y_pred,
                            color=self.quantile_colors[q],
                            linewidth=2,
                            label=label)

            except ImportError:
                print("[WARNING] statsmodels not available, using simple quantile regression")
                self._quantile_regression_simple(X_arr, y_arr)

            plt.xlabel(feature_name, fontweight='bold')
            plt.ylabel(target_name, fontweight='bold')
            plt.title(f'Quantile Regression: {feature_name} vs {target_name}',
                     fontweight='bold', fontsize=14)
            plt.legend(loc='best')
            plt.grid(True, alpha=0.3)

            self._save(f'quantile_regression_{target_name.lower()}.png', 'regression')

        except Exception as e:
            print(f"[WARNING] Quantile regression visualization failed: {e}")

    def _quantile_regression_simple(self, x, y):
        """
        Simple quantile regression approximation when statsmodels is not available.
        Bins x into groups and takes quantile of y in each bin.
        """
        # Create 20 bins
        bins = np.percentile(x, np.linspace(0, 100, 21))
        bin_indices = np.digitize(x, bins)

        for q in self.quantiles:
            x_points = []
            y_points = []

            # Calculate quantile for each bin
            for i in range(1, len(bins)):
                mask = bin_indices == i
                if np.sum(mask) > 0:
                    x_bin_center = (bins[i-1] + bins[i]) / 2
                    y_quantile = np.percentile(y[mask], q * 100)
                    x_points.append(x_bin_center)
                    y_points.append(y_quantile)

            if len(x_points) > 1:
                # Fit linear regression through quantile points
                coeffs = np.polyfit(x_points, y_points, 1)
                x_sorted = np.sort(x)
                y_pred = np.polyval(coeffs, x_sorted)

                label = f'Q{int(q*100)}' if q != 0.50 else 'Median (Q50)'
                plt.plot(x_sorted, y_pred,
                        color=self.quantile_colors[q],
                        linewidth=2,
                        label=label)

    def viz_quantile_coefficients(self, X, y, feature_names, target_name):
        """
        Visualize how coefficients change across quantiles.
        Shows if relationship is stronger for low vs high values.

        Args:
            X: Feature data (DataFrame or array)
            y: Target data
            feature_names: List of feature names
            target_name: Name of target variable
        """
        try:
            self.current_target = target_name

            # Convert to numpy array
            if hasattr(X, 'values'):
                X_arr = X.values
            else:
                X_arr = np.array(X)

            if hasattr(y, 'values'):
                y_arr = y.values.flatten()
            else:
                y_arr = np.array(y).flatten()

            # Remove NaN values
            mask = ~(np.isnan(y_arr) | np.any(np.isnan(X_arr), axis=1))
            X_arr = X_arr[mask]
            y_arr = y_arr[mask]

            if len(X_arr) < 50:
                print(f"[WARNING] Not enough data for quantile coefficients ({len(X_arr)} points)")
                return

            # Try statsmodels quantile regression
            try:
                import statsmodels.api as sm
                from statsmodels.regression.quantile_regression import QuantReg

                X_with_const = sm.add_constant(X_arr)

                # Store coefficients for each quantile
                coefficients = {name: [] for name in feature_names}

                for q in self.quantiles:
                    model = QuantReg(y_arr, X_with_const)
                    result = model.fit(q=q)

                    # Store coefficients (skip intercept)
                    for i, name in enumerate(feature_names):
                        coefficients[name].append(result.params[i + 1])

                # Create plot
                num_features = len(feature_names)
                fig, axes = plt.subplots(1, min(num_features, 3),
                                        figsize=(15, 5) if num_features > 1 else (8, 5))

                # Handle single subplot case
                if num_features == 1:
                    axes = [axes]
                elif num_features > 1:
                    axes = axes.flatten()

                # Plot first 3 features
                for idx, name in enumerate(feature_names[:3]):
                    ax = axes[idx] if num_features > 1 else axes[0]

                    quantile_labels = [f'Q{int(q*100)}' for q in self.quantiles]
                    colors = [self.quantile_colors[q] for q in self.quantiles]

                    ax.bar(quantile_labels, coefficients[name], color=colors, alpha=0.7)
                    ax.set_xlabel('Quantile', fontweight='bold')
                    ax.set_ylabel('Coefficient', fontweight='bold')
                    ax.set_title(f'{name}', fontweight='bold')
                    ax.grid(True, alpha=0.3, axis='y')
                    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

                plt.suptitle(f'Quantile Regression Coefficients: {target_name}',
                           fontweight='bold', fontsize=14)
                plt.tight_layout()

                self._save(f'quantile_coefficients_{target_name.lower()}.png', 'regression')

            except ImportError:
                print("[WARNING] statsmodels not available, cannot create quantile coefficient plot")

        except Exception as e:
            print(f"[WARNING] Quantile coefficients visualization failed: {e}")
