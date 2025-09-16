import duckdb, pandas as pd
from pathlib import Path

RAW = Path("backend/data/raw")
PROCESSED = Path("backend/data/processed")
WAREHOUSE = "backend/db/warehouse.duckdb"

PROCESSED.mkdir(parents=True, exist_ok=True)

def etl():
    crops = pd.read_csv(RAW / "crops.csv")
    rainfall = pd.read_csv(RAW / "rainfall.csv")
    air = pd.read_csv(RAW / "air_quality.csv")
    climate = pd.read_csv(RAW / "climate.csv")

    for df in [crops, rainfall, air, climate]:
        if "district" in df.columns:
            df["district"] = df["district"].str.title()

    crops.to_parquet(PROCESSED / "crops.parquet", index=False)
    rainfall.to_parquet(PROCESSED / "rainfall.parquet", index=False)
    air.to_parquet(PROCESSED / "air_quality.parquet", index=False)
    climate.to_parquet(PROCESSED / "climate.parquet", index=False)

    con = duckdb.connect(WAREHOUSE)
    con.execute("CREATE SCHEMA IF NOT EXISTS karnataka;")
    con.execute("CREATE OR REPLACE TABLE karnataka.crops AS SELECT * FROM read_parquet(?)", [str(PROCESSED / "crops.parquet")])
    con.execute("CREATE OR REPLACE TABLE karnataka.rainfall AS SELECT * FROM read_parquet(?)", [str(PROCESSED / "rainfall.parquet")])
    con.execute("CREATE OR REPLACE TABLE karnataka.air_quality AS SELECT * FROM read_parquet(?)", [str(PROCESSED / "air_quality.parquet")])
    con.execute("CREATE OR REPLACE TABLE karnataka.climate AS SELECT * FROM read_parquet(?)", [str(PROCESSED / "climate.parquet")])
    con.close()
    print("ETL complete.")

if __name__ == "__main__":
    etl()
