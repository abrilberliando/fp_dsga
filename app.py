"""
Food Waste Recommendation System
=================================
Entry point utama aplikasi Streamlit multipage.
Mengelola navigasi, layout sidebar, dan routing antar halaman.
"""

import streamlit as st
import os

# ─── Page Config (harus dipanggil pertama) ────────────────────────────────────
st.set_page_config(
    page_title="Food Waste Recommendation",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS Global ────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar background & width */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2e1a 0%, #2d4a2d 60%, #1e3a1e 100%);
        min-width: 260px !important;
    }

    /* Sidebar text warna putih */
    [data-testid="stSidebar"] * {
        color: #f0f4f0 !important;
    }

    /* Navigation item styling */
    [data-testid="stSidebarNav"] a {
        border-radius: 8px !important;
        margin-bottom: 4px !important;
        padding: 8px 12px !important;
        transition: background 0.2s ease !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background-color: rgba(255,255,255,0.12) !important;
    }
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background-color: rgba(100,200,100,0.25) !important;
        border-left: 3px solid #7ec87e !important;
    }

    /* Main content area */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Divider warna */
    hr {
        border-color: rgba(255,255,255,0.15) !important;
    }

    /* Hide default Streamlit menu & footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar: Logo / Header Area ─────────────────────────────────────────────
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        # Placeholder logo saat file belum tersedia
        st.markdown("""
        <div style="
            text-align: center;
            padding: 20px 10px 10px 10px;
            background: rgba(255,255,255,0.06);
            border-radius: 12px;
            margin-bottom: 8px;
        ">
            <div style="font-size: 48px;">♻️</div>
            <div style="
                font-size: 16px;
                font-weight: 700;
                letter-spacing: 0.5px;
                margin-top: 6px;
                color: #a8e6a8 !important;
            ">Food Waste</div>
            <div style="
                font-size: 11px;
                opacity: 0.7;
                letter-spacing: 1px;
                text-transform: uppercase;
            ">Recommendation System</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:6px'></div>", unsafe_allow_html=True)
    st.divider()

# ─── Navigation (Streamlit st.navigation API) ─────────────────────────────────
pages = {
    "📋 Navigation": [
        st.Page(
            "pages/dashboard_awal.py",
            title="Dashboard Awal",
            icon="🏠",
            default=True,
        ),
        st.Page(
            "pages/prediksi.py",
            title="Prediksi",
            icon="🔮",
        ),
        st.Page(
            "pages/ai_gemini_model.py",
            title="AI Model Description",
            icon="🤖",
        ),
        st.Page(
            "pages/deskripsi_model.py",
            title="ML Model Description",
            icon="📖",
        ),
    ]
}

pg = st.navigation(pages, position="sidebar", expanded=True)

# ─── Sidebar: Footer / Info Area ─────────────────────────────────────────────
with st.sidebar:
    # Spacer fleksibel
    st.markdown(
        "<div style='flex:1; min-height:40px'></div>",
        unsafe_allow_html=True
    )
    st.divider()

    # ─── LLM API Config Section ───────────────────────────────────────────────
    st.markdown("""
    <div style="
        background: rgba(255,152,0,0.08);
        border: 1px solid rgba(255,152,0,0.2);
        border-radius: 8px;
        padding: 12px 10px;
        margin-bottom: 12px;
    ">
        <div style="font-size: 11px; font-weight: 600; margin-bottom: 8px; color: #FF9800;">
            🔑 LLM API Config
        </div>
    </div>
    """, unsafe_allow_html=True)

    llm_api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="Masukkan LLM API key...",
        help="Kunci API untuk layanan LLM (OpenAI, Gemini, dll)",
        key="llm_api_key"
    )

    if llm_api_key:
        st.success("✓ API Key berhasil diisi", icon="✅")
        # Simpan ke session state
        st.session_state.llm_api_key = llm_api_key
    else:
        st.caption("⚠️ API Key belum dikonfigurasi")

    st.divider()

    st.markdown("""
    <div style="
        text-align: center;
        padding: 10px 8px;
        font-size: 11px;
        opacity: 0.55;
        line-height: 1.6;
    ">
        <div>🌱 <strong>Food Waste App</strong> v1.0.0</div>
        <div style="margin-top:4px;">Dibuat dengan Streamlit</div>
        <div>© 2024 · Semua hak dilindungi</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Jalankan halaman yang dipilih ────────────────────────────────────────────
pg.run()
