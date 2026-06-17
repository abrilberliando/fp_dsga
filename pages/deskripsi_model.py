""" Halaman: Deskripsi Model ========================= 
Menampilkan dokumentasi lengkap model ML yang digunakan: 
arsitektur, performa, fitur, dan metadata model. 
TODO (Tahap berikutnya): 
- Load metadata model dari models/ (json/yaml) 
- Tampilkan confusion matrix & classification report 
- Feature importance chart - ROC/AUC curve 
- Penjelasan SHAP / explainability 
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import json
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import ConfusionMatrixDisplay

# ─────────────────────────────────────────────────────────────
# PATH
# ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

METRICS_PATH = MODELS_DIR / "metrics.json"
CM_PATH = MODELS_DIR / "confusion_matrix.pkl"
MODEL_PATH = MODELS_DIR / "xgboost_model.pkl"
FEATURE_PATH = MODELS_DIR / "feature_names.pkl"
REPORT_PATH = MODELS_DIR / "classification_report.json"
COMPARISON_PATH = MODELS_DIR / "model_comparison.json"
ROC_PATH = MODELS_DIR / "roc_data.pkl"

# ─────────────────────────────────────────────────────────────
# WARNA (sama seperti Dashboard Awal)
# ─────────────────────────────────────────────────────────────
C = {
    "green": "#4caf50",
    "green2": "#66bb6a",
    "teal": "#26a69a",
    "blue": "#2196f3",
    "orange": "#ff9800",
    "red": "#f44336",
    "purple": "#9c27b0",
    "yellow": "#ffc107",
    "bg": "#0e1117",
    "card": "#1a1f2e",
    "border": "#2d3748",
    "text": "#e2e8f0",
    "muted": "#718096",
}

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<style>

.kpi-wrap {{
    background: {C['card']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    padding: 1.2rem;
    position: relative;
}}

.kpi-wrap::after {{
    content: '';
    position:absolute;
    top:0;
    left:0;
    right:0;
    height:3px;
    border-radius:14px 14px 0 0;
}}

.kpi-green::after {{
background:linear-gradient(90deg,{C['green']},{C['teal']});
}}

.kpi-blue::after {{
background:linear-gradient(90deg,{C['blue']},{C['purple']});
}}

.kpi-orange::after {{
background:linear-gradient(90deg,{C['orange']},{C['yellow']});
}}

.kpi-red::after {{
background:linear-gradient(90deg,{C['red']},{C['orange']});
}}

.kpi-icon {{
font-size:1.7rem;
}}

.kpi-lbl {{
font-size:.7rem;
color:{C['muted']};
text-transform:uppercase;
letter-spacing:.1em;
font-weight:600;
}}

.kpi-val {{
font-size:1.8rem;
font-weight:800;
color:{C['text']};
}}

.sec-hdr {{
display:flex;
align-items:center;
gap:.6rem;
padding:.5rem 0;
border-bottom:1px solid {C['border']};
margin:1.5rem 0 1rem;
}}

.sec-dot {{
width:9px;
height:9px;
border-radius:50%;
background:linear-gradient(135deg,{C['green']},{C['teal']});
}}

.sec-hdr h3 {{
margin:0;
color:{C['text']};
}}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PLOTLY BASE
# ─────────────────────────────────────────────────────────────
PBASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color=C["muted"],
        size=11
    ),
    margin=dict(
        t=42,
        b=36,
        l=36,
        r=16
    ),
)

# ─────────────────────────────────────────────────────────────
# LOAD
# ─────────────────────────────────────────────────────────────
metrics = {}
cm = None
model = None
features = []
report = {}
comparison = {}
roc_data = {}

if METRICS_PATH.exists():
    with open(METRICS_PATH) as f:
        metrics = json.load(f)

if CM_PATH.exists():
    cm = joblib.load(CM_PATH)

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)

if FEATURE_PATH.exists():
    features = joblib.load(FEATURE_PATH)

if REPORT_PATH.exists():
    with open(REPORT_PATH) as f:
        report = json.load(f)

if COMPARISON_PATH.exists():
    with open(COMPARISON_PATH) as f:
        comparison = json.load(f)

if ROC_PATH.exists():
    roc_data = joblib.load(ROC_PATH)

# ─── HEADER ─────────────────────────────────────────
st.markdown("""
<div style="border-left:4px solid #4caf50;
padding-left:16px;
margin-bottom:8px;">
<h1 style="margin:0;font-size:28px;font-weight:800;">
📖 Deskripsi Model
</h1>

