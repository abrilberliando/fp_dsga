"""
Halaman: Dashboard Awal
========================
Overview statistik utama, EDA, dan ringkasan model XGBoost
untuk sistem prediksi spoilage perishable goods.

Data: data/perishable_goods_management.csv (100K records)
Model: models/xgboost_model.pkl (XGBoost — binary:logistic)
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# PATH
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "perishable_goods_management.csv")

# ─────────────────────────────────────────────────────────────────────────────
# TEMA WARNA  (selaras dengan app.py — green sidebar)
# ─────────────────────────────────────────────────────────────────────────────
C = {
    "green"  : "#4caf50",
    "green2" : "#66bb6a",
    "teal"   : "#26a69a",
    "blue"   : "#2196f3",
    "orange" : "#ff9800",
    "red"    : "#f44336",
    "purple" : "#9c27b0",
    "yellow" : "#ffc107",
    "bg"     : "#0e1117",
    "card"   : "#1a1f2e",
    "border" : "#2d3748",
    "text"   : "#e2e8f0",
    "muted"  : "#718096",
}

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

/* ── Cards ── */
.kpi-wrap {{
    background: {C['card']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    padding: 1.2rem 1.4rem 1rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform .18s ease, border-color .18s ease;
}}
.kpi-wrap:hover {{
    transform: translateY(-3px);
    border-color: #4a5568;
}}
.kpi-wrap::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}}
.kpi-green::after  {{ background: linear-gradient(90deg,{C['green']},{C['teal']}); }}
.kpi-blue::after   {{ background: linear-gradient(90deg,{C['blue']},#7c3aed); }}
.kpi-orange::after {{ background: linear-gradient(90deg,{C['orange']},{C['yellow']}); }}
.kpi-red::after    {{ background: linear-gradient(90deg,{C['red']},{C['orange']}); }}
.kpi-purple::after {{ background: linear-gradient(90deg,{C['purple']},#ec4899); }}
.kpi-teal::after   {{ background: linear-gradient(90deg,{C['teal']},{C['blue']}); }}

.kpi-icon  {{ font-size:1.7rem; margin-bottom:.35rem; display:block; }}
.kpi-lbl   {{ font-size:.7rem; color:{C['muted']}; text-transform:uppercase;
              letter-spacing:.1em; font-weight:600; margin-bottom:.25rem; }}
.kpi-val   {{ font-size:1.9rem; font-weight:800; color:{C['text']};
              font-family:'JetBrains Mono',monospace; line-height:1; }}
.kpi-sub   {{ font-size:.73rem; margin-top:.3rem; font-weight:500; }}
.kpi-sub.up   {{ color:{C['green']}; }}
.kpi-sub.dn   {{ color:{C['red']}; }}
.kpi-sub.neu  {{ color:{C['muted']}; }}

/* ── Section headers ── */
.sec-hdr {{
    display:flex; align-items:center; gap:.6rem;
    padding:.5rem 0 .6rem 0;
    border-bottom: 1px solid {C['border']};
    margin: 1.8rem 0 1rem 0;
}}
.sec-hdr h3 {{ margin:0; font-size:1rem; font-weight:700; color:{C['text']}; }}
.sec-dot {{
    width:9px; height:9px; border-radius:50%; flex-shrink:0;
    background: linear-gradient(135deg,{C['green']},{C['teal']});
}}

/* ── Info boxes ── */
.ibox {{
    border-radius:10px; padding:.9rem 1.1rem;
    font-size:.8rem; line-height:1.65; color:{C['muted']};
}}
.ibox.green {{ background:rgba(76,175,80,.07); border:1px solid rgba(76,175,80,.25); }}
.ibox.orange{{ background:rgba(255,152,0,.07); border:1px solid rgba(255,152,0,.25); }}
.ibox.blue  {{ background:rgba(33,150,243,.07); border:1px solid rgba(33,150,243,.25); }}

/* ── Feat bar ── */
.fbar-wrap {{ margin-bottom:.45rem; }}
.fbar-row {{ display:flex; justify-content:space-between; margin-bottom:.2rem; }}
.fbar-name {{ font-size:.78rem; font-weight:600; color:{C['text']};
              font-family:'JetBrains Mono',monospace; }}
.fbar-pct  {{ font-size:.75rem; color:{C['green']}; font-family:'JetBrains Mono',monospace; }}
.fbar-bg   {{ background:#2d3748; border-radius:4px; height:5px; }}
.fbar-fill {{ border-radius:4px; height:5px;
              background:linear-gradient(90deg,{C['green']},{C['teal']}); }}

/* ── Pill tags ── */
.pill {{
    display:inline-block; padding:.22rem .7rem;
    border-radius:20px; font-size:.72rem; font-weight:600;
    margin:.15rem .1rem; font-family:'JetBrains Mono',monospace;
}}
.pill-green {{ background:rgba(76,175,80,.15); color:{C['green']};
               border:1px solid rgba(76,175,80,.35); }}
.pill-blue  {{ background:rgba(33,150,243,.15); color:{C['blue']};
               border:1px solid rgba(33,150,243,.35); }}
.pill-orange{{ background:rgba(255,152,0,.15);  color:{C['orange']};
               border:1px solid rgba(255,152,0,.35); }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background:{C['bg']}; }}
::-webkit-scrollbar-thumb {{ background:#4a5568; border-radius:3px; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["transaction_date", "expiration_date"])

    # Feature engineering (sama dengan train_model.py)
    df["temp_risk_score"]      = df["storage_temp"] * df["temp_deviation"]
    df["quality_handling"]     = df["handling_score"] * df["packaging_score"]
    df["price_ratio"]          = df["base_price"] / (df["cost_price"] + 1e-6)
    df["demand_pressure"]      = df["daily_demand"] / (df["initial_quantity"] + 1e-6)
    df["shelf_urgency"]        = 1 / (df["days_until_expiry"] + 1)
    df["temp_abuse_rate"]      = df["temp_abuse_events"] / (df["shelf_life_days"] + 1)
    df["supplier_quality"]     = df["supplier_score"] * df["handling_score"]
    df["sensitivity_exposure"] = df["spoilage_sensitivity"] * df["temp_deviation"]

    df["month_label"] = df["transaction_date"].dt.to_period("M").astype(str)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# FEATURE IMPORTANCE  (dari model .pkl asli)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_fi():
    try:
        import json
        feature_path = os.path.join(BASE_DIR, "models", "feature_importances.json")
        with open(feature_path, 'r') as f:
            data = json.load(f)
        fi = pd.DataFrame({"feature": list(data.keys()), "importance": list(data.values())})
        return fi.sort_values("importance", ascending=False).reset_index(drop=True)
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY LAYOUT BASE
# ─────────────────────────────────────────────────────────────────────────────
PBASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=C["muted"], size=11, family="Inter"),
    margin=dict(t=42, b=36, l=36, r=16),
    xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", showline=False),
    yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", showline=False),
)


# ─────────────────────────────────────────────────────────────────────────────
# LOAD
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("Memuat data…"):
    df = load_data()

fi_df = load_fi()


# ─────────────────────────────────────────────────────────────────────────────
# MAPPING — label tampilan (Indonesia) → nilai asli di dataset
# ─────────────────────────────────────────────────────────────────────────────
CAT_MAP = {
    "Bakery"         : "🍞 Roti & Kue",
    "Beverages"      : "🥤 Minuman",
    "Dairy"          : "🥛 Susu & Produk Susu",
    "Deli"           : "🥪 Deli & Olahan",
    "Frozen_Meals"   : "🧊 Makanan Beku",
    "Meat"           : "🥩 Daging",
    "Pharmaceuticals": "💊 Farmasi",
    "Produce"        : "🥦 Sayuran & Buah",
    "Ready_to_Eat"   : "🍱 Siap Saji",
    "Seafood"        : "🐟 Ikan & Seafood",
}

REG_MAP = {
    "Midwest"  : " Jawa Tengah",
    "Northeast": " Jawa Timur",
    "Southeast": " Sulawesi Selatan",
    "Southwest": " Bali & Nusa Tenggara",
    "West"     : " Jawa Barat & DKI Jakarta",
}

# Reverse map: label Indonesia → nilai asli
CAT_REV = {v: k for k, v in CAT_MAP.items()}
REG_REV = {v: k for k, v in REG_MAP.items()}

# Label Indonesia untuk setiap nilai unik di data
cat_labels_all = sorted([CAT_MAP.get(c, c) for c in df["category"].unique()])
reg_labels_all = sorted([REG_MAP.get(r, r) for r in df["region"].unique()])

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("##### 🔍 Filter Dashboard")

    sel_cat_label = st.multiselect(
        "Kategori Produk",
        options=cat_labels_all,
        default=cat_labels_all,
        key="db_cat",
    )
    sel_reg_label = st.multiselect(
        "Wilayah / Region",
        options=reg_labels_all,
        default=reg_labels_all,
        key="db_reg",
    )
    sel_grade = st.multiselect(
        "Quality Grade",
        options=["A", "B", "C"],
        default=["A", "B", "C"],
        key="db_grade",
    )

# Konversi label Indonesia kembali ke nilai asli untuk filter data
sel_cat = [CAT_REV.get(l, l) for l in sel_cat_label]
sel_reg = [REG_REV.get(l, l) for l in sel_reg_label]

mask = (
    df["category"].isin(sel_cat) &
    df["region"].isin(sel_reg) &
    df["quality_grade"].isin(sel_grade)
)
dff = df[mask].copy()

# Tambahkan kolom label Indonesia untuk keperluan chart
dff["kategori_id"] = dff["category"].map(CAT_MAP)
dff["wilayah_id"]  = dff["region"].map(REG_MAP)

if dff.empty:
    st.warning("⚠️ Tidak ada data untuk filter yang dipilih.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# ── HEADER ───────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-left:4px solid #4caf50; padding-left:16px; margin-bottom:4px;">
    <h1 style="margin:0; font-size:28px; font-weight:800;">🏠 Dashboard Awal</h1>
    <p style="margin:4px 0 0 0; opacity:.55; font-size:13px;">
        Overview & Statistik Sistem Prediksi Spoilage Perishable Goods — XGBoost
    </p>
</div>
""", unsafe_allow_html=True)

