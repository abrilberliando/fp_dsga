"""
AI Assistant & Gemini Documentation

Halaman AI Assistant (Retail Manager) dan dokumentasi Gemini (Stakeholder Teknis).

Tabs:
- Tab 1: Chat Assistant      
- Tab 2: Gemini Overview     
- Tab 3: API Configuration  
- Tab 4: Custom Prompt       
- Tab 5: AI Workflow         
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

# Konfigurasi Gemini jika API key sudah ada
if st.session_state.get("llm_api_key"):
    configure_gemini()

#Role check 
is_retail = "Retail Manager" in st.session_state.get("user_role", "Retail Manager")

#Tabs 
# Retail Manager: Chat tab tampil pertama (paling relevan)
# Stakeholder Teknis: urutan teknis lebih natural
if is_retail:
    tab_chat, tab_ov, tab_cfg, tab_prompt, tab_wf = st.tabs([
        "💬 Chat Assistant",
        "🔍 Gemini Overview",
        "⚙️ API Configuration",
        "📝 Custom Prompt",
        "🔄 AI Workflow",
    ])
else:
    tab_ov, tab_cfg, tab_prompt, tab_wf, tab_chat = st.tabs([
        "🔍 Gemini Overview",
        "⚙️ API Configuration",
        "📝 Custom Prompt",
        "🔄 AI Workflow",
        "💬 Chat Assistant",
    ])

# TAB CHAT ASSISTANT
with tab_chat:
    section_header("💬 Chat dengan AI Assistant")

    #Konteks dari prediksi.py 
    ctx = st.session_state.get("prediction_context")

    if ctx:
        risk_color = (
            C["green"] if ctx["risk_level"] == "AMAN"
            else C["orange"] if ctx["risk_level"] == "WASPADA"
            else C["red"]
        )
        st.markdown(f"""
<div class="ibox green" style="margin-bottom:1rem;">
    <b>📦 Konteks Aktif dari Prediksi Terakhir</b><br>
    <div style="display:flex; gap:1.5rem; margin-top:.5rem; flex-wrap:wrap;">
        <span>Produk: <b>{ctx['product_type']}</b></span>
        <span>Risiko: <b style="color:{risk_color};">{ctx['risk_level']}</b>
              ({ctx['risk_probability']}%)</span>
        <span>Kadaluarsa: <b>{ctx['days_until_expiry']} hari</b></span>
        <span>Penyimpanan: <b>{ctx['storage_condition']}</b></span>
    </div>
    <div style="font-size:.7rem; color:{C['muted']}; margin-top:.4rem;">
        Dianalisis pada {ctx.get('timestamp','—')}
    </div>
</div>
""", unsafe_allow_html=True)

        # Suggested questions berdasarkan risk level
        st.markdown(f'<div style="font-size:.78rem; color:{C["muted"]}; margin-bottom:.4rem;"><b>Pertanyaan cepat:</b></div>', unsafe_allow_html=True)
        sq_col1, sq_col2, sq_col3 = st.columns(3)
        if ctx["risk_level"] == "AMAN":
            sq = ["Bagaimana cara mempertahankan kualitas produk ini?",
                  "Kapan waktu yang tepat mulai memantau ulang?",
                  "Tips rotasi stok FIFO yang efektif?"]
        elif ctx["risk_level"] == "WASPADA":
            sq = [f"Diskon berapa % yang disarankan untuk {ctx['product_type']}?",
                  "Apa langkah pertama yang harus saya lakukan sekarang?",
                  "Bagaimana cara memperlambat proses pembusukan?"]
        else:
            sq = [f"Tindakan paling cepat untuk {ctx['product_type']} risiko tinggi?",
                  "Bagaimana strategi flash sale yang efektif?",
                  "Apakah produk ini masih layak dijual atau harus dibuang?"]

        for idx, question in enumerate(sq):
            col = [sq_col1, sq_col2, sq_col3][idx]
            with col:
                if st.button(question, key=f"sq_{question[:20]}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    with st.spinner("🤔 AI sedang menjawab..."):
                        context_str = (
                            f"Produk: {ctx['product_type']}, "
                            f"Risiko: {ctx['risk_level']} ({ctx['risk_probability']}%), "
                            f"Sisa {ctx['days_until_expiry']} hari kadaluarsa, "
                            f"Penyimpanan: {ctx['storage_condition']}"
                        )
                        full_prompt = (
                            f"Konteks produk retail:\n{context_str}\n\n"
                            f"Pertanyaan: {question}\n\n"
                            f"Jawab dalam Bahasa Indonesia, singkat dan actionable (maks 3 paragraf)."
                        )
                        answer = call_gemini(full_prompt)
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.rerun()
    else:
        st.markdown(f"""
