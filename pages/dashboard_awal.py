"""
Halaman: Dashboard Awal
========================
Menampilkan ringkasan data, statistik utama, dan overview sistem
rekomendasi food waste.

TODO (Tahap berikutnya):
- Integrasi data source (CSV / Database)
- Visualisasi chart (bar, pie, line)
- Metric cards dinamis
- Filter tanggal / kategori
"""

import streamlit as st

# ─── Judul Halaman ────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    border-left: 4px solid #4caf50;
    padding-left: 16px;
    margin-bottom: 8px;
">
    <h1 style="margin:0; font-size:28px;">🏠 Dashboard Awal</h1>
    <p style="margin:4px 0 0 0; opacity:0.6; font-size:14px;">
        Ringkasan & Overview Sistem Food Waste Recommendation
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Row 1: Metric Cards Placeholder ─────────────────────────────────────────
st.markdown("#### 📊 Statistik Utama")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Data",
        value="—",
        delta="Belum tersedia",
        help="Jumlah total data yang dimuat"
    )

with col2:
    st.metric(
        label="Prediksi Hari Ini",
        value="—",
        delta="Belum tersedia",
        help="Jumlah prediksi yang dibuat hari ini"
    )

with col3:
    st.metric(
        label="Akurasi Model",
        value="—",
        delta="Belum tersedia",
        help="Akurasi model prediksi saat ini"
    )

with col4:
    st.metric(
        label="Kategori Waste",
        value="—",
        delta="Belum tersedia",
        help="Jumlah kategori food waste"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─── Row 2: Chart Area Placeholder ───────────────────────────────────────────
st.markdown("#### 📈 Visualisasi Data")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("""
    <div style="
        background: rgba(76,175,80,0.06);
        border: 2px dashed rgba(76,175,80,0.3);
        border-radius: 12px;
        padding: 60px 20px;
        text-align: center;
        color: rgba(76,175,80,0.7);
    ">
        <div style="font-size:40px;">📉</div>
        <div style="font-size:16px; font-weight:600; margin-top:10px;">
            Area Chart — Tren Food Waste
        </div>
        <div style="font-size:12px; opacity:0.7; margin-top:6px;">
            Grafik tren data akan ditampilkan di sini
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div style="
        background: rgba(76,175,80,0.06);
        border: 2px dashed rgba(76,175,80,0.3);
        border-radius: 12px;
        padding: 40px 20px;
        text-align: center;
        color: rgba(76,175,80,0.7);
    ">
        <div style="font-size:40px;">🥧</div>
        <div style="font-size:14px; font-weight:600; margin-top:10px;">
            Pie Chart — Distribusi Kategori
        </div>
        <div style="font-size:12px; opacity:0.7; margin-top:6px;">
            Distribusi kategori akan ditampilkan di sini
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Row 3: Tabel Placeholder ─────────────────────────────────────────────────
st.markdown("#### 🗃️ Data Terbaru")

st.info(
    "⏳ **Placeholder** — Tabel data terbaru akan ditampilkan di sini "
    "setelah sumber data terhubung.",
    icon="📋"
)

# ─── Quick Navigation ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 🚀 Akses Cepat")

qn1, qn2, qn3 = st.columns(3)

with qn1:
    st.page_link(
        "pages/prediksi.py",
        label="🔮 Mulai Prediksi",
        help="Pergi ke halaman Prediksi"
    )

with qn2:
    st.page_link(
        "pages/deskripsi_model.py",
        label="📖 Lihat Model",
        help="Pergi ke halaman Deskripsi Model"
    )

with qn3:
    st.page_link(
        "pages/chatbot_model.py",
        label="🤖 Tanya Chatbot",
        help="Pergi ke halaman Chatbot Model"
    )
