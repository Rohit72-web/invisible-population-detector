# 🛰️ Invisible Population Detector (IPD)

> Identifying Population Gaps in Digital Governance using UIDAI Aadhaar Data (2025–2026)

## 🌐 Live Demo

🚀 Streamlit Deployment:  
https://invisible-population-detector-qcbb9xabwatjyk3nwbwmot.streamlit.app/#invisible-population-detector-ipd-uidai-2025

👉 [Launch IPD Dashboard](https://invisible-population-detector-qcbb9xabwatjyk3nwbwmot.streamlit.app/#invisible-population-detector-ipd-uidai-2025)

---

# 📌 Overview

Invisible Population Detector (IPD) is a governance analytics framework that detects potential **digitally invisible population zones** using UIDAI Aadhaar enrolment, demographic, and biometric datasets.

The project transforms Aadhaar activity into actionable governance intelligence by identifying:
- Low visibility districts
- Biometric stress regions
- Migration pressure zones
- High-risk inclusion gaps

---

# 🚀 Features

- 📊 Aadhaar Enrolment Analytics
- 🔥 Visibility Gap Score (VGS_proxy)
- 🧬 Biometric Stress Indicator (BSI)
- 🌍 Mobility Pressure Indicator (MPI)
- 📈 Interactive Streamlit Dashboard
- 🛠️ Governance Action Recommendations
- 📍 District-Level Hotspot Detection

---

# 🧠 Core Idea

The project estimates invisibility risk using Aadhaar activity imbalance.

```python
Invisible Population ≈ Expected Visibility − Observed Digital Visibility
```

Higher invisibility scores indicate districts that may be:
- Under-enrolled
- Biometrically excluded
- Migration affected
- Digitally underrepresented

---

# 🏗️ System Architecture

```text
UIDAI Enrolment Data
        +
UIDAI Demographic Data
        +
UIDAI Biometric Data
        ↓
Data Cleaning & Transformation
        ↓
Feature Engineering
        ↓
Visibility Gap Computation
        ↓
Risk Scoring
        ↓
Hotspot Detection
        ↓
Governance Recommendations
```

---

# 📊 Key Metrics

| Metric | Description |
|---|---|
| VGS_proxy | Visibility Gap Score |
| MPI | Mobility Pressure Indicator |
| BSI | Biometric Stress Indicator |
| Risk Level | High / Medium / Low |

---

# 📂 Expected Dataset Files

```text
api_data_aadhar_enrolment_*.csv
api_data_aadhar_demographic_*.csv
api_data_aadhar_biometric_*.csv
```

---

# 📌 Dataset Attributes

## Enrolment Dataset
- state
- district
- date
- age_0_5
- age_5_17
- age_18_greater

## Demographic Dataset
- demographic update indicators
- age-wise update activity

## Biometric Dataset
- biometric update indicators
- authentication-related signals

---

# 🖥️ Dashboard Modules

## 📌 Overview
- State-wise enrolment concentration
- Age composition analysis
- Monthly Aadhaar activity trends

## 🔥 Hotspots
- District invisibility ranking
- Visibility Gap Score analysis
- MPI vs BSI visualization

## 🛠️ Action Plan
- Governance intervention suggestions
- Risk-based recommendations
- Priority hotspot districts

---

# ⚙️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

---

# 📦 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ipd-project.git
cd ipd-project
```

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 3️⃣ Add Dataset Files

Place all UIDAI CSV datasets inside the project directory.

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 📈 Methodology

## Step 1 — Data Loading
Load enrolment, demographic, and biometric datasets.

## Step 2 — Data Cleaning
- Remove duplicates
- Handle missing values
- Standardize district names

## Step 3 — Aggregation
Compute district-wise Aadhaar activity.

## Step 4 — Feature Engineering
Generate:
- VGS_proxy
- MPI
- BSI

## Step 5 — Hotspot Detection
Identify districts with high invisibility risk.

## Step 6 — Governance Recommendations
Suggest interventions for high-risk districts.

---

# 🎯 Real-World Applications

## 🏥 Healthcare
Vaccination and healthcare inclusion analysis

## 🎓 Education
School-age identity coverage analysis

## 🍚 Welfare Systems
PDS/DBT exclusion detection

## 🌆 Urban Planning
Migration-aware governance analytics

## 🚨 Disaster Management
Population visibility estimation

---

# 🔥 Innovation Highlights

- Multi-source Aadhaar intelligence fusion
- Invisible population modelling
- Governance-oriented risk scoring
- Biometric exclusion interpretation
- Actionable hotspot prioritization

---

# 📌 Future Scope

- AI-based hotspot prediction
- Real-time dashboards
- GIS mapping integration
- Census microdata fusion
- Welfare linkage analytics

---

# 👨‍💻 Author

## Rohit Gupta

Invisible Population Detection (IPD) Framework  
UIDAI Governance Analytics Project

---

# 📜 Disclaimer

This project uses aggregated/public Aadhaar-related datasets and does not use or store raw biometric information or personally identifiable Aadhaar data.

All generated indicators are analytical proxies intended for research and governance analytics purposes only.

---

# ⭐ Final Thought

> “We transform Aadhaar coverage data into inclusion intelligence.”
