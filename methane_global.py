import ee
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# 1. Initialize
try:
    ee.Initialize(project='Methane_Project')
    print("🚀 Master Audit Engine Online! Processing the 12 Global Sites for past 5 years(2021-2025)!!!")
except Exception as e:
    ee.Authenticate()
    ee.Initialize()
    
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# 2. The 12-Country Global Baseline
master_audit_sites = [
    # Equatorial (Zone A)
    {'name': 'Mekong Delta', 'zone': 'Equatorial', 'country': 'Vietnam', 'coords': [105.8, 10.0]},
    {'name': 'West Java', 'zone': 'Equatorial', 'country': 'Indonesia', 'coords': [107.6, -6.9]},
    {'name': 'Rio Grande', 'zone': 'Equatorial', 'country': 'Brazil', 'coords': [-51.2, -30.0]},
    
    # Tropical (Zone B)
    {'name': 'Medinipur', 'zone': 'Tropical', 'country': 'India', 'coords': [87.32, 22.42]},
    {'name': 'Central Plains', 'zone': 'Tropical', 'country': 'Thailand', 'coords': [100.1, 14.2]},
    {'name': 'Mymensingh', 'zone': 'Tropical', 'country': 'Bangladesh', 'coords': [90.4, 24.7]},
    
    # Temperate (Zone C)
    {'name': 'Heilongjiang', 'zone': 'Temperate', 'country': 'China', 'coords': [127.0, 45.0]},
    {'name': 'Sacramento', 'zone': 'Temperate', 'country': 'USA', 'coords': [-121.7, 39.1]},
    {'name': 'Po Valley', 'zone': 'Temperate', 'country': 'Italy', 'coords': [9.2, 45.1]},
    
    # Sub-Polar (Zone D)
    {'name': 'Yamal', 'zone': 'Sub-Polar', 'country': 'Russia', 'coords': [70.0, 70.0]},
    {'name': 'Mackenzie', 'zone': 'Sub-Polar', 'country': 'Canada', 'coords': [-135.0, 68.0]},
    {'name': 'Finnmark', 'zone': 'Sub-Polar', 'country': 'Norway', 'coords': [24.0, 70.0]}
]

# 3. Longitudinal Extraction Logic
def run_master_audit(sites, start=2021, end=2025):
    all_data = []
    for year in range(start, end + 1):
        print(f"\n📅 Auditing Year: {year}")
        for site in sites:
            roi = ee.Geometry.Point(site['coords']).buffer(30000)
            col = (ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4')
                   .filterBounds(roi)
                   .filterDate(f'{year}-01-01', f'{year}-12-31')
                   .select('CH4_column_volume_mixing_ratio_dry_air'))
            
            for month in range(1, 13):
                # Live Heartbeat
                print(f"📡 Processing: {year} | {site['zone']} | {site['country']} | M{month:02d}...", end="\r")
                
                start_date = f'{year}-{month:02d}-01'
                end_date = ee.Date(start_date).advance(1, 'month')
                
                try:
                    stats = col.filterDate(start_date, end_date).mean().reduceRegion(
                        reducer=ee.Reducer.mean(),
                        geometry=roi,
                        scale=7000
                    ).get('CH4_column_volume_mixing_ratio_dry_air').getInfo()
                    
                    if stats:
                        all_data.append({
                            'year': year, 'month': month, 'CH4 Concentration (ppb)': stats,
                            'country': site['country'], 'zone': site['zone']
                        })
                except Exception:
                    continue
    return all_data

# 4. Execute and Export
audit_results = run_master_audit(master_audit_sites)
df_audit = pd.DataFrame(audit_results)
df_audit.to_csv('global_master_audit_2021_2025.csv', index=False)
print("\n\n✅ Master Audit Complete!")

# 5. Visualization: Identifying the Max Deviation Zone
plt.figure(figsize=(15, 10))
g = sns.FacetGrid(df_audit, col="zone", hue="year", col_wrap=2, height=5, aspect=1.2, palette='Set1')
g.map(sns.lineplot, "month", "CH4 Concentration (ppb)", marker='o')
g.add_legend(title="Year")
plt.subplots_adjust(top=0.9, hspace=0.3)
g.fig.suptitle('5-Year Longitudinal Zonal Comparison (12 Countries)', fontsize=18)
plt.savefig('master_audit_facetgrid.png', dpi=300)
plt.show()