# Badge pills
total_rec = len(dff)
spoil_pct = dff["was_spoiled"].mean() * 100
st.markdown(f"""
<div style="margin:.6rem 0 1.2rem 0;">
    <span class="pill pill-green">XGBoost · binary:logistic</span>
    <span class="pill pill-green">{total_rec:,} Records</span>
    <span class="pill pill-orange">Spoilage Rate {spoil_pct:.1f}%</span>
    <span class="pill pill-blue">100K Dataset · Kaggle</span>
    <span class="pill pill-blue">n_estimators=500 · max_depth=6</span>
</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# ── SECTION 1: KPI CARDS ─────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>📊 Statistik Utama</h3>
</div>
""", unsafe_allow_html=True)

total_products  = len(dff)
spoiled_n       = int(dff["was_spoiled"].sum())
spoilage_rate   = dff["was_spoiled"].mean() * 100
total_waste_cost= dff["waste_cost"].sum()
total_revenue   = dff["revenue"].sum()
units_wasted    = int(dff["units_wasted"].sum())
avg_profit_m    = dff["profit_margin_pct"].mean()
critical_items  = int((dff["days_until_expiry"] <= 2).sum())

k1, k2, k3, k4, k5, k6 = st.columns(6)

def kpi(col, color_cls, icon, label, value, sub, sub_cls):
    with col:
        st.markdown(f"""
        <div class="kpi-wrap {color_cls}">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-lbl">{label}</div>
            <div class="kpi-val">{value}</div>
            <div class="kpi-sub {sub_cls}">{sub}</div>
        </div>""", unsafe_allow_html=True)

