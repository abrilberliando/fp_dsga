import datetime
import streamlit as st
import pandas as pd
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.predictor import get_predictor
from utils.gemini_analyzer import get_cached_or_generate_report, display_analysis_report

st.title("🔮 Prediksi Risiko Food Waste")
st.caption("Aplikasi Prediksi Cerdas Khusus Staff Toko & Inventory")
st.divider()

# Load model safely
try:
    predictor = get_predictor()
except Exception as e:
    st.error("Gagal memuat model. Coba jalankan ulang python train_model.py")
    st.stop()

def init_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

init_state("prediction_completed", False)
init_state("last_prediction_prob", 0.0)
init_state("last_prediction_input_data", None)
init_state("last_prediction_feat_df", None)
init_state("last_user_inputs_display", None)
init_state("use_feature_eng", True)
init_state("generating_analysis", False)
init_state("force_regenerate_analysis", False)
init_state("ai_analysis_report", None)

st.container()

with st.container():
    st.header("📋 Masukkan Data Produk")
    st.info("💡 Silakan isi formulir di bawah ini sesuai dengan kondisi barang saat ini.")
    
    product_map = {
        "Susu & Olahannya (Dairy)": "Dairy",
        "Daging Mentah (Meat)": "Meat",
        "Sayur & Buah Segar (Produce)": "Produce",
        "Makanan Beku (Frozen Meals)": "Frozen_Meals",
        "Roti & Kue (Bakery)": "Bakery",
        "Obat-obatan & Vaksin (Pharmaceuticals)": "Pharmaceuticals",
        "Makanan Laut (Seafood)": "Seafood",
        "Makanan Siap Saji (Ready to Eat)": "Ready_to_Eat",
        "Minuman (Beverages)": "Beverages",
        "Daging Olahan & Keju (Deli)": "Deli"
    }

    with st.expander("1️⃣ Informasi Produk", expanded=True):
        product_name = st.selectbox("Pilih Nama Barang", list(product_map.keys()))
    
    with st.expander("2️⃣ Garis Waktu", expanded=True):
        days_until_expiry = st.number_input("Sisa Hari Sebelum Kadaluarsa", min_value=0, value=7, help="Masukkan berapa hari lagi barang akan kedaluwarsa")

    storage_temp_map = {
        "Freezer / Beku (-18°C)": -18.0,
        "Kulkas / Dingin (4°C)": 4.0,
        "Suhu Ruangan / Terbuka (25°C)": 25.0
    }
    
    quality_grade_map = {
        "⭐⭐⭐⭐⭐ (Sangat Segar / Baru)": "A",
        "⭐⭐⭐ (Normal / Agak Layu)": "B",
        "⭐ (Hampir Busuk / Berbau)": "C"
    }

    with st.expander("3️⃣ Kondisi Lingkungan", expanded=True):
        storage_location = st.selectbox("Disimpan Di Mana?", list(storage_temp_map.keys()))
        physical_condition = st.selectbox("Kondisi Fisik Saat Diterima", list(quality_grade_map.keys()))
    
    st.divider()
    
    btn_predict = st.button("🔍 Cek Risiko Pembusukan", type="primary", use_container_width=True)

