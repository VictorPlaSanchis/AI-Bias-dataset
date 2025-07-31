from typing import List, Dict, Any
import pandas as pd

def detect_constant_columns(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Detect columns with a single unique value.
    """
    results = []
    for col in df.columns:
        if df[col].nunique(dropna=False) <= 1:
            results.append({"feature": col, "type": "constant", "details": "Only one unique value"})
    return results


def detect_empty_columns(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Detect columns with all values missing or empty.
    """
    results = []
    for col in df.columns:
        if df[col].isna().all():
            results.append({"feature": col, "type": "empty", "details": "All values missing"})
    return results


def detect_id_columns(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Detect ID-like columns: high cardinality equals number of rows.
    """
    results = []
    n_rows = len(df)
    for col in df.columns:
        if df[col].nunique(dropna=False) == n_rows:
            results.append({"feature": col, "type": "id", "details": f"Unique values equals row count ({n_rows})"})
    return results


def detect_feature_pairs_high_corr(
    df: pd.DataFrame,
    threshold: float = 0.95
) -> List[Dict[str, Any]]:
    """
    Detect pairs of numeric features with Pearson correlation above threshold.
    """
    results = []
    nums = df.select_dtypes(include=["number"]).columns
    corr_matrix = df[nums].corr().abs()
    for i, col1 in enumerate(nums):
        for col2 in nums[i+1:]:
            if corr_matrix.loc[col1, col2] >= threshold:
                results.append({"feature_pair": (col1, col2), "type": "high_feature_corr", "corr_coeff": corr_matrix.loc[col1, col2]})
    return results

def detect_problem_columns(
    df: pd.DataFrame,
    corr_threshold: float = 0.95
) -> Dict[str, Any]:
    """
    Identify problematic columns: constants, empty, ID-like, and highly correlated pairs.
    """
    problems = []
    problems.extend(detect_constant_columns(df))
    problems.extend(detect_empty_columns(df))
    problems.extend(detect_id_columns(df))
    pair_corr = detect_feature_pairs_high_corr(df, corr_threshold)
    problems.extend(pair_corr)
    return {"problems": problems, "summary": {"n_problems": len(problems)}}