kpi(k1, "kpi-green",  "📦", "Total Produk",
    f"{total_products:,}", f"{len(sel_cat)} kategori aktif", "neu")

kpi(k2, "kpi-red",    "🦠", "Spoilage Rate",
    f"{spoilage_rate:.1f}%",
    f"⚠️ {spoiled_n:,} produk busuk" if spoilage_rate > 20 else f"✅ {spoiled_n:,} busuk",
    "dn" if spoilage_rate > 20 else "up")

kpi(k3, "kpi-orange", "💸", "Total Waste Cost",
    f"${total_waste_cost/1e6:.1f}M",
    f"dari revenue ${total_revenue/1e6:.0f}M", "dn")

kpi(k4, "kpi-blue",   "🗑️", "Unit Terbuang",
    f"{units_wasted/1e6:.2f}M",
    "unit produk terbuang sia-sia", "dn")

kpi(k5, "kpi-purple", "🚨", "Kritis ≤2 Hari",
    f"{critical_items:,}",
    "⚠️ Butuh tindakan segera" if critical_items > 500 else "✅ Terkendali",
    "dn" if critical_items > 500 else "up")

kpi(k6, "kpi-teal",   "📈", "Avg Profit Margin",
    f"{avg_profit_m:.1f}%",
    "margin keuntungan rata-rata", "up" if avg_profit_m > 15 else "dn")

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ── SECTION 2: TREN + DISTRIBUSI ─────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>📈 Tren & Distribusi Spoilage</h3>
</div>
""", unsafe_allow_html=True)

col_trend, col_pie = st.columns([3, 1])

with col_trend:
    monthly = (
        dff.groupby("month_label")
        .agg(spoiled=("was_spoiled", "sum"),
             total=("was_spoiled", "count"),
             waste_cost=("waste_cost", "sum"))
        .reset_index()
    )
    monthly["rate"] = monthly["spoiled"] / monthly["total"] * 100

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

    fig_trend.add_trace(go.Bar(
        x=monthly["month_label"],
        y=monthly["spoiled"],
        name="Jumlah Spoiled",
        marker=dict(color=C["red"], opacity=.55),
    ), secondary_y=False)

    fig_trend.add_trace(go.Scatter(
        x=monthly["month_label"],
        y=monthly["rate"],
        name="Spoilage Rate (%)",
        mode="lines+markers",
        line=dict(color=C["green"], width=2.5),
        marker=dict(size=5),
    ), secondary_y=True)

    fig_trend.update_layout(
        **PBASE,
        title=dict(text="Tren Spoilage Bulanan", font=dict(size=12, color=C["text"])),
        legend=dict(orientation="h", y=1.12, x=0, font=dict(size=10)),
        height=300,
    )
    fig_trend.update_yaxes(title_text="Jumlah Busuk", secondary_y=False,
                            title_font=dict(size=10), tickfont=dict(size=9))
    fig_trend.update_yaxes(title_text="Rate (%)", secondary_y=True,
                            title_font=dict(size=10), tickfont=dict(size=9))
    fig_trend.update_xaxes(tickangle=45, tickfont=dict(size=8))
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

with col_pie:
    vc = dff["was_spoiled"].value_counts().sort_index()
    fig_pie = go.Figure(go.Pie(
        labels=["Tidak Busuk", "Busuk"],
        values=vc.values,
        marker=dict(colors=[C["green"], C["red"]],
                    line=dict(color="#0e1117", width=3)),
        textinfo="label+percent",
        textfont=dict(size=10, color=C["text"]),
        hole=0.5,
        pull=[0, 0.05],
    ))
    fig_pie.update_layout(
    **{k: v for k, v in PBASE.items() if k != "xaxis" and k != "yaxis" and k != "margin"},
    title=dict(text="Distribusi Kelas", font=dict(size=12, color=C["text"])),
    showlegend=False,
    height=300,
    margin=dict(t=42, b=10, l=10, r=10),
)
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# ── SECTION 3: SPOILAGE PER KATEGORI & REGION ────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>🗺️ Analisis per Kategori & Region</h3>
</div>
""", unsafe_allow_html=True)

