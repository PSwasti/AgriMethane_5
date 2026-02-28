import ee
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

# Suppress annoying warnings
warnings.filterwarnings("ignore")

# 1. Initialize
try:
    ee.Initialize(project='Methane_Project')
    print("🚀 Phase 2: Tropical Deep Drill Engine Online!")
except Exception:
    ee.Authenticate()
    ee.Initialize()

# 2. Expanded Tropical Site List (The "Big 5")
tropical_deep_drill_sites = [
    {'name': 'Medinipur', 'country': 'India', 'coords': [87.32, 22.42]},
    {'name': 'Mymensingh', 'country': 'Bangladesh', 'coords': [90.4, 24.7]},
    {'name': 'Central Plains', 'country': 'Thailand', 'coords': [100.1, 14.2]},
    {'name': 'Mekong Delta', 'country': 'Vietnam', 'coords': [105.8, 10.0]},
    {'name': 'Ayeyarwady', 'country': 'Myanmar', 'coords': [95.2, 17.0]}
]

# 3. 5-Year High-Res Extraction
def run_deep_drill(sites, start=2021, end=2025):
    drill_data = []
    for year in range(start, end + 1):
        print(f"\n🚜 Drilling Year: {year}")
        for site in sites:
            roi = ee.Geometry.Point(site['coords']).buffer(30000)
            col = (ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4')
                   .filterBounds(roi)
                   .filterDate(f'{year}-01-01', f'{year}-12-31')
                   .select('CH4_column_volume_mixing_ratio_dry_air'))
            
            for month in range(1, 13):
                print(f"📡 High-Res Capture: {site['country']} | {year}-M{month:02d}...", end="\r")
                start_date = f'{year}-{month:02d}-01'
                end_date = ee.Date(start_date).advance(1, 'month')
                
                try:
                    val = col.filterDate(start_date, end_date).mean().reduceRegion(
                        reducer=ee.Reducer.mean(),
                        geometry=roi,
                        scale=7000
                    ).get('CH4_column_volume_mixing_ratio_dry_air').getInfo()
                    
                    if val:
                        drill_data.append({
                            'year': year, 'month': month, 'CH4 Concentration (ppb)': val,
                            'country': site['country'], 'site': site['name']
                        })
                except: continue
    return drill_data

# 4. Execute
results = run_deep_drill(tropical_deep_drill_sites)
df_drill = pd.DataFrame(results)
df_drill.to_csv('tropical_deep_drill_results.csv', index=False)
print("\n\n✅ Deep Drill Complete!")

# 5. The "Critical Comparison" Visual
# Using 'Set1' for high contrast so 2023 (Green) stays visible!
g = sns.FacetGrid(df_drill, col="country", hue="year", col_wrap=2, height=5, aspect=1.2, palette='Set1', sharey=False)
g.map(sns.lineplot, "month", "CH4 Concentration (ppb)", marker='o', linewidth=2.5)
g.add_legend(title="Year")
plt.subplots_adjust(top=0.88, hspace=0.4)
g.fig.suptitle('Phase 2: Tropical Deep Drill - 5 Country Methane Pulse (2021-2025)', fontsize=18)
plt.savefig('tropical_deep_drill_viz.png', dpi=300)
plt.show()
