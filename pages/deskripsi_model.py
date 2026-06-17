"""
Halaman: Deskripsi Model

Dokumentasi lengkap model ML: arsitektur, performa, feature importance, metadata.
Hanya tersedia untuk Stakeholder Teknis.
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import json
import joblib
from pathlib import Path

import plotly.graph_objects as go

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.theme import inject_css, COLORS, PLOTLY_BASE, page_header, section_header

inject_css()
C = COLORS
PBASE = PLOTLY_BASE

# path configuration
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

METRICS_PATH = MODELS_DIR / "metrics.json"
CM_PATH = MODELS_DIR / "confusion_matrix.pkl"
MODEL_PATH = MODELS_DIR / "xgboost_model.pkl"
FEATURE_PATH = MODELS_DIR / "feature_names.pkl"
REPORT_PATH = MODELS_DIR / "classification_report.json"
COMPARISON_PATH = MODELS_DIR / "model_comparison.json"
ROC_PATH = MODELS_DIR / "roc_data.pkl"

# load data with error handling
metrics = {}
cm = None
model = None
features = []
report = {}
comparison = {}
roc_data = {}

# track successfully loaded files
loaded_files = {
    "metrics": False,
    "confusion_matrix": False,
    "model": False,
    "features": False,
    "report": False,
    "comparison": False,
    "roc_data": False
}

try:
    if METRICS_PATH.exists():
        with open(METRICS_PATH) as f:
            metrics = json.load(f)
        loaded_files["metrics"] = True
except Exception as e:
    st.error(f"⚠️ Error loading metrics: {e}")

try:
    if CM_PATH.exists():
        cm = joblib.load(CM_PATH)
        loaded_files["confusion_matrix"] = True
except Exception as e:
    st.error(f"⚠️ Error loading confusion matrix: {e}")

try:
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        loaded_files["model"] = True
except Exception as e:
    st.error(f"⚠️ Error loading model: {e}")

try:
    if FEATURE_PATH.exists():
        features = joblib.load(FEATURE_PATH)
        loaded_files["features"] = True
except Exception as e:
    st.error(f"⚠️ Error loading features: {e}")

try:
    if REPORT_PATH.exists():
        with open(REPORT_PATH) as f:
            report = json.load(f)
        loaded_files["report"] = True
except Exception as e:
    st.error(f"⚠️ Error loading classification report: {e}")

try:
    if COMPARISON_PATH.exists():
        with open(COMPARISON_PATH) as f:
            comparison = json.load(f)
        loaded_files["comparison"] = True
except Exception as e:
    st.error(f"⚠️ Error loading model comparison: {e}")

try:
    if ROC_PATH.exists():
        roc_data = joblib.load(ROC_PATH)
        loaded_files["roc_data"] = True
except Exception as e:
    st.error(f"⚠️ Error loading ROC data: {e}")

# count successfully loaded files
total_files = len(loaded_files)
loaded_count = sum(loaded_files.values())

# page header
page_header(
    title="Performa Model",
    subtitle="Arsitektur, evaluasi, feature importance, dan metadata model XGBoost",
    icon="📖",
)

# Status indicator
if loaded_count == total_files:
    st.success(f"✅ Semua file model berhasil dimuat ({loaded_count}/{total_files})", icon="✨")
elif loaded_count > 0:
    st.warning(f"⚠️ Sebagian file model dimuat ({loaded_count}/{total_files}). Beberapa fitur mungkin tidak tersedia.", icon="⚠️")
else:
    st.error("❌ Tidak ada file model yang berhasil dimuat. Jalankan `train_model.py` terlebih dahulu.", icon="🚫")

st.markdown("""
<div style="margin:.5rem 0 1.2rem 0;">
    <span class="pill pill-green">🌳 XGBoost</span>
    <span class="pill pill-orange">⚖️ SMOTE</span>
    <span class="pill pill-blue">🥬 Food Waste Prediction</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs([
    "🧩 Overview",
    "📊 Performa",
    "🔑 Fitur",
    "📋 Metadata"
])

