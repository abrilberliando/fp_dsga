"""
Prediksi Risiko Food Waste
============================
Halaman untuk prediksi risiko pembusukan produk food waste.
UI/UX design dengan placeholder results (tanpa ML model atau Gemini API).
Fokus pada user experience dan interaksi flow.

Session State Usage:
- category, stock, expiry_days, discount (inputs)
- risk_probability, risk_status, ai_recommendation (dummy results)
"""

import streamlit as st

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(layout="wide")

# ─── Session State Initialization ─────────────────────────────────────────────
if "prediction_input" not in st.session_state:
    st.session_state.prediction_input = {
        "category": "Dairy",
        "stock": 100,
        "expiry_days": 5,
        "discount": 10.0
    }

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = {
        "risk_probability": None,
        "risk_status": None,
        "ai_recommendation": None
    }

if "prediction_triggered" not in st.session_state:
    st.session_state.prediction_triggered = False

# ─── Helper: Generate Dummy Prediction ─────────────────────────────────────────
def generate_dummy_prediction(category: str, stock: int, expiry_days: int, discount: float):
    """Generate placeholder prediction based on inputs."""
    # Simple logic untuk generate dummy risk score
    base_risk = 50.0
    
    # Risk increases dengan fewer days to expiry
    if expiry_days < 3:
        base_risk += 30
    elif expiry_days < 7:
        base_risk += 15
    else:
        base_risk -= 10
    
    # Risk increases dengan higher stock (potential waste)
    if stock > 500:
        base_risk += 20
    elif stock > 200:
        base_risk += 10
    
    # Risk decreases dengan higher discount
    if discount >= 20:
        base_risk -= 15
    elif discount >= 10:
        base_risk -= 5
    
    # Clamp to 0-100
    risk_probability = max(0, min(100, base_risk))
    
    # Determine risk status
    if risk_probability < 30:
        risk_status = "🟢 Risiko Rendah"
        status_color = "green"
    elif risk_probability < 60:
        risk_status = "🟡 Risiko Sedang"
        status_color = "orange"
    else:
        risk_status = "🔴 Risiko Tinggi"
        status_color = "red"
    
    # Generate placeholder AI recommendation
    ai_recommendation = {
        "risk_analysis": f"Produk kategori {category} memiliki stok {stock} unit dengan sisa waktu simpan {expiry_days} hari. Tingkat risiko pembusukan diperkirakan {risk_probability:.1f}% berdasarkan analisis data historis dan kondisi penyimpanan.",
        "actions": [
            "Prioritaskan penjualan dalam jadwal yang ditargetkan",
            f"Pertimbangkan diskon tambahan (current: {discount}%)",
            "Tempatkan produk di area promosi prominent",
            "Pantau pergerakan stok secara real-time",
            "Hindari restock produk serupa dalam periode ini"
        ]
    }
    
    return {
        "risk_probability": risk_probability,
        "risk_status": risk_status,
        "status_color": status_color,
        "ai_recommendation": ai_recommendation
    }


# ─── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 30px 10px;
    margin-bottom: 20px;
">
    <div style="font-size: 56px; margin-bottom: 12px;">🔮</div>
    <h1 style="
        margin: 0 0 8px 0;
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    ">Prediksi Risiko Food Waste</h1>
    <p style="
        margin: 8px 0 0 0;
        opacity: 0.7;
        font-size: 15px;
    ">Analisis risiko pembusukan produk berdasarkan data stok</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Main Layout: Form (left) + Results (right) ────────────────────────────────
col_form, col_results = st.columns([1, 1], gap="large")

# ══════════════════════════════════════════════════════════════════════════════
# COLUMN 1: FORM INPUT
# ══════════════════════════════════════════════════════════════════════════════
with col_form:
    with st.container(border=True):
        st.markdown("### 📋 Masukkan Data Produk")
        st.caption("Isi semua field untuk analisis risiko")
        
        st.markdown("")
        
        # Category Selection
        kategori = st.selectbox(
            "Kategori Produk",
            options=[
                "Dairy",
                "Bakery",
                "Meat",
                "Beverage",
                "Frozen Food",
                "Ready-to-Eat"
            ],
            index=0,
            help="Pilih kategori produk dari list",
            key="kategori_input"
        )
        
        st.markdown("")
        
        # Stock Input
        stok = st.number_input(
            "Jumlah Stok Saat Ini",
            min_value=0,
            max_value=100000,
            value=100,
            step=10,
            help="Jumlah unit produk yang tersedia di gudang/toko",
            key="stok_input"
        )
        
        st.markdown("")
        
        # Expiry Days Input
        sisa_hari = st.number_input(
            "Sisa Hari Menuju Kadaluarsa",
            min_value=0,
            max_value=365,
            value=5,
            step=1,
            help="Berapa hari lagi sampai produk kadaluarsa/tidak bisa dijual",
            key="expiry_input"
        )
        
        st.markdown("")
        
        # Discount Input
        diskon = st.slider(
            "Diskon Saat Ini (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=1.0,
            help="Persentase diskon yang sedang diterapkan pada produk",
            key="diskon_input"
        )
        
        st.markdown("")
        st.markdown("---")
        st.markdown("")
        
        # Predict Button
        btn_predict = st.button(
            "🔍 Prediksi Risiko",
            type="primary",
            use_container_width=True,
            key="predict_button"
        )
        
        if btn_predict:
            # Simpan input ke session state
            st.session_state.prediction_input = {
                "category": kategori,
                "stock": stok,
                "expiry_days": sisa_hari,
                "discount": diskon
            }
            
            # Generate dummy prediction
            result = generate_dummy_prediction(kategori, stok, sisa_hari, diskon)
            st.session_state.prediction_result = result
            st.session_state.prediction_triggered = True


