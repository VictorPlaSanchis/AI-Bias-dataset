import pandas as pd
import numpy as np
from scipy.stats import pearsonr, chi2_contingency
import itertools

def compute_numeric_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """Matriz de correlación de Pearson para todas las columnas numéricas."""
    numeric = df.select_dtypes(include=[np.number])
    return numeric.corr(method='pearson')

def compute_pearson_with_target(df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """Correlación de Pearson + p-value entre cada numérica y el target."""
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' not found")
    results = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        if col == target_col:
            continue
        x = df[col].dropna()
        y = df[target_col].dropna()
        joined = pd.concat([x, y], axis=1, join='inner')
        corr, p = pearsonr(joined[col], joined[target_col])
        results[col] = {'correlation': corr, 'p_value': p}
    return pd.DataFrame.from_dict(results, orient='index')

def cramers_v(x: pd.Series, y: pd.Series) -> float:
    """Cálculo de Cramér’s V para dos categóricas."""
    cm = pd.crosstab(x, y)
    chi2 = chi2_contingency(cm)[0]
    n = cm.sum().sum()
    phi2 = chi2 / n
    r, k = cm.shape
    # corrección de sesgo
    phi2_corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    r_corr = r - ((r-1)**2)/(n-1)
    k_corr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2_corr / min((k_corr-1), (r_corr-1)))

def compute_categorical_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """Matriz de Cramér’s V para todas las columnas categóricas."""
    cat = df.select_dtypes(include=['category', object])
    cols = cat.columns
    mat = pd.DataFrame(np.zeros((len(cols), len(cols))), index=cols, columns=cols)
    for a, b in itertools.combinations_with_replacement(cols, 2):
        v = cramers_v(cat[a].dropna(), cat[b].dropna())
        mat.loc[a, b] = mat.loc[b, a] = v
    return mat