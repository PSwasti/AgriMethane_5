import ee
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Authenticate and initialize Earth Engine
try:
    ee.Initialize(project='Methane_Project') # Replace it with your own! 
    print("🚀 Earth Engine Initialized.")
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# Define all the precision clusters for extraction (14 for India)
rice_sites = [
    {'name': 'Ludhiana', 'state': 'Punjab', 'coords': [75.85, 30.90]},
    {'name': 'Sangrur', 'state': 'Punjab', 'coords': [75.83, 30.22]},
    {'name': 'Bareilly', 'state': 'Uttar Pradesh', 'coords': [79.41, 28.36]},
    {'name': 'Gorakhpur', 'state': 'Uttar Pradesh', 'coords': [83.37, 26.76]},
    {'name': 'Rohtas', 'state': 'Bihar', 'coords': [83.98, 24.93]},
    {'name': 'Madhubani', 'state': 'Bihar', 'coords': [86.08, 26.35]},
    {'name': 'Bardhaman', 'state': 'West Bengal', 'coords': [87.86, 23.23]},
    {'name': 'Medinipur', 'state': 'West Bengal', 'coords': [87.32, 22.42]},
    {'name': 'Nizamabad', 'state': 'Telangana', 'coords': [78.10, 18.67]},
    {'name': 'Karimnagar', 'state': 'Telangana', 'coords': [79.13, 18.43]},
    {'name': 'Godavari Delta', 'state': 'Andhra Pradesh', 'coords': [82.24, 16.98]},
    {'name': 'Nellore', 'state': 'Andhra Pradesh', 'coords': [79.98, 14.44]},
    {'name': 'Thanjavur', 'state': 'Tamil Nadu', 'coords': [79.13, 10.78]},
    {'name': 'Thiruvarur', 'state': 'Tamil Nadu', 'coords': [79.64, 10.77]}
]

# Order for geographical visualization
north_to_south_order = [
    'Ludhiana', 'Sangrur', 'Bareilly', 'Gorakhpur', 
    'Rohtas', 'Madhubani', 'Bardhaman', 'Medinipur', 
    'Nizamabad', 'Karimnagar', 'Godavari Delta', 'Nellore', 
    'Thanjavur', 'Thiruvarur'
]

# Extraction function for Sentinel-5P Methane data
def analyze_site(site):
    print(f"🎯 Targeting: {site['name']}, {site['state']}")
    roi = ee.Geometry.Point(site['coords']).buffer(30000) # 30km buffer
    
    ch4_col = (ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4')
               .filterBounds(roi)
               .filterDate('2025-01-01', '2025-12-31')
               .select('CH4_column_volume_mixing_ratio_dry_air'))
    
    site_data = []
    for month in range(1, 13):
        start = f'2025-{month:02d}-01'
        end = ee.Date(start).advance(1, 'month')
        
        monthly_val = ch4_col.filterDate(start, end).mean().reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=roi,
            scale=7000
        ).get('CH4_column_volume_mixing_ratio_dry_air').getInfo()
        
        if monthly_val:
            site_data.append({
                'month': month, 'ch4': monthly_val,
                'area': site['name'], 'state': site['state']
            })
    return site_data

# Execute extraction loop
final_results = []
for site in rice_sites:
    try:
        data = analyze_site(site)
        final_results.extend(data)
    except Exception as e:
        print(f"⚠️ Error at {site['name']}: {e}")

# Save data to CSV
df_precision = pd.DataFrame(final_results)
df_precision.to_csv('methane_precision_2025.csv', index=False)

# Pivot data for analysis
pivot_df = df_precision.pivot_table(index='area', columns='month', values='ch4')

# Calculate the Methane Delta (October vs May)
if 5 in pivot_df.columns and 10 in pivot_df.columns:
    methane_delta = (pivot_df[10] - pivot_df[5]).dropna().sort_values(ascending=False)
    print("\n🏆 LEADERBOARD (Agricultural Surge):")
    print(methane_delta.round(2))
    
    # Save Delta Bar Chart
    plt.figure(figsize=(12, 6))
    methane_delta.plot(kind='bar', color='darkorange')
    plt.title('Methane Increase: May to Oct 2025')
    plt.ylabel('Delta CH4 (ppb)')
    plt.tight_layout()
    plt.savefig('methane_delta.png')

# Generate and save spatiotemporal heatmap
heatmap_data = pivot_df.reindex(north_to_south_order)
plt.figure(figsize=(16, 9))
sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt=".1f")
plt.title('2025 Methane Pulse across Indian Rice Clusters')
plt.savefig('methane_heatmap.png')
plt.show()
