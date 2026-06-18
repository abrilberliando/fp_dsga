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

# set_page_config app.py

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import inject_css, COLORS, page_header, section_header

inject_css()
C = COLORS

# Session State
for _k, _v in [
    ("gemini_test_result", None),
    ("gemini_connection_status", "Not Connected"),
    ("gemini_configured", False),
    ("chat_history", []),
]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

#Helper functions 
def configure_gemini():
    api_key = st.session_state.get("llm_api_key", "")
    if not api_key:
        return False
    try:
        genai.configure(api_key=api_key)
        st.session_state.gemini_configured = True
        return True
    except Exception:
        return False

def call_gemini(prompt_text: str) -> str:
    if not st.session_state.gemini_configured:
        if not configure_gemini():
            return "❌ API Key belum dikonfigurasi. Isi API Key di sidebar."
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

def test_gemini_connection():
    """Test koneksi ke Gemini API."""
    api_key = st.session_state.get("llm_api_key", "")
    if not api_key:
        return {"status": "FAILED", "message": "❌ API Key belum dikonfigurasi",
                "details": "Isi API Key di sidebar terlebih dahulu"}
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content("Reply with: Connection successful")
        if response.text:
            return {"status": "SUCCESS", "message": "✅ Koneksi Berhasil",
                    "details": f"Gemini 2.5 Flash aktif · {response.text[:80]}"}
        return {"status": "FAILED", "message": "❌ Tidak ada response", "details": "Coba lagi"}
    except Exception as e:
        return {"status": "FAILED", "message": "❌ Koneksi Gagal", "details": str(e)}


def get_system_prompt():
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
"""

#Page Header
page_header(
    title="AI Assistant & Gemini",
    subtitle="Chat Assistant berbasis Gemini AI · Dokumentasi integrasi untuk Stakeholder Teknis",
    icon="🤖",
)

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

# TAB API CONFIGURATION
with tab_cfg:
    section_header("⚙️ API Setup & Status")

    # Status info box dengan key detection
    if st.session_state.get("llm_api_key"):
        key_masked = st.session_state["llm_api_key"][:8] + "..." + st.session_state["llm_api_key"][-4:]
        st.markdown(f"""
