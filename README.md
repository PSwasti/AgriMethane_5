# AgriMethane_5 🛰️🌍

**Global Spatio-Temporal Fusion of Methane & Agricultural Phenology (2020–2025)**

## 🚀 Overview
`AgriMethane_5` is a scalable framework for correlating **Sentinel-5P CH4** concentrations with **Sentinel-2 NDVI** datasets. This project transitions from regional pilot studies to a 5-year global longitudinal analysis of agricultural emissions, providing data-driven insights into the climate impact of rice cultivation.

## 📊 Phase 1: Pilot Validation (Punjab, India)
To validate the correlation logic, a pilot study was conducted in the Punjab region for the 2025 harvest season.
* **Methane Spike:** Concentrations peaked at **~2000 ppb** during the transition from vegetative growth to harvest.
* **Phenology Correlation:** The CH4 spikes synchronized with the rapid decay in NDVI (**0.55 → 0.20**), marking the period of intensive harvest activity and soil disturbance.



## 🛠️ Technical Architecture
* **Engine:** Google Earth Engine (GEE) Python API.
* **Sensors:** TROPOMI (Trace Gas) & Sentinel-2 (Multispectral).
* **Optimization:** Implemented robust regex-based date sterilization and `merge_asof` temporal synchronization.
* **Environment:** Managed via Conda/Ubuntu (`earthengine-api`, `pandas`, `matplotlib`).

## 🗺️ Global Roadmap
- [x] **Phase 1:** Pipeline architecture and regional validation in Punjab.
- [ ] **Phase 2:** Global expansion to Southeast Asian and East Asian rice deltas (2020-2025).
- [ ] **Phase 3:** Integration of **Sentinel-1 (SAR)** data to monitor irrigation and flooding patterns.
- [ ] **Phase 4:** Development of a "Methane Super-Emitter" anomaly detection model.

## 📂 Repository Structure
* `engine.py`: Core processing logic and GEE integration.
* `requirements.txt`: Environment dependencies.
