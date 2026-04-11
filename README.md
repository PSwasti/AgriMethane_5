# AgriMethane_5 🛰️🌍

**Global Multivariate Fusion of Methane, Thermal, & Soil Moisture Dynamics (2021–2025)**

## 🚀 Overview
`AgriMethane_5` is a high-precision framework designed to solve the "Climate Paradox" of agricultural emissions. By synchronizing **TROPOMI (CH4)** mixing ratios with **MODIS** thermal data and **NASA SMAP** volumetric soil moisture, the engine identifies the non-linear triggers of methane surges across the world's intensive rice-growing regions.

## 🛠️ Project Evolution: Step-by-Step
The project followed a rigorous **5-Phase Engineering Lifecycle** to move from a regional hypothesis to a global audit.

### Phase 1: The Regional Prototype (Punjab Pilot)
* **Goal:** Establish a baseline correlation between methane and land temperature.
* **Tech:** Sentinel-5P (TROPOMI) + MODIS LST.
* **Result:** Confirmed a seasonal "Methane Pulse" in the Punjab belt, identifying a direct relationship between surface heat and gas release.

### Phase 2: National Validation (14-Cluster Audit)
* **Goal:** Scale the prototype to 14 production hubs across India to eliminate regional bias.
* **Tech:** GEE Python API + Coordinate-Based Cluster Sampling.
* **Result:** Identified **Medinipur, West Bengal** as a major hotspot (106.72 ppb surge) and mapped a North-to-South "Harvest Pulse."

### Phase 3: Solving the "Climate Paradox" (Triple-Sensor Fusion)
* **Goal:** Solve why heat sometimes *suppresses* methane. 
* **Tech:** Integration of **NASA SMAP (v008)** soil moisture data.
* **Result:** Discovered the **"Detonation Zone"**—methane only surges when Temp > 30°C and Moisture > 0.3.

### Phase 4: Infrastructure Overclocking (Agentic Refactoring)
* **Goal:** Move from manual scripts to a "Zero-Failure" robust pipeline.
* **Tech:** **Claude Code** & **Cursor** for automated API bridge refactoring (Python-to-JS).
* **Result:** Created a headless `.py` engine capable of processing terabyte-scale geospatial streams with automatic error-handling for orbital gaps.

### Phase 5: Global Longitudinal Scaling (60-Month Audit)
* **Goal:** Apply the validated "Detonation" logic to global river deltas.
* **Targets:** Amazon (Brazil), Mekong (Vietnam), Congo (DRC), and Lena River (Siberia).
* **Result:** Proved that while India is "Moisture-Limited," the Arctic is "Thermal-Limited," creating a unified global fingerprint for climate-driven methane surges.

## 📊 Technical Architecture
* **Sensors:** Sentinel-5P (CH4), MODIS (LST 1km), and NASA SMAP (9km v008 EASE-Grid).
* **Engine:** Google Earth Engine (GEE) Python API.
* **Analytics:** Multivariate OLS Regression (statsmodels).

---
*Developed for IIRS Project 2026*
