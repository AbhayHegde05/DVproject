import os
from dotenv import load_dotenv

load_dotenv()
WAREHOUSE = os.getenv("WAREHOUSE_PATH", "backend/db/warehouse.duckdb")
