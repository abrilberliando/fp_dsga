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
        st.markdown("#### 🧠 Tentang Model")
        with st.container(border=True):
            st.markdown("""
            | Atribut         | Nilai                      |
            |-----------------|----------------------------|
            | **Nama Model**  | *Belum dikonfigurasi*      |
            | **Tipe**        | *Belum dikonfigurasi*      |
            | **Versi**       | *v—*                      |
            | **Library**     | *Belum dikonfigurasi*      |
            | **Target**      | *Belum dikonfigurasi*      |
            | **Input Shape** | *Belum dikonfigurasi*      |
            """)

        st.markdown("#### 📝 Deskripsi")
        st.markdown("""
        <div style="
            background: rgba(156,39,176,0.06);
            border: 2px dashed rgba(156,39,176,0.3);
            border-radius: 12px;
            padding: 30px 20px;
            text-align: center;
            color: rgba(156,39,176,0.7);
        ">
            <div style="font-size:36px;">🧬</div>
            <div style="font-size:14px; font-weight:600; margin-top:10px;">
                Deskripsi model akan ditampilkan di sini
            </div>
            <div style="font-size:12px; opacity:0.7; margin-top:6px;">
                Muat konfigurasi model dari folder <code>models/</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_arch:
        st.markdown("#### 🏗️ Arsitektur / Pipeline")
        st.markdown("""
        <div style="
            background: rgba(156,39,176,0.06);
            border: 2px dashed rgba(156,39,176,0.3);
            border-radius: 12px;
            padding: 80px 20px;
            text-align: center;
            color: rgba(156,39,176,0.7);
        ">
            <div style="font-size:40px;">🗺️</div>
            <div style="font-size:14px; font-weight:600; margin-top:10px;">
                Diagram arsitektur model
            </div>
            <div style="font-size:12px; opacity:0.7; margin-top:6px;">
                Visualisasi pipeline preprocessing → model → output
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Tab 2: Performa ───────────────────────────────────────────────────────────
with tab_performance:
    st.markdown("#### 📈 Metrik Evaluasi")

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Accuracy", "—", help="Akurasi keseluruhan")
    mc2.metric("Precision", "—", help="Precision score")
    mc3.metric("Recall", "—", help="Recall score")
    mc4.metric("F1-Score", "—", help="F1 score")

    st.markdown("<br>", unsafe_allow_html=True)

    col_cm, col_roc = st.columns(2)

    with col_cm:
        st.markdown("**Confusion Matrix**")
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
                Confusion matrix akan ditampilkan di sini
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_roc:
        st.markdown("**ROC / AUC Curve**")
        st.markdown("""
        <div style="
            background: rgba(156,39,176,0.06);
            border: 2px dashed rgba(156,39,176,0.3);
            border-radius: 12px;
            padding: 60px 20px;
            text-align: center;
            color: rgba(156,39,176,0.7);
        ">
            <div style="font-size:36px;">📉</div>
            <div style="font-size:13px; margin-top:10px;">
                Kurva ROC/AUC akan ditampilkan di sini
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Classification Report**")
    st.info(
        "📋 **Placeholder** — Classification report akan ditampilkan setelah model dimuat.",
        icon="📊"
    )

# ── Tab 3: Fitur ──────────────────────────────────────────────────────────────
with tab_features:
    st.markdown("#### 🔑 Daftar Fitur Input")

    col_feat, col_imp = st.columns([1, 1], gap="large")

    with col_feat:
        st.markdown("**Fitur yang Digunakan**")
        st.info(
            "📋 **Placeholder** — Daftar fitur input model akan ditampilkan di sini.",
            icon="🔑"
        )

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
        | Key                     | Value                          |
        |-------------------------|--------------------------------|
        | **File Model**          | *Belum dimuat*                |
        | **Tanggal Training**    | *—*                           |
        | **Dataset Training**    | *Belum dikonfigurasi*         |
        | **Jumlah Data Train**   | *—*                           |
        | **Jumlah Data Test**    | *—*                           |
        | **Hyperparameter**      | *Belum dikonfigurasi*         |
        | **Framework Version**   | *—*                           |
        | **Python Version**      | *—*                           |
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Raw Config / JSON Metadata**")
    st.code('{\n  "model_name": "...",\n  "version": "...",\n  "params": {}\n}', language="json")
    st.caption("📁 File konfigurasi akan dimuat dari `models/model_config.json`")
