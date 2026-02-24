import ee
import pandas as pd
import re
import matplotlib.pyplot as plt

def initialize_gee(project_id):
    """Initializes Google Earth Engine."""
    ee.Initialize(project=project_id)

def get_methane_data(roi, start_date, end_date):
    """Extracts CH4 data from Sentinel-5P."""
    col = (ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4')
           .filterBounds(roi)
           .filterDate(start_date, end_date)
           .select('CH4_column_volume_mixing_ratio_dry_air'))

    def extract_stats(img):
        val = img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=roi,
            scale=7000,
            bestEffort=True
        ).get('CH4_column_volume_mixing_ratio_dry_air')
        return ee.Feature(None, {'date': img.date().format('YYYY-MM-DD'), 'ch4': val})

    features = col.map(extract_stats).filter(ee.Filter.notNull(['ch4'])).getInfo()
    return pd.DataFrame([f['properties'] for f in features['features']])

def get_ndvi_data(roi, start_date, end_date):
    """Extracts NDVI data from Sentinel-2."""
    s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
          .filterBounds(roi)
          .filterDate(start_date, end_date)
          .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)))

    def calc_ndvi(img):
        ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        mean_val = ndvi.reduceRegion(ee.Reducer.mean(), roi, 100).get('NDVI')
        return ee.Feature(None, {'date': img.date().format('YYYY-MM-DD'), 'ndvi': mean_val})

    features = s2.map(calc_ndvi).filter(ee.Filter.notNull(['ndvi'])).getInfo()
    return pd.DataFrame([f['properties'] for f in features['features']])

def clean_and_merge(df_ch4, df_ndvi):
    """Cleans malformed dates and merges datasets."""
    def clean_date(s):
        match = re.search(r'(\d{4}-\d{2}-\d{2})', str(s))
        return match.group(1) if match else None

    for df in [df_ch4, df_ndvi]:
        df['date_dt'] = pd.to_datetime(df['date'].apply(clean_date), errors='coerce')
        df.dropna(subset=['date_dt'], inplace=True)
        df.sort_values('date_dt', inplace=True)

    return pd.merge_asof(df_ch4, df_ndvi[['date_dt', 'ndvi']], on='date_dt', direction='nearest')

if __name__ == "__main__":
    # === USER CONFIGURATION ===
    # Replace with your Google Earth Engine Project ID
    PROJECT_ID = 'YOUR_PROJECT_ID_HERE' 
    
    # Define your Area of Interest (Default: Punjab Pilot Region)
    ROI_COORDINATES = [75.8573, 30.9010]
    BUFFER_DISTANCE = 15000 
    # ==========================

    print(f"Initializing AgriMethane_5 Engine with project: {PROJECT_ID}...")
    initialize_gee(PROJECT_ID)
    
    PUNJAB_ROI = ee.Geometry.Point(ROI_COORDINATES).buffer(BUFFER_DISTANCE)
