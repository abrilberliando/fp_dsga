import streamlit as st
import pandas as pd
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.predictor import get_predictor

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

init_state("category", "Bakery")
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

st.container()

with st.container():
    st.header("📋 Masukkan Data Produk")
    st.info("💡 Semua data di bawah ini (dari Bagian 1 hingga 4) akan digabungkan untuk menghasilkan satu prediksi risiko yang akurat.")
    
    with st.expander("1️⃣ Info Dasar Produk", expanded=True):
        st.selectbox("Jenis Produk", ["Bakery", "Beverages", "Dairy", "Deli", "Frozen_Meals", "Meat", "Pharmaceuticals", "Produce", "Ready_to_Eat", "Seafood"], key="category")
        st.selectbox("Kualitas Produk", ["A - Sangat Baik", "B - Standar", "C - Kurang Baik"], key="quality_grade")
        st.selectbox("Wilayah Toko", ["Midwest", "Northeast", "Southeast", "Southwest", "West"], key="region")
    
    with st.expander("2️⃣ Kondisi Penyimpanan", expanded=True):
        st.selectbox("Kondisi Suhu Penyimpanan", ["Chiller / Kulkas (4°C)", "Freezer (-18°C)", "Suhu Ruang Ber-AC (20°C)", "Suhu Ruang Biasa (25°C)", "Panas (>28°C)"], key="storage_temp_status")
        st.selectbox("Kestabilan Suhu", ["Sangat Stabil (Tidak berubah)", "Stabil (Berubah <1°C)", "Cukup Stabil (Berubah 1-3°C)", "Tidak Stabil (Berubah 3-5°C)", "Sangat Tidak Stabil (>5°C)"], key="temp_deviation_status")
        st.selectbox("Frekuensi Alat Pendingin Mati / Bermasalah", ["Tidak Pernah (0 kali)", "Jarang (1-2 kali)", "Kadang-kadang (3-5 kali)", "Sering (6-10 kali)", "Sangat Sering (>10 kali)"], key="temp_abuse_events_status")
        st.selectbox("Kondisi kemasan produk saat ini", ["Sempurna", "Sangat Baik", "Baik", "Biasa / Standar", "Rusak", "Rusak Parah"], key="packaging_status")
        st.selectbox("Tingkat kehati-hatian penanganan oleh staf", ["Sangat Hati-hati", "Hati-hati", "Biasa / Standar", "Kasar", "Sangat Kasar"], key="handling_status")
    
    with st.expander("3️⃣ Masa Simpan & Stok", expanded=True):
        st.number_input("Daya tahan total produk dari pabrik (hari)", min_value=1, value=14, key="shelf_life_days")
        st.number_input("Sisa hari sebelum kadaluarsa (hari)", min_value=0, value=7, key="days_until_expiry")
        st.number_input("Jumlah stok saat pertama masuk (unit)", min_value=1, value=50, key="initial_quantity")
        st.number_input("Jumlah stok yang sudah terjual (unit)", min_value=0, value=10, key="units_sold")
    
    with st.expander("4️⃣ Harga & Penjualan", expanded=True):
        st.number_input("Harga modal per unit (Rp)", min_value=0.0, value=10.0, key="cost_price", help="Masukkan dalam denominasi asli (misal: 10 atau 15)")
        st.number_input("Harga jual normal per unit (Rp)", min_value=0.0, value=15.0, key="base_price")
        st.number_input("Harga jual aktual saat ini per unit (Rp)", min_value=0.0, value=15.0, key="selling_price", help="Ubah jika produk sedang diskon")
    
    st.divider()
    btn_predict = st.button("🔍 Cek Risiko Pembusukan Dari Seluruh Data", type="primary", use_container_width=True)

