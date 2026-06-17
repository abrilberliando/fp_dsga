""" Halaman: Deskripsi Model ========================= 
Menampilkan dokumentasi lengkap model ML yang digunakan: 
arsitektur, performa, fitur, dan metadata model. 
TODO (Tahap berikutnya): 
- Load metadata model dari models/ (json/yaml) 
- Tampilkan confusion matrix & classification report 
- Feature importance chart - ROC/AUC curve 
- Penjelasan SHAP / explainability 
"""

import streamlit as st
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.metrics import ConfusionMatrixDisplay
import os

# ─── Load Data ─────────────────────────────────────────
METRICS_PATH = "models/metrics.json"
CM_PATH = "models/confusion_matrix.pkl"
MODEL_PATH = "models/xgboost_model.pkl"
FEATURE_PATH = "models/feature_names.pkl"
REPORT_PATH = "models/classification_report.json"
report = {}
COMPARISON_PATH = "models/model_comparison.json"
comparison = {}

metrics = {}
cm = None
model = None
features = []

if os.path.exists(METRICS_PATH):
    with open(METRICS_PATH) as f:
        metrics = json.load(f)

if os.path.exists(CM_PATH):
    cm = joblib.load(CM_PATH)

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

if os.path.exists(FEATURE_PATH):
    features = joblib.load(FEATURE_PATH)

if os.path.exists(REPORT_PATH):
    with open(REPORT_PATH) as f:
        report = json.load(f)
if os.path.exists(COMPARISON_PATH):
    with open(COMPARISON_PATH) as f:
        comparison = json.load(f)

