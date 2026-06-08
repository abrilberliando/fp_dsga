"""
AI Recommendation Assistant
=============================
Halaman untuk mengintegrasikan XGBoost Food Waste Prediction dengan Gemini API.
Menghasilkan rekomendasi bisnis yang dapat ditindaklanjuti oleh manager retail.

Architecture:
- Tab 1: AI Recommendation (Generate AI insights)
- Tab 2: Prediction Context (Data & results display)
- Tab 3: Prompt Logic (System prompt documentation)
- Tab 4: Chat Assistant (Conversational AI)
"""

import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(layout="wide")

# ─── Session State Initialization ─────────────────────────────────────────────
if "product_input" not in st.session_state:
    st.session_state.product_input = {}

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = {}

if "ai_recommendation" not in st.session_state:
    st.session_state.ai_recommendation = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "gemini_configured" not in st.session_state:
    st.session_state.gemini_configured = False

# ─── Helper Functions ─────────────────────────────────────────────────────────

def configure_gemini_api():
    """Konfigurasi Gemini API dari session state (API key dari sidebar)."""
    api_key = st.session_state.get("llm_api_key", "")
    if not api_key:
        return False
    try:
        genai.configure(api_key=api_key)
        st.session_state.gemini_configured = True
        return True
    except Exception as e:
        st.error(f"❌ Gagal konfigurasi Gemini: {e}")
        return False


def generate_system_prompt():
    """Generate system prompt untuk Gemini."""
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
    "inventory_recommendation": "rekomendasi tindakan inventory (contoh: increase stock, reduce stock, promote, dll)"
}"""


def call_gemini_api(prompt_text: str) -> str:
    """Panggil Gemini API dengan prompt."""
    if not st.session_state.gemini_configured:
        if not configure_gemini_api():
            return "❌ API Key tidak dikonfigurasi. Silakan isi API Key di sidebar."
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"❌ Error memanggil Gemini: {str(e)}"


def generate_ai_recommendation(product_data: dict, prediction_data: dict) -> dict:
    """Generate AI recommendation menggunakan Gemini."""
    
    system_prompt = generate_system_prompt()
    
    user_prompt = f"""
Berikut adalah data produk dan hasil prediksi model:

PRODUCT DATA:
- Kategori: {product_data.get('kategori', '-')}
- Jumlah Stok: {product_data.get('stok', 0)} unit
- Hari Hingga Kadaluarsa: {product_data.get('sisa_hari', 0)} hari
- Diskon Saat Ini: {product_data.get('diskon', 0)}%

PREDICTION RESULT:
- Risk Probability: {prediction_data.get('risk_probability', 0):.2f}%
- Risk Status: {prediction_data.get('risk_status', 'UNKNOWN')}
- Confidence Score: {prediction_data.get('confidence', 0):.2f}%

