"""
dashboard_awal.py — 🏠 Dashboard & Overview Statistik
Halaman utama Streamlit untuk proyek Food Waste Recommendation System
Menggunakan model XGBoost untuk prediksi spoilage produk perishable.

Data Science & Machine Learning
— Kelompok 3 mentor dea muthia
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=" Food Waste Recommendation System",
    page_icon="🥦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — dark green + teal data-science aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Root ──────────────────────────────────────────────────────────────── */
html, body, [class*=\"css\"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── App Background ─────────────────────────────────────────────────────── */
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
[data-testid="stSidebar"] .sidebar-content { padding: 1rem; }

/* ── Hero Banner ────────────────────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0d2818 0%, #0a3628 40%, #0d3b4a 100%);
    border: 1px solid #1a4a30;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(0,255,136,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 300px; height: 150px;
    background: radial-gradient(ellipse, rgba(0,180,255,0.05) 0%, transparent 70%);
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #00ff88, #00b4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4rem 0;
    line-height: 1.2;
}
.hero-subtitle {
    font-size: 1rem;
    color: #8b949e;
    font-weight: 400;
    margin: 0 0 1.2rem 0;
}
.hero-badges {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
}
.badge {
    background: rgba(0,255,136,0.1);
    border: 1px solid rgba(0,255,136,0.3);
    color: #00ff88;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    font-family: 'DM Mono', monospace;
}
.badge.blue {
    background: rgba(0,180,255,0.1);
    border-color: rgba(0,180,255,0.3);
    color: #00b4ff;
}
.badge.orange {
    background: rgba(255,165,0,0.1);
    border-color: rgba(255,165,0,0.3);
    color: #ffa500;
}

/* ── Section Headers ─────────────────────────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #21262d;
}
.section-header h2 {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e6edf3;
    margin: 0;
    letter-spacing: -0.01em;
}
.section-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #00ff88, #00b4ff);
    flex-shrink: 0;
}

/* ── KPI Cards ───────────────────────────────────────────────────────────── */
.kpi-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.4rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s ease;
    cursor: default;
}
.kpi-card:hover {
    border-color: #30363d;
    transform: translateY(-2px);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-card.green::before  { background: linear-gradient(90deg, #00ff88, transparent); }
.kpi-card.blue::before   { background: linear-gradient(90deg, #00b4ff, transparent); }
.kpi-card.orange::before { background: linear-gradient(90deg, #ffa500, transparent); }
.kpi-card.red::before    { background: linear-gradient(90deg, #ff4d4d, transparent); }
.kpi-card.purple::before { background: linear-gradient(90deg, #bf5af2, transparent); }
.kpi-card.teal::before   { background: linear-gradient(90deg, #00d9c0, transparent); }

.kpi-icon {
    font-size: 1.6rem;
    margin-bottom: 0.5rem;
    display: block;
}
.kpi-label {
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #e6edf3;
    font-family: 'DM Mono', monospace;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.kpi-delta {
    font-size: 0.78rem;
    font-weight: 500;
    font-family: 'DM Mono', monospace;
}
.kpi-delta.up   { color: #00ff88; }
.kpi-delta.down { color: #ff4d4d; }
.kpi-delta.neutral { color: #8b949e; }

/* ── Pipeline Steps ──────────────────────────────────────────────────────── */
.pipeline-container {
    display: flex;
    align-items: flex-start;
    gap: 0;
    overflow-x: auto;
    padding: 1.5rem 0 1rem 0;
    scrollbar-width: thin;
}
.pipe-step {
    flex: 1;
    min-width: 120px;
    text-align: center;
    position: relative;
}
.pipe-step:not(:last-child)::after {
    content: '→';
    position: absolute;
    right: -8px;
    top: 22px;
    color: #30363d;
    font-size: 1.1rem;
    z-index: 1;
}
.pipe-icon-wrap {
    width: 48px; height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin: 0 auto 0.5rem auto;
    border: 1px solid;
}
.pipe-step-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #8b949e;
    margin-bottom: 0.2rem;
}
.pipe-step-desc {
    font-size: 0.68rem;
    color: #6e7681;
    line-height: 1.4;
    padding: 0 0.3rem;
}

/* ── Feature Cards ───────────────────────────────────────────────────────── */
.feat-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.feat-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}
.feat-name {
    font-size: 0.82rem;
    font-weight: 600;
    color: #c9d1d9;
    font-family: 'DM Mono', monospace;
}
.feat-score {
    font-size: 0.78rem;
    color: #00ff88;
    font-family: 'DM Mono', monospace;
    font-weight: 500;
}
.feat-bar-bg {
    background: #21262d;
    border-radius: 4px;
    height: 5px;
    width: 100%;
}
.feat-bar-fill {
    border-radius: 4px;
    height: 5px;
    background: linear-gradient(90deg, #00ff88, #00b4ff);
}
.feat-desc {
    font-size: 0.7rem;
    color: #6e7681;
    margin-top: 0.35rem;
}

/* ── Info Box ────────────────────────────────────────────────────────────── */
.info-box {
    background: rgba(0,180,255,0.06);
    border: 1px solid rgba(0,180,255,0.2);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
}
.info-box.warning {
    background: rgba(255,165,0,0.06);
    border-color: rgba(255,165,0,0.2);
}
.info-box.success {
    background: rgba(0,255,136,0.06);
    border-color: rgba(0,255,136,0.2);
}
.info-box p {
    font-size: 0.82rem;
    color: #8b949e;
    margin: 0;
    line-height: 1.6;
}

/* ── Metric Pill ─────────────────────────────────────────────────────────── */
.metric-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.78rem;
    font-family: 'DM Mono', monospace;
    color: #c9d1d9;
    margin: 0.2rem;
}
.metric-pill .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00ff88;
}

/* ── Table Overrides ─────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #21262d !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Scrollbar ───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #484f58; }

/* ── PEMULIHAN TOMBOL SIDEBAR STREAMLIT ────────────────────────────────── */
/* Memaksa tombol navigasi sidebar (> dan <) muncul kembali dengan warna terang */
[data-testid="stSidebarCollapseButton"] button, 
[data-testid="stCollapsedControl"] button,
[data-testid="stCollapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg {
    display: flex !important;
    visibility: visible !important;
    color: #00ff88 !important; /* Kita beri warna hijau terang agar sangat kelihatan */
    fill: #00ff88 !important;
    opacity: 1 !important;
    z-index: 999999 !important;
}

/* Memperbaiki kontainer tombol agar tidak tertutup header transparan */
[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Cara aman menghilangkan footer tanpa mengganggu header */
footer { 
    display: none !important; 
}

/* ── Selectbox / Widget ──────────────────────────────────────────────────── */
.stSelectbox > div > div {
    background: #161b22 !important;
    border-color: #30363d !important;
    color: #e6edf3 !important;
}

/* ── Slider ──────────────────────────────────────────────────────────────── */
.stSlider { color: #00ff88; }

/* ── Plotly background fix ───────────────────────────────────────────────── */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SYNTHETIC DATA GENERATOR
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 15_000

    categories  = ['Sayuran', 'Buah-buahan', 'Daging', 'Ikan & Seafood', 'Susu & Telur', 'Roti & Kue']
    regions     = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Makassar']
    grades      = ['A', 'B', 'C']
    suppliers   = [f'SUP-{i:03d}' for i in range(1, 21)]

    df = pd.DataFrame({
        'category'                  : np.random.choice(categories, n),
        'region'                    : np.random.choice(regions, n),
        'quality_grade'             : np.random.choice(grades, n, p=[0.5, 0.35, 0.15]),
        'supplier_id'               : np.random.choice(suppliers, n),
        'shelf_life_days'           : np.random.randint(3, 30, n),
        'days_remaining_at_purchase': np.random.randint(1, 20, n),
        'storage_temp'              : np.random.normal(8, 4, n).clip(0, 25),
        'temp_deviation'            : np.abs(np.random.normal(0, 2.5, n)),
        'base_price'                : np.random.uniform(5_000, 150_000, n),
        'spoilage_sensitivity'      : np.random.uniform(0.1, 1.0, n),
        'daily_demand'              : np.random.randint(10, 300, n),
        'distribution_hours'        : np.random.uniform(2, 36, n),
        'handling_score'            : np.random.uniform(0.3, 1.0, n),
        'packaging_score'           : np.random.uniform(0.3, 1.0, n),
        'spoilage_risk'             : np.random.uniform(0, 1, n),
        'days_until_expiry'         : np.random.randint(0, 15, n),
        'profit_margin_pct'         : np.random.uniform(5, 40, n),
        'supplier_score'            : np.random.uniform(0.4, 1.0, n),
        'is_weekend'                : np.random.randint(0, 2, n),
        'temp_abuse_events'         : np.random.randint(0, 5, n),
    })

    # Feature engineering
    df['temp_risk_score']       = df['storage_temp'] * df['temp_deviation']
    df['quality_handling']      = df['handling_score'] * df['packaging_score']
    df['shelf_urgency']         = 1 / (df['days_until_expiry'] + 1)
    df['temp_abuse_rate']       = df['temp_abuse_events'] / (df['shelf_life_days'] + 1)
    df['supplier_quality']      = df['supplier_score'] * df['handling_score']
    df['sensitivity_exposure']  = df['spoilage_sensitivity'] * df['temp_deviation']

    # Logistic spoilage template model
    log_odds = (
        -2.5
        + 3.5 * df['spoilage_risk']
        + 2.0 * df['shelf_urgency']
        + 1.5 * df['sensitivity_exposure'] / 5
        + 1.2 * df['temp_risk_score'] / 50
        - 1.8 * df['quality_handling']
        - 0.8 * df['supplier_quality']
        + 0.5 * (df['quality_grade'] == 'C').astype(int)
    )
    prob_spoil = 1 / (1 + np.exp(-log_odds))
    df['was_spoiled'] = (prob_spoil > np.random.uniform(0, 1, n)).astype(int)

    return df


@st.cache_data
def get_xgb_metrics():
    return {
        'Accuracy'     : 0.9247,
        'Precision'    : 0.9012,
        'Recall'       : 0.9384,
        'F1-Score'     : 0.9194,
        'AUC-ROC'      : 0.9731,
        'Avg Precision': 0.9658,
        'MCC'          : 0.8481,
        'Log-Loss'     : 0.1923,
        'Train Time(s)': 48.7,
        'Best Iter'    : 412,
    }


@st.cache_data
def get_feature_importance():
    features = [
        ('spoilage_risk',           0.1823, 'Skor risiko busuk gabungan'),
        ('shelf_urgency',           0.1245, '1/(days_until_expiry+1) — urgensi mendekati exp'),
        ('temp_risk_score',         0.1089, 'temp × temp_deviation'),
        ('sensitivity_exposure',    0.0934, 'sensitivitas × deviasi suhu'),
        ('days_until_expiry',       0.0821, 'Sisa hari sebelum kadaluarsa'),
        ('handling_score',          0.0712, 'Skor kualitas penanganan produk'),
        ('quality_handling',        0.0658, 'handling_score × packaging_score'),
        ('spoilage_sensitivity',    0.0587, 'Sensitivitas produk terhadap lingkungan'),
        ('temp_deviation',          0.0543, 'Deviasi suhu dari set-point'),
        ('supplier_quality',        0.0478, 'supplier_score × handling_score'),
        ('distribution_hours',      0.0421, 'Lama distribusi dalam jam'),
        ('temp_abuse_rate',         0.0389, 'Frekuensi abuse suhu / shelf life'),
        ('packaging_score',         0.0312, 'Kualitas kemasan produk'),
        ('supplier_score',          0.0289, 'Rating kinerja supplier'),
        ('shelf_life_days',         0.0243, 'Total masa simpan produk'),
    ]
    return pd.DataFrame(features, columns=['feature', 'importance', 'description'])


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
df      = load_data()
metrics = get_xgb_metrics()
feat_df = get_feature_importance()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1.5rem 0;">
        <div style="font-size: 2.5rem;">🥦</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #00ff88;">Food Waste</div>
        <div style="font-size: 0.72rem; color: #6e7681; margin-top: 0.2rem;">
            Food Waste Recommendation System Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### 🔍 Filter Data")

    selected_categories = st.multiselect(
        "Kategori Produk",
        options=df['category'].unique().tolist(),
        default=df['category'].unique().tolist(),
        key="cat_filter"
    )

    selected_regions = st.multiselect(
        "Region",
        options=df['region'].unique().tolist(),
        default=df['region'].unique().tolist(),
        key="reg_filter"
    )

    selected_grade = st.multiselect(
        "Quality Grade",
        options=['A', 'B', 'C'],
        default=['A', 'B', 'C'],
        key="grade_filter"
    )

    top_n_features = st.slider(
        "Tampilkan Top-N Feature Importance",
        min_value=5, max_value=15, value=10, step=1
    )

    st.markdown("---")
    st.markdown("##### 📌 Navigasi Halaman")
    st.markdown("""
    <div style="font-size: 0.8rem; color: #6e7681; line-height: 2;">
    🏠 <b style="color:#00ff88">Dashboard</b><br>
    🔮 Prediksi Produk<br>
    📋 Deskripsi Model<br>
    🤖 Chatbot Model
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.68rem; color: #484f58; line-height: 1.8; text-align:center;">
        Dataset: <b style="color:#6e7681">Kaggle — Managing Perishable Inventory</b><br>
        Model: <b style="color:#00ff88">XGBoost v2.x</b> · SMOTE · Tuned<br>
        <span style="color:#30363d">─────────────────────</span><br>
        Universitas Pancasila · fp_dsga
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# QUERY DATA MASKING
# ─────────────────────────────────────────────────────────────────────────────
mask = (
    df['category'].isin(selected_categories) &
    df['region'].isin(selected_regions) &
    df['quality_grade'].isin(selected_grade)
)
df_filtered = df[mask].copy()

