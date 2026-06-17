"""
AI Model & Gemini Assistant
=============================
Halaman dokumentasi dan konfigurasi Gemini API untuk sistem Food Waste Recommendation.
Dirancang untuk trainer, evaluator, dan stakeholder yang ingin memahami integrasi AI.

Structure:
- Tab 1: Gemini Overview (Model info & capabilities)
- Tab 2: API Configuration (Setup & connection)
- Tab 3: Custom Prompt (System prompt documentation)
- Tab 4: AI Workflow (Visual pipeline & architecture)
"""

import streamlit as st
import google.generativeai as genai

# ─── Page Config ──────────────────────────────────────────────────────────────


# ─── Session State Initialization ─────────────────────────────────────────────
if "gemini_test_result" not in st.session_state:
    st.session_state.gemini_test_result = None

if "gemini_connection_status" not in st.session_state:
    st.session_state.gemini_connection_status = "Not Connected"

# ─── TEMA WARNA & CSS (Selaras dengan Dashboard) ──────────────────────────────
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
    height: 100%;
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

.kpi-icon  {{ font-size:1.5rem; margin-bottom:.35rem; display:inline-block; }}
.kpi-lbl   {{ font-size:.8rem; color:{C['text']}; font-weight:700; display:inline-block; margin-left:8px; }}
.kpi-val   {{ font-size:1.2rem; font-weight:800; color:{C['text']}; font-family:'JetBrains Mono',monospace; margin-top:8px; }}
.kpi-sub   {{ font-size:.75rem; margin-top:.4rem; font-weight:500; color:{C['muted']}; }}

/* ── Section headers ── */
.sec-hdr {{
    display:flex; align-items:center; gap:.6rem;
    padding:.5rem 0 .6rem 0;
    border-bottom: 1px solid {C['border']};
    margin: 1.8rem 0 1rem 0;
}}
.sec-hdr h3 {{ margin:0; font-size:1.1rem; font-weight:700; color:{C['text']}; }}
.sec-dot {{
    width:9px; height:9px; border-radius:50%; flex-shrink:0;
    background: linear-gradient(135deg,{C['blue']},{C['purple']});
}}

