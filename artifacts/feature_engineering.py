"""
Feature Engineering Module for Census Data Analysis
Provides feature creation, selection, transformation, and encoding capabilities
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
import warnings
warnings.filterwarnings('ignore')

# Import zero exclusion function from processing
from processing import should_exclude_zeros

try:
    from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
    from sklearn.feature_selection import SelectKBest, f_regression, f_classif, mutual_info_regression, mutual_info_classif
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("[WARNING] scikit-learn not available. Feature engineering will be limited.")


# ============================================================================
# NULL AND ZERO HANDLING
# ============================================================================

class SmartDataCleaner:
    """Intelligent handling of nulls and zeros in census data"""
    
    @staticmethod
    def handle_economic_zeros(df: pd.DataFrame, economic_cols: List[str],
                              strategy: str = 'filter') -> pd.DataFrame:
        """
        Handle zeros in economic variables intelligently
        
        Args:
            df: Input dataframe
            economic_cols: List of economic columns (income, rent, etc.)
            strategy: 'filter' (remove zeros), 'impute' (replace with median), 
                     'flag' (keep but add flag column), 'keep' (do nothing)
        """
        df_clean = df.copy()
        
        for col in economic_cols:
            if col not in df_clean.columns:
                continue
                
            if strategy == 'filter':
                # Remove rows where economic value is zero (likely not applicable)
                df_clean = df_clean[df_clean[col] > 0]
                
            elif strategy == 'impute':
                # Replace zeros with median of non-zero values
                non_zero_median = df_clean[df_clean[col] > 0][col].median()
                df_clean.loc[df_clean[col] == 0, col] = non_zero_median
                
            elif strategy == 'flag':
                # Keep zeros but add a binary flag column
                # Handle NA values: treat NA as not zero (0), zero as 1, non-zero as 0
                df_clean[f'{col}_is_zero'] = (df_clean[col] == 0).fillna(False).astype(int)
                
            # 'keep' does nothing
            
        return df_clean
    
    @staticmethod
    def distinguish_null_vs_zero(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """
        Create separate indicators for null vs zero values
        Useful for understanding missingness patterns
        """
        df_enhanced = df.copy()
        
        for col in cols:
            if col not in df_enhanced.columns:
                continue
            df_enhanced[f'{col}_is_null'] = df_enhanced[col].isna().astype(int)
            df_enhanced[f'{col}_is_zero'] = (df_enhanced[col] == 0).fillna(False).astype(int)
            
        return df_enhanced
    
    @staticmethod
    def impute_missing(df: pd.DataFrame, strategy: str = 'median') -> pd.DataFrame:
        """
        Impute missing values intelligently
        
        Args:
            strategy: 'median', 'mean', 'mode', 'forward_fill', 'backward_fill'
        """
        df_imputed = df.copy()
        numeric_cols = df_imputed.select_dtypes(include=[np.number]).columns
        
        # Exclude temporal, ID, and categorical-like columns from imputation
        exclude_patterns = ['Year', 'ID', 'SERIALNO', 'PUMA', 'State', 'Sex', 'Nativity']
        cols_to_impute = [col for col in numeric_cols 
                         if not any(pattern in col for pattern in exclude_patterns)]
        
        print(f"[VERBOSE] Imputing {len(cols_to_impute)} columns, excluding {len(numeric_cols) - len(cols_to_impute)} temporal/ID columns")
        
        for col in cols_to_impute:
            if df_imputed[col].isna().sum() == 0:
                continue
                
            if strategy == 'median':
                fill_value = df_imputed[col].median()
                if pd.notna(fill_value):
                    df_imputed[col].fillna(fill_value, inplace=True)
            elif strategy == 'mean':
                fill_value = df_imputed[col].mean()
                if pd.notna(fill_value):
                    df_imputed[col].fillna(fill_value, inplace=True)
            elif strategy == 'mode':
                mode_vals = df_imputed[col].mode()
                if len(mode_vals) > 0:
                    df_imputed[col].fillna(mode_vals[0], inplace=True)
            elif strategy == 'forward_fill':
                df_imputed[col].fillna(method='ffill', inplace=True)
            elif strategy == 'backward_fill':
                df_imputed[col].fillna(method='bfill', inplace=True)
                
        return df_imputed


# ============================================================================
# FEATURE CREATION
# ============================================================================

class FeatureCreator:
    """Create new features from existing census data"""
    
    @staticmethod
    def create_ratio_features(df: pd.DataFrame, numerators: List[str],
                             denominators: List[str]) -> pd.DataFrame:
        """Create ratio features from pairs of columns"""
        df_enhanced = df.copy()
        
        for num in numerators:
            for denom in denominators:
                if num in df_enhanced.columns and denom in df_enhanced.columns:
                    # Avoid division by zero
                    mask = df_enhanced[denom] != 0
                    feature_name = f'{num}_to_{denom}_ratio'
                    df_enhanced[feature_name] = np.nan
                    df_enhanced.loc[mask, feature_name] = (
                        df_enhanced.loc[mask, num] / df_enhanced.loc[mask, denom]
                    )
                    
        return df_enhanced
    
    @staticmethod
    def create_income_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create income-related derived features"""
        df_enhanced = df.copy()
        
        # Income per hour worked
        if 'Total_Person_Income' in df_enhanced.columns and 'Hours_Worked_Per_Week' in df_enhanced.columns:
            mask = (df_enhanced['Hours_Worked_Per_Week'] > 0) & (df_enhanced['Total_Person_Income'] > 0)
            df_enhanced['Income_Per_Hour'] = np.nan
            # Assuming 52 weeks per year
            df_enhanced.loc[mask, 'Income_Per_Hour'] = (
                df_enhanced.loc[mask, 'Total_Person_Income'] / 
                (df_enhanced.loc[mask, 'Hours_Worked_Per_Week'] * 52)
            )
        
        # Income per week worked
        if 'Total_Person_Income' in df_enhanced.columns and 'Weeks_Worked_Past_Year' in df_enhanced.columns:
            mask = (df_enhanced['Weeks_Worked_Past_Year'] > 0) & (df_enhanced['Total_Person_Income'] > 0)
            df_enhanced['Income_Per_Week_Worked'] = np.nan
            df_enhanced.loc[mask, 'Income_Per_Week_Worked'] = (
                df_enhanced.loc[mask, 'Total_Person_Income'] / 
                df_enhanced.loc[mask, 'Weeks_Worked_Past_Year']
            )
        
        # Total annual hours worked
        if 'Hours_Worked_Per_Week' in df_enhanced.columns and 'Weeks_Worked_Past_Year' in df_enhanced.columns:
            mask = (df_enhanced['Hours_Worked_Per_Week'] > 0) & (df_enhanced['Weeks_Worked_Past_Year'] > 0)
            df_enhanced['Total_Annual_Hours'] = np.nan
            df_enhanced.loc[mask, 'Total_Annual_Hours'] = (
                df_enhanced.loc[mask, 'Hours_Worked_Per_Week'] * df_enhanced.loc[mask, 'Weeks_Worked_Past_Year']
            )
        
        return df_enhanced
    
    @staticmethod
    def create_housing_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create housing-related derived features"""
        df_enhanced = df.copy()
        
        # Rent to property value ratio
        if 'Gross_Rent' in df_enhanced.columns and 'Property_Value' in df_enhanced.columns:
            mask = df_enhanced['Property_Value'] > 0
            df_enhanced['Annual_Rent_to_Value_Ratio'] = np.nan
            df_enhanced.loc[mask, 'Annual_Rent_to_Value_Ratio'] = (
                (df_enhanced.loc[mask, 'Gross_Rent'] * 12) / 
                df_enhanced.loc[mask, 'Property_Value']
            )
        
        # Total monthly housing cost
        cost_cols = ['Electricity_Cost_Monthly', 'Gas_Cost_Monthly']
        available_cost_cols = [col for col in cost_cols if col in df_enhanced.columns]
        if available_cost_cols:
            df_enhanced['Total_Monthly_Utility_Cost'] = df_enhanced[available_cost_cols].sum(axis=1)
        
        # Property tax as percentage of value
        if 'Property_Taxes_Yearly' in df_enhanced.columns and 'Property_Value' in df_enhanced.columns:
            mask = df_enhanced['Property_Value'] > 0
            df_enhanced['Property_Tax_Rate'] = np.nan
            df_enhanced.loc[mask, 'Property_Tax_Rate'] = (
                df_enhanced.loc[mask, 'Property_Taxes_Yearly'] / 
                df_enhanced.loc[mask, 'Property_Value'] * 100
            )
        
        return df_enhanced
    
    @staticmethod
    def create_age_groups(df: pd.DataFrame, age_col: str = 'Age') -> pd.DataFrame:
        """Create age group categories"""
        df_enhanced = df.copy()
        
        if age_col not in df_enhanced.columns:
            return df_enhanced
        
        # Filter out NA values before pd.cut to avoid "boolean value of NA is ambiguous" error
        valid_age_mask = df_enhanced[age_col].notna()
        
        bins = [0, 18, 25, 35, 45, 55, 65, 100]
        labels = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        
        # Initialize Age_Group column with NaN
        df_enhanced['Age_Group'] = pd.NA
        
        # Apply pd.cut only to valid (non-NA) age values
        if valid_age_mask.any():
            df_enhanced.loc[valid_age_mask, 'Age_Group'] = pd.cut(
                df_enhanced.loc[valid_age_mask, age_col], 
                bins=bins, 
                labels=labels, 
                right=False
            )
        
        return df_enhanced
    
    @staticmethod
    def create_temporal_features(df: pd.DataFrame, year_col: str = 'Census_Year') -> pd.DataFrame:
        """Create temporal features from year"""
        df_enhanced = df.copy()
        
        if year_col not in df_enhanced.columns:
            return df_enhanced
        
        # Years since earliest year in dataset
        min_year = df_enhanced[year_col].min()
        df_enhanced['Years_Since_Start'] = df_enhanced[year_col] - min_year
        
        # Decade
        df_enhanced['Decade'] = (df_enhanced[year_col] // 10) * 10
        
        return df_enhanced
    
    @staticmethod
    def create_interaction_features(df: pd.DataFrame, 
                                   col_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
        """Create interaction features (products) between column pairs"""
        df_enhanced = df.copy()
        
        for col1, col2 in col_pairs:
            if col1 in df_enhanced.columns and col2 in df_enhanced.columns:
                feature_name = f'{col1}_x_{col2}'
                df_enhanced[feature_name] = df_enhanced[col1] * df_enhanced[col2]
        
        return df_enhanced
    
    @staticmethod
    def create_polynomial_features(df: pd.DataFrame, cols: List[str],
                                  degree: int = 2) -> pd.DataFrame:
        """Create polynomial features (squared, cubed, etc.)"""
        df_enhanced = df.copy()
        
        for col in cols:
            if col not in df_enhanced.columns:
                continue
            for d in range(2, degree + 1):
                df_enhanced[f'{col}_power_{d}'] = df_enhanced[col] ** d
        
        return df_enhanced


# ============================================================================
# FEATURE SELECTION
# ============================================================================

class FeatureSelector:
    """Select most important features for modeling"""
    
    @staticmethod
    def select_by_correlation(df: pd.DataFrame, target_col: str,
                            threshold: float = 0.1, top_k: Optional[int] = None) -> List[str]:
        """Select features based on correlation with target"""
        numeric_df = df.select_dtypes(include=[np.number])

        if target_col not in numeric_df.columns:
            return []

        # Filter zeros for each column before correlation
        df_filtered = numeric_df.copy()
        for col in numeric_df.columns:
            if should_exclude_zeros(col):
                numeric_col = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered.loc[numeric_col <= 0, col] = np.nan

        # Calculate correlations
        correlations = df_filtered.corr()[target_col].abs().sort_values(ascending=False)
        
        # Remove target itself
        correlations = correlations.drop(target_col, errors='ignore')
        
        # Filter by threshold
        selected = correlations[correlations >= threshold].index.tolist()
        
        # Limit to top k if specified
        if top_k is not None:
            selected = selected[:top_k]
        
        return selected
    
    @staticmethod
    def select_by_variance(df: pd.DataFrame, threshold: float = 0.01) -> List[str]:
        """Remove low-variance features"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calculate variance
        variances = numeric_df.var()
        
        # Select features above threshold
        selected = variances[variances > threshold].index.tolist()
        
        return selected
    
    @staticmethod
    def select_by_mutual_information(df: pd.DataFrame, target_col: str,
                                    task: str = 'regression', top_k: int = 10) -> List[str]:
        """Select features using mutual information"""
        if not SKLEARN_AVAILABLE:
            return []
        
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        if target_col not in numeric_df.columns:
            return []
        
        X = numeric_df.drop(columns=[target_col])
        y = numeric_df[target_col]
        
        # Calculate mutual information
        if task == 'regression':
            mi_scores = mutual_info_regression(X, y, random_state=42)
        else:
            mi_scores = mutual_info_classif(X, y, random_state=42)
        
        # Create feature importance dataframe
        mi_df = pd.DataFrame({'feature': X.columns, 'mi_score': mi_scores})
        mi_df = mi_df.sort_values('mi_score', ascending=False)
        
        return mi_df.head(top_k)['feature'].tolist()
    
    @staticmethod
    def select_by_sklearn(df: pd.DataFrame, target_col: str,
                         task: str = 'regression', k: int = 10) -> List[str]:
        """Select top k features using sklearn's SelectKBest"""
        if not SKLEARN_AVAILABLE:
            return []
        
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        if target_col not in numeric_df.columns:
            return []
        
        X = numeric_df.drop(columns=[target_col])
        y = numeric_df[target_col]
        
        # Select score function
        score_func = f_regression if task == 'regression' else f_classif
        
        # Fit selector
        selector = SelectKBest(score_func=score_func, k=min(k, X.shape[1]))
        selector.fit(X, y)
        
        # Get selected features
        selected_mask = selector.get_support()
        selected_features = X.columns[selected_mask].tolist()
        
        return selected_features


