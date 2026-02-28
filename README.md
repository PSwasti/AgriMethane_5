# AgriMethane_5 🛰️🌍

**Global Spatio-Temporal Fusion of Methane & Agricultural Phenology (2020–2025)**

## 🚀 Overview
`AgriMethane_5` is a high-precision framework for correlating **Sentinel-5P CH4** concentrations with agricultural production cycles. This project leverages **Coordinate-Based Cluster Sampling** to monitor methane footprints across the world's most intensive rice-growing regions over a 5-year longitudinal window (2020–2025).

## 📊 2025 Precision Audit: National Validation (India)
To calibrate the global engine, a high-precision audit of 14 validated production hubs across India was conducted. By utilizing a **May Baseline vs. October Peak** logic, the engine isolates the "Agricultural Delta" ($\Delta$) from background industrial noise.

### Key Findings:
* **Indian Hotspot:** **Medinipur, West Bengal** recorded a maximum surge of **106.72 ppb**.
* **Regional Pulse:** Data confirms a synchronized North-to-South methane pulse linked to harvest migration.



## 🌍 Global Longitudinal Scope (2020–2025)
The project is currently scaling the India-validated logic to a **Global Context**, targeting the primary rice deltas of Southeast Asia, East Asia, and the Americas over a 60-month observation period.

* **Temporal Depth:** 5-year analysis (2020-2025) to detect shifts in emission intensity due to climate variability and irrigation changes.
* **Spatial Breadth:** Moving beyond the Indian subcontinent to monitor global "Methane Super-Emitters" in Mekong, Red River, and Mississippi deltas.



## 🛠️ Technical Architecture
* **Precision Extraction:** 30km radial buffers around coordinate-validated hubs.
* **Engine:** Google Earth Engine (GEE) Python API with 2026 project-based authentication.
* **Sensors:** TROPOMI (CH4) & Sentinel-2 (NDVI).
* **Optimization:** `merge_asof` temporal synchronization for multi-sensor data fusion.

## 🗺️ Roadmap
- [x] **Phase 1:** Pipeline architecture and Punjab regional pilot.
- [x] **Phase 2:** Precision expansion to **14 National Clusters** (India validation).
- [x] **Phase 3:** **Longitudinal Expansion:** Scaling to a 5-year longitudinal window (2020–2025) across Indian clusters to identify climate-driven emission trends.
- [x] **Phase 4:** **Global Scale-up:** Implementing the validated engine across major global rice deltas (example Mekong).


---
*Developed for IIRS Project 2026*
