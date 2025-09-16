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
