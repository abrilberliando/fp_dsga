"""
Halaman: Deskripsi Model
=========================
Menampilkan dokumentasi lengkap model ML yang digunakan:
arsitektur, performa, fitur, dan metadata model.

TODO (Tahap berikutnya):
- Load metadata model dari models/ (json/yaml)
- Tampilkan confusion matrix & classification report
- Feature importance chart
- ROC/AUC curve
- Penjelasan SHAP / explainability
"""

import streamlit as st

# ─── Judul Halaman ────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    border-left: 4px solid #9c27b0;
    padding-left: 16px;
    margin-bottom: 8px;
">
    <h1 style="margin:0; font-size:28px;">📖 Deskripsi Model</h1>
    <p style="margin:4px 0 0 0; opacity:0.6; font-size:14px;">
        Dokumentasi, arsitektur, dan evaluasi model Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Tab Layout ───────────────────────────────────────────────────────────────
tab_overview, tab_performance, tab_features, tab_metadata = st.tabs([
    "🧩 Overview",
    "📊 Performa",
    "🔑 Fitur",
    "📋 Metadata",
])

# ── Tab 1: Overview ───────────────────────────────────────────────────────────
with tab_overview:
    col_info, col_arch = st.columns([1, 1], gap="large")

    with col_info:
        st.markdown("#### 🌸 Tentang Model")

        with st.container(border=True):
            st.markdown("""
                | Atribut | Nilai |
                |----------|-------|
                | **Nama Model** | XGBoost |
                | **Tipe** | Classification |
                | **Versi** | v1.0 |
                | **Library** | xgboost |
                | **Target** | Food Waste Recommendation |
                | **Input Shape** | Dataset Features |
            """)

        st.markdown("#### 📝 Deskripsi")

        with st.container(border=True):
            st.write("""
            **XGBoost (Extreme Gradient Boosting)** merupakan algoritma machine learning
            berbasis decision tree yang menggunakan teknik boosting untuk meningkatkan
            performa prediksi secara iteratif.

            Model ini digunakan untuk melakukan klasifikasi kondisi produk,
            yaitu apakah termasuk **tidak busuk (0)** atau **busuk (1)**.

            Berdasarkan hasil evaluasi, model menunjukkan performa yang sangat baik:

            • Accuracy : 92.32%  
            • Precision : 85.34%  
            • Recall : 73.05%  
            • F1-Score : 78.71%  
            • AUC-ROC : 96.04%  

            Model dipilih karena mampu menangani hubungan non-linear antar fitur
            serta memberikan hasil prediksi yang stabil.
            """)

    with col_arch:
        st.markdown("#### 🏗️ Arsitektur / Pipeline")

        with st.container(border=True):
            st.markdown("""
    📂 Dataset

    ⬇️

    🧹 Data Cleaning & Preprocessing

    ⬇️

    🧠 Feature Engineering

    ⬇️

    ✂️ Train-Test Split

    ⬇️

    🌳 XGBoost Model Training

    ⬇️

    📊 Model Evaluation

    ⬇️

    🔮 Prediction (0 = Tidak Busuk, 1 = Busuk)

    ⬇️

    ♻️ Food Waste Recommendation
    """)

# ── Tab 2: Performa ───────────────────────────────────────────────────────────
with tab_performance:
    st.markdown("#### 📈 Metrik Evaluasi")

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Accuracy", "92.32%")
    mc2.metric("Precision", "85.34%")
    mc3.metric("Recall", "73.05%")
    mc4.metric("F1-Score", "78.71%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_cm, col_roc = st.columns(2)

    with col_cm:
        st.markdown("#### 🎯 Confusion Matrix")

        with st.container(border=True):
            st.info(
                "Visualisasi confusion matrix akan ditambahkan setelah hasil evaluasi model dimuat.",
                icon="📊"
            )

    with col_roc:
        st.markdown("#### 📈 ROC / AUC Curve")

        with st.container(border=True):
            st.info(
                "Kurva ROC dan nilai AUC akan ditampilkan di sini.",
                icon="📉"
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("** 📋 Classification Report**")
    st.info(
        "📋 **Placeholder** — Classification report akan ditampilkan setelah model dimuat.",
        icon="📊"
    )

# ── Tab 3: Fitur ──────────────────────────────────────────────────────────────
with tab_features:
    st.markdown("#### 🔑 Daftar Fitur Input")

    col_feat, col_imp = st.columns([1, 1], gap="large")

    with col_feat:
        st.markdown("### 🔑 Fitur Utama Model")

        with st.container(border=True):
            st.markdown("""
    - price_ratio
    - profit_margin_pct
    - spoilage_sensitivity
    - temp_abuse_events
    - temp_abuse_rate
    - units_sold
    - packaging_score
    - markdown_applied
    - quality_grade
    - shelf_urgency
    """)

    with col_imp:
        st.markdown("**Feature Importance**")
        st.markdown("""
        <div style="
            background: rgba(156,39,176,0.06);
            border: 2px dashed rgba(156,39,176,0.3);
            border-radius: 12px;
            padding: 60px 20px;
            text-align: center;
            color: rgba(156,39,176,0.7);
        ">
            <div style="font-size:36px;">📊</div>
            <div style="font-size:13px; margin-top:10px;">
                Feature importance chart akan ditampilkan di sini
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Tab 4: Metadata ───────────────────────────────────────────────────────────
with tab_metadata:
    st.markdown("#### 📋 Metadata Model")

    with st.container(border=True):
        st.markdown("""
    | Key | Value |
    |------|------|
    | **Model** | XGBoost |
    | **Task** | Classification |
    | **Library** | xgboost |
    | **Dataset** | Perishable Goods Dataset |
    | **Accuracy** | 92.32% |
    | **Precision** | 85.34% |
    | **Recall** | 73.05% |
    | **F1 Score** | 78.71% |
    | **AUC ROC** | 96.04% |
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Raw Config / JSON Metadata**")
    st.code('{\n  "model_name": "...",\n  "version": "...",\n  "params": {}\n}', language="json")
    st.caption("📁 File konfigurasi akan dimuat dari `models/model_config.json`")
