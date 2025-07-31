import pandas as pd
from typing import List, Dict, Any, Union

def evaluate_class_balance(
    df: pd.DataFrame,
    target_col: str,
    imbalance_threshold: float = 0.1
) -> Dict[str, Union[Dict[str, Any], float, str]]:
    """
    Evaluate class distribution in a discrete target column.
    Returns counts, proportions, and imbalance metric.

    imbalance_threshold: max allowed difference from uniform distribution.
    """
    counts = df[target_col].value_counts().to_dict()
    total = len(df)
    proportions = {cls: cnt / total for cls, cnt in counts.items()}
    num_classes = len(counts)
    ideal = 1 / num_classes
    max_dev = max(abs(p - ideal) for p in proportions.values())
    status = "balanced" if max_dev <= imbalance_threshold else "imbalanced"
    return {
        "counts": counts,
        "proportions": proportions,
        "max_deviation": max_dev,
        "status": status
    }