# ══════════════════════════════════════════════════════════════════════════════
# COLUMN 2: RESULTS DISPLAY
# ══════════════════════════════════════════════════════════════════════════════
with col_results:
    if st.session_state.prediction_triggered and st.session_state.prediction_result["risk_probability"] is not None:
        result = st.session_state.prediction_result
        
        # ─── Result Header ───────────────────────────────────────────────────
        with st.container(border=True):
            st.markdown("### 📊 Hasil Prediksi")
            st.caption("Hasil analisis risiko pembusukan produk")
            
            st.markdown("")
            
            # Metrics
            col_metric1, col_metric2 = st.columns(2)
            
            with col_metric1:
                st.metric(
                    "Risk Probability",
                    f"{result['risk_probability']:.1f}%",
                    delta=None
                )
            
            with col_metric2:
                st.metric(
                    "Status Risiko",
                    ' '.join(result['risk_status'].split()[1:]),
                    delta=None
                )
        
        st.markdown("")
        
        # ─── AI Recommendation Card ──────────────────────────────────────────
        with st.container(border=True):
            # Header with badge
            col_title, col_badge = st.columns([1, 0.3])
            with col_title:
                st.markdown("### ✨ AI Recommendation")
            with col_badge:
                st.info("Prototype Mode", icon="🔧")
            
            st.caption("Rekomendasi berbasis analisis dummy (belum terintegrasi model ML)")
            
            st.markdown("")
            
            # Risk Analysis
            st.markdown("#### 🔍 Analisis Risiko")
            st.markdown(f"_{result['ai_recommendation']['risk_analysis']}_")
            
            st.markdown("")
            
            # Recommendations
            st.markdown("#### 💡 Rekomendasi Aksi")
            for i, action in enumerate(result['ai_recommendation']['actions'], 1):
                st.write(f"{i}. {action}")
        
        st.markdown("")
        
        # ─── Debug Info (Expandable) ─────────────────────────────────────────
        with st.expander("🔧 Debug Info - Session State"):
            st.json({
                "input": st.session_state.prediction_input,
                "result": {
                    "risk_probability": result['risk_probability'],
                    "risk_status": result['risk_status'],
                    "status_color": result['status_color']
                }
            })
    
    else:
        # ─── Initial State ───────────────────────────────────────────────────
        with st.container(border=True):
            st.markdown("""
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 400px;
                text-align: center;
                color: rgba(150,150,150,0.8);
            ">
                <div style="font-size: 64px; margin-bottom: 16px;">🎯</div>
                <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                    Siap untuk Prediksi
                </div>
                <div style="font-size: 13px; opacity: 0.7; max-width: 280px; line-height: 1.6;">
                    Isi form di sebelah kiri dan klik "Prediksi Risiko" untuk melihat hasil analisis risiko pembusukan produk.
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── Information Footer ───────────────────────────────────────────────────────
st.markdown("")
st.divider()

st.markdown("""
### ℹ️ Informasi

**🔮 Status Halaman**: Prototype UI/UX dengan hasil dummy (placeholder)

**📦 Tahap Berikutnya**:
1. Integrasi model XGBoost dari folder `models/`
2. Implementasi preprocessing fitur real-time
3. Koneksi ke Gemini API untuk AI Recommendation
4. Export hasil prediksi ke format laporan

**💾 Session State**:
- Input pengguna dan hasil prediksi disimpan dalam session state
- Data tersedia untuk halaman lain melalui `st.session_state`
- Reset otomatis setiap refresh browser

**🔗 Integrasi**:
- Data dari halaman ini akan digunakan di "🤖 AI Model & Gemini"
- Hasil akan ditampilkan lebih detail di "✨ AI Recommendation"
""")
