"""
Categorical Encoding Module
Provides encoding capabilities for categorical variables
"""
import pandas as pd
from typing import Dict, List, Tuple

try:
    from sklearn.preprocessing import LabelEncoder
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("[WARNING] scikit-learn not available. Label encoding will be limited.")


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
