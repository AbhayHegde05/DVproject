from fastapi import APIRouter
from backend.services.query import query

router = APIRouter(prefix="/insights", tags=["insights"])

@router.get("/districts")
def districts():
    sql = "SELECT DISTINCT district FROM karnataka.crops ORDER BY district"
    return [r["district"] for r in query(sql).to_dict(orient="records")]

@router.get("/crops")
def crops(district: str | None = None):
    if district:
        sql = "SELECT DISTINCT crop FROM karnataka.crops WHERE district = ? ORDER BY crop"
        return [r["crop"] for r in query(sql, (district,)).to_dict(orient="records")]
    sql = "SELECT DISTINCT crop FROM karnataka.crops ORDER BY crop"
    return [r["crop"] for r in query(sql).to_dict(orient="records")]

@router.get("/yield_trend")
def yield_trend(district: str, crop: str | None = None):
    if crop:
        sql = """
        SELECT year, avg(yield_t_ha) AS yield_t_ha
        FROM karnataka.yield_by_year
        WHERE district = ? AND crop = ?
        GROUP BY year ORDER BY year
        """
        return query(sql, (district, crop)).to_dict(orient="records")
    sql = """
    SELECT year, avg(yield_t_ha) AS yield_t_ha
    FROM karnataka.yield_by_year
    WHERE district = ?
    GROUP BY year ORDER BY year
    """
    return query(sql, (district,)).to_dict(orient="records")

@router.get("/rainfall")
def rainfall(district: str):
    sql = "SELECT year, month, rainfall_mm FROM karnataka.rainfall WHERE district = ? ORDER BY year, month"
    return query(sql, (district,)).to_dict(orient="records")

@router.get("/air_quality")
def air_quality(district: str):
    sql = "SELECT date, pm25, pm10, aqi FROM karnataka.air_quality WHERE district = ? ORDER BY date"
    return query(sql, (district,)).to_dict(orient="records")