<div class="ibox green" style="display:flex; justify-content:space-between; align-items:center;">
    <div>
        🔑 <b>API Key Terdeteksi</b><br>
        <span style="font-size:.75rem; color:{C['muted']}; font-family:'JetBrains Mono',monospace;">
            {key_masked}
        </span>
    </div>
    <div style="text-align:right;">
        <span style="font-size:1.8rem;">✅</span>
    </div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class="ibox orange" style="display:flex; justify-content:space-between; align-items:center;">
    <div>
        🔑 <b>API Key Belum Dikonfigurasi</b><br>
        <span style="font-size:.75rem; color:{C['muted']};">
            Silakan isi <b>Gemini API Key</b> di sidebar untuk melanjutkan
        </span>
    </div>
    <div style="text-align:right;">
        <span style="font-size:1.8rem;">⚠️</span>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Connection Test Section
    section_header("🧪 Live Connection Test")
    
    col_test_left, col_test_right = st.columns([1, 1])
    
    with col_test_left:
        st.markdown(f"""
<div style="background:{C['card']}; border:1px solid {C['border']}; border-radius:12px; 
            padding:1.5rem; height:100%; display:flex; flex-direction:column; justify-content:space-between;">
    <div>
        <div style="font-size:.85rem; font-weight:600; color:{C['text']}; margin-bottom:.8rem;">
            📡 Test Koneksi API
        </div>
        <div style="font-size:.75rem; color:{C['muted']}; line-height:1.6; margin-bottom:1rem;">
            Verifikasi apakah API Key Anda valid dan dapat terhubung ke server Google AI.
            Test ini akan mengirim request sample untuk memastikan koneksi berjalan dengan baik.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        
        if st.button("🔗 Test Koneksi", type="primary", use_container_width=True, key="test_conn_btn"):
            with st.spinner("⏳ Menghubungkan ke Google AI..."):
                result = test_gemini_connection()
                st.session_state.gemini_test_result = result
                st.session_state.gemini_connection_status = (
                    "Connected & Verified" if result["status"] == "SUCCESS"
                    else "Verification Failed"
                )
                st.rerun()
    
    with col_test_right:
        st.markdown(f"""
<div style="background:{C['card']}; border:1px solid {C['border']}; border-radius:12px; 
            padding:1.5rem; height:100%;">
    <div style="font-size:.85rem; font-weight:600; color:{C['text']}; margin-bottom:.8rem;">
        📊 Hasil Test
    </div>
""", unsafe_allow_html=True)
        
        if st.session_state.gemini_test_result:
            r = st.session_state.gemini_test_result
            if r["status"] == "SUCCESS":
                st.success(r["message"])
                st.markdown(f"""
<div style="font-size:.72rem; color:{C['muted']}; margin-top:.5rem; 
            padding:.6rem; background:rgba(76,175,80,.1); border-radius:6px;">
    ✓ {r["details"]}
</div>
""", unsafe_allow_html=True)
            else:
                st.error(r["message"])
                st.markdown(f"""
<div style="font-size:.72rem; color:{C['muted']}; margin-top:.5rem; 
            padding:.6rem; background:rgba(244,67,54,.1); border-radius:6px;">
    ✗ {r["details"]}
</div>
""", unsafe_allow_html=True)
        else:
            st.info("⏸️ Belum ada hasil test")
            st.markdown(f"""
<div style="font-size:.72rem; color:{C['muted']}; margin-top:.5rem; 
            padding:.6rem; background:rgba(33,150,243,.08); border-radius:6px;">
    Klik tombol <b>Test Koneksi</b> di sebelah kiri untuk memulai verifikasi.
</div>
""", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Status Cards Section
    section_header("📈 Status Overview")
    s1, s2, s3 = st.columns(3)
    status_now = st.session_state.gemini_connection_status
    
    with s1:
        st.markdown(f"""
<div class="kpi-wrap {'kpi-green' if status_now=='Connected & Verified' else 'kpi-red' if status_now=='Verification Failed' else 'kpi-orange'}">
    <span class="kpi-icon">{'✅' if status_now=='Connected & Verified' else '❌' if status_now=='Verification Failed' else '⏳'}</span>
    <div class="kpi-lbl">Connection Status</div>
    <div class="kpi-val" style="font-size:.88rem;">{status_now.replace(' ', '<br>')}</div>
    <div class="kpi-sub neu" style="font-size:.68rem;">Real-time verification</div>
</div>""", unsafe_allow_html=True)
    
    with s2:
        st.markdown(f"""
<div class="kpi-wrap kpi-blue">
    <span class="kpi-icon">🤖</span>
    <div class="kpi-lbl">Active Model</div>
    <div class="kpi-val" style="font-size:.88rem;">Gemini 2.5<br>Flash</div>
    <div class="kpi-sub neu" style="font-size:.68rem;">Latest generation</div>
</div>""", unsafe_allow_html=True)
    
    with s3:
        st.markdown(f"""
<div class="kpi-wrap kpi-teal">
    <span class="kpi-icon">📡</span>
    <div class="kpi-lbl">Provider</div>
    <div class="kpi-val" style="font-size:.88rem;">Google AI</div>
    <div class="kpi-sub neu" style="font-size:.68rem;">generativeai SDK</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # API Key Tutorial
    with st.expander("Cara Mendapatkan Gemini API Key", expanded=False):
        st.markdown(f"""
<div style="padding:.5rem 0;">
    <ol style="line-height:2; color:{C['muted']};">
        <li><b>Buka Google AI Studio</b><br>
            <span style="font-size:.75rem;">
                <a href="https://makersuite.google.com/app/apikey" target="_blank" 
                   style="color:{C['blue']};">https://makersuite.google.com/app/apikey</a>
            </span>
        </li>
        <li><b>Login</b> dengan akun Google Anda</li>
        <li><b>Klik "Create API Key"</b><br>
            <span style="font-size:.75rem;">Pilih atau buat Google Cloud project baru</span>
        </li>
        <li><b>Copy</b> string API key yang muncul</li>
        <li><b>Paste</b> ke kolom <b>Gemini API Key</b> di sidebar aplikasi</li>
        <li><b>Test koneksi</b> menggunakan tombol di atas untuk verifikasi</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# TAB CUSTOM PROMPT
with tab_prompt:
    section_header("📝 System Prompt Documentation")
    st.caption("Instruksi inti yang mengatur bagaimana Gemini menginterpretasi prediksi XGBoost. Read-only.")

    col_h, col_tip = st.columns([1, 1])
    with col_h:
        st.markdown("#### 💾 Core Instruction Template")
    with col_tip:
        st.markdown(f"""
<div style='text-align:right; margin-top:6px; font-size:.75rem; color:{C["muted"]}'>
    💡 Hover pojok kanan atas untuk menyalin
</div>""", unsafe_allow_html=True)

    st.code(get_system_prompt(), language="text")

    st.download_button(
        label="📥 Download Prompt Template (.txt)",
        data=get_system_prompt(),
        file_name="gemini_system_prompt.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.markdown("---")
    with st.expander("🔍 Struktur Prompt"):
        st.markdown("""
**Role Definition** — Konsultan retail food waste  
**Context Injection** — Data produk + hasil prediksi XGBoost  
**Output Format** — Ringkasan · Faktor Utama · Rekomendasi · Kesimpulan  
**Rules** — Bahasa Indonesia · max 250 kata · no ML theory · actionable  
**3. Quality Criteria:** Actionable, Data-driven, Specific, Profitable  
**4. Output Format Specification:** Struktur laporan 7 poin yang komprehensif.
""")
# TAB AI WORKFLOW
with tab_wf:
    section_header("🔄 System Architecture & Data Flow")
    st.caption("Alur data dari input pengguna hingga rekomendasi AI.")

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