import duckdb
from backend.utils.io import WAREHOUSE

def query(sql: str, params: tuple = ()):
    con = duckdb.connect(WAREHOUSE, read_only=True)
    try:
        return con.execute(sql, params).df()
    finally:
        con.close()
    