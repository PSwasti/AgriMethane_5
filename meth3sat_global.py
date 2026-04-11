import ee
import pandas as pd
import datetime
import statsmodels.api as sm
import os

def initialize_engine(project_id):
    try:
        ee.Initialize(project=project_id)
        print(f"✅ Earth Engine Initialized: {project_id}")
    except Exception:
        print("🔑 Authentication required. Launching browser...")
        ee.Authenticate()
        ee.Initialize(project=project_id)

GLOBAL_HUBS = {
    'Amazon_Basin_Brazil': [-54.70, -2.44],
    'Mekong_Delta_Vietnam': [105.80, 10.00],
    'Lena_River_Delta_Siberia': [126.70, 72.30],
    'Congo_Basin_DRC': [18.26, 0.04],
    'Punjab_Rice_Hub_India': [75.85, 30.90]
}

def run_global_audit(coords, name, start='2021-01-01', end='2025-12-31'):
    """
    Extracts multi-sensor data with a 'Methane-First' priority.
    Discards month ONLY if methane data is missing.
    """
    point = ee.Geometry.Point(coords).buffer(25000) # 25km Global Footprint
    date_range = pd.date_range(start, end, freq='MS')
    results = []

    # ASSET IDs (Optimized for 2026 tracking)
    ch4_id = "COPERNICUS/S5P/OFFL/L3_CH4"
    lst_id = "MODIS/061/MOD11A1"
    smap_id = "NASA/SMAP/SPL4SMGP/008"

    print(f"🛰️  Processing: {name}...")

    for date in date_range:
        m_start = date.strftime('%Y-%m-%d')
        m_end = (date + pd.DateOffset(months=1)).strftime('%Y-%m-%d')
        
        try:
            # Independent Reductions to prevent cascading failures
            ch4_val = ee.ImageCollection(ch4_id).select('CH4_column_volume_mixing_ratio_dry_air') \
                        .filterDate(m_start, m_end).mean() \
                        .reduceRegion(ee.Reducer.mean(), point, 10000).get('CH4_column_volume_mixing_ratio_dry_air').getInfo()
            
            if ch4_val is None:
                continue

            temp_val = ee.ImageCollection(lst_id).select('LST_Day_1km') \
                         .filterDate(m_start, m_end).mean().multiply(0.02).subtract(273.15) \
                         .reduceRegion(ee.Reducer.mean(), point, 2000).get('LST_Day_1km').getInfo()

            moist_val = ee.ImageCollection(smap_id).select('sm_surface') \
                          .filterDate(m_start, m_end).mean() \
                          .reduceRegion(ee.Reducer.mean(), point, 11000).get('sm_surface').getInfo()

            results.append({
                'Hub': name,
                'Date': date,
                'CH4_ppb': ch4_val,
                'Temp_C': temp_val,
                'Moisture': moist_val
            })
        except Exception:
            continue

    return results

if __name__ == "__main__":
    PROJECT_ID = 'methane-analysis'#Replace with your own Project ID
    initialize_engine(PROJECT_ID)

    full_global_data = []
    for hub, loc in GLOBAL_HUBS.items():
        full_global_data.extend(run_global_audit(loc, hub))

    df = pd.DataFrame(full_global_data)
    
    output_file = "global_methane_audit_final.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Audit Complete. Data saved to {output_file}")
    print(f"📊 Total Observations: {len(df)}")
    print("\n🌍 GLOBAL HUB SENSITIVITY REPORT (ppb/°C)")
    print("-" * 45)
    for hub in df['Hub'].unique():
        hub_df = df[df['Hub'] == hub].dropna()
        if len(hub_df) > 5:
            X = sm.add_constant(hub_df[['Temp_C', 'Moisture']])
            y = hub_df['CH4_ppb']
            res = sm.OLS(y, X).fit()
            k = res.params['Temp_C']
            print(f"{hub:25} | k = {k:.2f}")