col_cat, col_reg = st.columns(2)

with col_cat:
    cat_stats = (
        dff.groupby("category")
        .agg(spoiled=("was_spoiled", "sum"),
             total=("was_spoiled", "count"),
             waste_cost=("waste_cost", "sum"))
        .reset_index()
    )
    cat_stats["rate"] = cat_stats["spoiled"] / cat_stats["total"] * 100
    cat_stats = cat_stats.sort_values("rate", ascending=True)

    fig_cat = go.Figure(go.Bar(
        x=cat_stats["rate"],
        y=cat_stats["category"],
        orientation="h",
        marker=dict(
            color=cat_stats["rate"],
            colorscale=[[0, C["green"]], [0.5, C["orange"]], [1, C["red"]]],
            line=dict(color="rgba(0,0,0,0)", width=0),
        ),
        text=[f"{v:.1f}%" for v in cat_stats["rate"]],
        textposition="outside",
        textfont=dict(color=C["text"], size=10),
    ))
    fig_cat.update_layout(
        **PBASE,
        title=dict(text="Spoilage Rate per Kategori (%)", font=dict(size=12, color=C["text"])),
        xaxis_title="Spoilage Rate (%)",
        height=320,
    )
    st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})

with col_reg:
    hm_data = (
        dff.groupby(["category", "region"])["was_spoiled"]
        .mean()
        .mul(100)
        .unstack(fill_value=0)
    )
    fig_hm = go.Figure(go.Heatmap(
        z=hm_data.values,
        x=hm_data.columns.tolist(),
        y=hm_data.index.tolist(),
        colorscale=[[0, "#0d2818"], [0.5, "#1a5c3a"], [1, "#f44336"]],
        text=[[f"{v:.1f}%" for v in row] for row in hm_data.values],
        texttemplate="%{text}",
        textfont=dict(size=8),
        showscale=True,
        colorbar=dict(title=dict(text="Rate%", font=dict(size=9)), tickfont=dict(size=8),
              len=0.8, thickness=12),
        xgap=2, ygap=2,
    ))
    fig_hm.update_layout(
        **{k: v for k, v in PBASE.items() if "axis" not in k},
        title=dict(text="Heatmap: Kategori × Region (%)", font=dict(size=12, color=C["text"])),
        xaxis=dict(tickfont=dict(size=9), tickangle=20),
        yaxis=dict(tickfont=dict(size=9)),
        height=320,
    )
    st.plotly_chart(fig_hm, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# ── SECTION 4: EDA FITUR ─────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>🔬 Analisis Fitur Utama</h3>
</div>
""", unsafe_allow_html=True)

tab_box, tab_scatter, tab_corr = st.tabs([
    "📦 Distribusi per Kelas",
    "🎯 Scatter Risiko",
    "🔥 Korelasi",
])

sample3k = dff.sample(min(3000, len(dff)), random_state=42)

with tab_box:
    bc1, bc2 = st.columns(2)
    with bc1:
        fig_b1 = px.box(
            sample3k, x="was_spoiled", y="temp_abuse_events",
            color="was_spoiled",
            color_discrete_map={0: C["green"], 1: C["red"]},
            labels={"was_spoiled": "Label", "temp_abuse_events": "Temp Abuse Events"},
            title="Temp Abuse Events vs Kelas",
        )
        fig_b1.update_layout(**PBASE, height=300,
                             title_font=dict(size=12, color=C["text"]))
        st.plotly_chart(fig_b1, use_container_width=True, config={"displayModeBar": False})

    with bc2:
        fig_b2 = px.box(
            sample3k, x="was_spoiled", y="shelf_urgency",
            color="was_spoiled",
            color_discrete_map={0: C["blue"], 1: C["orange"]},
            labels={"was_spoiled": "Label", "shelf_urgency": "Shelf Urgency"},
            title="Shelf Urgency vs Kelas",
        )
        fig_b2.update_layout(**PBASE, height=300,
                             title_font=dict(size=12, color=C["text"]))
        st.plotly_chart(fig_b2, use_container_width=True, config={"displayModeBar": False})

with tab_scatter:
    fig_sc = px.scatter(
        sample3k,
        x="temp_abuse_events",
        y="profit_margin_pct",
        color="was_spoiled",
        color_discrete_map={0: C["green"], 1: C["red"]},
        opacity=0.45,
        size_max=5,
        labels={
            "temp_abuse_events": "Temp Abuse Events (fitur #1)",
            "profit_margin_pct": "Profit Margin %",
            "was_spoiled": "Label",
        },
        title="Temp Abuse Events vs Profit Margin — diwarnai per kelas spoilage",
    )
    fig_sc.update_traces(marker_size=4)
    fig_sc.update_layout(**PBASE, height=330,
                         title_font=dict(size=12, color=C["text"]),
                         legend=dict(font=dict(size=10)))
    st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

with tab_corr:
    num_cols = [
        "temp_abuse_events", "units_sold", "profit_margin_pct", "temp_abuse_rate",
        "packaging_score", "spoilage_sensitivity", "handling_score", "supplier_score",
        "shelf_urgency", "days_until_expiry", "temp_deviation", "spoilage_risk",
        "quality_handling", "shelf_life_days", "was_spoiled",
    ]
    corr = dff[num_cols].corr()
    fig_corr = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale="RdYlGn",
        zmid=0,
        text=[[f"{v:.2f}" for v in row] for row in corr.values],
        texttemplate="%{text}",
        textfont=dict(size=7.5),
        colorbar=dict(title=dict(text="r", font=dict(size=9)), tickfont=dict(size=8), len=0.9, thickness=12),
        xgap=1, ygap=1,
    ))
    fig_corr.update_layout(
    **{k: v for k, v in PBASE.items() if "axis" not in k and k != "margin"},
    title=dict(text="Correlation Heatmap — Fitur Numerik", font=dict(size=12, color=C["text"])),
    xaxis=dict(tickangle=40, tickfont=dict(size=8)),
    yaxis=dict(tickfont=dict(size=8)),
    height=460,
    margin=dict(t=42, b=60, l=90, r=20),
)
    st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# ── SECTION 5: FEATURE IMPORTANCE ────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>🔑 Feature Importance XGBoost</h3>
</div>
""", unsafe_allow_html=True)