# tab 1: overview
with tab1:

    # header
    section_header("🧩 Overview Model")

    # kpi cards
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

    # model information and dataset overview
    col1, col2 = st.columns([1,1])

    with col1:

        section_header("🧠 Model Information")

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

        section_header("📊 Dataset Overview")

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

    # important features list
    section_header("🔑 Important Features")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.info("Storage Temperature")
        st.info("Product Quality")

    with col2:
        st.info("Days Until Expiry")
        st.info("Supply Chain Status")

    with col3:
        st.info("Inventory Level")
        st.info("Store Location")

    with col4:
        st.info("Demand Forecast")
        st.info("Spoilage Risk")

    st.markdown("<br>", unsafe_allow_html=True)

    # jupyter notebook information
    section_header("📓 Jupyter Notebook")

    notebook_path = BASE_DIR / "notebooks" / "XGBoost_CatBoost_Perishable_Goods.ipynb"
    
    if notebook_path.exists():
        st.markdown(f"""
<div class="ibox blue">
    <b>Training Notebook Available</b><br><br>
    
    File: <code>XGBoost_CatBoost_Perishable_Goods.ipynb</code><br>
    Location: <code>notebooks/</code><br><br>
    
    Notebook ini berisi:<br>
    • Exploratory Data Analysis (EDA)<br>
    • Data preprocessing dan feature engineering<br>
    • Training XGBoost dan CatBoost models<br>
    • Model comparison dan evaluation<br>
    • Hyperparameter tuning<br>
    • SMOTE untuk handling imbalanced data<br><br>
    
    <b>Cara membuka:</b><br>
    <code>jupyter notebook notebooks/XGBoost_CatBoost_Perishable_Goods.ipynb</code>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="ibox orange">
    Notebook tidak ditemukan di folder <code>notebooks/</code>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # training pipeline visualization
    section_header("⚙️ Training Pipeline")

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

# tab 2: performance metrics
with tab2:

    # header
    section_header("📈 Model Performance")

    # kpi cards
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

    # performance metrics chart
    section_header("📊 Performance Metrics")

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

    # model comparison section
    section_header("🎯 XGBoost vs CatBoost")

    if comparison and len(comparison) > 0:
        metric_mapping = {
            "Accuracy": "accuracy",
            "Precision": "precision",
            "Recall": "recall",
            "F1 Score": "f1",  # ✅ Fixed: use "f1" not "f1_score"
            "AUC": "auc"
        }

        selected_metric = st.selectbox(
            "Pilih Metric untuk Perbandingan",
            list(metric_mapping.keys()),
            key="metric_selector"
        )

        metric_key = metric_mapping[selected_metric]

        xgb_value = comparison.get("XGBoost", {}).get(metric_key, 0)
        cat_value = comparison.get("CatBoost", {}).get(metric_key, 0)

        # Create comparison chart
        fig = go.Figure()

        fig.add_bar(
            x=["XGBoost", "CatBoost"],
            y=[xgb_value, cat_value],
            marker_color=[C["green"], C["orange"]],
            text=[f"{xgb_value:.4f}", f"{cat_value:.4f}"],
            textposition="outside",
            textfont=dict(size=14, color=C["text"])
        )

        # Create custom layout by copying PBASE and updating
        layout_config = PBASE.copy()
        layout_config.update({
            "title": f"{selected_metric} Comparison",
            "yaxis_title": selected_metric,
            "height": 450,
        })
        
        fig.update_layout(**layout_config)
        
        # Update yaxis range separately to avoid conflict
        fig.update_yaxes(range=[0, min(1.1, max(xgb_value, cat_value) * 1.2)])

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        # Show winner
        winner = "XGBoost" if xgb_value > cat_value else "CatBoost" if cat_value > xgb_value else "Tie"
        diff = abs(xgb_value - cat_value)
        
        if winner != "Tie":
            st.markdown(f"""
<div class="ibox {'green' if winner == 'XGBoost' else 'orange'}">
    <b>{winner}</b> menang dengan selisih <b>{diff:.4f}</b> ({diff/max(xgb_value, cat_value)*100:.2f}%) pada metric <b>{selected_metric}</b>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class="ibox blue">
    <b>Tie</b> - Kedua model memiliki performa yang sama pada metric <b>{selected_metric}</b>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="ibox orange">
    ⚠️ Data perbandingan model belum tersedia.<br>
    Jalankan <code>train_comparison.py</code> untuk membandingkan XGBoost dan CatBoost.
</div>
""", unsafe_allow_html=True)

    # confusion matrix and roc curve
    section_header("📉 Evaluation Curves")

    col1, col2 = st.columns(2)

    # confusion matrix (plotly)
    with col1:
        section_header("Confusion Matrix")
        if cm is not None:
            fig_cm = go.Figure(go.Heatmap(
                z=cm,
                x=["Not Spoiled", "Spoiled"],
                y=["Not Spoiled", "Spoiled"],
                colorscale=[[0, C["card"]], [1, C["green"]]],
                text=[[str(v) for v in row] for row in cm],
                texttemplate="<b>%{text}</b>",
                textfont=dict(size=18, color=C["text"]),
                showscale=False,
                xgap=3, ygap=3,
            ))
            layout_cm = PBASE.copy()
            layout_cm.update({
                "title": dict(text="Confusion Matrix", font=dict(size=12, color=C["text"])),
                "height": 350,
            })
            fig_cm.update_layout(**layout_cm)
            fig_cm.update_xaxes(title="Predicted", tickfont=dict(size=11))
            fig_cm.update_yaxes(title="Actual", tickfont=dict(size=11), autorange="reversed")
            st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown(f'<div class="ibox orange">⚠️ Confusion matrix belum tersedia.<br>Jalankan <code>train_model.py</code> terlebih dahulu.</div>', unsafe_allow_html=True)

    # roc curve (plotly)
    with col2:
        section_header("ROC Curve")
        roc_path_abs = MODELS_DIR / "roc_data.pkl"
        if roc_path_abs.exists():
            roc_loaded = joblib.load(roc_path_abs)
            fpr = roc_loaded.get("fpr", [])
            tpr = roc_loaded.get("tpr", [])
            auc_val = metrics.get("auc", 0)

            fig_roc = go.Figure()
            fig_roc.add_scatter(
                x=fpr, y=tpr, mode="lines",
                name=f"AUC = {auc_val:.4f}",
                line=dict(color=C["green"], width=2.5),
            )
            fig_roc.add_scatter(
                x=[0, 1], y=[0, 1], mode="lines",
                line=dict(color=C["red"], dash="dash", width=1.5),
                showlegend=False,
            )
            layout_roc = PBASE.copy()
            layout_roc.update({
                "title": dict(text="ROC Curve", font=dict(size=12, color=C["text"])),
                "legend": dict(font=dict(size=11), x=0.6, y=0.1),
                "height": 350,
            })
            fig_roc.update_layout(**layout_roc)
            fig_roc.update_xaxes(title="False Positive Rate", range=[0, 1])
            fig_roc.update_yaxes(title="True Positive Rate", range=[0, 1])
            st.plotly_chart(fig_roc, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown(f'<div class="ibox orange">⚠️ ROC data belum tersedia.</div>', unsafe_allow_html=True)

    # classification report
    section_header("📋 Classification Report")

    if report and isinstance(report, dict) and len(report) > 0:
        try:
            # Convert report to DataFrame
            df_report = pd.DataFrame(report).transpose()
            
            # Round numeric columns
            numeric_cols = df_report.select_dtypes(include=[np.number]).columns
            df_report[numeric_cols] = df_report[numeric_cols].round(4)
            
            # Style the dataframe
            st.dataframe(
                df_report,
                use_container_width=True,
                column_config={
                    "precision": st.column_config.NumberColumn(
                        "Precision",
                        format="%.4f"
                    ),
                    "recall": st.column_config.NumberColumn(
                        "Recall",
                        format="%.4f"
                    ),
                    "f1-score": st.column_config.NumberColumn(
                        "F1-Score",
                        format="%.4f"
                    ),
                    "support": st.column_config.NumberColumn(
                        "Support",
                        format="%.0f"
                    )
                }
            )
            
            # Explanation
            st.markdown(f"""
<div class="ibox green" style="margin-top:1rem;">
    <b>📊 Interpretasi Classification Report</b><br><br>
    
    • <b>Class 0 (Not Spoiled):</b> Produk yang tidak mengalami pembusukan<br>
    • <b>Class 1 (Spoiled):</b> Produk yang mengalami pembusukan<br><br>
    
    • <b>Precision:</b> Dari semua prediksi positif, berapa yang benar<br>
    • <b>Recall:</b> Dari semua kasus positif actual, berapa yang terdeteksi<br>
    • <b>F1-Score:</b> Harmonic mean dari precision dan recall<br>
    • <b>Support:</b> Jumlah sampel actual untuk setiap class
</div>
""", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error menampilkan classification report: {e}")
            st.json(report)  # Fallback: show raw JSON
    else:
        st.markdown("""
<div class="ibox orange">
    ⚠️ Classification report belum tersedia.<br>
    Jalankan <code>train_model.py</code> untuk generate report.
</div>
""", unsafe_allow_html=True)

# tab 3: feature analysis
with tab3:
    section_header("🔑 Feature Analysis")

    if model is not None and len(features) > 0:

        importance = model.feature_importances_

        df_imp = pd.DataFrame({
            "Feature": features,
            "Importance": importance
        }).sort_values(
            by="Importance",
            ascending=False
        )

        # kpi cards
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

        # top 10 feature importance chart
        section_header("📊 Top 10 Feature Importance")

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

        # full feature ranking table
        section_header("📋 Full Feature Ranking")

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

        # insight section
        section_header("💡 Insight")

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

# tab 4: metadata
with tab4:
    section_header("📋 Model Metadata")

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

    # model information table
    section_header("🧠 Model Information")

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

    # raw metrics json
    section_header("⚙️ Raw Metrics JSON")

    st.json(metrics)

    # model summary
    section_header("📄 Model Summary")

    st.markdown(f"""
    <div class="ibox green">

    <b>🌳 XGBoost Performance</b>

    <br><br>

    🎯 Accuracy : {metrics.get('accuracy',0)*100:.2f}%<br>
    📌 Precision : {metrics.get('precision',0)*100:.2f}%<br>
    🔍 Recall : {metrics.get('recall',0)*100:.2f}%<br>
    ⚡ F1 Score : {metrics.get('f1',0)*100:.2f}%<br>
    📈 AUC : {metrics.get('auc',0):.4f}

    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # model files status table
    section_header("📁 Model Files Status")
    
    file_status = pd.DataFrame({
        "File": [
            "metrics.json",
            "confusion_matrix.pkl",
            "xgboost_model.pkl",
            "feature_names.pkl",
            "classification_report.json",
            "model_comparison.json",
            "roc_data.pkl"
        ],
        "Status": [
            "✅ Loaded" if loaded_files["metrics"] else "❌ Not Found",
            "✅ Loaded" if loaded_files["confusion_matrix"] else "❌ Not Found",
            "✅ Loaded" if loaded_files["model"] else "❌ Not Found",
            "✅ Loaded" if loaded_files["features"] else "❌ Not Found",
            "✅ Loaded" if loaded_files["report"] else "❌ Not Found",
            "✅ Loaded" if loaded_files["comparison"] else "❌ Not Found",
            "✅ Loaded" if loaded_files["roc_data"] else "❌ Not Found"
        ],
        "Description": [
            "Model performance metrics",
            "Confusion matrix untuk evaluation",
            "Trained XGBoost model",
            "Feature names list",
            "Detailed classification report",
            "XGBoost vs CatBoost comparison",
            "ROC curve data (FPR, TPR, AUC)"
        ]
    })
    
    st.dataframe(
        file_status,
        use_container_width=True,
        hide_index=True,
        column_config={
            "File": st.column_config.TextColumn("File Name", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Description": st.column_config.TextColumn("Description", width="large")
        }
    )
    
    if loaded_count < total_files:
        st.markdown(f"""
<div class="ibox orange">
    ⚠️ <b>{total_files - loaded_count} file(s) belum tersedia.</b><br><br>
    Jalankan script berikut untuk generate model files:<br>
    • <code>python train_model.py</code> - Generate model utama<br>
    • <code>python train_comparison.py</code> - Generate model comparison
</div>
""", unsafe_allow_html=True)