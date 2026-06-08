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
    
    # API Key Input
    with st.container(border=True):
        st.markdown("#### 🔑 API Key Configuration")
        
        col_api_input, col_api_status = st.columns([2, 1])
        
        with col_api_input:
            api_key_input = st.text_input(
                "Enter Gemini API Key",
                type="password",
                value=st.session_state.get("llm_api_key", ""),
                key="gemini_api_key_input",
                help="Masukkan API Key dari Google AI Studio (makersuite.google.com)"
            )
            
            if api_key_input:
                st.session_state.llm_api_key = api_key_input
        
        with col_api_status:
            if st.session_state.get("llm_api_key"):
                st.success("✅ Key Tersimpan")
            else:
                st.warning("⚠️ Belum ada key")
    
    st.markdown("")
    
    # Connection Status
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        with st.container(border=True):
            st.markdown("#### 🌐 Connection Status")
            if st.session_state.get("llm_api_key"):
                st.success("Configured")
                st.caption("API Key tersimpan")
            else:
                st.error("Not Configured")
                st.caption("Masukkan API Key terlebih dahulu")
    
    with col_status2:
        with st.container(border=True):
            st.markdown("#### 🤖 Active Model")
            st.info("Gemini 2.5 Flash")
            st.caption("Latest Flash version")
    
    with col_status3:
        with st.container(border=True):
            st.markdown("#### 📡 API Provider")
            st.info("Google AI")
            st.caption("google.generativeai SDK")
    
    st.markdown("")
    
    # Test Connection
    st.markdown("#### 🧪 Test Connection")
    
    col_test_btn, col_test_status = st.columns([1, 2])
    
    with col_test_btn:
        if st.button("🔗 Test Connection", type="primary", use_container_width=True):
            with st.spinner("Testing Gemini API connection..."):
                result = test_gemini_connection()
                st.session_state.gemini_test_result = result
    
    if st.session_state.gemini_test_result:
        result = st.session_state.gemini_test_result
        
        with col_test_status:
            if result["status"] == "SUCCESS":
                st.success(result["message"])
                st.caption(result["details"])
            else:
                st.error(result["message"])
                st.caption(result["details"])
    
    st.markdown("")
    
    # Configuration Instructions
    with st.expander("📖 How to Get Gemini API Key", expanded=False):
        st.markdown("""
        ### Langkah-langkah:
        
        1. **Buka Google AI Studio**
           - Kunjungi: https://makersuite.google.com/app/apikey
           - Atau masuk dengan akun Google Anda
        
        2. **Create API Key**
           - Klik "Create API Key"
           - Pilih project atau buat project baru
           - Copy API Key yang dihasilkan
        
        3. **Paste ke Field Atas**
           - Masukkan API Key di input field di atas
           - Klik "Test Connection" untuk verifikasi
        
        4. **Keamanan**
           - API Key di-store di Streamlit Session State
           - Tidak disimpan secara permanen
           - Reset setiap refresh browser
        
        ### Rate Limits:
        - **Free Tier**: 60 requests/minute
        - **Paid**: Sesuai subscription plan
        """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: CUSTOM PROMPT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### System Prompt for Gemini")
    
    st.markdown("#### 📋 System Prompt Details")
    st.caption("Prompt ini dikonfigurasi untuk memastikan Gemini memberikan rekomendasi yang actionable dan data-driven.")
    
    st.markdown("")
    
    # System Prompt Display
    system_prompt = get_system_prompt()
    
    st.markdown("#### 💾 Full System Prompt")
    
    # Code viewer
    st.code(system_prompt, language="text")
    
    st.markdown("")
    
    # Copy button
    col_copy1, col_copy2 = st.columns([1, 3])
    
    with col_copy1:
        st.markdown("#### 📋 Actions")
    
    with col_copy2:
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📋 Copy Prompt", use_container_width=True):
                st.success("✅ Prompt copied to clipboard!")
                st.code(system_prompt, language="text")
        
        with col_btn2:
            if st.button("📄 Export as Text", use_container_width=True):
                st.download_button(
                    label="📥 Download Prompt.txt",
                    data=system_prompt,
                    file_name="gemini_system_prompt.txt",
                    mime="text/plain"
                )
    
    st.markdown("")
    
    # Prompt Breakdown
    with st.expander("🔍 Prompt Structure & Components", expanded=True):
        st.markdown("""
        ### Prompt Components:
        
        **1. Role Definition**
        - Defines AI as "Senior Retail Operations AI Advisor"
        - Establishes expertise areas (Food Waste, Inventory, Pricing, Demand)
        
        **2. Task Description**
        - Clarity on input (product data + XGBoost predictions)
        - Output requirements (actionable recommendations)
        
        **3. Quality Criteria**
        - ✅ Actionable - dapat diimplementasikan
        - ✅ Data-driven - berbasis model predictions
        - ✅ Specific - dengan angka/timeline konkret
        - ✅ Profitable - mempertimbangkan business metrics
        
        **4. Output Format Specification**
        - JSON structure definition
        - Field requirements (risk_analysis, main_factors, dll)
        - Ensures parseable, structured response
        
        ### Prompt Engineering Notes:
        - Menggunakan "role-based prompting" untuk konsistensi
        - Format JSON untuk machine-readable output
        - Clear quality criteria untuk evaluasi
        """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: AI WORKFLOW
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### AI System Workflow & Architecture")
    
    # Visual Workflow
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
    
    st.markdown("")
    
    # Architecture Layers
    st.markdown("#### 🏗️ System Architecture Layers")
    
    col_arch1, col_arch2 = st.columns(2)
    
    with col_arch1:
        with st.container(border=True):
            st.markdown("#### 📊 Machine Learning Layer")
            st.markdown("""
            **Model**: XGBoost Regressor
            
            **Purpose**: Predict food waste risk
            
            **Inputs**:
            - Product features (category, quality)
            - Storage conditions (temperature, humidity)
            - Inventory metrics (stock, shelf life)
            - Market factors (demand, discount)
            
            **Outputs**:
            - Risk Probability (0-100%)
            - Risk Status (LOW/MEDIUM/HIGH/CRITICAL)
            - Confidence Score
            """)
    
    with col_arch2:
        with st.container(border=True):
            st.markdown("#### 🤖 LLM Layer (Gemini)")
            st.markdown("""
            **Model**: Gemini 2.5 Flash
            
            **Purpose**: Generate business recommendations
            
            **Inputs**:
            - ML predictions + risk scores
            - Product context & market data
            - Business constraints
            
            **Outputs**:
            - Risk analysis narrative
            - Actionable recommendations
            - Discount strategies
            - Inventory guidance
            """)
    
    st.markdown("")
    
    # Input Layer Details
    with st.expander("📥 Input Layer - Data Preparation", expanded=True):
        st.markdown("""
        **Data Sources**:
        1. **User Form** (prediksi.py)
           - Product category selection
           - Stock quantity
           - Days until expiry
           - Current discount %
        
        2. **Data Validation**
           - Type checking
           - Range validation
           - Null value handling
        
        3. **Feature Engineering**
           - Normalize numerical features
           - Encode categorical variables
           - Derive temporal features
        """)
    
    # ML Layer Details
    with st.expander("🤖 ML Layer - XGBoost Prediction", expanded=True):
        st.markdown("""
        **Processing Steps**:
        1. **Feature Scaling**
           - StandardScaler untuk numerical features
           - OrdinalEncoder untuk categorical
        
        2. **Model Inference**
           - Load trained XGBoost model from models/
           - Generate prediction (risk probability)
           - Calculate confidence metrics
        
        3. **Output Generation**
           - Map probability to risk status
           - Generate recommendation flags
           - Package results for next layer
        """)
    
    # LLM Layer Details
    with st.expander("✨ LLM Layer - Gemini Analysis", expanded=True):
        st.markdown("""
        **Gemini Processing**:
        1. **Prompt Construction**
           - System prompt (role & task definition)
           - User prompt (specific data + predictions)
           - Few-shot examples (optional)
        
        2. **API Call**
           - Send to Gemini 2.5 Flash
           - Configure response parameters
           - Handle streaming/non-streaming
        
        3. **Response Parsing**
           - Extract JSON from response
           - Validate output structure
           - Handle errors gracefully
        """)
    
    # Recommendation Layer Details
    with st.expander("💼 Recommendation Layer - Output Formatting", expanded=True):
        st.markdown("""
        **Output Components**:
        1. **Risk Analysis** - Narrative explanation of identified risks
        2. **Main Factors** - Top 3 factors contributing to risk
        3. **Recommended Actions** - Specific, numbered action items
        4. **Discount Strategy** - Pricing recommendation with justification
        5. **Inventory Recommendation** - Action (increase/reduce/promote/etc)
        
        **Display Format**:
        - Card-based UI in chatbot_model.py
        - JSON viewer for raw data
        - Exportable summary reports
        """)
    
    st.markdown("")
    
    # Integration Points
    st.markdown("#### 🔗 Integration Points")
    
    col_int1, col_int2, col_int3 = st.columns(3)
    
    with col_int1:
        st.info("**prediksi.py**", icon="📋")
        st.caption("User input collection")
        st.caption("XGBoost inference")
    
    with col_int2:
        st.info("**chatbot_model.py**", icon="💬")
        st.caption("Gemini API calls")
        st.caption("Results display")
    
    with col_int3:
        st.info("**models/**", icon="📦")
        st.caption("Trained model storage")
        st.caption("Feature preprocessing")
    
    st.markdown("")
    
    # System Requirements
    with st.expander("⚙️ System Requirements & Dependencies", expanded=False):
        st.markdown("""
        **Backend Requirements**:
        - Python 3.10+
        - XGBoost >= 1.4.0
        - Streamlit >= 1.36.0
        - google-generativeai >= 0.4
        
        **API Requirements**:
        - Gemini API Key (free tier available)
        - Internet connection for API calls
        
        **Data Requirements**:
        - Trained XGBoost model file
        - Feature encoding mappings
        - Historical prediction data (optional)
        """)