fi_left, fi_right = st.columns([3, 2])

if fi_df is not None:
    top12 = fi_df.head(12).sort_values("importance")

    with fi_left:
        fig_fi = go.Figure(go.Bar(
            x=top12["importance"],
            y=top12["feature"],
            orientation="h",
            marker=dict(
                color=top12["importance"],
                colorscale=[[0, C["blue"]], [0.5, C["green"]], [1, C["orange"]]],
                line=dict(color="rgba(0,0,0,0)", width=0),
            ),
            text=[f"{v:.4f}" for v in top12["importance"]],
            textposition="outside",
            textfont=dict(color=C["text"], size=9),
        ))
        fig_fi.update_layout(
        **{k: v for k, v in PBASE.items() if k != "yaxis"},
        title=dict(text="Top 12 Feature Importance — Model XGBoost (dari .pkl asli)",
        font=dict(size=12, color=C["text"])),
        xaxis_title="Importance Score",
        height=380,
        yaxis=dict(tickfont=dict(size=9), gridcolor="#2d3748"),
        )
        st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})

    with fi_right:
        st.markdown("**📖 Penjelasan Fitur Terpenting**")
        feat_explain = {
            "temp_abuse_events"  : ("🌡️", "Jumlah kejadian abuse suhu — paling dominan"),
            "units_sold"         : ("🛒", "Unit terjual — demand tinggi = fresher stock"),
            "profit_margin_pct"  : ("💰", "Margin profit % — produk rugi rentan dibuang"),
            "temp_abuse_rate"    : ("⚡", "Frekuensi abuse suhu / shelf life"),
            "markdown_applied"   : ("🏷️", "Diskon diterapkan — sinyal produk mendekati expire"),
            "is_promoted"        : ("📣", "Status promosi — mempengaruhi kecepatan turnover"),
            "packaging_score"    : ("📦", "Kualitas kemasan — pelindung dari lingkungan"),
            "spoilage_sensitivity": ("🔬","Sensitivitas produk thd perubahan suhu"),
            "price_ratio"        : ("💲", "Rasio harga jual vs biaya — profitabilitas"),
            "handling_score"     : ("🤲", "Kualitas penanganan dalam rantai distribusi"),
            "supplier_score"     : ("🏭", "Rating kinerja supplier — konsistensi kualitas"),
            "region"             : ("🗺️", "Wilayah — kondisi iklim & infrastruktur logistik"),
        }
        max_imp = fi_df["importance"].max()
        for _, row in fi_df.head(8).iterrows():
            icon, desc = feat_explain.get(row["feature"], ("📌", "Fitur model XGBoost"))
            pct = row["importance"] / max_imp
            rank_color = C["orange"] if pct > 0.7 else C["green"] if pct > 0.35 else C["blue"]
            st.markdown(f"""
            <div class="fbar-wrap">
                <div class="fbar-row">
                    <span class="fbar-name">{icon} {row['feature']}</span>
                    <span class="fbar-pct">{row['importance']:.4f}</span>
                </div>
                <div class="fbar-bg">
                    <div class="fbar-fill" style="width:{pct*100:.0f}%;
                        background:linear-gradient(90deg,{rank_color},{rank_color}88);">
                    </div>
                </div>
                <div style="font-size:.68rem; color:{C['muted']}; margin-top:.18rem;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ibox orange" style="margin-top:.8rem;">
            💡 <b style="color:{C['orange']}">Key Insight:</b><br>
            <b>temp_abuse_events</b> adalah fitur paling dominan (19.6%).
            Monitoring suhu real-time dan pengurangan kejadian abuse suhu
            adalah prioritas utama untuk menekan spoilage.
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("ℹ️ File model tidak ditemukan. Jalankan `train_model.py` terlebih dahulu.")


# ─────────────────────────────────────────────────────────────────────────────
# ── SECTION 6: MODEL OVERVIEW ────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>⚙️ Konfigurasi & Pipeline Model XGBoost</h3>
</div>
""", unsafe_allow_html=True)

