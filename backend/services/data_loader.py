import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'datasets')

def load_rainfall_data():
    rainfall_dir = os.path.join(DATA_DIR, 'rainfall')
    rainfall_files = [os.path.join(rainfall_dir, f) for f in os.listdir(rainfall_dir) if f.endswith('.csv')]
    df_list = [pd.read_csv(f) for f in rainfall_files]
    return pd.concat(df_list, ignore_index=True)

def load_air_quality_data():
    air_quality_file = os.path.join(DATA_DIR, 'Air Quality in INDIA.csv')
    return pd.read_csv(air_quality_file)

def load_crop_data():
    crop_files = [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if f.endswith(('.xls', '.xlsx'))
    ]

    df_list = []
    for f in crop_files:
        if f.endswith('.xlsx'):
            df_list.append(pd.read_excel(f, engine='openpyxl'))
        elif f.endswith('.xls'):
            df_list.append(pd.read_excel(f, engine='xlrd'))
    
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()
