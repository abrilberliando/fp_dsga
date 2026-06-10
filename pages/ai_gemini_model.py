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
    """Return system prompt untuk Gemini."""
    return """Anda adalah Senior Retail Operations AI Advisor yang ahli dalam:
- Food Waste Prediction & Management
- Inventory Optimization
- Pricing Strategy
- Demand Forecasting

Tugasmu: Berdasarkan data produk dan hasil prediksi model XGBoost, berikan rekomendasi bisnis yang:
1. Actionable (dapat langsung dijalankan manager)
2. Data-driven (berbasis probabilitas risk dari model)
3. Specific (dengan angka, persentase, atau timeline)
4. Profitable (mempertimbangkan margin dan cost)

Format response HARUS dalam JSON dengan struktur:
{
    "risk_analysis": "penjelasan mendalam tentang risk yang diidentifikasi",
    "main_factors": ["faktor 1", "faktor 2", "faktor 3"],
    "recommended_actions": ["aksi 1", "aksi 2", "aksi 3"],
    "suggested_discount_strategy": "strategi diskon dengan alasan bisnis",
    "inventory_recommendation": "rekomendasi tindakan inventory"
}"""


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
    "🔄 AI Workflow & Simulation"
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
# TAB 3: CUSTOM PROMPT (Interactive Editor)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### System Prompt Configuration")
    st.caption("Prompt ini adalah 'otak' yang mengatur bagaimana Gemini berperilaku. Kamu bisa melihat atau masuk ke Mode Editor untuk mengubah persona AI.")
    
    st.markdown("")
    
    # 1. Inisialisasi Memori (Hanya berjalan sekali)
    if "prompt_edit_mode" not in st.session_state:
        st.session_state.prompt_edit_mode = False
    
    if "active_system_prompt" not in st.session_state:
        st.session_state.active_system_prompt = get_system_prompt()

    # 2. Logika Mode Tampilan
    if not st.session_state.prompt_edit_mode:
        # ==========================================
        # VIEW MODE (Mode Baca)
        # ==========================================
        col_header, col_tip = st.columns([1, 1])
        with col_header:
            st.markdown("#### 💾 Current System Prompt")
        with col_tip:
            st.markdown("""
            <div style='text-align: right; margin-top: 5px; opacity: 0.8;'>
                <small>💡 <b>Tip:</b> Arahkan kursor ke pojok kanan atas kotak kode untuk menyalin.</small>
            </div>
            """, unsafe_allow_html=True)
            
        # Menampilkan prompt yang sedang aktif
        st.code(st.session_state.active_system_prompt, language="text")
        
        st.markdown("")
        st.markdown("#### 📋 Actions")
        
        col_action1, col_action2 = st.columns(2)
        with col_action1:
            # Tombol untuk masuk ke mode edit
            if st.button("✏️ Masuk Mode Editor", type="primary", use_container_width=True):
                st.session_state.prompt_edit_mode = True
                st.rerun() # Refresh layar langsung
                
        with col_action2:
            st.download_button(
                label="📥 Download Prompt as .txt",
                data=st.session_state.active_system_prompt,
                file_name="gemini_system_prompt.txt",
                mime="text/plain",
                use_container_width=True
            )
            
    else:
        # ==========================================
        # EDIT MODE (Mode Edit)
        # ==========================================
        st.markdown("#### 📝 Editor Mode")
        st.info("⚠️ **Perhatian:** Jangan menghapus bagian instruksi format JSON di bagian bawah prompt agar aplikasi tidak error.")
        
        # Kotak teks yang bisa diedit
        edited_text = st.text_area(
            "Edit System Prompt:", 
            value=st.session_state.active_system_prompt, 
            height=400,
            label_visibility="collapsed"
        )
        
        st.markdown("")
        
        # Deretan Tombol Kontrol Editor idemu
        col_edit1, col_edit2, col_edit3 = st.columns(3)
        
        with col_edit1:
            if st.button("💾 Simpan Perubahan", type="primary", use_container_width=True):
                st.session_state.active_system_prompt = edited_text
                st.session_state.prompt_edit_mode = False
                st.rerun()
                
        with col_edit2:
            if st.button("🔄 Reset ke Awal", use_container_width=True):
                # Kembalikan ke fungsi get_system_prompt() bawaan
                st.session_state.active_system_prompt = get_system_prompt()
                st.session_state.prompt_edit_mode = False
                st.rerun()
                
        with col_edit3:
            if st.button("❌ Keluar (Tanpa Simpan)", use_container_width=True):
                st.session_state.prompt_edit_mode = False
                st.rerun()

    st.markdown("---")
    
    # Prompt Breakdown
    with st.expander("🔍 Membedah Struktur Prompt", expanded=False):
        st.markdown("""
        ### Prompt Components:
        **1. Role Definition:** Defines AI as "Senior Retail Operations AI Advisor"
        **2. Task Description:** Clarity on input (product data + XGBoost predictions)
        **3. Quality Criteria:** Actionable, Data-driven, Specific, Profitable
        **4. Output Format Specification:** Wajib menggunakan format JSON terstruktur.
        """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: AI WORKFLOW & SIMULATION
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 🧪 Live AI Playground")
    st.caption("Gunakan area ini untuk mensimulasikan bagaimana Gemini mengolah data produk dan hasil prediksi XGBoost menjadi rekomendasi strategi retail.")

    # Bagian 1: Input Simulasi (Dummy Data)
    with st.container(border=True):
        st.markdown("#### 📥 Step 1: Input Simulation Data")
        col_in1, col_in2, col_in3 = st.columns(3)
        
        with col_in1:
            sim_kategori = st.selectbox("Kategori Produk", ["Dairy", "Buah & Sayur", "Daging", "Frozen Food", "Bakery"])
            sim_stok = st.number_input("Jumlah Stok (Unit)", min_value=0, value=150)
            
        with col_in2:
            sim_sisa_hari = st.slider("Sisa Hari Kadaluarsa", 0, 30, 3)
            sim_diskon = st.slider("Diskon Saat Ini (%)", 0, 90, 10)
            
        with col_in3:
            sim_risk_prob = st.slider("XGBoost Risk Probability (%)", 0, 100, 85)
            sim_risk_status = st.select_slider("XGBoost Risk Status", options=["LOW", "MEDIUM", "HIGH", "CRITICAL"], value="HIGH")

    st.markdown("")

    # Bagian 2: Tombol Eksekusi
    col_play_spacer, col_play_btn = st.columns([3, 1])
    with col_play_btn:
        generate_test = st.button("🔮 Generate AI Analysis", type="primary", use_container_width=True)

    # Bagian 3: Logika Pemanggilan API
    if generate_test:
        if not st.session_state.get("llm_api_key"):
            st.error("❌ API Key belum diisi di Sidebar!")
        else:
            with st.spinner("Gemini sedang menganalisis data simulasi..."):
                try:
                    active_prompt = st.session_state.get("active_system_prompt", get_system_prompt())
                    
                    user_msg = f"""
                    DATA PRODUK SIMULASI:
                    - Kategori: {sim_kategori}
                    - Stok: {sim_stok} unit
                    - Sisa Hari: {sim_sisa_hari} hari
                    - Diskon: {sim_diskon}%
                    
                    HASIL PREDIKSI XGBOOST:
                    - Risk Probability: {sim_risk_prob}%
                    - Status: {sim_risk_status}
                    """
                    
                    genai.configure(api_key=st.session_state.llm_api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(f"{active_prompt}\n\n{user_msg}")
                    
                    st.markdown("---")
                    st.markdown("### 💼 AI Strategic Recommendation")
                    
                    try:
                        import json
                        raw_text = response.text
                        start_idx = raw_text.find('{')
                        end_idx = raw_text.rfind('}') + 1
                        
                        if start_idx != -1 and end_idx > start_idx:
                            json_str = raw_text[start_idx:end_idx]
                            res_json = json.loads(json_str)
                        else:
                            raise ValueError("Format JSON tidak ditemukan di dalam teks")
                        
                        st.success(f"**Analisis Risiko:** {res_json.get('risk_analysis', 'N/A')}")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            with st.container(border=True):
                                st.markdown("##### ⚙️ Faktor Utama")
                                for f in res_json.get('main_factors', []):
                                    st.write(f"- {f}")
                        with c2:
                            with st.container(border=True):
                                st.markdown("##### 📦 Rekomendasi Inventory")
                                st.info(res_json.get('inventory_recommendation', 'N/A'))
                        
                        with st.container(border=True):
                            st.markdown("##### ✅ Aksi Strategis")
                            for a in res_json.get('recommended_actions', []):
                                st.write(f"- {a}")
                                
                        st.warning(f"**Strategi Harga:** {res_json.get('suggested_discount_strategy', 'N/A')}")
                        
                    except:
                        st.write(response.text)
                        
                except Exception as e:
                    st.error(f"Gagal generate rekomendasi: {e}")

    st.markdown("---")
    
    # Bagian 4: Arsitektur (Dikembalikan dari kode aslimu yang sangat bagus)
    with st.expander("🏗️ View System Architecture & Data Flow", expanded=False):
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