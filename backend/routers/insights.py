from fastapi import APIRouter, Body
from backend.services.data_loader import load_crop_data, load_rainfall_data, load_air_quality_data
from typing import List, Dict
import pandas as pd

router = APIRouter(prefix="/insights", tags=["insights"])

@router.get("/districts")
def districts():
    df = load_crop_data()
    return sorted(df['district'].unique().tolist())

@router.get("/crops")
def crops():
    df = load_crop_data()
    return sorted(df['crop'].unique().tolist())

@router.post("/crop_visualization")
def crop_visualization(
    districts: List[str] = Body(...),
    crops: List[str] = Body(...),
    years: List[int] = Body(...)
):
    df = load_crop_data()
    df_filtered = df[df['district'].isin(districts) & df['crop'].isin(crops) & df['year'].isin(years)]
    result = df_filtered.groupby(['district', 'crop', 'year']).agg(yield_t_ha=('yield_t_ha', 'mean')).reset_index()
    return result.to_dict(orient="records")

@router.post("/environmental_correlation")
def environmental_correlation(payload: Dict = Body(...)):
    district = payload["district"]
    crop = payload["crop"]

    df_crops = load_crop_data()
    df_rainfall = load_rainfall_data()
    df_crops_filtered = df_crops[(df_crops['district'] == district) & (df_crops['crop'] == crop)]
    
    # Assuming rainfall data has 'district', 'year', and 'rainfall_mm' columns
    df_rainfall_agg = df_rainfall.groupby(['district', 'year']).agg(total_rainfall_mm=('rainfall_mm', 'sum')).reset_index()

    df_merged = pd.merge(df_crops_filtered, df_rainfall_agg, on=['district', 'year'], how='left')
    
    return df_merged.to_dict(orient="records")

@router.get("/air_quality")
def air_quality_visualization():
    df = load_air_quality_data()
    return df.to_dict(orient="records")