# ─── HEADER ─────────────────────────────────────────
st.markdown("""
<div style="
text-align:center;
padding:25px;
border-radius:18px;
background: linear-gradient(135deg,#2e7d32,#66bb6a);
color:white;
box-shadow:0px 4px 15px rgba(0,0,0,0.15);
">

<h1 style="
margin-bottom:5px;
font-size:42px;
">
🥬 Deskripsi Model
</h1>

<p style="
font-size:18px;
opacity:0.95;
margin-bottom:15px;
">
Food Waste Prediction System using XGBoost
</p>

<span style="
background:white;
color:#2e7d32;
padding:8px 16px;
border-radius:20px;
font-weight:bold;
margin-right:8px;
">
🌳 XGBoost
</span>

<span style="
background:white;
color:#2e7d32;
padding:8px 16px;
border-radius:20px;
font-weight:bold;
">
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
# ─── Tabs 1 Overview ─────────────────────────────────────────
# ─── TAB 1 : OVERVIEW ─────────────────────────
with tab1:

    st.markdown("""
    <div style="padding:10px 0;">
        <h1 style="margin-bottom:0;">🥬 Food Waste Prediction System</h1>
        <p style="color:gray;">
            Machine Learning Based Perishable Goods Management
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ==========================================
    # TOP SECTION
    # ==========================================
    col1, col2 = st.columns([1, 1.3], gap="large")

    # ─── LEFT : MODEL INFO ────────────────────
    with col1:

        st.markdown("## 🧠 Model Information")

        st.markdown("""
        <div style="
        background: linear-gradient(135deg,#2e7d32,#66bb6a);
        padding:20px;
        border-radius:12px;
        color:white;
        ">

        <h3>🌳 XGBoost Classifier</h3>

        <hr style="opacity:0.3;">

        <ul>
        <li>🎯 Prediction Target : was_spoiled</li>
        <li>📊 Task Type : Binary Classification</li>
        <li>🌳 Main Model : XGBoost Classifier</li>
        <li>⚖️ Data Balancing : SMOTE</li>
        <li>🥬 Domain : Food Waste Prediction</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎯 Project Objective")

        st.info("""
        Sistem ini digunakan untuk memprediksi kemungkinan
        produk mengalami pembusukan sebelum terjual.

        Prediksi dilakukan berdasarkan kondisi penyimpanan,
        umur simpan produk, kualitas barang, tingkat
        persediaan, serta faktor permintaan pasar.

        Tujuan utama sistem adalah membantu mengurangi
        food waste dan meningkatkan efisiensi manajemen
        inventori produk perishable.
        """)

    # ─── RIGHT : DATASET OVERVIEW ─────────────
    with col2:

        st.markdown("## 📊 Dataset Overview")

        st.success("""
        **Managing Perishable Inventory Dataset**

        Dataset berisi data simulasi pengelolaan inventori
        produk mudah rusak (perishable goods).

        Data digunakan untuk memprediksi apakah suatu
        produk berpotensi mengalami pembusukan sebelum
        terjual berdasarkan kondisi penyimpanan dan
        karakteristik produk.
        """)

        d1, d2 = st.columns(2)

        d1.metric("🎯 Target", "was_spoiled")
        d2.metric("🤖 Model", "XGBoost")

        st.markdown("### 📌 Data Characteristics")

        st.markdown("""
        - 🌡️ Storage Temperature
        - 📅 Days Until Expiry
        - 📦 Inventory Level
        - 📈 Demand Forecast
        - ⭐ Product Quality Score
        - 🚚 Supply Chain Status
        - 🏪 Store Location
        - ⚠️ Spoilage Risk
        """)

        st.markdown("### ⚙️ Training Pipeline")

        st.code("""
Dataset
   ↓
Data Cleaning
   ↓
Encoding
   ↓
SMOTE
   ↓
Train-Test Split
   ↓
XGBoost Training
   ↓
Model Evaluation
   ↓
Prediction
        """)

    st.divider()

    # ==========================================
    # IMPORTANT FEATURES
    # ==========================================
    st.markdown("## 📦 Important Features")

    c1, c2, c3, c4 = st.columns(4)

    c1.info("🌡️ Storage Temperature")
    c2.info("📅 Days Until Expiry")
    c3.info("📦 Inventory Level")
    c4.info("📈 Demand Forecast")

    c5, c6, c7, c8 = st.columns(4)

    c5.info("⭐ Product Quality")
    c6.info("🚚 Supply Chain Status")
    c7.info("🏪 Store Location")
    c8.info("⚠️ Spoilage Risk")

    st.divider()

    # ==========================================
    # WORKFLOW
    # ==========================================
    st.markdown("## 🔄 Prediction Workflow")

    st.markdown("""
    <div style="
    display:flex;
    gap:10px;
    flex-wrap:wrap;
    justify-content:center;
    align-items:center;
    ">

    <div style="background:#e8f5e9;padding:12px;border-radius:10px;">
    📂 Dataset
    </div>

    <div>➡️</div>

    <div style="background:#e3f2fd;padding:12px;border-radius:10px;">
    🧹 Preprocessing
    </div>

    <div>➡️</div>

    <div style="background:#ede7f6;padding:12px;border-radius:10px;">
    ⚙️ Encoding
    </div>

    <div>➡️</div>

    <div style="background:#fff3e0;padding:12px;border-radius:10px;">
    ⚖️ SMOTE
    </div>

    <div>➡️</div>

    <div style="background:#f3e5f5;padding:12px;border-radius:10px;">
    🌳 XGBoost
    </div>

    <div>➡️</div>

    <div style="background:#e0f7fa;padding:12px;border-radius:10px;">
    📊 Evaluation
    </div>

    <div>➡️</div>

    <div style="background:#fce4ec;padding:12px;border-radius:10px;">
    🔮 Prediction
    </div>

    </div>
    """, unsafe_allow_html=True)
# ─── TAB 2: PERFORMA ─────────────────────────
with tab2:
    st.subheader("📈 Model Performance")

    # ── METRICS CARDS ─────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Accuracy", f"{metrics.get('accuracy',0)*100:.2f}%")
    c2.metric("Precision", f"{metrics.get('precision',0)*100:.2f}%")
    c3.metric("Recall", f"{metrics.get('recall',0)*100:.2f}%")
    c4.metric("F1 Score", f"{metrics.get('f1',0)*100:.2f}%")

    st.divider()

    # ── GRAFIK SEMUA METRICS ─────────────────────────
    st.subheader("📊 Perbandingan Semua Metrics")

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

    st.bar_chart(df_all.set_index("Metric"))

    st.divider()

# ── GRAFIK INTERAKTIF (DROPDOWN) ─────────────────────────
    st.subheader("🎯 Perbandingan Model (XGBoost vs CatBoost)")

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
        marker_color="#7B1FA2",
        text=[f"{xgb_value:.4f}"],
        textposition="outside"
    )

    fig.add_bar(
        name="CatBoost",
        x=["CatBoost"],
        y=[cat_value],
        marker_color="#FF9800",
        text=[f"{cat_value:.4f}"],
        textposition="outside"
    )

    fig.update_layout(
        title=f"{selected_metric} Comparison",
        yaxis_title=selected_metric,
        height=500,
        hovermode="x",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "toImageButtonOptions": {
                "format": "png"
            }
        }
    )

    # ── CONFUSION MATRIX + ROC ─────────────────────────
    col1, col2 = st.columns(2)

    # CONFUSION MATRIX
    # ===================================================
    with col1:

        st.subheader("🎯 Confusion Matrix")

        if cm is not None:

            fig, ax = plt.subplots(figsize=(7, 6))

            disp = ConfusionMatrixDisplay(
                confusion_matrix=cm,
                display_labels=["Not Spoiled", "Spoiled"]
            )

            disp.plot(
                ax=ax,
                cmap="Blues",
                values_format="d"
            )

            ax.set_title(
                "Confusion Matrix",
                fontsize=14,
                pad=15
            )

            plt.tight_layout()

            st.pyplot(fig)

        else:
            st.warning("Confusion matrix belum tersedia")


    # ===================================================
    # ROC CURVE
    # ===================================================
    with col2:

        st.subheader("📉 ROC Curve")

        ROC_PATH = "models/roc_data.pkl"

        if os.path.exists(ROC_PATH):

            roc_data = joblib.load(ROC_PATH)

            fpr = roc_data.get("fpr", [])
            tpr = roc_data.get("tpr", [])

            fig, ax = plt.subplots(figsize=(7, 6))

            ax.plot(
                fpr,
                tpr,
                linewidth=3,
                label=f"AUC = {metrics.get('auc',0):.4f}"
            )

            ax.plot(
                [0, 1],
                [0, 1],
                linestyle="--",
                color="red",
                label="Random Guess"
            )

            ax.set_xlabel("False Positive Rate")
            ax.set_ylabel("True Positive Rate")

            ax.set_title(
                "ROC Curve",
                fontsize=14,
                pad=15
            )

            ax.legend()

            plt.tight_layout()

            st.pyplot(fig)

        else:
            st.info("ROC belum tersedia")

    st.divider()

    # ── CLASSIFICATION REPORT ─────────────────────────
    st.subheader("📋 Classification Report")

    try:
        if isinstance(report, dict) and len(report) > 0:
            df_report = pd.DataFrame(report).transpose()

            # rapihin angka
            df_report = df_report.round(3)

            st.dataframe(df_report, use_container_width=True)
        else:
            st.warning("Classification report kosong / belum ada")

    except Exception as e:
        st.error(f"Gagal load report: {e}")

# ─── TAB 3: FITUR ─────────────────────────
with tab3:

    st.subheader("🔑 Feature Analysis")

    if model is not None and len(features) > 0:

        importance = model.feature_importances_

        df_imp = pd.DataFrame({
            "Feature": features,
            "Importance": importance
        }).sort_values(
            by="Importance",
            ascending=False
        )

        # ===============================
        # TOP CARDS
        # ===============================
        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Features",
            len(features)
        )

        c2.metric(
            "Most Important",
            df_imp.iloc[0]["Feature"]
        )

        c3.metric(
            "Importance Score",
            f"{df_imp.iloc[0]['Importance']:.4f}"
        )

        st.divider()

        # ===============================
        # TOP 10 IMPORTANCE
        # ===============================
        st.subheader("📊 Top 10 Feature Importance")

        fig, ax = plt.subplots(figsize=(8,5))

        top10 = df_imp.head(10)

        ax.barh(
            top10["Feature"][::-1],
            top10["Importance"][::-1]
        )

        ax.set_xlabel("Importance Score")
        ax.set_ylabel("Feature")
        ax.set_title("Top 10 Important Features")

        st.pyplot(fig)

        st.divider()

        # ===============================
        # FEATURE TABLE
        # ===============================
        st.subheader("📋 Full Feature Ranking")

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

        st.divider()

        # ===============================
        # FEATURE INSIGHT
        # ===============================
        st.subheader("💡 Insight")

        st.info(
            f"""
            Feature paling berpengaruh terhadap prediksi spoilage adalah
            **{df_imp.iloc[0]['Feature']}**
            dengan skor importance
            **{df_imp.iloc[0]['Importance']:.4f}**.

            Model lebih banyak mengambil keputusan berdasarkan kombinasi
            feature-feature dengan importance tinggi.
            """
        )

    else:
        st.warning("Model atau feature belum tersedia")
        # ─── TAB 4: METADATA ─────────────────────────
with tab4:

    st.subheader("📋 Model Metadata")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Model",
        "XGBoost"
    )

    c2.metric(
        "Task",
        "Binary Class"
    )

    c3.metric(
        "Features",
        len(features)
    )

    c4.metric(
        "AUC",
        f"{metrics.get('auc',0):.3f}"
    )

    st.divider()

    # ===============================
    # MODEL INFORMATION
    # ===============================
    st.subheader("🧠 Model Information")

    st.markdown(f"""
| Property | Value |
|-----------|--------|
| Algorithm | XGBoost |
| Problem Type | Binary Classification |
| Target Variable | was_spoiled |
| Total Features | {len(features)} |
| Training Method | SMOTE + XGBoost |
| Evaluation Metrics | Accuracy, Precision, Recall, F1, AUC |
    """)

    st.divider()

    # ===============================
    # JSON VIEWER
    # ===============================
    st.subheader("⚙️ Raw Metrics JSON")

    st.json(metrics)

    st.divider()

    # ===============================
    # MODEL SUMMARY
    # ===============================
    st.subheader("📄 Model Summary")

    st.success(
        f"""
        Model XGBoost berhasil mencapai:

        • Accuracy : {metrics.get('accuracy',0)*100:.2f}%  
        • Precision : {metrics.get('precision',0)*100:.2f}%  
        • Recall : {metrics.get('recall',0)*100:.2f}%  
        • F1 Score : {metrics.get('f1',0)*100:.2f}%  
        • AUC : {metrics.get('auc',0):.3f}
        """
    )