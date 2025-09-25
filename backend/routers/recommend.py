from fastapi import APIRouter, UploadFile, File
import pandas as pd
from backend.services.recommend import recommend_chart

router = APIRouter(prefix="/recommend", tags=["recommend"])

@router.post("/")
async def recommend(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    return recommend_chart(df)