# ============================================================================
# FEATURE TRANSFORMATION
# ============================================================================

class FeatureTransformer:
    """Transform features for better model performance"""
    
    @staticmethod
    def log_transform(df: pd.DataFrame, cols: List[str],
                     add_constant: float = 1.0) -> pd.DataFrame:
        """Apply log transformation to skewed features"""
        df_transformed = df.copy()
        
        for col in cols:
            if col not in df_transformed.columns:
                continue
            # Add constant to handle zeros, then log transform
            df_transformed[f'{col}_log'] = np.log(df_transformed[col] + add_constant)
        
        return df_transformed
    
    @staticmethod
    def sqrt_transform(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """Apply square root transformation"""
        df_transformed = df.copy()
        
        for col in cols:
            if col not in df_transformed.columns:
                continue
            # Only transform non-negative values
            mask = df_transformed[col] >= 0
            df_transformed[f'{col}_sqrt'] = np.nan
            df_transformed.loc[mask, f'{col}_sqrt'] = np.sqrt(df_transformed.loc[mask, col])
        
        return df_transformed
    
    @staticmethod
    def box_cox_transform(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """Apply Box-Cox transformation for normalization"""
        try:
            from scipy.stats import boxcox
        except ImportError:
            print("[WARNING] scipy not available for Box-Cox transformation")
            return df
        
        df_transformed = df.copy()
        
        for col in cols:
            if col not in df_transformed.columns:
                continue
            # Box-Cox requires positive values
            if (df_transformed[col] > 0).all():
                try:
                    df_transformed[f'{col}_boxcox'], _ = boxcox(df_transformed[col])
                except:
                    pass
        
        return df_transformed
    
    @staticmethod
    def standardize(df: pd.DataFrame, cols: List[str],
                   method: str = 'robust') -> pd.DataFrame:
        """Standardize features using different methods"""
        if not SKLEARN_AVAILABLE:
            return df
        
        df_transformed = df.copy()
        
        # Select scaler
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            return df_transformed
        
        # Transform specified columns
        available_cols = [c for c in cols if c in df_transformed.columns]
        if available_cols:
            df_transformed[available_cols] = scaler.fit_transform(df_transformed[available_cols])
        
        return df_transformed
    
    @staticmethod
    def bin_numeric_features(df: pd.DataFrame, cols: List[str],
                            n_bins: int = 5, strategy: str = 'quantile') -> pd.DataFrame:
        """Bin continuous features into categories"""
        df_transformed = df.copy()
        
        for col in cols:
            if col not in df_transformed.columns:
                continue
            
            if strategy == 'quantile':
                df_transformed[f'{col}_binned'] = pd.qcut(
                    df_transformed[col], q=n_bins, labels=False, duplicates='drop'
                )
            else:  # uniform
                df_transformed[f'{col}_binned'] = pd.cut(
                    df_transformed[col], bins=n_bins, labels=False
                )
        
        return df_transformed


# ============================================================================
# ENCODING
# ============================================================================

class CategoricalEncoder:
    """Encode categorical variables for modeling"""
    
    @staticmethod
    def one_hot_encode(df: pd.DataFrame, cols: List[str],
                      drop_first: bool = True) -> pd.DataFrame:
        """One-hot encode categorical variables"""
        df_encoded = df.copy()
        
        for col in cols:
            if col not in df_encoded.columns:
                continue
            # Create dummies
            dummies = pd.get_dummies(df_encoded[col], prefix=col, drop_first=drop_first)
            df_encoded = pd.concat([df_encoded, dummies], axis=1)
            df_encoded = df_encoded.drop(columns=[col])
        
        return df_encoded
    
    @staticmethod
    def label_encode(df: pd.DataFrame, cols: List[str]) -> Tuple[pd.DataFrame, Dict]:
        """Label encode categorical variables"""
        if not SKLEARN_AVAILABLE:
            return df, {}
        
        df_encoded = df.copy()
        encoders = {}
        
        for col in cols:
            if col not in df_encoded.columns:
                continue
            encoder = LabelEncoder()
            df_encoded[col] = encoder.fit_transform(df_encoded[col].astype(str))
            encoders[col] = encoder
        
        return df_encoded, encoders
    
    @staticmethod
    def frequency_encode(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """Encode categories by their frequency"""
        df_encoded = df.copy()
        
        for col in cols:
            if col not in df_encoded.columns:
                continue
            freq_map = df_encoded[col].value_counts(normalize=True).to_dict()
            df_encoded[f'{col}_freq'] = df_encoded[col].map(freq_map)
        
        return df_encoded


# ============================================================================
# DIMENSIONALITY REDUCTION
# ============================================================================

class DimensionalityReducer:
    """Reduce feature dimensionality"""
    
    @staticmethod
    def pca_transform(df: pd.DataFrame, n_components: int = 10) -> Tuple[pd.DataFrame, Any]:
        """Apply PCA for dimensionality reduction"""
        if not SKLEARN_AVAILABLE:
            return df, None
        
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        # Standardize before PCA
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_df)
        
        # Apply PCA
        pca = PCA(n_components=min(n_components, scaled_data.shape[1]))
        pca_data = pca.fit_transform(scaled_data)
        
        # Create dataframe with PCA components
        pca_cols = [f'PC{i+1}' for i in range(pca_data.shape[1])]
        pca_df = pd.DataFrame(pca_data, columns=pca_cols, index=numeric_df.index)
        
        return pca_df, pca
    
    @staticmethod
    def get_pca_explained_variance(pca: Any) -> Dict[str, float]:
        """Get explained variance from fitted PCA"""
        if pca is None:
            return {}
        
        return {
            'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
            'cumulative_variance': np.cumsum(pca.explained_variance_ratio_).tolist()
        }
