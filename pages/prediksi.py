import streamlit as st
import pandas as pd
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.predictor import get_predictor
from utils.gemini_analyzer import get_cached_or_generate_report, display_analysis_report

st.set_page_config(
    page_title="Prediksi Risiko Food Waste",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Prediksi Risiko Food Waste")
st.caption("Analisis risiko pembusukan produk berdasarkan data stok dan model XGBoost")
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

init_state("category_ui", "Roti & Kue (Bakery)")
init_state("quality_grade", "A - Sangat Baik")
init_state("region", "Midwest")
init_state("storage_temp", 4.0)
init_state("temp_deviation", 1.0)
init_state("temp_abuse_events", 0)
init_state("distribution_hours", 24.0)
init_state("shelf_life_days", 14)
init_state("days_until_expiry", 7)
init_state("days_remaining_at_purchase", 7)
init_state("cost_price", 10000)
init_state("base_price", 15000)
init_state("selling_price", 15000)
init_state("discount_pct", 0)
init_state("markdown_applied", "Belum")
init_state("initial_quantity", 20)
init_state("units_sold", 5)
init_state("daily_demand", 2)
init_state("demand_variability", 0.5)
init_state("handling_score", 8)
init_state("packaging_score", 8)
init_state("supplier_score", 8)
init_state("spoilage_sensitivity", 0.50)
init_state("spoilage_risk", 0.10)
init_state("day_of_week", "Senin")
init_state("is_weekend", "Bukan Weekend")
init_state("month", 1)
init_state("is_promoted", "Tidak")
init_state("prediction_completed", False)
init_state("last_prediction_prob", 0.0)
init_state("last_prediction_input_data", None)
init_state("last_prediction_feat_df", None)
init_state("last_user_inputs_display", None)
init_state("last_prediction_metrics", None)
init_state("generating_analysis", False)
init_state("force_regenerate_analysis", False)
init_state("ai_analysis_report", None)

st.container()

with st.container():
    st.header("📋 Masukkan Data Produk")
    st.info("💡 Semua data di bawah ini (dari Bagian 1 hingga 4) akan digabungkan untuk menghasilkan satu prediksi risiko yang akurat.")
    
    category_display_map = {
        "Roti & Kue (Bakery)": "Bakery",
        "Minuman (Beverages)": "Beverages",
        "Susu & Olahannya (Dairy)": "Dairy",
        "Daging Olahan & Keju (Deli)": "Deli",
        "Makanan Beku (Frozen Meals)": "Frozen_Meals",
        "Daging Mentah (Meat)": "Meat",
        "Obat-obatan & Vaksin (Pharmaceuticals)": "Pharmaceuticals",
        "Sayur & Buah Segar (Produce)": "Produce",
        "Makanan Siap Saji (Ready to Eat)": "Ready_to_Eat",
        "Makanan Laut (Seafood)": "Seafood"
    }

    with st.expander("1️⃣ Info Dasar Produk", expanded=True):
        st.selectbox("Jenis Produk", list(category_display_map.keys()), key="category_ui")
    
    with st.expander("2️⃣ Kondisi Penyimpanan", expanded=True):
        st.selectbox("Kondisi Suhu Penyimpanan", ["Chiller / Kulkas (4°C)", "Freezer (-18°C)", "Suhu Ruang Ber-AC (20°C)", "Suhu Ruang Biasa (25°C)", "Panas (>28°C)"], key="storage_temp_status")
    
    with st.expander("3️⃣ Masa Simpan & Stok", expanded=True):
        st.number_input("Sisa hari sebelum kadaluarsa (hari)", min_value=0, value=7, key="days_until_expiry")
    
    with st.expander("4️⃣ Harga & Penjualan", expanded=True):
        st.number_input("Harga modal per unit (Rp)", min_value=0.0, value=10.0, key="cost_price", help="Masukkan dalam denominasi asli (misal: 10 atau 15)")
        st.number_input("Harga jual per unit (Rp)", min_value=0.0, value=15.0, key="selling_price")
    
    st.divider()
    btn_predict = st.button("🔍 Cek Risiko Pembusukan Dari Seluruh Data", type="primary", use_container_width=True)

with st.container():
    st.header("📊 Hasil Prediksi")

    user_inputs_display = {
        "category_display": st.session_state.get("category_ui", "Roti & Kue (Bakery)"),
        "storage_temp_status": st.session_state.get("storage_temp_status", "Unknown")
    }

    show_results = btn_predict or st.session_state.prediction_completed

    revenue = 0.0
    profit = 0.0
    profit_margin_pct = 0.0
    discount_pct = 0.0
    markdown_applied = 0
    sisa_stok = 0
    potensi_rugi = 0.0

    if show_results:
        if btn_predict:
            with st.spinner("Sedang menganalisis produk..."):
                time.sleep(1)

                # Set dummy data for removed fields
                dummy_initial_quantity = 50
                dummy_units_sold = 10
                dummy_shelf_life_days = st.session_state.days_until_expiry + 14

                # Calculations
                revenue = st.session_state.selling_price * dummy_units_sold
                profit = revenue - (st.session_state.cost_price * dummy_initial_quantity)
                profit_margin_pct = (profit / revenue * 100) if revenue > 0 else 0.0

                discount_pct = 0.0
                markdown_applied = 0

                # Prepare data dict
                quality_map = {"A - Sangat Baik": "A", "B - Standar": "B", "C - Kurang Baik": "C"}
                packaging_map = {
                    "Sempurna": 10, "Sangat Baik": 9, "Baik": 7,
                    "Biasa / Standar": 5, "Rusak": 3, "Rusak Parah": 1
                }
                handling_map = {
                    "Sangat Hati-hati": 10, "Hati-hati": 8, "Biasa / Standar": 5,
                    "Kasar": 3, "Sangat Kasar": 1
                }
                storage_temp_map = {
                    "Freezer (-18°C)": -18.0, "Chiller / Kulkas (4°C)": 4.0,
                    "Suhu Ruang Ber-AC (20°C)": 20.0, "Suhu Ruang Biasa (25°C)": 25.0, "Panas (>28°C)": 30.0
                }
                temp_dev_map = {
                    "Sangat Stabil (Tidak berubah)": 0.0, "Stabil (Berubah <1°C)": 0.5,
                    "Cukup Stabil (Berubah 1-3°C)": 2.0, "Tidak Stabil (Berubah 3-5°C)": 4.0,
                    "Sangat Tidak Stabil (>5°C)": 7.0
                }
                abuse_events_map = {
                    "Tidak Pernah (0 kali)": 0, "Jarang (1-2 kali)": 1,
                    "Kadang-kadang (3-5 kali)": 4, "Sering (6-10 kali)": 8, "Sangat Sering (>10 kali)": 15
                }

                cat = category_display_map[st.session_state.category_ui]
                sensitivity_map = {
                    "Bakery": 0.50, "Beverages": 0.40, "Dairy": 0.70, "Deli": 0.75,
                    "Frozen_Meals": 0.30, "Meat": 0.90, "Pharmaceuticals": 0.85,
                    "Produce": 0.60, "Ready_to_Eat": 0.90, "Seafood": 0.95
                }
                risk_map = {
                    "Bakery": 0.18, "Beverages": 0.18, "Dairy": 0.20, "Deli": 0.20,
                    "Frozen_Meals": 0.17, "Meat": 0.20, "Pharmaceuticals": 0.20,
                    "Produce": 0.19, "Ready_to_Eat": 0.22, "Seafood": 0.21
                }

                input_data = {
                    "category": cat,
                    "region": "Midwest",
                    "quality_grade": "A", # Default Sangat Baik (Asumsi optimal karena disembunyikan)
                    "storage_temp": storage_temp_map.get(st.session_state.storage_temp_status, 4.0),
                    "temp_deviation": 0.0, # Default Sangat Stabil
                    "handling_score": 9, # Default Sangat Hati-hati
                    "packaging_score": 9, # Default Sangat Baik
                    "base_price": st.session_state.selling_price,
                    "cost_price": st.session_state.cost_price,
                    "daily_demand": 5.0, # Asumsi demand tinggi (laku)
                    "initial_quantity": dummy_initial_quantity,
                    "days_until_expiry": st.session_state.days_until_expiry,
                    "temp_abuse_events": 0, # Default Tidak pernah
                    "shelf_life_days": dummy_shelf_life_days,
                    "supplier_score": 9,
                    "spoilage_sensitivity": sensitivity_map.get(cat, 0.50),
                    "distribution_hours": 12.0, # Asumsi distribusi cepat
                    "days_remaining_at_purchase": st.session_state.days_until_expiry,
                    "selling_price": st.session_state.selling_price,
                    "discount_pct": discount_pct,
                    "markdown_applied": markdown_applied,
                    "units_sold": dummy_units_sold,
                    "demand_variability": 0.2, # Asumsi stabil
                    "spoilage_risk": risk_map.get(cat, 0.18),
                    "day_of_week": 0,
                    "is_weekend": 0,
                    "month": 1,
                    "is_promoted": 0,
                    "revenue": revenue,
                    "profit": profit,
                    "profit_margin_pct": profit_margin_pct
                }

                prob, feat_df = predictor.predict(input_data)
                
                # --- LONG EXPIRY SAFEGUARD (AI Hallucination Fix) ---
                # Jika user memasukkan sisa hari yang sangat besar (misal 360 hari),
                # model XGBoost bisa bingung karena di luar kebiasaan data pelatihan.
                # Kita paksa turunkan risikonya karena barang yang kadaluarsanya masih lama = AMAN.
                if st.session_state.days_until_expiry > 90:
                    prob = prob * 0.10
                elif st.session_state.days_until_expiry > 30:
                    prob = prob * 0.30
                elif st.session_state.days_until_expiry > 14:
                    prob = prob * 0.60

                sisa_stok = dummy_initial_quantity - dummy_units_sold
                
                # --- EXPIRY PENALTY LOGIC ---
                # Semakin dekat kadaluarsa dan masih ada stok, risiko membusuk meroket tajam
                if sisa_stok > 0:
                    if st.session_state.days_until_expiry == 0:
                        prob += 0.70  # Sangat fatal, pasti terbuang besok jika tidak laku hari ini
                    elif st.session_state.days_until_expiry <= 2:
                        prob += 0.40
                    elif st.session_state.days_until_expiry <= 5:
                        prob += 0.15


                    
                # --- FROZEN FOOD FATAL TEMPERATURE LOGIC ---
                # Jika makanan rentan beku (Frozen Meals, Meat, Seafood) ditaruh di suhu ruang (>= 20C),
                # barang akan mencair dan busuk dalam hitungan jam, berapapun sisa hari kadaluarsanya!
                if cat in ["Frozen_Meals", "Meat", "Seafood", "Dairy"] and input_data["storage_temp"] >= 20.0:
                    prob = max(prob, 0.90)  # Paksa jadi Sangat Berbahaya (90%)
                    
                # --- PRICING PENALTY LOGIC ---
                # Jika markup harga terlalu tinggi (>50%), risiko basi naik tajam karena sepi pembeli
                markup = (st.session_state.selling_price - st.session_state.cost_price) / (st.session_state.cost_price + 1e-6)
                if markup > 0.50 and sisa_stok > 0:
                    penalty = min(0.40, (markup - 0.50) * 0.30)
                    prob += penalty

                prob = min(0.999, prob)

                st.session_state.prediction_completed = True
                st.session_state.last_prediction_prob = prob
                st.session_state.last_prediction_input_data = input_data
                st.session_state.last_prediction_feat_df = feat_df
                st.session_state.last_user_inputs_display = user_inputs_display
                st.session_state.last_prediction_metrics = {
                    "revenue": revenue,
                    "profit": profit,
                    "profit_margin_pct": profit_margin_pct,
                    "discount_pct": discount_pct,
                    "markdown_applied": markdown_applied,
                    "sisa_stok": sisa_stok,
                    "potensi_rugi": sisa_stok * st.session_state.cost_price,
                }
        else:
            input_data = st.session_state.last_prediction_input_data
            prob = st.session_state.last_prediction_prob
            feat_df = st.session_state.last_prediction_feat_df
            user_inputs_display = st.session_state.last_user_inputs_display or user_inputs_display
            metrics = st.session_state.last_prediction_metrics or {}
            revenue = metrics.get("revenue", 0)
            profit = metrics.get("profit", 0)
            profit_margin_pct = metrics.get("profit_margin_pct", 0.0)
            discount_pct = metrics.get("discount_pct", 0.0)
            markdown_applied = metrics.get("markdown_applied", 0)
            sisa_stok = metrics.get("sisa_stok", 40) # dummy sisa stok
            potensi_rugi = metrics.get("potensi_rugi", sisa_stok * st.session_state.cost_price)

            if input_data is None:
                st.info("👈 Silakan klik tombol **Cek Risiko Pembusukan** untuk menjalankan prediksi terlebih dahulu.")
                st.stop()

        if prob < 0.25:
            st.success(f"🟢 AMAN — Risiko Rendah ({prob*100:.1f}%)")
            st.markdown("- Produk dalam kondisi baik\n- Lanjutkan penyimpanan sesuai prosedur\n- Pantau kembali jika mendekati tanggal kadaluarsa")
        elif prob < 0.50:
            st.warning(f"🟡 WASPADA — Risiko Sedang ({prob*100:.1f}%)")
            st.markdown("- Periksa kondisi suhu penyimpanan sekarang\n- Pertimbangkan diskon 10–20%\n- Pindahkan ke rak yang lebih terlihat pelanggan\n- Cek ulang kondisi kemasan produk")
        else:
            st.error(f"🔴 BERISIKO TINGGI — Tindakan Segera! ({prob*100:.1f}%)")
            st.markdown("- Segera berikan diskon 25–40%\n- Lakukan flash sale atau bundling hari ini\n- Pindahkan ke area promosi / rak depan\n- Periksa dan perbaiki kondisi suhu penyimpanan\n- Laporkan ke manajer toko untuk tindakan lanjut")

        st.divider()
        st.subheader("💡 Rekomendasi Tindakan")

        # Logika Saran Diskon yang mempertimbangkan margin profit
        if st.session_state.selling_price <= st.session_state.cost_price:
            # Jika sudah tidak profit (jual modal / rugi)
            if prob < 0.50:
                saran_diskon = "0% (Sudah Harga Modal)"
            else:
                saran_diskon = "10% - 30% (Cuci Gudang / Potong Rugi)"
        else:
            # Jika masih ada profit
            if prob < 0.25:
                saran_diskon = "0% (Harga Normal)"
            elif prob < 0.50:
                saran_diskon = "10% - 20%"
            else:
                saran_diskon = "30% - 50% (Flash Sale)"

        st.metric("🏷️ Saran Diskon Optimal", saran_diskon)

        with st.expander("📊 Faktor Penyebab Paling Berpengaruh"):
            display_df = feat_df.copy()
            # Hapus kolom teknis agar tidak membingungkan user awam
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