pipe_col, hp_col = st.columns([2, 1])

with pipe_col:
    steps = [
        ("🗂️", C["blue"],   "Load CSV",      "100K rows<br>42 kolom"),
        ("🔍", C["teal"],   "EDA",            "Distribusi<br>Korelasi"),
        ("🛠️", C["purple"], "Preprocessing", "LabelEnc<br>FeatureEng×8"),
        ("⚖️", C["orange"], "SMOTE",          "Balance<br>minority class"),
        ("🎛️", C["green"],  "Hypertuning",   "GridSearch<br>CV"),
        ("🚀", C["green"],  "XGBoost Fit",   "n_est=500<br>max_depth=6"),
        ("📊", C["blue"],   "Evaluasi",       "AUC·F1<br>Confusion"),
    ]

    cols_pipe = st.columns(len(steps))
    for col, (icon, color, label, desc) in zip(cols_pipe, steps):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding:.3rem 0;">
                <div style="width:46px;height:46px;border-radius:12px;
                            background:{color}18;border:1px solid {color}44;
                            display:flex;align-items:center;justify-content:center;
                            font-size:1.2rem;margin:0 auto .4rem auto;">{icon}</div>
                <div style="font-size:.65rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:.06em;color:{color};margin-bottom:.18rem;">
                    {label}</div>
                <div style="font-size:.62rem;color:{C['muted']};line-height:1.45;">
                    {desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ibox green" style="margin-top:1rem;">
        <b style="color:{C['green']}">+8 Feature Engineering:</b>
        <code>temp_risk_score</code> · <code>quality_handling</code> ·
        <code>price_ratio</code> · <code>demand_pressure</code> ·
        <code>shelf_urgency</code> · <code>temp_abuse_rate</code> ·
        <code>supplier_quality</code> · <code>sensitivity_exposure</code>
    </div>
    """, unsafe_allow_html=True)

with hp_col:
    st.markdown("**⚙️ Hyperparameter Terpilih**")
    hp = {
        "objective"           : "binary:logistic",
        "n_estimators"        : "500",
        "max_depth"           : "6",
        "learning_rate (η)"   : "0.05",
        "subsample"           : "0.8",
        "colsample_bytree"    : "0.8",
        "reg_alpha (L1)"      : "0.1",
        "reg_lambda (L2)"     : "1.0",
        "min_child_weight"    : "3",
        "gamma (γ)"           : "0.1",
        "tree_method"         : "hist",
        "early_stopping"      : "30 rounds",
    }
    hp_df = pd.DataFrame(hp.items(), columns=["Parameter", "Nilai"])
    st.dataframe(
        hp_df, hide_index=True, use_container_width=True, height=382,
        column_config={
            "Parameter": st.column_config.TextColumn(width="medium"),
            "Nilai"    : st.column_config.TextColumn(width="small"),
        },
    )


# ─────────────────────────────────────────────────────────────────────────────
# ── SECTION 7: WASTE COST ANALYSIS ───────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>💸 Analisis Kerugian (Waste Cost)</h3>
</div>
""", unsafe_allow_html=True)

