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
st.set_page_config(layout="wide")

# ─── Session State Initialization ─────────────────────────────────────────────
if "gemini_test_result" not in st.session_state:
    st.session_state.gemini_test_result = None

if "gemini_connection_status" not in st.session_state:
    st.session_state.gemini_connection_status = "Not Connected"

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


# ─── Page Title ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 20px 10px;
">
    <div style="font-size: 48px;">🤖</div>
    <h1 style="margin:8px 0 4px 0; font-size:32px;">AI Model & Gemini Assistant</h1>
    <p style="margin:0; opacity:0.6; font-size:14px;">
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
    st.markdown("### Model Information & Capabilities")
    
    # Model Basic Info
    col_model1, col_model2, col_model3 = st.columns(3)
    
    with col_model1:
        with st.container(border=True):
            st.markdown("#### 🎯 Model Name")
            st.markdown("**Gemini 2.5 Flash**")
            st.caption("Latest generation AI model by Google")
    
    with col_model2:
        with st.container(border=True):
            st.markdown("#### 📦 Version")
            st.markdown("**2.5 Flash**")
            st.caption("Optimized for speed & cost")
    
    with col_model3:
        with st.container(border=True):
            st.markdown("#### 🌐 Provider")
            st.markdown("**Google AI**")
            st.caption("google.generativeai API")
    
    st.markdown("")
    
    # Model Purpose
    with st.container(border=True):
        st.markdown("#### 🎯 Tujuan Penggunaan")
        st.markdown("""
Memberikan **rekomendasi operasional retail berdasarkan hasil prediksi model XGBoost**.

Model Gemini diintegrasikan untuk:
1. **Analisis Mendalam** - Menginterpretasi hasil prediksi risiko dari XGBoost
2. **Rekomendasi Bisnis** - Membuat strategi actionable untuk manager retail
3. **Konteks Tambahan** - Menambah konteks bisnis pada data teknis
4. **Natural Language** - Menghasilkan rekomendasi dalam bahasa yang mudah dipahami
        """)
    
    st.markdown("")
    
    # Input & Output
    col_io1, col_io2 = st.columns(2)
    
    with col_io1:
        with st.container(border=True):
            st.markdown("#### 📥 Input yang Diterima")
            inputs = [
                "🏷️ Kategori Produk (e.g., Dairy, Buah)",
                "📦 Jumlah Stok (unit)",
                "📅 Sisa Hari Kadaluarsa (hari)",
                "💰 Diskon Saat Ini (%)",
                "⚠️ Probabilitas Risiko (0-100%)",
                "🎯 Status Risiko (LOW/MEDIUM/HIGH/CRITICAL)"
            ]
            for inp in inputs:
                st.write(f"• {inp}")
    
    with col_io2:
        with st.container(border=True):
            st.markdown("#### 📤 Output yang Dihasilkan")
            outputs = [
                "🔍 Analisis Risiko (detailed explanation)",
                "💬 Main Factors (faktor utama risiko)",
                "✅ Rekomendasi Aksi (actionable steps)",
                "🏷️ Strategi Diskon (pricing recommendation)",
                "📊 Saran Inventaris (inventory action)",
                "📈 Faktor Tambahan (contributing factors)"
            ]
            for out in outputs:
                st.write(f"• {out}")
    
    st.markdown("")
    
    # Key Features
    st.markdown("#### ⚡ Key Features")
    
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    
    with col_feat1:
        st.success("✅ JSON Response Parsing")
        st.caption("Structured output dalam format JSON")
    
    with col_feat2:
        st.info("⚡ Fast Response Time")
        st.caption("~2-5 detik per request")
    
    with col_feat3:
        st.warning("💰 Cost-Effective")
        st.caption("Flash model pricing terjangkau")
    
    st.markdown("")
    
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
    st.markdown("### Gemini API Setup & Configuration")
    
    # 1. API Key Info (Terpusat ke Sidebar)
    with st.container(border=True):
        col_api_info, col_api_status = st.columns([2, 1])
        
        with col_api_info:
            st.markdown("#### 🔑 API Key Status")
            st.info("💡 Pengaturan API Key sekarang dikelola secara terpusat melalui **Sidebar** di sebelah kiri layar untuk keamanan global.")
            
        with col_api_status:
            st.markdown("<br>", unsafe_allow_html=True) # Spacer sejajar
            if st.session_state.get("llm_api_key"):
                st.success("✅ Key Terdeteksi di Sidebar")
            else:
                st.warning("⚠️ Key Belum Diisi di Sidebar")
                
    st.markdown("")
    
    # 2. Test Connection Area (Fungsi Live Test)
    st.markdown("#### 🧪 Live Verification Test")
    with st.container(border=True):
        col_test_btn, col_test_status = st.columns([1, 2])
        
        with col_test_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔗 Run Live Connection Test", type="primary", use_container_width=True):
                with st.spinner("Menghubungkan ke server Google AI..."):
                    # Memanggil fungsi test_gemini_connection yang ada di bagian atas file
                    result = test_gemini_connection()
                    st.session_state.gemini_test_result = result
                    
                    # Update status global berdasarkan hasil test
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
                
    st.markdown("")
    
    # 3. Dynamic Connection Status Cards
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        with st.container(border=True):
            st.markdown("#### 🌐 Connection Status")
            status_now = st.session_state.gemini_connection_status
            
            if status_now == "Connected & Verified":
                st.success(status_now)
                st.caption("API Key valid & sukses terverifikasi")
            elif status_now == "Verification Failed":
                st.error(status_now)
                st.caption("Koneksi ditolak server Google AI")
            else:
                st.warning("Not Connected")
                st.caption("Koneksi belum diuji coba")
                
    with col_status2:
        with st.container(border=True):
            st.markdown("#### 🤖 Active Model")
            st.info("Gemini 2.5 Flash")
            st.caption("Varian optimal untuk kecepatan & kuota")
            
    with col_status3:
        with st.container(border=True):
            st.markdown("#### 📡 API Provider")
            st.info("Google AI")
            st.caption("google.generativeai SDK")
            
    st.markdown("")
    
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
    st.markdown("### 📝 System Prompt Documentation")
    st.caption("Prompt ini adalah instruksi inti yang mengatur bagaimana Gemini mengevaluasi prediksi dari model XGBoost. Halaman ini murni sebagai dokumentasi arsitektur AI (Read-Only).")
    
    st.markdown("")
    
    col_header, col_tip = st.columns([1, 1])
    with col_header:
        st.markdown("#### 💾 Core Instruction Template")
    with col_tip:
        st.markdown("""
        <div style='text-align: right; margin-top: 5px; opacity: 0.8;'>
            <small>💡 <b>Tip:</b> Arahkan kursor ke pojok kanan atas kotak kode untuk menyalin.</small>
        </div>
        """, unsafe_allow_html=True)
        
    # Menampilkan prompt statis dari fungsi
    st.code(get_system_prompt(), language="text")
    
    st.markdown("")
    
    # Tombol Download tetap dipertahankan untuk evaluator
    st.download_button(
        label="📥 Download Full Prompt Template (.txt)",
        data=get_system_prompt(),
        file_name="gemini_system_prompt_documentation.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")
    
    # Prompt Breakdown (Tidak diubah, tetap dipertahankan)
    with st.expander("🔍 Membedah Struktur Prompt", expanded=False):
        st.markdown("""
        ### Prompt Components:
        **1. Role Definition:** Defines AI as "Senior Retail Operations AI Advisor"
        **2. Task Description:** Clarity on input (product data + XGBoost predictions)
        **3. Quality Criteria:** Actionable, Data-driven, Specific, Profitable
        **4. Output Format Specification:** Struktur laporan 7 poin yang komprehensif.
        """)
# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: AI WORKFLOW
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 🏗️ System Architecture & Data Flow")
    st.caption("Alur kerja sistem terintegrasi dari input pengguna, prediksi XGBoost, hingga analisis oleh Gemini.")

    st.markdown("#### 🔄 Data Flow Pipeline")
    
    with st.container(border=True):
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="
                display: flex;
                justify-content: space-around;
                align-items: center;
                margin: 20px 0;
                font-size: 14px;
                font-weight: 600;
            ">
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">📋</div>
                    <div>User Input</div>
                    <div style="font-size: 11px; opacity: 0.6; margin-top: 4px;">
                        Kategori, Stok,<br/>Kadaluarsa, Diskon
                    </div>
                </div>
                <div style="font-size: 24px; opacity: 0.5;">→</div>
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">🤖</div>
                    <div>XGBoost Model</div>
                    <div style="font-size: 11px; opacity: 0.6; margin-top: 4px;">
                        ML Prediction<br/>Risk Score
                    </div>
                </div>
                <div style="font-size: 24px; opacity: 0.5;">→</div>
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">⚠️</div>
                    <div>Risk Analysis</div>
                    <div style="font-size: 11px; opacity: 0.6; margin-top: 4px;">
                        Probability &<br/>Risk Status
                    </div>
                </div>
                <div style="font-size: 24px; opacity: 0.5;">→</div>
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">✨</div>
                    <div>Gemini LLM</div>
                    <div style="font-size: 11px; opacity: 0.6; margin-top: 4px;">
                        Natural Language<br/>Analysis
                    </div>
                </div>
                <div style="font-size: 24px; opacity: 0.5;">→</div>
                <div style="flex: 1; text-align: center;">
                    <div style="font-size: 36px; margin-bottom: 8px;">💼</div>
                    <div>Recommendation</div>
                    <div style="font-size: 11px; opacity: 0.6; margin-top: 4px;">
                        Actionable<br/>Business Advice
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 🏗️ System Architecture Layers")
    col_arch1, col_arch2 = st.columns(2)
    
    with col_arch1:
        with st.container(border=True):
            st.markdown("##### 📊 Machine Learning Layer")
            st.markdown("""
            **Model**: XGBoost Regressor  
            **Purpose**: Predict food waste risk  
            **Inputs**: Product features, Storage conditions, Inventory metrics, Market factors  
            **Outputs**: Risk Probability (0-100%), Risk Status, Confidence Score
            """)
    
    with col_arch2:
        with st.container(border=True):
            st.markdown("##### 🤖 LLM Layer (Gemini)")
            st.markdown("""
            **Model**: Gemini 2.5 Flash  
            **Purpose**: Generate business recommendations  
            **Inputs**: ML predictions, Product context, Business constraints  
            **Outputs**: Risk narrative, Actionable recommendations, Discount strategies
            """)