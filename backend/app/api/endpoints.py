from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from typing import Optional
import pandas as pd

from app.schema_inference.infer import ColumnTypeInferer
from app.services.leak_detection import detect_data_leaks
from app.services.evaluate_class_balance import evaluate_class_balance
from app.services.detect_problematic_columns import detect_problem_columns

router = APIRouter()

@router.post("/analyze")
async def analyze_dataset(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    preview = df.head(3).to_dict(orient="records")
    columns = df.columns.tolist()
    return {"columns": columns, "preview": preview}

@router.post("/schema/infer")
async def infer_schema(file: UploadFile = File(...)):
    """
    Recibe un CSV subido y devuelve un dict {columna: tipo} según schema_inference.
    """
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error leyendo CSV: {e}")

    inferer = ColumnTypeInferer()
    tipos = {
        col: inferer.infer(df[col]).value
        for col in df.columns
    }
    return {"schema": tipos}

@router.post("/correlation")
async def correlation_analysis(
    file: UploadFile = File(...),
    target: str | None = None
) -> dict:
    """
    Devuelve:
      - numeric_corr: matriz Pearson de todas las numéricas.
      - pearson_target: correlaciones vs. target (si se proporciona).
      - categorical_corr: matriz Cramér’s V de categóricas.
    """
    import pandas as pd
    from app.services.correlation_service import (
        compute_numeric_correlation,
        compute_pearson_with_target,
        compute_categorical_correlation,
    )

    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV inválido: {e}")

    resp: dict = {}
    # Pearson general
    num_corr = compute_numeric_correlation(df)
    resp["numeric_corr"] = num_corr.round(3).to_dict()

    # Pearson vs. target (opcional)
    if target:
        try:
            pt = compute_pearson_with_target(df, target)
            resp["pearson_target"] = pt.round(3).to_dict(orient="index")
        except KeyError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Categóricas
    cat_corr = compute_categorical_correlation(df)
    resp["categorical_corr"] = cat_corr.round(3).to_dict()

    return resp

@router.post("/detect-data-leaks", summary="Detect data leaks in a dataset")
async def detect_data_leaks_endpoint(
    file: UploadFile = File(..., description="CSV file containing the dataset"),
    target_col: str = Query(..., description="Name of the target column to check against"),
    corr_threshold: float = Query(0.95, ge=0.0, le=1.0, description="Threshold for Pearson correlation"),
    mi_threshold: float = Query(0.5, ge=0.0, description="Threshold for mutual information score"),
    discrete_target: Optional[bool] = Query(False, description="Whether the target is discrete (classification)")
):
    """
    Accepts a CSV upload and parameters, returns detected data leaks:
    - identical features
    - high-correlation features
    - high mutual information features
    """
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {e}")

    if target_col not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target column '{target_col}' not found in dataset")

    result = detect_data_leaks(
        df,
        target_col,
        corr_threshold=corr_threshold,
        mi_threshold=mi_threshold,
        discrete_target=discrete_target
    )
    return result

@router.post("/evaluate-class-balance", summary="Evaluate class balance for a discrete target column")
async def evaluate_class_balance_endpoint(
    file: UploadFile = File(..., description="CSV file containing the dataset"),
    target_col: str = Query(..., description="Name of the discrete target column"),
    imbalance_threshold: float = Query(0.1, ge=0.0, le=1.0, description="Max allowed deviation from uniform distribution to consider balanced")
):
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {e}")
    if target_col not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target column '{target_col}' not found in dataset")
    result = evaluate_class_balance(df, target_col, imbalance_threshold)
    return result

@router.post("/detect-problem-columns", summary="Identify problematic columns in a dataset")
async def detect_problem_columns_endpoint(
    file: UploadFile = File(..., description="CSV file containing the dataset"),
    corr_threshold: float = Query(0.95, ge=0.0, le=1.0, description="Threshold for feature-feature correlation")
):
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {e}")
    result = detect_problem_columns(df, corr_threshold)
    return result

