from typing import List, Dict, Any
import pandas as pd
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression


def detect_identical(df: pd.DataFrame, target_col: str) -> List[Dict[str, Any]]:
    """
    Detect columns identical to the target.
    Returns a list of dicts with feature name and detail.
    """
    results = []
    target = df[target_col]
    for col in df.columns:
        if col == target_col:
            continue
        if df[col].equals(target):
            results.append({
                "feature": col,
                "type": "identical",
                "details": "100% equal to target"
            })
    return results


def detect_high_corr(df: pd.DataFrame, target_col: str, threshold: float = 0.95) -> List[Dict[str, Any]]:
    """
    Detect numeric columns with Pearson correlation above threshold.
    """
    results = []
    target = df[target_col]
    for col in df.select_dtypes(include=["number"]).columns:
        if col == target_col:
            continue
        corr = df[col].corr(target)
        if abs(corr) >= threshold:
            results.append({
                "feature": col,
                "type": "high_corr",
                "corr_coeff": corr
            })
    return results


def detect_high_mi(
    df: pd.DataFrame,
    target_col: str,
    threshold: float = 0.5,
    discrete_target: bool = False
) -> List[Dict[str, Any]]:
    """
    Detect features with high mutual information with the target.
    Use appropriate MI function depending on target type.
    """
    results = []
    X = df.drop(columns=[target_col])
    y = df[target_col]
    # Determine MI function based on target type
    if discrete_target:
        mi = mutual_info_classif(X.select_dtypes(include=["number"]), y)
    else:
        mi = mutual_info_regression(X.select_dtypes(include=["number"]), y)
    for idx, col in enumerate(X.select_dtypes(include=["number"]).columns):
        if mi[idx] >= threshold:
            results.append({
                "feature": col,
                "type": "high_mi",
                "mi_score": mi[idx]
            })
    return results


def detect_data_leaks(
    df: pd.DataFrame,
    target_col: str,
    corr_threshold: float = 0.95,
    mi_threshold: float = 0.5,
    discrete_target: bool = False
) -> Dict[str, Any]:
    """
    Run all leak detection methods and compile results.
    """
    leaks = []
    leaks.extend(detect_identical(df, target_col))
    leaks.extend(detect_high_corr(df, target_col, corr_threshold))
    leaks.extend(detect_high_mi(df, target_col, mi_threshold, discrete_target))
    return {"leaks": leaks, "summary": {"n_leaks": len(leaks)}}