<p style="margin:4px 0 0 0;
opacity:.55;
font-size:13px;">
Arsitektur, performa, feature importance, dan metadata model XGBoost
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:1rem;">

<span style="
padding:6px 14px;
border-radius:20px;
background:rgba(76,175,80,.15);
color:#4caf50;
font-size:.75rem;
font-weight:700;">
🌳 XGBoost
</span>

<span style="
padding:6px 14px;
border-radius:20px;
background:rgba(255,152,0,.15);
color:#ff9800;
font-size:.75rem;
font-weight:700;">
⚖️ SMOTE
</span>

<span style="
padding:6px 14px;
border-radius:20px;
background:rgba(33,150,243,.15);
color:#2196f3;
font-size:.75rem;
font-weight:700;">
🥬 Food Waste Prediction
</span>

</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Tabs ─────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🧩 Overview",
    "📊 Performa",
    "🔑 Fitur",
    "📋 Metadata"
])
# ─── TAB 1 : OVERVIEW ─────────────────────────
with tab1:

    # ==============================
    # HEADER
    # ==============================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>🧩 Overview Model</h3>
    </div>
    """, unsafe_allow_html=True)

    # ==============================
    # KPI CARD
    # ==============================
    c1, c2, c3, c4 = st.columns(4)

    def info_card(col, color_cls, icon, label, value, sub):
        with col:
            st.markdown(f"""
            <div class="kpi-wrap {color_cls}">
                <span class="kpi-icon">{icon}</span>
                <div class="kpi-lbl">{label}</div>
                <div class="kpi-val">{value}</div>
                <div class="kpi-sub neu">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    info_card(
        c1,
        "kpi-green",
        "🌳",
        "MODEL",
        "XGBoost",
        "Classifier utama"
    )

    info_card(
        c2,
        "kpi-blue",
        "🎯",
        "TARGET",
        "was_spoiled",
        "Binary classification"
    )

    info_card(
        c3,
        "kpi-orange",
        "⚖️",
        "BALANCING",
        "SMOTE",
        "Imbalanced handling"
    )

    info_card(
        c4,
        "kpi-purple",
        "📦",
        "FEATURES",
        str(len(features)),
        "Total feature"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # MODEL INFO + DATASET
    # ==================================================
    col1, col2 = st.columns([1,1])

    with col1:

        st.markdown("""
        <div class="sec-hdr">
            <div class="sec-dot"></div>
            <h3>🧠 Model Information</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ibox green">
        <b>🌳 XGBoost Classifier</b><br><br>

        🎯 Target : <b>was_spoiled</b><br>
        📊 Task : Binary Classification<br>
        ⚖️ Data Balancing : SMOTE<br>
        🥬 Domain : Food Waste Prediction<br>
        📦 Total Feature : {len(features)}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="ibox blue">
        <b>🎯 Project Objective</b><br><br>

        Sistem ini digunakan untuk memprediksi kemungkinan produk mengalami pembusukan sebelum terjual.

        Prediksi dilakukan berdasarkan kondisi penyimpanan, umur simpan produk, kualitas barang, tingkat persediaan, serta faktor permintaan pasar.

        Tujuan utama sistem adalah membantu mengurangi food waste dan meningkatkan efisiensi manajemen inventori produk perishable.
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="sec-hdr">
            <div class="sec-dot"></div>
            <h3>📊 Dataset Overview</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="ibox orange">
        <b>Managing Perishable Inventory Dataset</b><br><br>

        Dataset berisi data simulasi pengelolaan inventori produk mudah rusak (perishable goods).

        Data digunakan untuk memprediksi apakah suatu produk berpotensi mengalami pembusukan sebelum terjual berdasarkan kondisi penyimpanan dan karakteristik produk.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        d1, d2 = st.columns(2)

        with d1:
            st.metric("🎯 Target", "was_spoiled")

        with d2:
            st.metric("🤖 Model", "XGBoost")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # IMPORTANT FEATURES
    # ==================================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>🔑 Important Features</h3>
    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.info("🌡️ Storage Temperature")
        st.info("⭐ Product Quality")

    with col2:
        st.info("📅 Days Until Expiry")
        st.info("🚚 Supply Chain Status")

    with col3:
        st.info("📦 Inventory Level")
        st.info("🏪 Store Location")

    with col4:
        st.info("📈 Demand Forecast")
        st.info("⚠️ Spoilage Risk")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # TRAINING PIPELINE
    # ==================================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>⚙️ Training Pipeline</h3>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("📂", "Dataset"),
        ("🧹", "Cleaning"),
        ("⚙️", "Encoding"),
        ("⚖️", "SMOTE"),
        ("🌳", "XGBoost"),
        ("📊", "Evaluation"),
        ("🔮", "Prediction")
    ]

    cols = st.columns(len(steps))

    for col, (icon, label) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="kpi-wrap kpi-green"
            style="text-align:center;padding:1rem;height:90px;">
                <div style="font-size:25px">{icon}</div>
                <div style="font-size:.8rem;font-weight:600;margin-top:10px;">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)
# ─── TAB 2: PERFORMA ─────────────────────────
with tab2:

    # ==================================================
    # HEADER
    # ==================================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>📈 Model Performance</h3>
    </div>
    """, unsafe_allow_html=True)

    # ==================================================
    # KPI CARDS
    # ==================================================
    c1, c2, c3, c4 = st.columns(4)

    info_card(
        c1,
        "kpi-green",
        "🎯",
        "ACCURACY",
        f"{metrics.get('accuracy',0)*100:.2f}%",
        "Overall Performance"
    )

    info_card(
        c2,
        "kpi-blue",
        "📌",
        "PRECISION",
        f"{metrics.get('precision',0)*100:.2f}%",
        "Positive Prediction"
    )

    info_card(
        c3,
        "kpi-orange",
        "🔍",
        "RECALL",
        f"{metrics.get('recall',0)*100:.2f}%",
        "Detection Rate"
    )

    info_card(
        c4,
        "kpi-purple",
        "⚡",
        "F1 SCORE",
        f"{metrics.get('f1',0)*100:.2f}%",
        "Balanced Metric"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # PERFORMANCE METRICS
    # ==================================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>📊 Performance Metrics</h3>
    </div>
    """, unsafe_allow_html=True)

    import pandas as pd

    df_all = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1"],
        "Value": [
            metrics.get("accuracy", 0),
            metrics.get("precision", 0),
            metrics.get("recall", 0),
            metrics.get("f1", 0),
        ]
    })

    fig_metric = go.Figure()

    fig_metric.add_bar(
        x=df_all["Metric"],
        y=df_all["Value"],
        marker_color=[
            C["green"],
            C["blue"],
            C["orange"],
            C["purple"]
        ],
        text=[f"{x:.3f}" for x in df_all["Value"]],
        textposition="outside"
    )

    fig_metric.update_layout(
        **PBASE,
        title="Performance Metrics",
        yaxis_title="Score",
        height=350
    )

    st.plotly_chart(
        fig_metric,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # ==================================================
    # MODEL COMPARISON
    # ==================================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>🎯 XGBoost vs CatBoost</h3>
    </div>
    """, unsafe_allow_html=True)

    metric_mapping = {
        "Accuracy": "accuracy",
        "Precision": "precision",
        "Recall": "recall",
        "F1 Score": "f1_score",
    }

    selected_metric = st.selectbox(
        "Pilih Metric",
        list(metric_mapping.keys())
    )

    metric_key = metric_mapping[selected_metric]

    xgb_value = comparison.get("XGBoost", {}).get(metric_key, 0)
    cat_value = comparison.get("CatBoost", {}).get(metric_key, 0)

    fig = go.Figure()

    fig.add_bar(
        name="XGBoost",
        x=["XGBoost"],
        y=[xgb_value],
        marker_color=C["green"],
        text=[f"{xgb_value:.4f}"],
        textposition="outside"
    )

    fig.add_bar(
        name="CatBoost",
        x=["CatBoost"],
        y=[cat_value],
        marker_color=C["orange"],
        text=[f"{cat_value:.4f}"],
        textposition="outside"
    )

    fig.update_layout(
        **PBASE,
        title=f"{selected_metric} Comparison",
        yaxis_title=selected_metric,
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # ==================================================
    # CONFUSION MATRIX + ROC CURVE
    # ==================================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>🎯 Evaluation Curves</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ---------- CONFUSION MATRIX ----------
    with col1:

        st.subheader("Confusion Matrix")

        if cm is not None:

            fig_cm, ax = plt.subplots(figsize=(6,5))

            disp = ConfusionMatrixDisplay(
                confusion_matrix=cm,
                display_labels=["Not Spoiled", "Spoiled"]
            )

            disp.plot(
                ax=ax,
                cmap="Blues",
                values_format="d"
            )

            st.pyplot(fig_cm)

        else:
            st.warning("Confusion matrix belum tersedia")

    # ---------- ROC CURVE ----------
    with col2:

        st.subheader("ROC Curve")

        ROC_PATH = "models/roc_data.pkl"

        if os.path.exists(ROC_PATH):

            roc_data = joblib.load(ROC_PATH)

            fpr = roc_data.get("fpr", [])
            tpr = roc_data.get("tpr", [])

            fig_roc, ax = plt.subplots(figsize=(6,5))

            ax.plot(
                fpr,
                tpr,
                linewidth=3,
                label=f"AUC = {metrics.get('auc',0):.4f}"
            )

            ax.plot(
                [0,1],
                [0,1],
                linestyle="--",
                color="red"
            )

            ax.legend()

            st.pyplot(fig_roc)

        else:
            st.info("ROC belum tersedia")

    # ==================================================
    # CLASSIFICATION REPORT
    # ==================================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>📋 Classification Report</h3>
    </div>
    """, unsafe_allow_html=True)

    try:

        if isinstance(report, dict) and len(report) > 0:

            df_report = pd.DataFrame(report).transpose()
            df_report = df_report.round(3)

            st.dataframe(
                df_report,
                use_container_width=True
            )

        else:
            st.warning("Classification report kosong")

    except Exception as e:

        st.error(f"Gagal load report : {e}")
# ─── TAB 3: FITUR ─────────────────────────
with tab3:

    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>🔑 Feature Analysis</h3>
    </div>
    """, unsafe_allow_html=True)

    if model is not None and len(features) > 0:

        importance = model.feature_importances_

        df_imp = pd.DataFrame({
            "Feature": features,
            "Importance": importance
        }).sort_values(
            by="Importance",
            ascending=False
        )

        # ====================================
        # KPI
        # ====================================
        c1, c2, c3 = st.columns(3)

        info_card(
            c1,
            "kpi-green",
            "📦",
            "TOTAL FEATURES",
            str(len(features)),
            "Feature model"
        )

        info_card(
            c2,
            "kpi-blue",
            "🥇",
            "TOP FEATURE",
            df_imp.iloc[0]["Feature"],
            "Most important"
        )

        info_card(
            c3,
            "kpi-orange",
            "📈",
            "IMPORTANCE",
            f"{df_imp.iloc[0]['Importance']:.4f}",
            "Highest score"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ====================================
        # TOP 10 FEATURE IMPORTANCE
        # ====================================
        st.markdown("""
        <div class="sec-hdr">
            <div class="sec-dot"></div>
            <h3>📊 Top 10 Feature Importance</h3>
        </div>
        """, unsafe_allow_html=True)

        top10 = df_imp.head(10).sort_values(
            by="Importance"
        )

        fig = go.Figure()

        fig.add_bar(
            x=top10["Importance"],
            y=top10["Feature"],
            orientation="h",
            marker_color=C["green"],
            text=[f"{v:.4f}" for v in top10["Importance"]],
            textposition="outside"
        )

        fig.update_layout(
            **PBASE,
            title="Top 10 Important Features",
            xaxis_title="Importance Score",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        # ====================================
        # TABLE
        # ====================================
        st.markdown("""
        <div class="sec-hdr">
            <div class="sec-dot"></div>
            <h3>📋 Full Feature Ranking</h3>
        </div>
        """, unsafe_allow_html=True)

        df_imp["Rank"] = range(
            1,
            len(df_imp)+1
        )

        st.dataframe(
            df_imp[
                ["Rank","Feature","Importance"]
            ],
            use_container_width=True
        )

        # ====================================
        # INSIGHT
        # ====================================
        st.markdown("""
        <div class="sec-hdr">
            <div class="sec-dot"></div>
            <h3>💡 Insight</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ibox green">
        <b>{df_imp.iloc[0]["Feature"]}</b>
        merupakan feature paling berpengaruh terhadap prediksi spoilage dengan skor
        <b>{df_imp.iloc[0]["Importance"]:.4f}</b>.

        Model mengambil keputusan berdasarkan kombinasi feature-feature dengan
        importance tertinggi.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Model atau feature belum tersedia")
# ─── TAB 4 : METADATA ─────────────────────────
with tab4:

    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>📋 Model Metadata</h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    info_card(
        c1,
        "kpi-green",
        "🌳",
        "MODEL",
        "XGBoost",
        "Main algorithm"
    )

    info_card(
        c2,
        "kpi-blue",
        "🎯",
        "TASK",
        "Binary",
        "Classification"
    )

    info_card(
        c3,
        "kpi-orange",
        "📦",
        "FEATURES",
        str(len(features)),
        "Total features"
    )

    info_card(
        c4,
        "kpi-purple",
        "📈",
        "AUC",
        f"{metrics.get('auc',0):.3f}",
        "ROC performance"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ===================================
    # MODEL INFORMATION
    # ===================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>🧠 Model Information</h3>
    </div>
    """, unsafe_allow_html=True)

    model_info = pd.DataFrame({
        "Property":[
            "Algorithm",
            "Problem Type",
            "Target Variable",
            "Total Features",
            "Training Method",
            "Evaluation Metrics"
        ],
        "Value":[
            "XGBoost",
            "Binary Classification",
            "was_spoiled",
            len(features),
            "SMOTE + XGBoost",
            "Accuracy, Precision, Recall, F1, AUC"
        ]
    })

    st.dataframe(
        model_info,
        use_container_width=True,
        hide_index=True
    )

    # ===================================
    # RAW JSON
    # ===================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>⚙️ Raw Metrics JSON</h3>
    </div>
    """, unsafe_allow_html=True)

    st.json(metrics)

    # ===================================
    # SUMMARY
    # ===================================
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>📄 Model Summary</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ibox green">

    <b>🌳 XGBoost Performance</b>

    <br><br>

    🎯 Accuracy : {metrics.get('accuracy',0)*100:.2f}%<br>
    📌 Precision : {metrics.get('precision',0)*100:.2f}%<br>
    🔍 Recall : {metrics.get('recall',0)*100:.2f}%<br>
    ⚡ F1 Score : {metrics.get('f1',0)*100:.2f}%<br>
    📈 AUC : {metrics.get('auc',0):.3f}

    </div>
    """, unsafe_allow_html=True)