wc1, wc2 = st.columns(2)

with wc1:
    wc_cat = dff.groupby("category")["waste_cost"].sum().sort_values(ascending=False).reset_index()
    fig_wc = px.bar(
        wc_cat, x="category", y="waste_cost",
        color="waste_cost",
        color_continuous_scale=[[0, C["teal"]], [0.5, C["orange"]], [1, C["red"]]],
        labels={"waste_cost": "Total Waste Cost ($)", "category": "Kategori"},
        title="Total Waste Cost per Kategori",
    )
    fig_wc.update_layout(**PBASE, height=300,
                          title_font=dict(size=12, color=C["text"]),
                          coloraxis_showscale=False)
    fig_wc.update_xaxes(tickangle=25, tickfont=dict(size=9))
    st.plotly_chart(fig_wc, use_container_width=True, config={"displayModeBar": False})

with wc2:
    # Scatter: waste_pct vs profit_margin
    fig_wc2 = px.scatter(
        dff.sample(min(4000, len(dff)), random_state=1),
        x="waste_pct", y="profit_margin_pct",
        color="category",
        opacity=0.45,
        size_max=5,
        labels={"waste_pct": "Waste % per Transaksi",
                "profit_margin_pct": "Profit Margin %"},
        title="Waste % vs Profit Margin per Kategori",
    )
    fig_wc2.update_traces(marker_size=4)
    fig_wc2.update_layout(**PBASE, height=300,
                           title_font=dict(size=12, color=C["text"]),
                           legend=dict(font=dict(size=9), y=1.0))
    st.plotly_chart(fig_wc2, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# ── SECTION 8: QUICK NAVIGATION ──────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>🚀 Akses Cepat ke Halaman Lain</h3>
</div>
""", unsafe_allow_html=True)

nav_cols = st.columns(3)
nav_items = [
    ("pages/prediksi.py",       "🔮 Mulai Prediksi",    "Input data produk & dapatkan prediksi spoilage real-time"),
    ("pages/deskripsi_model.py","📖 Deskripsi Model",   "Lihat arsitektur, performa, dan evaluasi model XGBoost"),
    ("pages/ai_gemini_model.py","🤖 AI Model (Gemini)", "Tanya jawab interaktif tentang model dengan AI"),
]
for col, (page, label, desc) in zip(nav_cols, nav_items):
    with col:
        st.markdown(f"""
        <div class="kpi-wrap kpi-green" style="text-align:center; padding:1.2rem 1rem; min-height:90px;">
            <div style="font-size:.88rem; font-weight:700; color:{C['green']};
                        margin-bottom:.4rem;">{label}</div>
            <div style="font-size:.73rem; color:{C['muted']}; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(page, label=label)

st.divider()
st.markdown(f"""
<div style="text-align:center; font-size:.72rem; color:{C['muted']}; line-height:1.8;">
    🌱 <b>Food Waste Recommendation System</b> &nbsp;·&nbsp;
    Dataset: Kaggle — Managing Perishable Inventory (100K records) &nbsp;·&nbsp;
    Model: XGBoost v2.x · SMOTE · Universitas Pancasila · fp_dsga
</div>
""", unsafe_allow_html=True)
