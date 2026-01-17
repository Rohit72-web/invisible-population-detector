import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Invisible Population Detector (IPD)", layout="wide")

BASE_DIR = Path(__file__).parent

st.title("🛰️ Invisible Population Detector (IPD) — UIDAI 2025")
st.caption("Built using UIDAI Enrolment + Demographic + Biometric datasets (Mar–Dec 2025)")

# ----------------------------
# Helper functions
# ----------------------------
def safe_div(a, b):
    return np.where(b == 0, np.nan, a / b)

@st.cache_data(show_spinner=False)
def load_uidai_enrolment():
    files = sorted(BASE_DIR.glob("api_data_aadhar_enrolment_*.csv"))
    if not files:
        raise FileNotFoundError(f"Enrolment CSVs not found in: {BASE_DIR}")

    df = pd.concat([pd.read_csv(f, low_memory=False) for f in files], ignore_index=True)

    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    for c in ["age_0_5", "age_5_17", "age_18_greater"]:
        df[c] = pd.to_numeric(df.get(c, 0), errors="coerce").fillna(0).astype(int)

    df["total_enrolments"] = df[["age_0_5", "age_5_17", "age_18_greater"]].sum(axis=1)

    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["state"] = df["state"].fillna("Unknown").astype(str)
    df["district"] = df["district"].fillna("Unknown").astype(str)

    return df

@st.cache_data(show_spinner=False)
def load_uidai_demo():
    files = sorted(BASE_DIR.glob("api_data_aadhar_demographic_*.csv"))
    if not files:
        raise FileNotFoundError(f"Demographic CSVs not found in: {BASE_DIR}")

    df = pd.concat([pd.read_csv(f, low_memory=False) for f in files], ignore_index=True)

    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    age_cols = [c for c in df.columns if "age" in c.lower()]

    for c in age_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

    df["total_demo_updates"] = df[age_cols].sum(axis=1)

    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["state"] = df["state"].fillna("Unknown").astype(str)
    df["district"] = df["district"].fillna("Unknown").astype(str)

    return df

@st.cache_data(show_spinner=False)
def load_uidai_bio():
    files = sorted(BASE_DIR.glob("api_data_aadhar_biometric_*.csv"))
    if not files:
        raise FileNotFoundError(f"Biometric CSVs not found in: {BASE_DIR}")

    df = pd.concat([pd.read_csv(f, low_memory=False) for f in files], ignore_index=True)

    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    bio_cols = [c for c in df.columns if ("bio" in c.lower()) or ("age" in c.lower())]

    for c in bio_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

    df["total_bio_updates"] = df[bio_cols].sum(axis=1)

    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["state"] = df["state"].fillna("Unknown").astype(str)
    df["district"] = df["district"].fillna("Unknown").astype(str)

    return df

# ----------------------------
# Load datasets
# ----------------------------
enrol = load_uidai_enrolment()
demo = load_uidai_demo()
bio = load_uidai_bio()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

months = sorted(enrol["month"].dropna().unique())
month_sel = st.sidebar.selectbox("Month", ["All"] + months, index=0)

states = sorted(enrol["state"].dropna().unique())
state_sel = st.sidebar.selectbox("State", ["All"] + states, index=0)

def apply_filters(df):
    out = df.copy()
    if month_sel != "All":
        out = out[out["month"] == month_sel]
    if state_sel != "All":
        out = out[out["state"] == state_sel]
    return out

enrol_f = apply_filters(enrol)
demo_f = apply_filters(demo)
bio_f = apply_filters(bio)

# ----------------------------
# KPI Cards (Proof scale)
# ----------------------------
total_enrol = int(enrol_f["total_enrolments"].sum())
total_demo = int(demo_f["total_demo_updates"].sum())
total_bio = int(bio_f["total_bio_updates"].sum())

# Peak spike day (global)
daily = enrol.groupby("date").agg(total=("total_enrolments", "sum")).reset_index()
daily = daily.dropna().sort_values("total", ascending=False)

if len(daily) > 0:
    spike_date = daily.iloc[0]["date"].strftime("%Y-%m-%d")
    spike_val = int(daily.iloc[0]["total"])
else:
    spike_date = "N/A"
    spike_val = 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Enrolments", f"{total_enrol:,}")
c2.metric("Total Demographic Updates", f"{total_demo:,}")
c3.metric("Total Biometric Updates", f"{total_bio:,}")
c4.metric("Peak Spike Day", spike_date)
c5.metric("Spike Count", f"{spike_val:,}")

st.divider()

# ----------------------------
# Tabs
# ----------------------------
tab1, tab2, tab3 = st.tabs(["📌 Overview", "🔥 Hotspots (Final Result)", "🛠️ Action Plan"])

