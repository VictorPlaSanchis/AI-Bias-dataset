from fastapi import APIRouter, UploadFile, File
import pandas as pd

router = APIRouter()

@router.post("/analyze")
async def analyze_dataset(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    preview = df.head(3).to_dict(orient="records")
    columns = df.columns.tolist()
    return {"columns": columns, "preview": preview}