with st.container():
    st.header("📊 Hasil Prediksi")
    
    if btn_predict:
        # Validation
        if st.session_state.units_sold > st.session_state.initial_quantity:
            st.error("Unit terjual tidak boleh melebihi stok awal.")
            st.stop()
        if st.session_state.cost_price > st.session_state.base_price:
            st.warning("Harga modal lebih tinggi dari harga jual — produk ini kemungkinan merugi.")
        if st.session_state.days_until_expiry > st.session_state.shelf_life_days:
            st.error("Sisa hari kadaluarsa tidak boleh melebihi total daya tahan produk.")
            st.stop()
            
        with st.spinner("Sedang menganalisis produk..."):
            time.sleep(1) # simulate brief thinking
            
            # Calculations
            revenue = st.session_state.selling_price * st.session_state.units_sold
            profit = revenue - (st.session_state.cost_price * st.session_state.initial_quantity)
            profit_margin_pct = (profit / revenue * 100) if revenue > 0 else 0.0
            
            discount_amount = st.session_state.base_price - st.session_state.selling_price
            discount_pct = (discount_amount / st.session_state.base_price * 100) if st.session_state.base_price > 0 else 0.0
            markdown_applied = 1 if discount_pct > 0 else 0
            
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
            
            # Dynamic category defaults (from dataset averages)
            cat = st.session_state.category
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
                "region": st.session_state.region,
                "quality_grade": quality_map.get(st.session_state.quality_grade, "A"),
                "storage_temp": storage_temp_map.get(st.session_state.storage_temp_status, 4.0),
                "temp_deviation": temp_dev_map.get(st.session_state.temp_deviation_status, 1.0),
                "handling_score": handling_map.get(st.session_state.handling_status, 5),
                "packaging_score": packaging_map.get(st.session_state.packaging_status, 5),
                "base_price": st.session_state.base_price,
                "cost_price": st.session_state.cost_price,
                "daily_demand": 2.0, # Default hidden
                "initial_quantity": st.session_state.initial_quantity,
                "days_until_expiry": st.session_state.days_until_expiry,
                "temp_abuse_events": abuse_events_map.get(st.session_state.temp_abuse_events_status, 0),
                "shelf_life_days": st.session_state.shelf_life_days,
                "supplier_score": 8, # Default hidden
                "spoilage_sensitivity": sensitivity_map.get(cat, 0.50),
                "distribution_hours": 24.0, # Default hidden
                "days_remaining_at_purchase": st.session_state.days_until_expiry,
                "selling_price": st.session_state.selling_price,
                "discount_pct": discount_pct,
                "markdown_applied": markdown_applied,
                "units_sold": st.session_state.units_sold,
                "demand_variability": 0.5, # Default hidden
                "spoilage_risk": risk_map.get(cat, 0.18),
                "day_of_week": 0, # Default hidden
                "is_weekend": 0, # Default hidden
                "month": 1, # Default hidden
                "is_promoted": 0, # Default hidden
                "revenue": revenue,
                "profit": profit,
                "profit_margin_pct": profit_margin_pct
            }
            
            prob, feat_df = predictor.predict(input_data)
            
            # --- Business Logic Guards (Rule-based Adjustments) ---
            # Jika kadaluarsa sisa <= 2 hari dan stok belum terjual masih banyak
            sisa_stok = st.session_state.initial_quantity - st.session_state.units_sold
            if st.session_state.days_until_expiry <= 2 and sisa_stok > 10:
                prob += 0.35  # Boost risiko sangat tinggi
            elif st.session_state.days_until_expiry <= 5 and sisa_stok > 10:
                prob += 0.15  # Boost risiko menengah
                
            # Jika kondisi penyimpanan parah (Panas atau sering rusak)
            if input_data["storage_temp"] >= 25.0:
                prob += 0.20
            if input_data["temp_abuse_events"] >= 4:
                prob += 0.15
            
            # Cap probability at 99.9%
            prob = min(0.999, prob)
            
            
            # Output Results
            if prob < 0.15:
                st.success(f"🟢 AMAN — Risiko Rendah ({prob*100:.1f}%)")
                st.markdown("- Produk dalam kondisi baik\n- Lanjutkan penyimpanan sesuai prosedur\n- Pantau kembali jika mendekati tanggal kadaluarsa")
            elif prob < 0.40:
                st.warning(f"🟡 WASPADA — Risiko Sedang ({prob*100:.1f}%)")
                st.markdown("- Periksa kondisi suhu penyimpanan sekarang\n- Pertimbangkan diskon 10–20%\n- Pindahkan ke rak yang lebih terlihat pelanggan\n- Cek ulang kondisi kemasan produk")
            else:
                st.error(f"🔴 BERISIKO TINGGI — Tindakan Segera! ({prob*100:.1f}%)")
                st.markdown("- Segera berikan diskon 25–40%\n- Lakukan flash sale atau bundling hari ini\n- Pindahkan ke area promosi / rak depan\n- Periksa dan perbaiki kondisi suhu penyimpanan\n- Laporkan ke manajer toko untuk tindakan lanjut")
            st.divider()
            st.subheader("💡 Analisis Bisnis & Rekomendasi Tindakan")
            
            sisa_stok = st.session_state.initial_quantity - st.session_state.units_sold
            potensi_rugi = sisa_stok * st.session_state.cost_price
            
            if prob < 0.15:
                saran_diskon = "0% (Harga Normal)"
            elif prob < 0.40:
                saran_diskon = "10% - 20%"
            else:
                saran_diskon = "30% - 50% (Flash Sale)"
                
            col_a, col_b = st.columns(2)
            col_a.metric("📦 Sisa Stok Belum Terjual", f"{sisa_stok} Unit")
            col_b.metric("🏷️ Saran Diskon Optimal", saran_diskon)
            
            col_c, col_d = st.columns(2)
            col_c.metric("💸 Estimasi Profit Saat Ini", f"Rp {profit:,.0f}")
            col_d.metric("⚠️ Potensi Kerugian Jika Busuk", f"Rp {potensi_rugi:,.0f}")
            
            with st.expander("📊 Faktor Paling Berpengaruh"):
                st.dataframe(feat_df, use_container_width=True, hide_index=True)
    else:
        st.info("👈 Silakan isi data produk di sebelah kiri dan klik tombol **Cek Risiko Pembusukan**.")
