# Invisible Population Detector (IPD) — UIDAI 2025

A Streamlit-based data analytics dashboard for analyzing UIDAI (Aadhaar) enrolment, demographic, and biometric data to identify districts with low visibility and invisibility risk.

## Features

- **📌 Overview Tab**: Top states, age composition, monthly trends
- **🔥 Hotspots Tab**: District-level Visibility Gap Score (VGS_proxy) analysis
- **🛠️ Action Plan Tab**: Governance recommendations for high-risk districts

## Prerequisites

- Python 3.8+
- CSV datasets placed in the same directory as `app.py`:
  - `api_data_aadhar_enrolment_*.csv`
  - `api_data_aadhar_demographic_*.csv`
  - `api_data_aadhar_biometric_*.csv`

## Installation

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deploying to Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [streamlit.io/cloud](https://share.streamlit.io/)
   - Click "New app"
   - Select your GitHub repository
   - Select branch: `main`
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Upload CSV Files** (Important for Cloud Deployment):
   - After deployment, the app will show file not found errors
   - You need to upload CSV files OR commit them to GitHub
   - To commit: `git add *.csv` and `git push`

## Data Files

Place all UIDAI CSV files in the project root directory. The app uses glob patterns to find:
- Enrolment: `api_data_aadhar_enrolment_*.csv`
- Demographic: `api_data_aadhar_demographic_*.csv`
- Biometric: `api_data_aadhar_biometric_*.csv`

## Troubleshooting

### "Files not found" error
- Ensure CSV files are in the same directory as `app.py`
- Check file naming matches the patterns above

### Slow loading on Streamlit Cloud
- The app caches data with `@st.cache_data` to avoid reloading
- First run may take 1-2 minutes with large CSV files
- Subsequent runs are instant

### Link not working after fixing
- Clear browser cache: Ctrl+Shift+Delete
- Redeploy: Go to Streamlit Cloud settings and click "Reboot app"
- Check GitHub repo is public

## Architecture

```
Enrolment Data
       ↓
    Load & Process
       ↓
    Calculate Metrics
       ↓
    [VGS_proxy, MPI, BSI]
       ↓
    Visualizations & Recommendations
```

## Key Metrics

- **VGS_proxy**: Visibility Gap Score (1 = very low visibility)
- **MPI**: Mobility Pressure Index (demographic updates ratio)
- **BSI**: Biometric Stress Index (biometric updates ratio)

## License

Open source for policy analysis