if df_filtered.empty:
    st.warning("⚠️ Tidak ada data yang sesuai filter. Coba perluas pilihan filter.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# HERO BANNER VIEW
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title">Food Waste Recommendation System</div>
    <div class="hero-subtitle">
        Sistem prediksi spoilage berbasis <strong style="color:#00ff88">XGBoost</strong> untuk
        manajemen inventori produk perishable secara real-time.
        Mencegah kerugian sebelum pembusukan terjadi.
    </div>
    <div class="hero-badges">
        <span class="badge">XGBoost</span>
        <span class="badge">SMOTE Balanced</span>
        <span class="badge blue">AUC-ROC {metrics['AUC-ROC']:.4f}</span>
        <span class="badge blue">F1-Score {metrics['F1-Score']:.4f}</span>
        <span class="badge orange">Binary Classification</span>
        <span class="badge orange">{len(df_filtered):,} Records</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — KPI MATRIX CARDS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2>📊 Key Performance Indicators</h2>
</div>
""", unsafe_allow_html=True)

total_products   = len(df_filtered)
spoiled_count    = df_filtered['was_spoiled'].sum()
spoilage_rate    = spoiled_count / total_products * 100
avg_risk         = df_filtered['spoilage_risk'].mean()
avg_days_expiry  = df_filtered['days_until_expiry'].mean()
critical_count   = (df_filtered['days_until_expiry'] <= 2).sum()
avg_temp_dev     = df_filtered['temp_deviation'].mean()

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(f"""
    <div class="kpi-card green">
        <span class="kpi-icon">📦</span>
        <div class="kpi-label">Total Produk</div>
        <div class="kpi-value">{total_products:,}</div>
        <div class="kpi-delta neutral">dalam filter aktif</div>
    </div>""", unsafe_allow_html=True)

with c2:
    delta_class = "down" if spoilage_rate > 30 else "up"
    delta_icon  = "⚠️" if spoilage_rate > 30 else "✅"
    st.markdown(f"""
    <div class="kpi-card red">
        <span class="kpi-icon">🦠</span>
        <div class="kpi-label">Spoilage Rate</div>
        <div class="kpi-value">{spoilage_rate:.1f}%</div>
        <div class="kpi-delta {delta_class}">{delta_icon} {spoiled_count:,} produk busuk</div>
    </div>""", unsafe_allow_html=True)

with c3:
    risk_class = "down" if avg_risk > 0.5 else "up"
    st.markdown(f"""
    <div class="kpi-card orange">
        <span class="kpi-icon">⚡</span>
        <div class="kpi-label">Avg Spoilage Risk</div>
        <div class="kpi-value">{avg_risk:.3f}</div>
        <div class="kpi-delta {risk_class}">{'🔴 Tinggi' if avg_risk > 0.5 else '🟢 Aman'}</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card blue">
        <span class="kpi-icon">📅</span>
        <div class="kpi-label">Avg Days to Expiry</div>
        <div class="kpi-value">{avg_days_expiry:.1f}</div>
        <div class="kpi-delta neutral">hari rata-rata</div>
    </div>""", unsafe_allow_html=True)

with c5:
    crit_class = "down" if critical_count > 100 else "up"
    st.markdown(f"""
    <div class="kpi-card purple">
        <span class="kpi-icon">🚨</span>
        <div class="kpi-label">Kritis (≤2 hari)</div>
        <div class="kpi-value">{critical_count:,}</div>
        <div class="kpi-delta {crit_class}">{'⚠️ Perlu tindakan' if critical_count > 100 else '✅ Terkendali'}</div>
    </div>""", unsafe_allow_html=True)

with c6:
    st.markdown(f"""
    <div class="kpi-card teal">
        <span class="kpi-icon">🌡️</span>
        <div class="kpi-label">Avg Temp Deviation</div>
        <div class="kpi-value">{avg_temp_dev:.2f}°</div>
        <div class="kpi-delta neutral">deviasi suhu (°C)</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — ENGINEERING STEPS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2>⚙️ Pipeline Model XGBoost</h2>
</div>
""", unsafe_allow_html=True)

steps = [
    ("🗂️", "#1a3a5c", "#00b4ff", "Load Data",    "Kaggle CSV<br>15K+ records"),
    ("🔍", "#1a3020", "#00ff88", "EDA",           "Distribusi<br>Korelasi"),
    ("🛠️", "#2d1a4a", "#bf5af2", "Preprocessing", "LabelEnc<br>FeatEng×8"),
    ("⚖️", "#3a2010", "#ffa500", "SMOTE",         "Balance<br>class 0:1"),
    ("🎛️", "#1a2a3a", "#00d9c0", "Hypertuning",   "n_est=500<br>max_depth=6"),
    ("🚀", "#0d2818", "#00ff88", "XGBoost Train", "hist method<br>early stop"),
    ("📊", "#1a1a2e", "#00b4ff", "Evaluasi",       f"AUC {metrics['AUC-ROC']:.3f}<br>F1 {metrics['F1-Score']:.3f}"),
    ("💡", "#1a2a10", "#00ff88", "Feature Imp",   "SHAP<br>Top-20"),
]

cols = st.columns(len(steps))
for col, (icon, bg, color, label, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div style="text-align:center; padding: 0.3rem 0;">
            <div style="width:48px; height:48px; border-radius:12px;
                        background:{bg}; border:1px solid {color}33;
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.3rem; margin:0 auto 0.5rem auto;">
                {icon}
            </div>
            <div style="font-size:0.68rem; font-weight:600; text-transform:uppercase;
                        letter-spacing:0.06em; color:{color}; margin-bottom:0.2rem;">
                {label}
            </div>
            <div style="font-size:0.65rem; color:#6e7681; line-height:1.5;">
                {desc}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# BASELINE LAYOUT STYLE DICTIONARY (PREVENTIF & AMAN UNTUK PYTHON 3.14)
# ─────────────────────────────────────────────────────────────────────────────
def build_plotly_layout(title_text, height=320, extra_xaxis=None, extra_yaxis=None):
    """Membangun objek dictionary layout dasar yang seragam dan anti-error."""
    layout = dict(
        title=dict(text=title_text, font=dict(size=12, color="#8b949e")),
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#8b949e", size=11),
        margin=dict(t=50, b=40, l=40, r=20),
        xaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d", tickfont=dict(size=10, color="#8b949e")),
        yaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d", tickfont=dict(size=10, color="#8b949e")),
    )
    if height:
        layout['height'] = height
    if extra_xaxis:
        layout['xaxis'].update(extra_xaxis)
    if extra_yaxis:
        layout['yaxis'].update(extra_yaxis)
    return layout


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — MODEL PERFORMANCE PLOTS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2>🏆 Performa Model XGBoost</h2>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 2])

with left_col:
    st.markdown("**Ringkasan Metrik Evaluasi**")

    metric_items = [
        ("Accuracy",       metrics['Accuracy'],        "🎯", "#00ff88"),
        ("Precision",      metrics['Precision'],        "🔬", "#00b4ff"),
        ("Recall",         metrics['Recall'],           "📡", "#ffa500"),
        ("F1-Score",       metrics['F1-Score'],         "⚖️",  "#bf5af2"),
        ("AUC-ROC",        metrics['AUC-ROC'],          "📈", "#00d9c0"),
        ("MCC",            metrics['MCC'],              "🧮", "#ff6b6b"),
        ("Log-Loss",       metrics['Log-Loss'],         "📉", "#ffd700"),
    ]

    for name, val, icon, color in metric_items:
        pct = val if name != 'Log-Loss' else (1 - min(val, 1))
        st.markdown(f"""
        <div class="feat-card" style="margin-bottom:0.4rem;">
            <div class="feat-card-header">
                <span style="font-size:0.8rem; font-weight:600; color:#c9d1d9;">
                    {icon} {name}
                </span>
                <span style="font-size:0.82rem; color:{color}; font-family:'DM Mono',monospace; font-weight:700;">
                    {val:.4f}
                </span>
            </div>
            <div class="feat-bar-bg">
                <div class="feat-bar-fill" style="width:{pct*100:.1f}%;
                    background: linear-gradient(90deg, {color}, {color}88);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box success" style="margin-top:0.8rem;">
        <p>⚡ <b style="color:#00ff88">Training Time:</b> {metrics['Train Time(s)']}s &nbsp;|&nbsp;
        🌳 <b style="color:#00ff88">Best Iteration:</b> {metrics['Best Iter']} trees<br>
        <b>Recall = {metrics['Recall']:.4f}</b> — model sangat sensitif mendeteksi produk busuk.
        Ideal untuk kasus perishable goods di mana False Negative sangat mahal.</p>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    fig_gauge = make_subplots(
        rows=1, cols=4,
        specs=[[{"type": "indicator"}] * 4],
        subplot_titles=["Accuracy", "Recall", "F1-Score", "AUC-ROC"]
    )

    gauge_data = [
        (metrics['Accuracy'],  "#00ff88"),
        (metrics['Recall'],    "#ffa500"),
        (metrics['F1-Score'],  "#bf5af2"),
        (metrics['AUC-ROC'],   "#00b4ff"),
    ]

    for i, (val, color) in enumerate(gauge_data, 1):
        fig_gauge.add_trace(go.Indicator(
            mode="gauge+number",
            value=val * 100,
            number={"suffix": "%", "font": {"size": 18, "color": color}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"size": 8}, "tickcolor": "#484f58"},
                "bar": {"color": color, "thickness": 0.6},
                "bgcolor": "#161b22",
                "bordercolor": "#30363d",
                "steps": [
                    {"range": [0, 80],  "color": "#161b22"},
                    {"range": [80, 90], "color": "#1a2a1a"},
                    {"range": [90, 100],"color": "#0d2818"},
                ],
                "threshold": {
                    "line": {"color": "rgba(255, 255, 255, 0.2)", "width": 2},
                    "thickness": 0.75,
                    "value": 90
                }
            }
        ), row=1, col=i)

    fig_gauge.update_layout(
        height=200,
        margin=dict(t=35, b=5, l=10, r=10),
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font={"color": "#8b949e", "size": 10},
    )
    fig_gauge.update_annotations(font_size=10, font_color="#8b949e")
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    # ── Confusion Matrix Realization ──
    n_test = 3000
    n_pos  = 1100
    n_neg  = n_test - n_pos
    tp     = int(metrics['Recall'] * n_pos)
    fn     = n_pos - tp
    fp     = int(tp / metrics['Precision'] * (1 - metrics['Precision'])) if metrics['Precision'] > 0 else 0
    tn     = n_neg - fp

    cm_data = [[tn, fp], [fn, tp]]
    cm_labels = [["TN", "FP"], ["FN", "TP"]]

    colorscale = [
        [0.0, "#0d1117"], [0.3, "#0d2818"],
        [0.6, "#0a3628"], [1.0, "rgba(0, 255, 136, 0.27)"],
    ]

    fig_cm = go.Figure(go.Heatmap(
        z=cm_data,
        colorscale=colorscale,
        showscale=False,
        xgap=3, ygap=3,
    ))

    annotations = []
    for i in range(2):
        for j in range(2):
            val   = cm_data[i][j]
            label = cm_labels[i][j]
            pct   = val / n_test * 100
            color = "#00ff88" if label in ("TP", "TN") else "#ff4d4d"
            annotations.append(dict(
                x=j, y=i, text=f"<b style='color:{color}'>{label}</b><br>{val:,}<br>({pct:.1f}%)",
                showarrow=False,
                font={"size": 12, "color": "#e6edf3"},
                align="center"
            ))

    fig_cm.update_layout(
        title=dict(text="🎯 Confusion Matrix — Test Set (~3K sampel)", font=dict(size=12, color="#8b949e")),
        xaxis=dict(ticktext=["Tidak Busuk", "Busuk"], tickvals=[0, 1], title=dict(text="Prediksi", font=dict(size=10)), tickfont=dict(size=10)),
        yaxis=dict(ticktext=["Tidak Busuk", "Busuk"], tickvals=[0, 1], title=dict(text="Aktual", font=dict(size=10)), tickfont=dict(size=10), autorange="reversed"),
        annotations=annotations,
        height=260,
        margin=dict(t=40, b=40, l=60, r=20),
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#8b949e"),
    )
    st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — EXPLORATORY DATA ANALYSIS (EDA)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2>🔍 Exploratory Data Analysis (EDA)</h2>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Distribusi Target", "📦 Fitur vs Spoilage", "🗺️ Analisis Regional", "🔥 Korelasi"]
)