/* ── Info boxes ── */
.ibox {{
    border-radius:10px; padding:.9rem 1.1rem;
    font-size:.8rem; line-height:1.65; color:{C['muted']};
}}
.ibox.green {{ background:rgba(76,175,80,.07); border:1px solid rgba(76,175,80,.25); }}
.ibox.orange{{ background:rgba(255,152,0,.07); border:1px solid rgba(255,152,0,.25); }}
.ibox.blue  {{ background:rgba(33,150,243,.07); border:1px solid rgba(33,150,243,.25); }}
.ibox.purple{{ background:rgba(156,39,176,.07); border:1px solid rgba(156,39,176,.25); }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background:{C['bg']}; }}
::-webkit-scrollbar-thumb {{ background:#4a5568; border-radius:3px; }}
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ─────────────────────────────────────────────────────────

def test_gemini_connection():
    """Test koneksi ke Gemini API."""
    api_key = st.session_state.get("llm_api_key", "")
    
    if not api_key:
        return {
            "status": "FAILED",
            "message": "❌ API Key belum dikonfigurasi",
            "details": "Silakan isi API Key di sidebar terlebih dahulu"
        }
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Simple test request
        response = model.generate_content("Test connection: reply with 'Connection successful'")
        
        if response.text:
            return {
                "status": "SUCCESS",
                "message": "✅ Koneksi Berhasil",
                "details": f"Model: Gemini 2.5 Flash | Response: {response.text[:100]}..."
            }
        else:
            return {
                "status": "FAILED",
                "message": "❌ Tidak ada response dari API",
                "details": "Coba lagi atau periksa API key"
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "message": "❌ Koneksi Gagal",
            "details": f"Error: {str(e)}"
        }

def get_system_prompt():
    """Return system prompt dokumentasi untuk Gemini."""
    return """Anda adalah konsultan retail yang membantu mengurangi food waste berdasarkan hasil prediksi machine learning.

Analisis data berikut:

HASIL PREDIKSI

* Probabilitas Risiko: {probability}
* Kategori Risiko: {risk_level}

DATA PRODUK
{product_context}

Tugas:

Buat laporan singkat dan praktis dengan format:

## Ringkasan

Jelaskan kondisi produk saat ini dalam 2-3 kalimat.

## Faktor Utama

Sebutkan maksimal 3 faktor yang paling berpengaruh terhadap risiko.

## Rekomendasi

Berikan maksimal 3 tindakan yang dapat dilakukan segera.

## Kesimpulan

Berikan ringkasan singkat dalam 1-2 kalimat.

Aturan:

* Fokus pada tindakan operasional.
* Gunakan bahasa Indonesia yang jelas dan profesional.
* Maksimal 250 kata.
* Hindari penjelasan teori machine learning.
* Hindari pengulangan informasi input.
* Prioritaskan informasi yang paling penting bagi manager toko.
"""

def copy_to_clipboard(text: str):
    """Helper untuk copy text (display only, real copy di browser)."""
    st.code(text, language="text")

def custom_card(icon, title, value, subtitle, color_cls):
    """Membungkus konten menjadi card UI ala dashboard"""
    return f"""
    <div class="kpi-wrap {color_cls}">
        <div><span class="kpi-icon">{icon}</span><span class="kpi-lbl">{title}</span></div>
        <div class="kpi-val">{value}</div>
        <div class="kpi-sub">{subtitle}</div>
    </div>
    """


# ─── Page Title ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="border-left:4px solid {C['blue']}; padding-left:16px; margin-bottom:24px;">
    <h1 style="margin:0; font-size:28px; font-weight:800; display:flex; align-items:center; gap:10px;">
        🤖 AI Model & Gemini Assistant
    </h1>
    <p style="margin:4px 0 0 0; opacity:.55; font-size:13px;">
        Dokumentasi & Konfigurasi Gemini API untuk Food Waste Recommendation System
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Gemini Overview",
    "⚙️ API Configuration",
    "📝 Custom Prompt",
    "🔄 AI Workflow"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: GEMINI OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>Model Information & Capabilities</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Basic Info (Menggunakan UI Card)
    col_model1, col_model2, col_model3 = st.columns(3)
    
    with col_model1:
        st.markdown(custom_card("🎯", "Model Name", "Gemini 2.5 Flash", "Latest generation AI model by Google", "kpi-blue"), unsafe_allow_html=True)
    with col_model2:
        st.markdown(custom_card("📦", "Version", "2.5 Flash", "Optimized for speed & cost", "kpi-purple"), unsafe_allow_html=True)
    with col_model3:
        st.markdown(custom_card("🌐", "Provider", "Google AI", "google.generativeai API", "kpi-teal"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Model Purpose
    st.markdown(f"""
    <div class="kpi-wrap kpi-orange" style="padding: 1.5rem;">
        <h4 style="margin-top:0; color:{C['text']}; font-weight:700;">🎯 Tujuan Penggunaan</h4>
        <p style="color:{C['muted']}; font-size:0.9rem; line-height:1.6;">Memberikan <b>rekomendasi operasional retail berdasarkan hasil prediksi model XGBoost</b>.</p>
        <p style="color:{C['muted']}; font-size:0.9rem; margin-bottom:0.5rem;">Model Gemini diintegrasikan untuk:</p>
        <ul style="color:{C['muted']}; font-size:0.85rem; line-height:1.8;">
            <li><b>Analisis Mendalam</b> - Menginterpretasi hasil prediksi risiko dari XGBoost</li>
            <li><b>Rekomendasi Bisnis</b> - Membuat strategi actionable untuk manager retail</li>
            <li><b>Konteks Tambahan</b> - Menambah konteks bisnis pada data teknis</li>
            <li><b>Natural Language</b> - Menghasilkan rekomendasi dalam bahasa yang mudah dipahami</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input & Output
    col_io1, col_io2 = st.columns(2)
    
    with col_io1:
        st.markdown(f"""
        <div class="kpi-wrap kpi-blue">
            <h4 style="margin-top:0; color:{C['text']}; font-weight:700;">📥 Input yang Diterima</h4>
            <ul style="color:{C['muted']}; font-size:0.85rem; line-height:1.8; list-style-type:none; padding-left:0;">
                <li>🏷️ Kategori Produk (e.g., Dairy, Buah)</li>
                <li>📦 Jumlah Stok (unit)</li>
                <li>📅 Sisa Hari Kadaluarsa (hari)</li>
                <li>💰 Diskon Saat Ini (%)</li>
                <li>⚠️ Probabilitas Risiko (0-100%)</li>
                <li>🎯 Status Risiko (LOW/MEDIUM/HIGH/CRITICAL)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_io2:
        st.markdown(f"""
        <div class="kpi-wrap kpi-green">
            <h4 style="margin-top:0; color:{C['text']}; font-weight:700;">📤 Output yang Dihasilkan</h4>
            <ul style="color:{C['muted']}; font-size:0.85rem; line-height:1.8; list-style-type:none; padding-left:0;">
                <li>🔍 Analisis Risiko (detailed explanation)</li>
                <li>💬 Main Factors (faktor utama risiko)</li>
                <li>✅ Rekomendasi Aksi (actionable steps)</li>
                <li>🏷️ Strategi Diskon (pricing recommendation)</li>
                <li>📊 Saran Inventaris (inventory action)</li>
                <li>📈 Faktor Tambahan (contributing factors)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Features
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>Key Features</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    
    with col_feat1:
        st.markdown(f"""<div class="ibox green">✅ <b style="color:{C['green']}">JSON Response Parsing</b><br>Structured output dalam format JSON</div>""", unsafe_allow_html=True)
    with col_feat2:
        st.markdown(f"""<div class="ibox blue">⚡ <b style="color:{C['blue']}">Fast Response Time</b><br>~2-5 detik per request</div>""", unsafe_allow_html=True)
    with col_feat3:
        st.markdown(f"""<div class="ibox orange">💰 <b style="color:{C['orange']}">Cost-Effective</b><br>Flash model pricing terjangkau</div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Model Parameters
    with st.expander("📊 Model Parameters & Configuration", expanded=True):
        st.markdown("""
        | Parameter | Value | Description |
        |-----------|-------|-------------|
        | **Model ID** | gemini-2.5-flash | Official model identifier |
        | **API Version** | Latest | Auto-updated by SDK |
        | **Max Tokens** | 1000+ | Output length limit |
        | **Temperature** | Default (0.7) | Creativity/determinism balance |
        | **Top P** | Default | Nucleus sampling |
        | **Response Format** | JSON | Structured output |
        """)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: API CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>Gemini API Setup & Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. API Key Info
    st.markdown(f"""
    <div class="ibox blue" style="margin-bottom: 1.5rem;">
        💡 <b style="color:{C['blue']}">Pengaturan API Key Terpusat:</b><br>
        Pengaturan API Key sekarang dikelola secara terpusat melalui <b>Sidebar</b> di sebelah kiri layar untuk keamanan global seluruh sistem.
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Test Connection Area (Fungsi Live Test)
    st.markdown("<h4 style='font-size:1rem;'>🧪 Live Verification Test</h4>", unsafe_allow_html=True)
    with st.container(border=True):
        col_test_btn, col_test_status = st.columns([1, 2])
        
        with col_test_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔗 Run Live Connection Test", type="primary", use_container_width=True):
                with st.spinner("Menghubungkan ke server Google AI..."):
                    result = test_gemini_connection()
                    st.session_state.gemini_test_result = result
                    
                    if result["status"] == "SUCCESS":
                        st.session_state.gemini_connection_status = "Connected & Verified"
                    else:
                        st.session_state.gemini_connection_status = "Verification Failed"
                        
        with col_test_status:
            if st.session_state.gemini_test_result:
                result = st.session_state.gemini_test_result
                if result["status"] == "SUCCESS":
                    st.success(result["message"])
                    st.caption(result["details"])
                else:
                    st.error(result["message"])
                    st.caption(result["details"])
            else:
                st.caption("Silakan masukkan API Key di sidebar kiri terlebih dahulu, lalu klik tombol untuk menguji keaslian koneksi.")
                
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Dynamic Connection Status Cards
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        status_now = st.session_state.gemini_connection_status
        if status_now == "Connected & Verified":
            st.markdown(custom_card("🌐", "Connection", status_now, "API Key valid & aktif", "kpi-green"), unsafe_allow_html=True)
        elif status_now == "Verification Failed":
            st.markdown(custom_card("🌐", "Connection", status_now, "Koneksi ditolak server", "kpi-red"), unsafe_allow_html=True)
        else:
            st.markdown(custom_card("🌐", "Connection", status_now, "Koneksi belum diuji", "kpi-orange"), unsafe_allow_html=True)
            
    with col_status2:
        st.markdown(custom_card("🤖", "Active Model", "Gemini 2.5 Flash", "Optimal untuk kecepatan", "kpi-blue"), unsafe_allow_html=True)
        
    with col_status3:
        st.markdown(custom_card("📡", "API Provider", "Google AI", "google.generativeai SDK", "kpi-purple"), unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4. Instructions Expander
    with st.expander("📖 How to Get Gemini API Key", expanded=False):
        st.markdown("""
        ### Langkah-langkah Mendapatkan Key:
        
        1. **Buka Google AI Studio**
           - Kunjungi: https://makersuite.google.com/app/apikey
           - Masuk menggunakan akun Google Anda.
        
        2. **Create API Key**
           - Klik tombol **"Create API Key"**.
           - Pilih project Google Cloud Anda atau buat baru secara instan.
           - Salin (*Copy*) string kode rahasia yang muncul.
        
        3. **Gunakan di Dashboard**
           - Tempelkan (*Paste*) kode tersebut ke dalam kolom input di **Sidebar Kiri** aplikasi ini.
           - Klik tombol **"Run Live Connection Test"** di atas untuk mengaktifkan sistem rekomendasi AI.
        """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: CUSTOM PROMPT (Documentation Mode)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>System Prompt Documentation</h3>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Prompt ini adalah instruksi inti yang mengatur bagaimana Gemini mengevaluasi prediksi dari model XGBoost. Halaman ini murni sebagai dokumentasi arsitektur AI (Read-Only).")
    
    st.markdown("")
    
    col_header, col_tip = st.columns([1, 1])
    with col_header:
        st.markdown("<h4 style='font-size:1rem; margin:0;'>💾 Core Instruction Template</h4>", unsafe_allow_html=True)
    with col_tip:
        st.markdown(f"""
        <div style='text-align: right; opacity: 0.8; color:{C['muted']};'>
            <small>💡 <b>Tip:</b> Arahkan kursor ke pojok kanan atas kotak kode untuk menyalin.</small>
        </div>
        """, unsafe_allow_html=True)
        
    # Menampilkan prompt statis dari fungsi
    st.code(get_system_prompt(), language="text")
    
    st.markdown("")
    
    st.download_button(
        label="📥 Download Full Prompt Template (.txt)",
        data=get_system_prompt(),
        file_name="gemini_system_prompt_documentation.txt",
        mime="text/plain",
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: AI WORKFLOW
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="sec-hdr">
        <div class="sec-dot"></div>
        <h3>System Architecture & Data Flow</h3>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Alur kerja sistem terintegrasi dari input pengguna, prediksi XGBoost, hingga analisis oleh Gemini.")

    st.markdown("<h4 style='font-size:1rem; margin-top:1.5rem;'>🔄 Data Flow Pipeline</h4>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background:{C['card']}; border-radius:10px;">
            <div style="
                display: flex;
                justify-content: space-around;
                align-items: center;
                margin: 20px 0;
                font-size: 14px;
                font-weight: 600;
                color: {C['text']};
            ">
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">📋</div>
                    <div>User Input</div>
                    <div style="font-size: 11px; color: {C['muted']}; margin-top: 4px;">
                        Kategori, Stok,<br/>Kadaluarsa, Diskon
                    </div>
                </div>
                <div style="font-size: 24px; color: {C['muted']};">→</div>
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">🤖</div>
                    <div>XGBoost Model</div>
                    <div style="font-size: 11px; color: {C['muted']}; margin-top: 4px;">
                        ML Prediction<br/>Risk Score
                    </div>
                </div>
                <div style="font-size: 24px; color: {C['muted']};">→</div>
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">⚠️</div>
                    <div>Risk Analysis</div>
                    <div style="font-size: 11px; color: {C['muted']}; margin-top: 4px;">
                        Probability &<br/>Risk Status
                    </div>
                </div>
                <div style="font-size: 24px; color: {C['muted']};">→</div>
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">✨</div>
                    <div>Gemini LLM</div>
                    <div style="font-size: 11px; color: {C['muted']}; margin-top: 4px;">
                        Natural Language<br/>Analysis
                    </div>
                </div>
                <div style="font-size: 24px; color: {C['muted']};">→</div>
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">💼</div>
                    <div>Recommendation</div>
                    <div style="font-size: 11px; color: {C['muted']}; margin-top: 4px;">
                        Actionable<br/>Business Advice
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<h4 style='font-size:1rem;'>🏗️ System Architecture Layers</h4>", unsafe_allow_html=True)
    col_arch1, col_arch2 = st.columns(2)
    
    with col_arch1:
        st.markdown(f"""
        <div class="kpi-wrap kpi-blue" style="padding: 1.5rem;">
            <h5 style="margin-top:0; color:{C['text']}; font-weight:700;">📊 Machine Learning Layer</h5>
            <ul style="color:{C['muted']}; font-size:0.85rem; line-height:1.8; list-style-type:none; padding-left:0;">
                <li><b style="color:{C['blue']}">Model:</b> XGBoost Regressor</li>
                <li><b style="color:{C['blue']}">Purpose:</b> Predict food waste risk</li>
                <li><b style="color:{C['blue']}">Inputs:</b> Product features, Storage conditions, Inventory metrics</li>
                <li><b style="color:{C['blue']}">Outputs:</b> Risk Probability (0-100%), Risk Status</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_arch2:
        st.markdown(f"""
        <div class="kpi-wrap kpi-purple" style="padding: 1.5rem;">
            <h5 style="margin-top:0; color:{C['text']}; font-weight:700;">🤖 LLM Layer (Gemini)</h5>
            <ul style="color:{C['muted']}; font-size:0.85rem; line-height:1.8; list-style-type:none; padding-left:0;">
                <li><b style="color:{C['purple']}">Model:</b> Gemini 2.5 Flash</li>
                <li><b style="color:{C['purple']}">Purpose:</b> Generate business recommendations</li>
                <li><b style="color:{C['purple']}">Inputs:</b> ML predictions, Product context, Constraints</li>
                <li><b style="color:{C['purple']}">Outputs:</b> Actionable recommendations, Discount strategies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)