import ee
import pandas as pd
import datetime
import statsmodels.api as sm

def initialize_gee(project_id):
    try:
        ee.Initialize(project='methane-analysis')# Use your project id here
        print(f"✅ Earth Engine Initialized: {project_id}")
    except Exception:
        print("🔑 Authentication required...")
        ee.Authenticate()
        ee.Initialize(project=project_id)
def get_independent_stats(coords, name, start='2021-01-01', end='2025-12-31'):
    """
    Performs multi-sensor fusion for a specific coordinate.
    Layers: Sentinel-5P (CH4), MODIS (LST), NASA SMAP (Moisture).
    """
    point = ee.Geometry.Point(coords).buffer(20000) # 20km search buffer
    date_list = pd.date_range(start, end, freq='MS')
    data_rows = []

    print(f"🛰️ Deep Drilling Hub: {name}...")
    
    for date in date_list:
        m_start = date.strftime('%Y-%m-%d')
        m_end = (date + pd.DateOffset(months=1)).strftime('%Y-%m-%d')
        
        try:
            # 1st one- Sentinel-5P Methane
            ch4 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CH4") \
                    .select('CH4_column_volume_mixing_ratio_dry_air') \
                    .filterDate(m_start, m_end).mean() \
                    .reduceRegion(ee.Reducer.mean(), point, 10000) \
                    .get('CH4_column_volume_mixing_ratio_dry_air').getInfo()
            
            # 2nd one- MODIS Land Surface Temp
            temp = ee.ImageCollection("MODIS/061/MOD11A1") \
                    .select('LST_Day_1km') \
                    .filterDate(m_start, m_end).mean() \
                    .multiply(0.02).subtract(273.15) \
                    .reduceRegion(ee.Reducer.mean(), point, 2000) \
                    .get('LST_Day_1km').getInfo()
            
            # 3rd one- NASA SMAP Soil Moisture
            moist = ee.ImageCollection("NASA/SMAP/SPL4SMGP/008") \
                    .select('sm_surface') \
                    .filterDate(m_start, m_end).mean() \
                    .reduceRegion(ee.Reducer.mean(), point, 11000) \
                    .get('sm_surface').getInfo()

            if all([ch4, temp, moist]):
                data_rows.append({
                    'Hub': name,
                    'Date': date,
                    'CH4_ppb': ch4,
                    'Temp_C': temp,
                    'Moisture': moist
                })
        except Exception:
            continue # We skip months with missing data/orbital gaps

    return data_rows

if __name__ == "__main__":
    # Settings
    PROJECT_ID = 'methane-analysis'#Use your project id here
    initialize_gee(PROJECT_ID)

    HUBS = {
        'West Bengal (Medinipur)': [87.32, 22.42],
        'Punjab (Ludhiana)': [75.85, 30.90],
        'Andhra (Nellore)': [79.98, 14.44],
        'Tamil Nadu (Thanjavur)': [79.12, 10.78],
        'UP (Varanasi)': [82.97, 25.31]
    }

    final_results = []
    for hub_name, location in HUBS.items():
        final_results.extend(get_independent_stats(location, hub_name))
    df_full = pd.DataFrame(final_results).dropna(subset=['CH4_ppb'])
    df_full.to_csv("india_methane_multivariate_final.csv", index=False)
    print(f"\n🎉 SUCCESS! Extracted {len(df_full)} synchronized data points.")
    X = df_full[['Temp_C', 'Moisture']]
    X = sm.add_constant(X)
    y = df_full['CH4_ppb']
    model = sm.OLS(y, X).fit()

    print("\n🔬 FINAL MULTIVARIATE REPORT")
    print("-" * 30)
    print(f"🌡️ Temp Sensitivity: {model.params['Temp_C']:.2f} ppb/°C")
    print(f"💧 Moisture Sensitivity: {model.params['Moisture']:.2f} ppb/unit")
    print(f"📈 Model R-Squared: {model.rsquared:.4f}")