Berikan rekomendasi bisnis yang detail dan actionable dalam format JSON."""

    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    response_text = call_gemini_api(full_prompt)
    
    # Parse response
    try:
        import json
        # Extract JSON dari response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)
            return result
    except:
        pass
    
    return {
        "risk_analysis": response_text,
        "main_factors": [],
        "recommended_actions": [],
        "suggested_discount_strategy": "-",
        "inventory_recommendation": "-"
    }


def render_recommendation_card(recommendation: dict):
    """Render AI recommendation dalam card format."""
    if not recommendation:
        st.info("📌 Belum ada rekomendasi. Klik tombol 'Generate AI Recommendation' di atas.")
        return
    
    # Risk Analysis
    with st.container(border=True):
        st.markdown("#### 🔍 Risk Analysis")
        st.markdown(recommendation.get('risk_analysis', '-'))
    
    # Main Factors
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("#### ⚙️ Main Factors")
            factors = recommendation.get('main_factors', [])
            if factors:
                for i, factor in enumerate(factors, 1):
                    st.write(f"{i}. {factor}")
            else:
                st.caption("Tidak ada faktor utama")
    
    # Inventory Recommendation
    with col2:
        with st.container(border=True):
            st.markdown("#### 📦 Inventory Recommendation")
            st.info(recommendation.get('inventory_recommendation', '-'), icon="📌")
    
    # Recommended Actions
    with st.container(border=True):
        st.markdown("#### ✅ Recommended Actions")
        actions = recommendation.get('recommended_actions', [])
        if actions:
            for i, action in enumerate(actions, 1):
                st.write(f"{i}. {action}")
        else:
            st.caption("Tidak ada rekomendasi aksi")
    
    # Discount Strategy
    with st.container(border=True):
        st.markdown("#### 💰 Suggested Discount Strategy")
        st.success(recommendation.get('suggested_discount_strategy', '-'), icon="💡")


# ─── Page Title ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 20px 10px;
">
    <div style="font-size: 48px;">🤖</div>
    <h1 style="margin:8px 0 4px 0; font-size:32px;">AI Recommendation Assistant</h1>
    <p style="margin:0; opacity:0.6; font-size:14px;">
        Integrasi XGBoost Prediction + Gemini API untuk rekomendasi bisnis retail
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Check API Key Configuration ──────────────────────────────────────────────
if not st.session_state.get("llm_api_key"):
    st.warning(
        "⚠️ **API Key Belum Dikonfigurasi**  \n"
        "Silakan isi LLM API Key di sidebar untuk mengaktifkan fitur AI Recommendation.",
        icon="🔑"
    )
else:
    configure_gemini_api()
    if st.session_state.gemini_configured:
        st.success("✅ Gemini API siap digunakan", icon="✨")

st.markdown("")

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 AI Recommendation",
    "📊 Prediction Context",
    "📋 Prompt Logic",
    "💬 Chat Assistant"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: AI RECOMMENDATION
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### AI-Powered Business Recommendation")
    
    # Dummy data untuk demo (dalam production, ini akan dari form prediksi.py)
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.metric("Risk Probability", "45%", delta="-5%")
    with col_info2:
        st.metric("Risk Status", "⚠️ MEDIUM")
    with col_info3:
        st.metric("Product", "Dairy")
    
    st.markdown("")
    
    # Product Information
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        st.info(f"📦 Stock: 100 unit", icon="📊")
    with col_p2:
        st.info(f"📅 Days to Expiry: 5 days", icon="⏰")
    with col_p3:
        st.info(f"💰 Discount: 10%", icon="🏷️")
    with col_p4:
        st.info(f"✨ Confidence: 78%", icon="🎯")
    
    st.markdown("")
    
    # Generate Button
    col_btn_spacer, col_btn = st.columns([3, 1])
    with col_btn:
        generate_btn = st.button(
            "🔮 Generate AI Recommendation",
            type="primary",
            use_container_width=True
        )
    
    if generate_btn:
        with st.spinner("🔄 Menghasilkan rekomendasi dari Gemini..."):
            # Demo data (dalam production, ambil dari session state)
            product_data = {
                'kategori': 'Dairy',
                'stok': 100,
                'sisa_hari': 5,
                'diskon': 10
            }
            prediction_data = {
                'risk_probability': 45.0,
                'risk_status': 'MEDIUM',
                'confidence': 78.0
            }
            
            recommendation = generate_ai_recommendation(product_data, prediction_data)
            st.session_state.ai_recommendation = recommendation
    
    st.markdown("")
    
    # Display Recommendation
    st.markdown("---")
    render_recommendation_card(st.session_state.ai_recommendation)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: PREDICTION CONTEXT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Prediction Data & Results")
    
    col_ctx1, col_ctx2 = st.columns(2)
    
    with col_ctx1:
        st.markdown("#### 📥 Input Data")
        with st.container(border=True):
            st.metric("Product Category", "Dairy")
            st.metric("Stock Quantity", "100 unit")
            st.metric("Days Until Expiry", "5 days")
            st.metric("Current Discount", "10%")
    
    with col_ctx2:
        st.markdown("#### 📤 Prediction Results")
        with st.container(border=True):
            st.metric("Risk Probability", "45%")
            st.metric("Risk Status", "⚠️ MEDIUM")
            st.metric("Confidence Score", "78%")
            st.metric("Predicted Waste", "~22.5 units")
    
    st.markdown("")
    
    # Session State Display
    st.markdown("#### 💾 Session State Data")
    col_state1, col_state2 = st.columns(2)
    
    with col_state1:
        st.info("**Product Input**", icon="📦")
        if st.session_state.product_input:
            st.json(st.session_state.product_input)
        else:
            st.caption("Kosong (data dari prediksi.py)")
    
    with col_state2:
        st.success("**Prediction Result**", icon="🎯")
        if st.session_state.prediction_result:
            st.json(st.session_state.prediction_result)
        else:
            st.caption("Kosong (data dari prediksi.py)")
    
    st.markdown("")
    
    if st.session_state.ai_recommendation:
        st.warning("**AI Recommendation Generated**", icon="🤖")
        st.json(st.session_state.ai_recommendation)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: PROMPT LOGIC
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### System Prompt & Workflow Logic")
    
    st.markdown("#### 🔧 System Prompt")
    system_prompt = generate_system_prompt()
    with st.container(border=True):
        st.code(system_prompt, language="text")
    
    st.markdown("")
    
    st.markdown("#### 📥 Input Variables")
    input_vars = {
        "kategori_produk": "Product category (e.g., Dairy, Fruits, Vegetables)",
        "jumlah_stok": "Current stock quantity in units",
        "sisa_hari_kadaluarsa": "Days until product expiry",
        "diskon_persen": "Current discount percentage",
        "risk_probability": "ML model predicted risk (0-100%)",
        "risk_status": "Risk level classification (LOW, MEDIUM, HIGH, CRITICAL)"
    }
    
    for var, desc in input_vars.items():
        st.write(f"- **{var}**: {desc}")
    
    st.markdown("")
    
    st.markdown("#### 📤 Output Structure")
    output_structure = {
        "risk_analysis": "Detailed explanation of identified risks",
        "main_factors": ["Factor 1", "Factor 2", "Factor 3"],
        "recommended_actions": ["Action 1", "Action 2", "Action 3"],
        "suggested_discount_strategy": "Specific discount strategy with justification",
        "inventory_recommendation": "Specific inventory action recommendation"
    }
    st.json(output_structure)
    
    st.markdown("")
    
    st.markdown("#### 🔄 Workflow")
    st.markdown("""
    1. **User Input** → Fill form di `prediksi.py` (kategori, stok, hari kadaluarsa, diskon)
    2. **ML Prediction** → XGBoost model prediksi risk probability & status
    3. **Data Combination** → Gabungkan input + hasil prediksi
    4. **Gemini API Call** → Kirim ke Gemini dengan system prompt
    5. **JSON Parsing** → Extract dan parse response JSON
    6. **Display Results** → Tampilkan rekomendasi dalam UI cards
    7. **Chat Context** → Simpan untuk referensi di chat assistant
    """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: CHAT ASSISTANT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 💬 Conversational AI Assistant")
    
    st.info(
        "🤖 Chat dengan AI Assistant tentang: Food Waste, Inventory Management, Retail Operations, Prediction Interpretation",
        icon="💡"
    )
    
    # Display chat history
    st.markdown("#### Chat History")
    
    chat_container = st.container(border=True, height=400)
    
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"], avatar=message.get("avatar")):
                    st.markdown(message["content"])
        else:
            st.caption("💬 Mulai percakapan dengan AI Assistant...")
            st.markdown("""
            **Apa yang bisa aku bantu?**
            - Jelaskan prediksi risiko untuk produk ini
            - Apa strategi diskon yang disarankan?
            - Bagaimana cara mengurangi food waste?
            - Rekomendasi inventory apa untuk produk ini?
            """)
    
    st.markdown("")
    
    # Chat input
    user_input = st.chat_input(
        "Ketik pertanyaan atau pesan...",
        key="chat_input"
    )
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "avatar": "👤"
        })
        
        # Generate AI response
        with st.spinner("🔄 AI sedang memikirkan jawaban..."):
            # Create context from recommendation and prediction
            context_msg = f"""
User meminta: {user_input}

Konteks dari rekomendasi sebelumnya:
- Risk Analysis: {st.session_state.ai_recommendation.get('risk_analysis', 'Tidak ada')}
- Recommended Actions: {st.session_state.ai_recommendation.get('recommended_actions', [])}

Berikan jawaban yang fokus pada Food Waste Management, Inventory Optimization, Retail Operations, atau Prediction Interpretation.
Jawab dalam bahasa Indonesia, singkat dan jelas (max 3 paragraf).
            """
            
            response_text = call_gemini_api(context_msg)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response_text,
                "avatar": "🤖"
            })
        
        # Rerun untuk update chat
        st.rerun()
    
    st.markdown("")
    
    # Clear chat history button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
