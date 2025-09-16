import pandas as pd

def recommend_chart(df: pd.DataFrame):
    cols = df.columns.tolist()
    numeric = df.select_dtypes(include="number").columns.tolist()
    if "year" in df.columns and numeric:
        return {"chart": "line", "x": "year", "y": numeric[0]}
    if len(numeric) >= 2:
        return {"chart": "scatter", "x": numeric[0], "y": numeric[1]}
    if numeric:
        cat = [c for c in cols if c not in numeric][0]
        return {"chart": "bar", "x": cat, "y": numeric[0]}
    return {"chart": "table"}