with st.container():
    st.header("📊 Hasil Prediksi")

    user_inputs_display = {
        "product_name": product_name,
        "days_until_expiry": days_until_expiry,
        "storage_location": storage_location,
        "physical_condition": physical_condition
    }

    show_results = btn_predict or st.session_state.prediction_completed

    if show_results:
        if btn_predict:
            with st.spinner("Sedang menganalisis produk..."):
                time.sleep(1)

                cat = product_map[product_name]
                storage_temp = storage_temp_map[storage_location]
                quality_grade = quality_grade_map[physical_condition]

                # Gunakan model Lite yang hanya menerima 4 fitur aktual yang diinput user
                input_data = {
                    "category": cat,
                    "storage_temp": storage_temp,
                    "days_until_expiry": days_until_expiry,
                    "quality_grade": quality_grade
                }

                prob, feat_df = predictor.predict(input_data)
                        
                prob = min(0.999, max(0.001, prob))

                st.session_state.prediction_completed = True
                st.session_state.last_prediction_prob = prob
                st.session_state.last_prediction_input_data = input_data
                st.session_state.last_prediction_feat_df = feat_df
                st.session_state.last_user_inputs_display = user_inputs_display
        else:
            input_data = st.session_state.last_prediction_input_data
            prob = st.session_state.last_prediction_prob
            feat_df = st.session_state.last_prediction_feat_df
            user_inputs_display = st.session_state.last_user_inputs_display or user_inputs_display

            if input_data is None:
                st.info("👈 Silakan klik tombol **Cek Risiko Pembusukan** untuk menjalankan prediksi terlebih dahulu.")
                st.stop()
                
        # --- BUSINESS LOGIC OUTPUT ---
        product = user_inputs_display['product_name']

        if prob < 0.25:
            st.success(f"🟢 AMAN — Risiko Rendah ({prob*100:.1f}%)")
            st.markdown(f"> **Sistem Memprediksi:** Produk **{product}** saat ini dalam kondisi aman dengan risiko pembusukan yang sangat kecil.")
        elif prob < 0.50:
            st.warning(f"🟡 AMAN (WASPADA) — Risiko Sedang ({prob*100:.1f}%)")
            st.markdown(f"> **Sistem Memprediksi:** Produk **{product}** mulai menunjukkan risiko. Pertimbangkan untuk mengecek ulang kondisinya atau memajangnya di rak depan.")
        else:
            st.error(f"🔴 BERISIKO TINGGI — Tindakan Segera! ({prob*100:.1f}%)")
            st.markdown(f"> **Peringatan Sistem:** Gawat! Produk **{product}** memiliki risiko sangat tinggi untuk terbuang sia-sia dalam waktu dekat. Anda harus segera melakukan diskon promosi atau pemindahan rak secepatnya!")

        st.divider()

        with st.expander("📊 Faktor Penyebab Paling Berpengaruh"):
            display_df = feat_df.copy()
            if "Fitur Teknis" in display_df.columns:
                display_df = display_df.drop(columns=["Fitur Teknis"])
            
            st.dataframe(
                display_df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Pengaruh (%)": st.column_config.NumberColumn(
                        "Tingkat Pengaruh",
                        help="Seberapa besar faktor ini berkontribusi terhadap risiko pembusukan",
                        format="%.1f%%"
                    ),
                    "Penyebab (Faktor Utama)": st.column_config.TextColumn(
                        "Faktor Penyebab Utama",
                        width="large"
                    )
                }
            )

        st.divider()
        st.subheader("🤖 AI Analysis Report")
        st.caption("Analisis mendalam dan rekomendasi berbasis AI menggunakan Gemini")

        api_key = st.session_state.get("llm_api_key", "")
        if not api_key:
            st.warning(
                "⚠️ API Key belum dikonfigurasi.\n\n"
                "Untuk menggunakan fitur AI Analysis Report, silakan isi "
                "**Gemini API Key** di sidebar terlebih dahulu.",
                icon="🔑"
            )
        else:
            col_generate, col_refresh = st.columns([4, 1])
            with col_generate:
                if st.button(
                    "📄 Generate AI Analysis Report",
                    key="btn_generate_analysis",
                    type="primary",
                    use_container_width=True
                ):
                    st.session_state.generating_analysis = True
            with col_refresh:
                if st.button(
                    "🔄",
                    key="btn_refresh_analysis",
                    help="Force regenerate analysis (ignore cache)",
                    use_container_width=True
                ):
                    st.session_state.force_regenerate_analysis = True

            if st.session_state.get("generating_analysis") or st.session_state.get("force_regenerate_analysis"):
                with st.spinner("⏳ Sedang menganalisis data produk dengan AI..."):
                    report = get_cached_or_generate_report(
                        input_data=input_data,
                        prob=prob,
                        user_inputs=user_inputs_display,
                        force_regenerate=st.session_state.get("force_regenerate_analysis", False)
                    )
                    if report:
                        st.session_state.ai_analysis_report = report
                        st.session_state.generating_analysis = False
                        st.session_state.force_regenerate_analysis = False
                        st.rerun()
                    else:
                        st.error(
                            "❌ Gagal generate analysis.\n\n"
                            "Kemungkinan penyebab:\n"
                            "- API Key tidak valid\n"
                            "- Koneksi internet terputus\n"
                            "- Rate limit API tercapai"
                        )
                        st.session_state.generating_analysis = False
                        st.session_state.force_regenerate_analysis = False

            if "ai_analysis_report" in st.session_state and st.session_state.ai_analysis_report:
                st.markdown(
                    """
                    <div style="
                        background: rgba(76, 175, 80, 0.05);
                        border-left: 4px solid #4caf50;
                        padding: 16px;
                        border-radius: 6px;
                        margin: 16px 0;
                    ">
                    """,
                    unsafe_allow_html=True
                )
                display_analysis_report(st.session_state.ai_analysis_report)
                st.markdown("</div>", unsafe_allow_html=True)
                st.caption(
                    "✓ Hasil analisis telah di-cache. Klik 🔄 untuk generate ulang."
                )
            else:
                st.info(
                    "👆 Klik tombol **Generate AI Analysis Report** untuk mendapatkan "
                    "rekomendasi mendalam dari AI berdasarkan data produk dan hasil prediksi."
                )
    else:
        st.info("👈 Silakan isi data produk di sebelah kiri dan klik tombol **Cek Risiko Pembusukan**.")
