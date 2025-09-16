from fastapi import APIRouter, UploadFile, File
import pandas as pd

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.post("/preview")
async def preview(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    return {
        "columns": list(df.columns),
        "dtypes": {k: str(v) for k, v in df.dtypes.items()},
        "head": df.head(10).to_dict(orient="records")
    }