<div class="ibox orange" style="text-align:center; padding:1.5rem;">
    <div style="font-size:1.8rem; margin-bottom:.5rem;">🔮</div>
    <b>Belum Ada Konteks Prediksi</b><br>
    <span style="font-size:.82rem; color:{C['muted']};">
        Buka halaman <b>Prediksi Risiko</b> dan jalankan analisis produk terlebih dahulu.<br>
        Konteks produk akan otomatis tersedia di sini.
    </span>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    #API Key check 
    if not st.session_state.get("llm_api_key"):
        st.markdown(f"""
<div class="ibox orange">
    <b>API Key belum dikonfigurasi.</b>
    Isi <b>Gemini API Key</b> di sidebar untuk mengaktifkan Chat Assistant.
</div>
""", unsafe_allow_html=True)
    else:
        #Chat history display
        chat_box = st.container(height=420, border=False)
        with chat_box:
            if st.session_state.chat_history:
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
                        st.markdown(msg["content"])
            else:
                st.markdown(f"""
<div style="text-align:center; padding:2rem; color:{C['muted']};">
    <div style="font-size:2rem; margin-bottom:.5rem;">💬</div>
    Mulai percakapan dengan AI Assistant.<br>
    <span style="font-size:.78rem;">Tanyakan apa saja tentang manajemen food waste.</span>
</div>
""", unsafe_allow_html=True)

        #Input area 
        user_input = st.chat_input("Ketik pertanyaan Anda...")

        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.spinner("🤔 AI sedang menjawab..."):
                # Build context-aware prompt
                if ctx:
                    context_str = (
                        f"Konteks produk saat ini:\n"
                        f"- Produk: {ctx['product_type']}\n"
                        f"- Tingkat risiko: {ctx['risk_level']} ({ctx['risk_probability']}%)\n"
                        f"- Sisa kadaluarsa: {ctx['days_until_expiry']} hari\n"
                        f"- Kondisi penyimpanan: {ctx['storage_condition']}\n"
                    )
                else:
                    context_str = "Tidak ada konteks prediksi aktif."

                full_prompt = (
                    f"Anda adalah konsultan retail ahli food waste management.\n"
                    f"{context_str}\n"
                    f"Pertanyaan user: {user_input}\n\n"
                    f"Jawab dalam Bahasa Indonesia yang jelas dan praktis. "
                    f"Fokus pada tindakan operasional. Maksimal 3 paragraf."
                )
                answer = call_gemini(full_prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

        # ── Clear history ─────────────────────────────────────────────────
        if st.session_state.chat_history:
            if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

# TAB GEMINI OVERVIEW
with tab_ov:
    section_header("🔍 Model Information & Capabilities")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
<div class="kpi-wrap kpi-green">
    <span class="kpi-icon">🎯</span>
    <div class="kpi-lbl">Model</div>
    <div class="kpi-val" style="font-size:1.2rem;">Gemini 2.5</div>
    <div class="kpi-sub neu">Flash variant</div>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
<div class="kpi-wrap kpi-blue">
    <span class="kpi-icon">⚡</span>
    <div class="kpi-lbl">Response Time</div>
    <div class="kpi-val" style="font-size:1.2rem;">2–5s</div>
    <div class="kpi-sub neu">per request</div>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
<div class="kpi-wrap kpi-orange">
    <span class="kpi-icon">🌐</span>
    <div class="kpi-lbl">Provider</div>
    <div class="kpi-val" style="font-size:1.2rem;">Google AI</div>
    <div class="kpi-sub neu">generativeai SDK</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("🎯 Tujuan Penggunaan")
    st.markdown(f"""
<div class="ibox green">
Gemini diintegrasikan untuk memberikan <b>rekomendasi operasional retail</b>
berdasarkan hasil prediksi model XGBoost:<br><br>
1. <b>Analisis Mendalam</b> — Interpretasi hasil prediksi risiko spoilage<br>
2. <b>Rekomendasi Bisnis</b> — Strategi actionable untuk manager retail<br>
3. <b>Chat Assistant</b> — Tanya-jawab kontekstual berbasis data produk aktif<br>
4. <b>Natural Language</b> — Output dalam Bahasa Indonesia yang mudah dipahami
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_in, col_out = st.columns(2)
    with col_in:
        section_header("📥 Input yang Diterima")
        for item in ["Kategori & jenis produk","Sisa hari kadaluarsa",
                      "Kondisi penyimpanan","Probabilitas risiko (0–100%)",
                      "Harga modal & jual","Stok & unit terjual"]:
            st.write(f"• {item}")
    with col_out:
        section_header("📤 Output yang Dihasilkan")
        for item in ["Analisis risiko mendalam","Faktor utama risiko",
                      "Rekomendasi tindakan (actionable)","Strategi diskon optimal",
                      "Saran manajemen inventori","Percakapan kontekstual"]:
            st.write(f"• {item}")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Model Parameters & Configuration"):
        st.markdown("""
| Parameter | Value | Keterangan |
|-----------|-------|------------|
| **Model ID** | gemini-2.5-flash | Official model identifier |
| **Temperature** | 0.4 | Balanced determinism |
| **Top P** | 0.92 | Nucleus sampling |
| **Max Output Tokens** | 4096 | Output length limit |
| **Response Language** | Bahasa Indonesia | Default untuk laporan |
""")
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