# ----------------------------
# TAB 1: Overview
# ----------------------------
with tab1:
    st.subheader("1) Top States by Enrolment Activity (Proof of concentration)")

    state_enrol = enrol_f.groupby("state").agg(total=("total_enrolments", "sum")).reset_index()
    state_enrol = state_enrol.sort_values("total", ascending=False).head(15)

    fig = px.bar(state_enrol, x="state", y="total",
                 title="Top 15 States by Enrolment Activity (UIDAI 2025)")
    st.plotly_chart(fig, use_container_width=True)

    st.info("✅ Meaning: Aadhaar activity is highly uneven across states → governance infrastructure demand is concentrated.")

    st.subheader("2) Age Composition of Enrolments (Proves child-heavy demand)")

    age_totals = enrol_f[["age_0_5", "age_5_17", "age_18_greater"]].sum().reset_index()
    age_totals.columns = ["age_group", "count"]

    fig2 = px.pie(age_totals, names="age_group", values="count",
                  title="Age-wise Enrolment Composition")
    st.plotly_chart(fig2, use_container_width=True)

    st.success("✅ Outcome: Most enrolments come from child buckets → enrolment demand depends strongly on family/child registration cycles.")

    st.subheader("3) Monthly Trends (Enrol vs Demo vs Bio)")

    m_en = enrol.groupby("month").agg(enrol=("total_enrolments", "sum")).reset_index()
    m_de = demo.groupby("month").agg(demo=("total_demo_updates", "sum")).reset_index()
    m_bi = bio.groupby("month").agg(bio=("total_bio_updates", "sum")).reset_index()

    m = m_en.merge(m_de, on="month", how="outer").merge(m_bi, on="month", how="outer").fillna(0)
    m = m.sort_values("month")

    fig3 = px.line(m, x="month", y=["enrol", "demo", "bio"], markers=True,
                   title="Monthly Aadhaar Activity Comparison (All India)")
    st.plotly_chart(fig3, use_container_width=True)

    st.info("✅ Meaning: Governance demand is multi-dimensional → not only enrolment, but also updates + biometric stress matter.")

# ----------------------------
# TAB 2: Hotspots (Final Result Proof)
# ----------------------------
with tab2:
    st.subheader("🔥 District Hotspots (Invisible Population Risk Zones)")

    st.markdown("""
**Final Output of IPD:** District-level **Visibility Gap Score (VGS_proxy)**  
We compute an Aadhaar-only proxy for “low visibility districts” within each state:

- `expected_enrol_per_district = state_total_enrolments / number_of_districts_in_state`
- `VGS_proxy = 1 − (observed_enrolments / expected_enrol_per_district)`

✅ Higher **VGS_proxy** = district is far below state-average activity → potential invisibility risk.
""")

    dist = enrol_f.groupby(["state", "district"]).agg(
        observed_enrolments=("total_enrolments", "sum")
    ).reset_index()

    state_stats = dist.groupby("state").agg(
        state_total=("observed_enrolments", "sum"),
        num_districts=("district", "nunique")
    ).reset_index()

    dist = dist.merge(state_stats, on="state", how="left")
    dist["expected_enrol_per_district"] = dist["state_total"] / dist["num_districts"]
    dist["VGS_proxy"] = 1 - (dist["observed_enrolments"] / dist["expected_enrol_per_district"])
    dist["VGS_proxy"] = dist["VGS_proxy"].clip(lower=-1, upper=5)

    # Add MPI and BSI (deep insights)
    d_demo = demo_f.groupby(["state", "district"]).agg(demo=("total_demo_updates", "sum")).reset_index()
    d_bio = bio_f.groupby(["state", "district"]).agg(bio=("total_bio_updates", "sum")).reset_index()

    dist = dist.merge(d_demo, on=["state", "district"], how="left").merge(d_bio, on=["state", "district"], how="left")
    dist = dist.fillna(0)

    dist["MPI"] = safe_div(dist["demo"], dist["observed_enrolments"])
    dist["BSI"] = safe_div(dist["bio"], dist["observed_enrolments"])

    dist["risk"] = pd.cut(dist["VGS_proxy"], bins=[-10, 0.10, 0.20, 10],
                          labels=["Low", "Medium", "High"])

    topN = st.slider("Show Top N Hotspots", 5, 50, 20)
    hotspots = dist.sort_values("VGS_proxy", ascending=False).head(topN)

    colA, colB = st.columns([1, 1])
    with colA:
        fig4 = px.bar(
            hotspots.sort_values("VGS_proxy"),
            x="VGS_proxy",
            y=hotspots.sort_values("VGS_proxy")["district"] + " (" + hotspots.sort_values("VGS_proxy")["state"] + ")",
            orientation="h",
            title=f"Top {topN} Districts by Visibility Gap Score (VGS_proxy)"
        )
        st.plotly_chart(fig4, use_container_width=True)

    with colB:
        st.dataframe(
            hotspots[["state", "district", "observed_enrolments", "expected_enrol_per_district", "VGS_proxy", "MPI", "BSI", "risk"]],
            use_container_width=True
        )

    st.subheader("MPI vs BSI (Bubble = Enrolments)")
    fig5 = px.scatter(
        dist,
        x="MPI", y="BSI",
        size="observed_enrolments",
        color="risk",
        hover_data=["state", "district", "VGS_proxy", "observed_enrolments"],
        title="District Typology: Mobility Pressure vs Biometric Stress"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.success("✅ This is your FINAL RESULT proof: hotspot zones + risk type (mobility / biometric stress).")

# ----------------------------
# TAB 3: Action Plan (Decision output)
# ----------------------------
with tab3:
    st.subheader("🛠️ Governance Action Plan (Top Hotspots)")

    dist_sorted = dist.sort_values("VGS_proxy", ascending=False).head(25).copy()

    def recommend(row):
        actions = []
        if row["VGS_proxy"] > 0.20:
            actions.append("Mobile enrolment + outreach camps")
        if row["MPI"] > 0.50:
            actions.append("Assisted demographic update drive (migration/churn)")
        if row["BSI"] > 0.50:
            actions.append("Biometric recapture support + assisted verification")
        if not actions:
            actions.append("Monitor (low risk)")
        return " | ".join(actions)

    dist_sorted["recommended_action"] = dist_sorted.apply(recommend, axis=1)

    st.dataframe(
        dist_sorted[["state", "district", "VGS_proxy", "MPI", "BSI", "risk", "recommended_action"]],
        use_container_width=True
    )

    st.info("✅ This converts your analysis into a practical output: Detect → Prioritize → Intervene → Monitor")

st.caption("Note: VGS_proxy is an Aadhaar-only intra-state proxy for invisibility risk. Final policy action must validate hotspots with local baselines / census microdata when available.")
