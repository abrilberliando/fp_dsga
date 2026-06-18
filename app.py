"""
Food Waste Recommendation System

Entry point utama aplikasi Streamlit multipage.
Mengelola navigasi, layout sidebar, role selector, dan routing antar halaman.
"""

import streamlit as st
import os
import sys

#add base directory to path for utils imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# page config
st.set_page_config(
    page_title="Food Waste Recommendation",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

#inject global css 
from utils.theme import inject_css, COLORS
inject_css()

# Force sidebar to stay open with JavaScript
st.markdown("""
<script>
    // Prevent sidebar from closing
    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.display = 'block';
        sidebar.style.visibility = 'visible';
    }
    
    // Hide collapse button
    const collapseButton = window.parent.document.querySelector('[data-testid="collapsedControl"]');
    if (collapseButton) {
        collapseButton.style.display = 'none';
    }
</script>
""", unsafe_allow_html=True)

#custom sidebar css 
st.markdown(f"""
<style>
    /* Force sidebar to always be visible */
    section[data-testid="stSidebar"] {{
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        transform: translateX(0) !important;
        transition: none !important;
    }}
    
    /* Hide all collapse controls */
    [data-testid="collapsedControl"] {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    button[kind="header"] {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    /* Remove collapse button from sidebar header */
    section[data-testid="stSidebar"] > div:first-child > button {{
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }}
    
    /* Ensure main content adjusts for permanent sidebar */
    .main {{
        margin-left: 0 !important;
    }}
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['card']} 0%, #141822 50%, {COLORS['bg']} 100%);
        border-right: 1px solid {COLORS['border']};
        min-width: 280px !important;
        max-width: 280px !important;
    }}
    
    /* Sidebar Text Colors */
    [data-testid="stSidebar"] * {{ 
        color: {COLORS['text']} !important; 
    }}
    
    /* Navigation Items */
    [data-testid="stSidebarNav"] a {{
        background: rgba(255,255,255,0.03);
        border: 1px solid {COLORS['border']};
        border-radius: 10px !important;
        margin-bottom: 6px !important;
        margin-top: 0px !important;
        padding: 10px 14px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 500;
    }}
    
    /* Navigation Hover */
    [data-testid="stSidebarNav"] a:hover {{
        background: rgba(76,175,80,0.08) !important;
        border-color: rgba(76,175,80,0.3) !important;
        transform: translateX(4px);
    }}
    
    /* Active Navigation Item */
    [data-testid="stSidebarNav"] a[aria-selected="true"] {{
        background: linear-gradient(135deg, rgba(76,175,80,0.15), rgba(38,166,154,0.15)) !important;
        border-left: 3px solid {COLORS['green']} !important;
        border-color: rgba(76,175,80,0.4) !important;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(76,175,80,0.2);
    }}
    
    /* Navigation Section Headers */
    [data-testid="stSidebarNav"] li[role="listitem"]:has(> span) {{
        font-size: .7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .12em;
        color: {COLORS['muted']} !important;
        margin-top: 12px !important;
        margin-bottom: 6px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        padding-left: 4px;
    }}
    
    /* First section header - reduce top margin */
    [data-testid="stSidebarNav"] li[role="listitem"]:has(> span):first-of-type {{
        margin-top: 0px !important;
    }}
    
    /* Navigation list container - reduce internal spacing */
    [data-testid="stSidebarNav"] ul {{
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }}
    
    /* Navigation sections - reduce spacing between groups */
    [data-testid="stSidebarNav"] > div {{
        gap: 0px !important;
    }}
    
    /* List items - ensure consistent spacing */
    [data-testid="stSidebarNav"] li {{
        margin-bottom: 0px !important;
    }}

    /* Main Container */
    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* Divider Lines */
    hr {{ 
        border-color: {COLORS['border']} !important;
        margin: 1rem 0 !important;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Sidebar Custom Components */
    
    /* Logo Container */
    .sidebar-logo {{
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
        background: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 14px;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }}
    .sidebar-logo::after {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {COLORS['green']}, {COLORS['teal']});
        border-radius: 14px 14px 0 0;
    }}
    .sidebar-logo-icon {{ 
        font-size: 56px; 
        margin-bottom: 8px;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(76,175,80,0.3));
    }}
    .sidebar-logo-title {{ 
        font-size: 18px; 
        font-weight: 800; 
        letter-spacing: .5px;
        color: {COLORS['green']};
        margin-bottom: 4px;
        font-family: 'Inter', sans-serif;
    }}
    .sidebar-logo-subtitle {{ 
        font-size: 10px; 
        opacity: .65; 
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: {COLORS['muted']};
        font-weight: 600;
    }}

    /* Role Selector */
    .role-container {{
        background: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
    }}
    .role-label {{
        font-size: .7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .12em;
        color: {COLORS['muted']};
        margin-bottom: .6rem;
        display: flex;
        align-items: center;
        gap: .4rem;
    }}
    .role-info {{
        font-size: .72rem;
        color: {COLORS['muted']};
        line-height: 1.6;
        padding: .6rem .8rem;
        border-radius: 8px;
        margin-top: .6rem;
        border: 1px solid {COLORS['border']};
    }}
    .role-info.retail {{
        background: rgba(76,175,80,.06);
        border-color: rgba(76,175,80,.2);
    }}
    .role-info.tech {{
        background: rgba(33,150,243,.06);
        border-color: rgba(33,150,243,.2);
    }}

    /* API Key Section */
    .api-key-container {{
        background: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 1rem 1.1rem .8rem 1.1rem;
        margin-bottom: 1rem;
        position: relative;
    }}
    .api-key-header {{
        display: flex;
        align-items: center;
        gap: .5rem;
        font-size: .75rem;
        font-weight: 700;
        color: {COLORS['orange']};
        margin-bottom: .8rem;
        text-transform: uppercase;
        letter-spacing: .08em;
    }}
    .api-key-icon {{
        font-size: 1.1rem;
        filter: drop-shadow(0 2px 4px rgba(255,152,0,0.3));
    }}

    /* Footer */
    .sidebar-footer {{
        text-align: center;
        padding: 1rem .8rem;
        font-size: .7rem;
        color: {COLORS['muted']};
        line-height: 1.8;
        background: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
    }}
    .sidebar-footer strong {{
        color: {COLORS['text']};
        font-weight: 700;
    }}
    .sidebar-footer-badge {{
        display: inline-block;
        padding: .2rem .5rem;
        border-radius: 6px;
        font-size: .65rem;
        font-weight: 600;
        margin-top: .4rem;
        background: rgba(76,175,80,.1);
        border: 1px solid rgba(76,175,80,.25);
        color: {COLORS['green']};
    }}

    /* Radio Button Override */
    [data-testid="stSidebar"] .stRadio > div {{
        gap: .4rem !important;
    }}
    [data-testid="stSidebar"] .stRadio label {{
        background: rgba(255,255,255,0.02);
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: .6rem .9rem !important;
        transition: all 0.2s ease;
        font-size: .8rem;
    }}
    [data-testid="stSidebar"] .stRadio label:hover {{
        background: rgba(76,175,80,0.05);
        border-color: rgba(76,175,80,0.3);
    }}
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {{
        background: linear-gradient(135deg, rgba(76,175,80,0.12), rgba(38,166,154,0.12));
        border-color: {COLORS['green']};
        font-weight: 600;
    }}

    /* Text Input Override */
    [data-testid="stSidebar"] input {{
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 8px !important;
        font-size: .8rem !important;
        padding: .6rem .9rem !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stSidebar"] input:focus {{
        border-color: {COLORS['green']} !important;
        box-shadow: 0 0 0 2px rgba(76,175,80,0.1) !important;
    }}
</style>
""", unsafe_allow_html=True)

#session state initialization 
if "user_role" not in st.session_state:
    st.session_state.user_role = "🛒 Retail Manager"

#sidebar logo 
with st.sidebar:
    logo_path = os.path.join(BASE_DIR, "assets", "logo.png")
    if os.path.exists(logo_path):
        st.markdown('<div style="padding:.5rem 0;">', unsafe_allow_html=True)
        st.image(logo_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sidebar-logo">
            <span class="sidebar-logo-icon">♻️</span>
            <div class="sidebar-logo-title">Food Waste</div>
            <div class="sidebar-logo-subtitle">Recommendation System</div>
        </div>
        """, unsafe_allow_html=True)

    # ─── role selector ──────────────────────────────────────────────────────
    st.markdown('<div class="role-container">', unsafe_allow_html=True)
    st.markdown('<div class="role-label">👤 Mode Pengguna</div>', unsafe_allow_html=True)
    
    role = st.radio(
        label="mode_pengguna",
        options=["🛒 Retail Manager", "🔬 Stakeholder Teknis"],
        index=0 if st.session_state.user_role == "🛒 Retail Manager" else 1,
        key="role_radio",
        label_visibility="collapsed",
    )
    st.session_state.user_role = role

    # display role information
    if "Retail Manager" in role:
        st.markdown("""
        <div class="role-info retail">
            <strong>📋 Mode Operasional</strong><br/>
            Prediksi risiko & rekomendasi aksi untuk operasional harian
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="role-info tech">
            <strong>🔬 Mode Analitik</strong><br/>
            Akses penuh: data, model, evaluasi & AI architecture
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

#role-based navigation
is_retail = "Retail Manager" in st.session_state.user_role

if is_retail:
    # retail manager: operational pages only
    pages = {
        "📋 Operasional": [
            st.Page(
                "pages/prediksi.py",
                title="Prediksi Risiko",
                icon="🔮",
                default=True,
            ),
            st.Page(
                "pages/ai_gemini_model.py",
                title="AI Assistant",
                icon="🤖",
            ),
        ]
    }
else:
    # stakeholder teknis: full access
    pages = {
        "📋 Operasional": [
            st.Page(
                "pages/prediksi.py",
                title="Prediksi Risiko",
                icon="🔮",
            ),
            st.Page(
                "pages/ai_gemini_model.py",
                title="AI Assistant",
                icon="🤖",
            ),
        ],
        "🔬 Analitik": [
            st.Page(
                "pages/dashboard_awal.py",
                title="Dashboard & Data",
                icon="🏠",
                default=True,
            ),
            st.Page(
                "pages/deskripsi_model.py",
                title="Performa Model",
                icon="📖",
            ),
        ],
    }

pg = st.navigation(pages, position="sidebar", expanded=True)

#Sidebar Toggle Helper 
# Info box untuk membantu user jika sidebar tersembunyi
st.markdown(f"""
<div style="position: fixed; top: 0.5rem; right: 0.5rem; z-index: 999998; 
            background: {COLORS['card']}; border: 1px solid {COLORS['border']}; 
            border-radius: 8px; padding: 0.5rem 0.8rem; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.2); font-size: 0.7rem; color: {COLORS['muted']};
            display: flex; align-items: center; gap: 0.4rem;">
    <span style="font-size: 1rem;">☰</span>
    <span>Klik ikon menu ☰ di kiri atas untuk buka sidebar</span>
</div>
""", unsafe_allow_html=True)

#sidebar api key and footer 
with st.sidebar:
    st.markdown(
        "<div style='flex:1; min-height:20px'></div>",
        unsafe_allow_html=True
    )

    # api key section
    st.markdown('<div class="api-key-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="api-key-header">
        <span class="api-key-icon">🔑</span>
        <span>Gemini API Key</span>
    </div>
    """, unsafe_allow_html=True)

    llm_api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="Masukkan Gemini API key...",
        help="Diperlukan untuk fitur AI Analysis dan Chat Assistant",
        key="llm_api_key",
        label_visibility="collapsed",
    )

    if llm_api_key:
        st.success("✅ API Key aktif", icon="✨")
    else:
        st.caption("⚠️ Isi API Key untuk mengaktifkan fitur AI")

    st.markdown('</div>', unsafe_allow_html=True)

    # footer
    st.markdown("""
    <div class="sidebar-footer">
        <div>🌱 <strong>Food Waste App</strong></div>
        <div class="sidebar-footer-badge">v2.0.0</div>
        <div style="margin-top:.5rem; font-size:.65rem;">
            Streamlit · XGBoost · Gemini 
        </div>
        <div style="margin-top:.3rem; opacity:.6;">
            2026 · Kelompok 3 DSGA
        </div>
    </div>
    """, unsafe_allow_html=True)

#run selected page 
pg.run()
