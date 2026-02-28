import ee
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Authenticate and initialize Earth Engine
try:
    ee.Initialize(project='Methane_Project') # Replace it with your own! 
    print("🚀 Earth Engine Initialized for a 5-year 'All India Study'! \n We're looking at 14 precision clusters across the 7 most rice producing states in India!")
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# Define all the 14 precision clusters for extraction
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
    'Thanjavur', 'Thiruvarur']

# Extraction function (Updated to except the "year" parameter)
def analyze_site(site, year):
    roi = ee.Geometry.Point(site['coords']).buffer(30000) # 30km buffer
    
    ch4_col = (ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4')
               .filterBounds(roi)
               .filterDate(f'{year}-01-01', f'{year}-12-31')
               .select('CH4_column_volume_mixing_ratio_dry_air'))
    
    site_year_data = []
    for month in range(1, 13):
        # Progress heartbeat
        print(f"📡 Processing: {year} | 🎯 Targeting: {site['name']}, {site['state']}"| Month {month:02d}...", end="\r")
        
        start = f'{year}-{month:02d}-01'
        end = ee.Date(start).advance(1, 'month')
        
        try:
            monthly_val = ch4_col.filterDate(start, end).mean().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=roi,
                scale=7000
            ).get('CH4_column_volume_mixing_ratio_dry_air').getInfo()
            
            if monthly_val:
                site_year_data.append({
                    'year': year, 'month': month, 'ch4': monthly_val,
                    'area': site['name'], 'state': site['state']
                })
        except Exception:
            continue
    return site_year_data

# 3. Execute longitudinal extraction loop (2021-2025)
final_results = []
for year in range(2021, 2026):
    print(f"\n📅 Starting Extraction for Year: {year}")
    for site in rice_sites:
        try:
            data = analyze_site(site, year)
            final_results.extend(data)
        except Exception as e:
            print(f"⚠️ Error at {site['name']} in {year}: {e}")

# 4. Save data
df_long = pd.DataFrame(final_results)
df_long.to_csv('methane_extraction_2021_2025.csv', index=False)
print("\n\n✅ 5-Year Extraction Complete!")

# 5. FacetGrid: The 14-Site Gallery (The core visual)
sns.set_theme(style="whitegrid")
g = sns.FacetGrid(df_long, col="area", hue="year", col_wrap=2, 
                  height=4, aspect=1.5, palette='viridis')
g.map(sns.lineplot, "month", "ch4", marker='o')
g.set_axis_labels("Month", "CH4 (ppb)")
g.set_titles(col_template="{col_name}")
g.add_legend(title="Year")
plt.subplots_adjust(top=0.92, hspace=0.4)
g.fig.suptitle('5-Year Methane Pulse: 14 Precision Clusters', fontsize=20)
plt.savefig('national_gallery_2021_2025.png', dpi=300)

# 6. Spatiotemporal Heatmap (Averaged across 5 years to show geographical 'Zones')
# This bridges the 1-year heatmap logic to the new 5-year data
pivot_all = df_long.groupby(['area', 'month'])['ch4'].mean().unstack()
heatmap_data = pivot_all.reindex(north_to_south_order)
plt.figure(figsize=(16, 9))
sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt=".1f")
plt.title('Multi-Year Mean Methane Pulse (North to South 2021-2025)')
plt.savefig('methane_heatmap.png')

plt.show()

