# broker.py
import requests
import pandas as pd
import os

API_KEY = "b6f1332cc88aa45230815c4f6b54e2f3" # Your key
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

# Mapping human names to FRED Series IDs
# International IDs are usually Monthly; US IDs are Daily.
COUNTRY_MAP = {
    "US": "DGS10",
    "AUSTRALIA": "IRLTLT01AUM156N",
    "UK": "IRLTLT01GBM156N",
    "GERMANY": "IRLTLT01DEM156N",
    "JAPAN": "IRLTLT01JPM156N",
    "CANADA": "IRLTLT01CAM156N"
}

def fetch_yield(country_name):

    os.makedirs("cache", exist_ok=True)

    series_id = COUNTRY_MAP.get(country_name.upper())
    if not series_id:
        print(f"⚠️ {country_name} not found in MAPPING.")
        return None

    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 50 
    }

    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()['observations']
        df = pd.DataFrame(data)
        
        # Clean data
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna(subset=['value'])
        
        # Save to cache
        save_path = f"cache/{country_name.upper()}.csv"
        df[['date', 'value']].to_csv(save_path, index=False)
        return save_path
    
    print(f"❌ API Error for {country_name}: {response.status_code}")
    return None