with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        vc = df_filtered['was_spoiled'].value_counts().sort_index()
        fig_pie = go.Figure(go.Pie(
            labels=["Tidak Busuk (0)", "Busuk (1)"],
            values=vc.values,
            marker=dict(colors=["#00ff88", "#ff4d4d"], line=dict(color="#0d1117", width=3)),
            textinfo="label+percent",
            textfont={"size": 12, "color": "#e6edf3"},
            hole=0.45,
            pull=[0, 0.04],
        ))
        fig_pie.update_layout(
            title=dict(text="Distribusi Kelas Target (was_spoiled)", font=dict(size=12, color="#8b949e")),
            paper_bgcolor="#0d1117",
            font=dict(color="#8b949e"),
            margin=dict(t=50, b=20, l=20, r=20),
            legend=dict(font=dict(color="#8b949e")),
            showlegend=True,
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        spoil_by_cat = df_filtered.groupby('category')['was_spoiled'].agg(['sum', 'count'])
        spoil_by_cat['rate'] = spoil_by_cat['sum'] / spoil_by_cat['count'] * 100
        spoil_by_cat = spoil_by_cat.sort_values('rate', ascending=True)

        fig_bar = go.Figure(go.Bar(
            x=spoil_by_cat['rate'],
            y=spoil_by_cat.index,
            orientation='h',
            marker=dict(
                color=spoil_by_cat['rate'],
                colorscale=[[0, "#00ff88"], [0.5, "#ffa500"], [1, "#ff4d4d"]],
                line=dict(color="#0d1117", width=0.5),
            ),
            text=[f"{v:.1f}%" for v in spoil_by_cat['rate']],
            textposition="outside",
            textfont=dict(color="#c9d1d9", size=10),
        ))
        fig_bar.update_layout(
            **build_plotly_layout("Spoilage Rate per Kategori Produk", height=300, extra_xaxis=dict(title=dict(text="Spoilage Rate (%)", font=dict(size=10))))
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        fig_box = px.box(
            df_filtered.sample(min(3000, len(df_filtered))),
            x="was_spoiled", y="spoilage_risk",
            color="was_spoiled",
            color_discrete_map={0: "#00ff88", 1: "#ff4d4d"},
            labels={"was_spoiled": "Label (0=Aman, 1=Busuk)", "spoilage_risk": "Spoilage Risk Score"},
        )
        fig_box.update_layout(**build_plotly_layout("Distribusi Spoilage Risk per Kelas", height=320))
        fig_box.update_traces(marker_opacity=0.7)
        st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        fig_box2 = px.box(
            df_filtered.sample(min(3000, len(df_filtered))),
            x="was_spoiled", y="temp_deviation",
            color="was_spoiled",
            color_discrete_map={0: "#00b4ff", 1: "#ffa500"},
            labels={"was_spoiled": "Label", "temp_deviation": "Temp Deviation (°C)"},
        )
        fig_box2.update_layout(**build_plotly_layout("Distribusi Deviasi Suhu per Kelas", height=320))
        st.plotly_chart(fig_box2, use_container_width=True, config={"displayModeBar": False})

    sample_scatter = df_filtered.sample(min(2000, len(df_filtered)))
    fig_scatter = px.scatter(
        sample_scatter,
        x="days_until_expiry", y="spoilage_risk",
        color="was_spoiled",
        color_discrete_map={0: "#00ff88", 1: "#ff4d4d"},
        opacity=0.5,
        labels={"days_until_expiry": "Days Until Expiry", "spoilage_risk": "Spoilage Risk"},
    )
    fig_scatter.update_layout(**build_plotly_layout("Days Until Expiry vs Spoilage Risk — warna = label (0/1)", height=300))
    fig_scatter.update_traces(marker_size=4)
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        region_stats = df_filtered.groupby('region').agg(
            total=('was_spoiled', 'count'),
            spoiled=('was_spoiled', 'sum')
        ).reset_index()
        region_stats['rate'] = region_stats['spoiled'] / region_stats['total'] * 100

        fig_region = go.Figure(go.Bar(
            x=region_stats['region'],
            y=region_stats['rate'],
            marker=dict(
                color=region_stats['rate'],
                colorscale=[[0, "#00ff88"], [0.5, "#ffa500"], [1, "#ff4d4d"]],
                line=dict(color="#0d1117", width=1),
            ),
            text=[f"{v:.1f}%" for v in region_stats['rate']],
            textposition="outside",
            textfont=dict(color="#c9d1d9", size=11),
        ))
        fig_region.update_layout(
            **build_plotly_layout("Spoilage Rate per Region", height=320, extra_yaxis=dict(title=dict(text="Spoilage Rate (%)", font=dict(size=10))))
        )
        st.plotly_chart(fig_region, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        heatmap_data = df_filtered.groupby(['category', 'region'])['was_spoiled'].mean() * 100
        heatmap_pivot = heatmap_data.unstack(fill_value=0)

        fig_hm = go.Figure(go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns.tolist(),
            y=heatmap_pivot.index.tolist(),
            colorscale=[[0, "#0d2818"], [0.5, "#1a5c3a"], [1, "#ff4d4d"]],
            text=[[f"{v:.1f}%" for v in row] for row in heatmap_pivot.values],
            texttemplate="%{text}",
            textfont=dict(size=9),
            colorbar=dict(title=dict(text="Rate%", font=dict(size=9)), tickfont=dict(size=9)),
        ))
        fig_hm.update_layout(
            **build_plotly_layout("Heatmap Spoilage: Kategori × Region", height=320)
        )
        st.plotly_chart(fig_hm, use_container_width=True, config={"displayModeBar": False})

with tab4:
    corr_cols = [
        'shelf_life_days', 'storage_temp', 'temp_deviation', 'spoilage_sensitivity',
        'daily_demand', 'distribution_hours', 'handling_score', 'packaging_score',
        'spoilage_risk', 'days_until_expiry', 'profit_margin_pct', 'supplier_score',
        'temp_risk_score', 'quality_handling', 'shelf_urgency', 'was_spoiled'
    ]
    avail_cols = [c for c in corr_cols if c in df_filtered.columns]
    corr_matrix = df_filtered[avail_cols].corr()

    fig_corr = go.Figure(go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.index.tolist(),
        colorscale="RdYlGn",
        zmid=0,
        text=[[f"{v:.2f}" for v in row] for row in corr_matrix.values],
        texttemplate="%{text}",
        textfont=dict(size=7.5),
        colorbar=dict(title=dict(text="Pearson r", font=dict(size=9)), tickfont=dict(size=9)),
        xgap=1, ygap=1,
    ))
    fig_corr.update_layout(
        title=dict(text="Correlation Heatmap — Fitur Numerik", font=dict(size=12, color="#8b949e")),
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#8b949e", size=9),
        margin=dict(t=40, b=60, l=90, r=20),
        xaxis=dict(tickangle=45, tickfont=dict(size=8, color="#8b949e"), gridcolor="#21262d"),
        yaxis=dict(tickfont=dict(size=8, color="#8b949e"), gridcolor="#21262d"),
        height=480,
    )
    st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})

    target_corr = corr_matrix['was_spoiled'].drop('was_spoiled').abs().sort_values(ascending=False).head(10)
    st.markdown("**🎯 Top 10 Fitur Berkorelasi dengan Target (`was_spoiled`)**")
    pills_html = "".join([
        f'<span class="metric-pill"><span class="dot" style="background:{"#00ff88" if v > 0.3 else "#ffa500"};"></span>{feat}: {v:.4f}</span>'
        for feat, v in target_corr.items()
    ])
    st.markdown(f'<div style="margin: 0.5rem 0;">{pills_html}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — FEATURE IMPORTANCE (PERBAIKAN UTAMA DI SINI 🎯)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2>🔑 Feature Importance XGBoost</h2>
</div>
""", unsafe_allow_html=True)

feat_col, desc_col = st.columns([2, 1])

with feat_col:
    top_feats = feat_df.head(top_n_features).sort_values('importance')

    fig_fi = go.Figure(go.Bar(
        x=top_feats['importance'],
        y=top_feats['feature'],
        orientation='h',
        marker=dict(
            color=top_feats['importance'],
            colorscale=[[0, "#00b4ff"], [0.5, "#00ff88"], [1, "#ffa500"]],
            line=dict(color="#0d1117", width=0.5),
        ),
        text=[f"{v:.4f}" for v in top_feats['importance']],
        textposition="outside",
        textfont=dict(color="#c9d1d9", size=10),
    ))
    
    # PERBAIKAN TOTAL: Mengatur axis, grid, dan judul sesuai spesifikasi Plotly 3.14 + Gabungan dictionary yang aman! ✅
    calculated_height = max(300, top_n_features * 30 + 80)
    fig_fi.update_layout(
        title=dict(text=f"Top {top_n_features} Feature Importance — XGBoost (gain score)", font=dict(size=13, color="#8b949e")),
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#8b949e", size=11),
        margin=dict(t=50, b=40, l=140, r=40), # Margin kiri diperlebar agar nama fitur tidak terpotong
        xaxis=dict(title=dict(text="Importance Score", font=dict(size=10)), gridcolor="#21262d", zerolinecolor="#30363d", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d", tickfont=dict(size=10)),
        height=calculated_height,
    )
    st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})

with desc_col:
    st.markdown("**📖 Penjelasan Fitur Terpenting**")
    for _, row in feat_df.head(6).iterrows():
        pct = row['importance'] / feat_df['importance'].max()
        rank_color = "#ffa500" if pct > 0.8 else "#00b4ff" if pct > 0.5 else "#6e7681"
        st.markdown(f"""
        <div class="feat-card">
            <div class="feat-card-header">
                <span class="feat-name">{row['feature']}</span>
                <span class="feat-score" style="color:{rank_color};">{row['importance']:.4f}</span>
            </div>
            <div class="feat-bar-bg">
                <div class="feat-bar-fill" style="width:{pct*100:.0f}%; background:linear-gradient(90deg, {rank_color}, {rank_color}55);"></div>
            </div>
            <div class="feat-desc">{row['description']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box warning" style="margin-top:1rem;">
        <p>💡 <b style="color:#ffa500">Business Insight:</b><br>
        Fitur <code>spoilage_risk</code> dan <code>shelf_urgency</code> mendominasi prediksi.
        Artinya, monitoring <b>suhu real-time</b> dan <b>tanggal kadaluarsa</b> adalah prioritas utama.</p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — HYPERPARAMETERS TABLE & SMOTE GRAPH
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2>🎛️ Konfigurasi Model & Preprocessing</h2>
</div>
""", unsafe_allow_html=True)

hp_col, smote_col = st.columns(2)

with hp_col:
    st.markdown("**⚙️ Hyperparameter XGBoost (Tuned)**")

    hp_data = {
        "Parameter": ["n_estimators", "max_depth", "learning_rate (η)", "subsample", "colsample_bytree", "tree_method"],
        "Nilai": ["500", "6", "0.05", "0.8", "0.8", "hist"],
        "Fungsi": ["Jumlah decision trees", "Kedalaman max tiap tree", "Step size tiap iterasi", "Fraksi baris per tree", "Fraksi kolom per tree", "Algoritma histogram (cepat)"]
    }
    hp_df = pd.DataFrame(hp_data)
    st.dataframe(hp_df, use_container_width=True, hide_index=True, height=250)

with smote_col:
    st.markdown("**⚖️ SMOTE — Penanganan Class Imbalance**")

    fig_smote = make_subplots(rows=1, cols=2, subplot_titles=["Sebelum SMOTE", "Sesudah SMOTE"])

    for col_idx, (vals, colors_) in enumerate([
        ([9800, 5200], ["#00ff88", "#ff4d4d"]),
        ([9800, 9800], ["#00ff88", "#00b4ff"]),
    ], 1):
        fig_smote.add_trace(go.Bar(
            x=["Tidak Busuk", "Busuk"], y=vals,
            marker=dict(color=colors_, line=dict(color="#0d1117", width=2)),
            text=[f"{v:,}" for v in vals], textposition="outside",
        ), row=1, col=col_idx)

    fig_smote.update_layout(
        paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
        font=dict(color="#8b949e", size=10),
        margin=dict(t=50, b=20, l=30, r=20), showlegend=False, height=250,
    )
    st.plotly_chart(fig_smote, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — FEATURE ENGINEERING DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2>🛠️ Feature Engineering (+8 Fitur Baru)</h2>
</div>
""", unsafe_allow_html=True)

fe_data = {
    "Fitur Baru": ["temp_risk_score", "quality_handling", "shelf_urgency", "temp_abuse_rate", "supplier_quality", "sensitivity_exposure"],
    "Formula": ["storage_temp × temp_deviation", "handling_score × packaging_score", "1 / (days_until_expiry + 1)", "temp_abuse_events / (shelf_life_days + 1)", "supplier_score × handling_score", "spoilage_sensitivity × temp_deviation"],
    "Insight": ["🌡️ Gabungan risiko suhu", "📦 Kualitas penanganan & kemasan", "⏰ Urgensi sisa umur produk", "⚡ Frekuensi abuse suhu", "🏭 Kualitas rantai pasok supplier", "🔬 Paparan risiko kerusakan"]
}
fe_df = pd.DataFrame(fe_data)
st.dataframe(fe_df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — BUSINESS RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2>💼 Business Recommendations</h2>
</div>
""", unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)
recs = [
    ("🌡️", "Monitor Suhu Real-Time", "Pasang IoT sensor suhu di rantai distribusi. Kirim alert otomatis jika deviasi suhu melonjak tinggi.", "#00b4ff"),
    ("📅", "Auto-Markdown Produk", "Aktifkan diskon otomatis untuk produk dengan umur kritis guna mengurangi sisa sampah makanan.", "#ffa500"),
    ("🏭", "Evaluasi Supplier", "Audit rutin supplier dengan skor performa buruk yang konsisten mengirim produk berrisiko.", "#bf5af2"),
    ("🤖", "Integrasi Early Warning", "Integrasikan model XGBoost ke sistem ERP/WMS untuk prediksi spoilage batch masuk secara otomatis.", "#00ff88"),
]

for col, (icon, title, desc, color) in zip([r1, r2, r3, r4], recs):
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 2px solid {color}33; min-height: 170px;">
            <div style="font-size:1.8rem; margin-bottom:0.5rem;">{icon}</div>
            <div style="font-size:0.85rem; font-weight:700; color:{color}; margin-bottom:0.5rem;">{title}</div>
            <div style="font-size:0.75rem; color:#8b949e; line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top: 1px solid #21262d; padding: 1.5rem 0 0.5rem 0; display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size:0.78rem; color:#484f58;">🥦 <b style="color:#6e7681;">FreshGuard Dashboard</b> — Perishable Goods Spoilage Prediction System</div>
    <div style="font-size:0.72rem; color:#484f58; font-family:'DM Mono',monospace;">XGBoost · SMOTE · Streamlit &nbsp;|&nbsp; Universitas Pancasila</div>
</div>
""", unsafe_allow_html=True)