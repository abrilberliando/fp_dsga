"""
Halaman: Prediksi Risiko

Prediksi risiko pembusukan produk dengan form card layout.
Menampilkan hasil sebagai KPI card visual.
Role-aware: Retail Manager melihat form simpel, Stakeholder Teknis
mendapat akses field advanced.
"""

import streamlit as st
import pandas as pd
import time
import sys
import os
from datetime import datetime

# add base directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.predictor import get_predictor
from utils.gemini_analyzer import get_cached_or_generate_report, display_analysis_report
from utils.theme import inject_css, COLORS, section_header, page_header, prediction_result_card

inject_css()
C = COLORS

# session state initialization
def _init(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

_init("prediction_completed", False)
_init("last_prediction_prob", 0.0)
_init("last_prediction_input_data", None)
_init("last_prediction_feat_df", None)
_init("last_user_inputs_display", None)
_init("last_prediction_metrics", None)
_init("generating_analysis", False)
_init("force_regenerate_analysis", False)
_init("ai_analysis_report", None)
_init("prediction_context", None)

# lookup maps for form options
CATEGORY_MAP = {
    "Roti & Kue (Bakery)"           : "Bakery",
    "Minuman (Beverages)"           : "Beverages",
    "Susu & Olahannya (Dairy)"      : "Dairy",
    "Daging Olahan & Keju (Deli)"   : "Deli",
    "Makanan Beku (Frozen Meals)"   : "Frozen_Meals",
    "Daging Mentah (Meat)"          : "Meat",
    "Obat-obatan & Vaksin (Pharma)" : "Pharmaceuticals",
    "Sayur & Buah Segar (Produce)"  : "Produce",
    "Makanan Siap Saji (Ready Eat)" : "Ready_to_Eat",
    "Makanan Laut (Seafood)"        : "Seafood",
}
STORAGE_TEMP_MAP = {
    "Freezer (-18°C)"       : -18.0,
    "Chiller / Kulkas (4°C)": 4.0,
    "Suhu Ruang Ber-AC (20°C)": 20.0,
    "Suhu Ruang Biasa (25°C)" : 25.0,
    "Panas (>28°C)"         : 30.0,
}
TEMP_DEV_MAP = {
    "Sangat Stabil (tidak berubah)" : 0.0,
    "Stabil (berubah <1°C)"         : 0.5,
    "Cukup Stabil (berubah 1–3°C)"  : 2.0,
    "Tidak Stabil (berubah 3–5°C)"  : 4.0,
    "Sangat Tidak Stabil (>5°C)"    : 7.0,
}
ABUSE_MAP = {
    "Tidak Pernah (0×)"       : 0,
    "Jarang (1–2×)"           : 1,
    "Kadang-kadang (3–5×)"    : 4,
    "Sering (6–10×)"          : 8,
    "Sangat Sering (>10×)"    : 15,
}
PACKAGING_MAP = {
    "Sempurna"       : 10,
    "Sangat Baik"    : 9,
    "Baik"           : 7,
    "Standar"        : 5,
    "Rusak"          : 3,
    "Rusak Parah"    : 1,
}
HANDLING_MAP = {
    "Sangat Hati-hati" : 10,
    "Hati-hati"        : 8,
    "Standar"          : 5,
    "Kasar"            : 3,
    "Sangat Kasar"     : 1,
}
SENSITIVITY_MAP = {
    "Bakery":0.50,"Beverages":0.40,"Dairy":0.70,"Deli":0.75,
    "Frozen_Meals":0.30,"Meat":0.90,"Pharmaceuticals":0.85,
    "Produce":0.60,"Ready_to_Eat":0.90,"Seafood":0.95,
}
RISK_BASE_MAP = {
    "Bakery":0.18,"Beverages":0.18,"Dairy":0.20,"Deli":0.20,
    "Frozen_Meals":0.17,"Meat":0.20,"Pharmaceuticals":0.20,
    "Produce":0.19,"Ready_to_Eat":0.22,"Seafood":0.21,
}

# load model
try:
    predictor = get_predictor()
except Exception:
    st.error("⚠️ Model tidak ditemukan. Jalankan `train_model.py` terlebih dahulu.")
    st.stop()

# check user role
is_retail = "Retail Manager" in st.session_state.get("user_role", "Retail Manager")

# page header
page_header(
    title="Prediksi Risiko Pembusukan",
    subtitle="Analisis risiko spoilage produk perishable berbasis model XGBoost + logika bisnis retail",
    icon="🔮",
)

# Badge pills
st.markdown("""
<div style="margin:.5rem 0 1.2rem 0;">
    <span class="pill pill-green">XGBoost · binary:logistic</span>
    <span class="pill pill-blue">Input Produk Real-time</span>
    <span class="pill pill-orange">AI Recommendation Ready</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# input form column and results column
col_form, col_result = st.columns([1, 1], gap="large")

# input form column
with col_form:
    section_header("📋 Data Produk")

    # card 1: product information
    st.markdown("""
<div class="input-card">
    <div class="input-card-title">📦 Informasi Produk</div>
</div>
""", unsafe_allow_html=True)
    cat_ui = st.selectbox(
        "Jenis Produk",
        options=list(CATEGORY_MAP.keys()),
        key="pred_cat_ui",
        help="Kategori produk menentukan sensitivitas spoilage bawaan",
    )

    # advanced fields: quality grade & region (stakeholder teknis only)
    if not is_retail:
        st.selectbox(
            "Quality Grade",
            options=["A - Sangat Baik", "B - Standar", "C - Kurang Baik"],
            key="pred_quality_grade",
        )
        st.selectbox(
            "Wilayah Distribusi",
            options=["Midwest", "Northeast", "Southeast", "Southwest", "West"],
            key="pred_region",
        )

    # card 2: storage conditions
    st.markdown("""
<div class="input-card" style="margin-top:.8rem;">
    <div class="input-card-title">🌡️ Kondisi Penyimpanan</div>
</div>
""", unsafe_allow_html=True)
    storage_opt = st.selectbox(
        "Suhu Penyimpanan",
        options=list(STORAGE_TEMP_MAP.keys()),
        key="pred_storage",
    )

    if not is_retail:
        st.selectbox(
            "Stabilitas Suhu",
            options=list(TEMP_DEV_MAP.keys()),
            key="pred_temp_dev",
        )
        st.selectbox(
            "Kejadian Abuse Suhu",
            options=list(ABUSE_MAP.keys()),
            key="pred_abuse",
        )
        st.selectbox(
            "Kualitas Kemasan",
            options=list(PACKAGING_MAP.keys()),
            key="pred_packaging",
        )
        st.selectbox(
            "Kualitas Penanganan",
            options=list(HANDLING_MAP.keys()),
            key="pred_handling",
        )

    # card 3: shelf life and stock
    st.markdown("""
<div class="input-card" style="margin-top:.8rem;">
    <div class="input-card-title">📅 Masa Simpan & Stok</div>
</div>
""", unsafe_allow_html=True)
    
    # initial stock - displayed for all roles as it's important for operations
    initial_qty = st.number_input(
        "Stok awal (unit)",
        min_value=1, max_value=10000, value=50, step=1,
        key="pred_initial_qty",
        help="Jumlah unit produk saat pertama kali masuk ke toko",
    )
    
    # units sold - displayed for all roles
    units_sold = st.number_input(
        "Unit sudah terjual",
        min_value=0, max_value=initial_qty, value=min(10, initial_qty), step=1,
        key="pred_units_sold",
        help="Berapa unit yang sudah berhasil dijual",
    )
    
    # calculate and display remaining stock in real-time
    sisa_stok_display = initial_qty - units_sold
    if sisa_stok_display > 0:
        stok_color = C['green'] if sisa_stok_display > initial_qty * 0.5 else C['orange'] if sisa_stok_display > initial_qty * 0.2 else C['red']
        st.markdown(f"""
<div style="font-size:.78rem; padding:.4rem .6rem; border-radius:6px;
            background:rgba(76,175,80,.07); border:1px solid rgba(76,175,80,.2);
            margin-top:.2rem; color:{stok_color}; font-weight:600;">
    📦 Sisa Stok: {sisa_stok_display} unit ({sisa_stok_display/initial_qty*100:.0f}% dari stok awal)
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div style="font-size:.78rem; padding:.4rem .6rem; border-radius:6px;
            background:rgba(244,67,54,.07); border:1px solid rgba(244,67,54,.2);
            margin-top:.2rem; color:{C['red']}; font-weight:600;">
    ⚠️ Stok Habis Terjual
</div>
""", unsafe_allow_html=True)
    
    days_expiry = st.number_input(
        "Sisa hari sebelum kadaluarsa",
        min_value=0, max_value=730, value=7, step=1,
        key="pred_days_expiry",
        help="Masukkan berapa hari lagi produk ini kadaluarsa",
    )

    if not is_retail:
        shelf_life = st.number_input(
            "Total shelf life produk (hari)",
            min_value=1, max_value=730, value=21, step=1,
            key="pred_shelf_life",
            help="Total masa simpan sejak produksi",
        )

    # card 4: price and margin
    st.markdown("""
<div class="input-card" style="margin-top:.8rem;">
    <div class="input-card-title">💰 Harga & Margin</div>
</div>
""", unsafe_allow_html=True)
    cost_price = st.number_input(
        "Harga modal per unit (Rp)",
        min_value=0.0, value=10000.0, step=500.0,
        key="pred_cost",
        format="%.0f",
    )
    sell_price = st.number_input(
        "Harga jual per unit (Rp)",
        min_value=0.0, value=15000.0, step=500.0,
        key="pred_sell",
        format="%.0f",
    )

    # calculate margin automatically
    if cost_price > 0 and sell_price > 0:
        markup = (sell_price - cost_price) / cost_price * 100
        margin_col = C["green"] if markup > 0 else C["red"]
        sign = "+" if markup >= 0 else ""
        st.markdown(f"""
<div style="font-size:.78rem; padding:.4rem .6rem; border-radius:6px;
            background:rgba(76,175,80,.07); border:1px solid rgba(76,175,80,.2);
            margin-top:.2rem; color:{margin_col}; font-weight:600;">
    💹 Markup: {sign}{markup:.1f}% &nbsp;·&nbsp;
    Margin: Rp {(sell_price - cost_price):,.0f}/unit
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    btn_predict = st.button(
        "🔍 Analisis Risiko Pembusukan",
        type="primary",
        use_container_width=True,
        key="btn_predict_main",
    )

# results column
with col_result:
    section_header("📊 Hasil Analisis")

    show_results = btn_predict or st.session_state.prediction_completed

    if not show_results:
        st.markdown(f"""
<div class="ibox blue" style="text-align:center; padding:2rem;">
    <div style="font-size:2.5rem; margin-bottom:.8rem;">🔮</div>
    <div style="font-size:.95rem; font-weight:600; color:{C['text']}; margin-bottom:.4rem;">
        Belum Ada Prediksi
    </div>
    <div style="font-size:.8rem; color:{C['muted']};">
        Isi data produk di kiri lalu klik<br>
        <b>Analisis Risiko Pembusukan</b>
    </div>
</div>
""", unsafe_allow_html=True)

    if show_results:
        # run new prediction
        if btn_predict:
            with st.spinner("⏳ Menganalisis produk..."):
                time.sleep(0.8)

                cat = CATEGORY_MAP[cat_ui]

                # get stock values from input (all roles now have access to these fields)
                initial_qty     = st.session_state.get("pred_initial_qty", 50)
                units_sold_val  = st.session_state.get("pred_units_sold", 10)

                # advanced values: use user input (stakeholder) or defaults (retail)
                if is_retail:
                    quality_grade   = "A"
                    region          = "Midwest"
                    temp_deviation  = 0.0
                    temp_abuse      = 0
                    packaging_score = 9
                    handling_score  = 9
                    shelf_life_days = days_expiry + 14
                else:
                    grade_raw       = st.session_state.get("pred_quality_grade", "A - Sangat Baik")
                    quality_grade   = grade_raw.split(" - ")[0]
                    region          = st.session_state.get("pred_region", "Midwest")
                    temp_deviation  = TEMP_DEV_MAP.get(st.session_state.get("pred_temp_dev","Sangat Stabil (tidak berubah)"), 0.0)
                    temp_abuse      = ABUSE_MAP.get(st.session_state.get("pred_abuse","Tidak Pernah (0×)"), 0)
                    packaging_score = PACKAGING_MAP.get(st.session_state.get("pred_packaging","Sangat Baik"), 9)
                    handling_score  = HANDLING_MAP.get(st.session_state.get("pred_handling","Hati-hati"), 8)
                    shelf_life_days = st.session_state.get("pred_shelf_life", 21)

                storage_temp = STORAGE_TEMP_MAP.get(storage_opt, 4.0)
                revenue      = sell_price * units_sold_val
                profit       = revenue - (cost_price * initial_qty)
                profit_m_pct = (profit / revenue * 100) if revenue > 0 else 0.0
                sisa_stok    = max(0, initial_qty - units_sold_val)

                input_data = {
                    "category"               : cat,
                    "region"                 : region,
                    "quality_grade"          : quality_grade,
                    "storage_temp"           : storage_temp,
                    "temp_deviation"         : temp_deviation,
                    "handling_score"         : handling_score,
                    "packaging_score"        : packaging_score,
                    "base_price"             : sell_price,
                    "cost_price"             : cost_price,
                    "daily_demand"           : 5.0,
                    "initial_quantity"       : initial_qty,
                    "days_until_expiry"      : days_expiry,
                    "temp_abuse_events"      : temp_abuse,
                    "shelf_life_days"        : shelf_life_days,
                    "supplier_score"         : 9,
                    "spoilage_sensitivity"   : SENSITIVITY_MAP.get(cat, 0.50),
                    "distribution_hours"     : 12.0,
                    "days_remaining_at_purchase": days_expiry,
                    "selling_price"          : sell_price,
                    "discount_pct"           : 0.0,
                    "markdown_applied"       : 0,
                    "units_sold"             : units_sold_val,
                    "demand_variability"     : 0.2,
                    "spoilage_risk"          : RISK_BASE_MAP.get(cat, 0.18),
                    "day_of_week"            : 0,
                    "is_weekend"             : 0,
                    "month"                  : 1,
                    "is_promoted"            : 0,
                    "revenue"                : revenue,
                    "profit"                 : profit,
                    "profit_margin_pct"      : profit_m_pct,
                }

                prob, feat_df = predictor.predict(input_data)

                # business logic adjustments
                if days_expiry > 90:
                    prob *= 0.10
                elif days_expiry > 30:
                    prob *= 0.30
                elif days_expiry > 14:
                    prob *= 0.60

                if sisa_stok > 0:
                    if days_expiry == 0:
                        prob += 0.70
                    elif days_expiry <= 2:
                        prob += 0.40
                    elif days_expiry <= 5:
                        prob += 0.15

                if cat in ["Frozen_Meals","Meat","Seafood","Dairy"] and storage_temp >= 20.0:
                    prob = max(prob, 0.90)

                markup_ratio = (sell_price - cost_price) / (cost_price + 1e-6)
                if markup_ratio > 0.50 and sisa_stok > 0:
                    prob += min(0.40, (markup_ratio - 0.50) * 0.30)

                prob = min(0.999, prob)

                user_inputs_display = {
                    "category_display"    : cat_ui,
                    "storage_temp_status" : storage_opt,
                }

                # save to session state
                st.session_state.prediction_completed     = True
                st.session_state.last_prediction_prob     = prob
                st.session_state.last_prediction_input_data = input_data
                st.session_state.last_prediction_feat_df  = feat_df
                st.session_state.last_user_inputs_display = user_inputs_display
                st.session_state.last_prediction_metrics  = {
                    "revenue"         : revenue,
                    "profit"          : profit,
                    "profit_margin_pct": profit_m_pct,
                    "sisa_stok"       : sisa_stok,
                    "potensi_rugi"    : sisa_stok * cost_price,
                }
                # context for ai assistant chat
                if prob < 0.25:
                    risk_level_str = "AMAN"
                elif prob < 0.50:
                    risk_level_str = "WASPADA"
                else:
                    risk_level_str = "BERISIKO TINGGI"

                st.session_state.prediction_context = {
                    "product_type"       : cat_ui,
                    "category_raw"       : cat,
                    "risk_level"         : risk_level_str,
                    "risk_probability"   : round(prob * 100, 1),
                    "days_until_expiry"  : days_expiry,
                    "storage_condition"  : storage_opt,
                    "cost_price"         : cost_price,
                    "selling_price"      : sell_price,
                    "sisa_stok"          : sisa_stok,
                    "timestamp"          : datetime.now().strftime("%d/%m/%Y %H:%M"),
                }
                # reset old ai report cache when new data arrives
                st.session_state.ai_analysis_report = None

        else:
            # retrieve from session state
            input_data         = st.session_state.last_prediction_input_data
            prob               = st.session_state.last_prediction_prob
            feat_df            = st.session_state.last_prediction_feat_df
            user_inputs_display= st.session_state.last_user_inputs_display or {}
            metrics            = st.session_state.last_prediction_metrics or {}
            revenue            = metrics.get("revenue", 0)
            profit             = metrics.get("profit", 0)
            profit_m_pct       = metrics.get("profit_margin_pct", 0.0)
            sisa_stok          = metrics.get("sisa_stok", 0)

            if input_data is None:
                st.info("👈 Klik tombol **Analisis Risiko** untuk memulai prediksi.")
                st.stop()

        # prediction result card
        if prob < 0.25:
            res_cls, res_label, res_badge, res_sub = (
                "res-green", "AMAN",
                "Risiko Rendah",
                "Produk dalam kondisi baik. Lanjutkan prosedur penyimpanan normal.",
            )
        elif prob < 0.50:
            res_cls, res_label, res_badge, res_sub = (
                "res-orange", "WASPADA",
                "Risiko Sedang",
                "Ada faktor yang perlu diperhatikan. Pertimbangkan tindakan pencegahan.",
            )
        else:
            res_cls, res_label, res_badge, res_sub = (
                "res-red", "BERISIKO TINGGI",
                "Tindakan Segera!",
                "Produk memerlukan penanganan hari ini untuk mencegah kerugian.",
            )

        prediction_result_card(prob, res_label, res_sub, res_badge, res_cls)
        st.markdown("<br>", unsafe_allow_html=True)

        # kpi metrics row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
<div class="kpi-wrap kpi-blue">
    <span class="kpi-icon">📅</span>
    <div class="kpi-lbl">Sisa Kadaluarsa</div>
    <div class="kpi-val">{days_expiry}</div>
    <div class="kpi-sub neu">hari lagi</div>
</div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
<div class="kpi-wrap kpi-orange">
    <span class="kpi-icon">📦</span>
    <div class="kpi-lbl">Sisa Stok</div>
    <div class="kpi-val">{sisa_stok}</div>
    <div class="kpi-sub neu">unit tersisa</div>
</div>""", unsafe_allow_html=True)
        with m3:
            potensi_rugi = sisa_stok * input_data.get("cost_price", 0)
            st.markdown(f"""
<div class="kpi-wrap kpi-red">
    <span class="kpi-icon">💸</span>
    <div class="kpi-lbl">Potensi Rugi</div>
    <div class="kpi-val">Rp{potensi_rugi/1000:.0f}k</div>
    <div class="kpi-sub dn">jika tidak laku</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # discount suggestion
        sell_p = input_data.get("selling_price", 0)
        cost_p = input_data.get("cost_price", 0)
        if sell_p <= cost_p:
            saran_diskon = "0% — Sudah harga modal" if prob < 0.50 else "10%–30% — Cuci gudang / potong rugi"
        else:
            if prob < 0.25:
                saran_diskon = "0% — Harga normal"
            elif prob < 0.50:
                saran_diskon = "10%–20%"
            else:
                saran_diskon = "30%–50% — Flash Sale hari ini"

        st.markdown(f"""
<div class="ibox {'green' if prob < 0.25 else 'orange' if prob < 0.50 else 'red'}">
    🏷️ <b>Saran Diskon Optimal:</b> &nbsp;<span style="font-size:1rem;font-weight:800;">{saran_diskon}</span>
</div>
""", unsafe_allow_html=True)

        # action recommendations
        if prob < 0.25:
            actions = [
                "Lanjutkan penyimpanan sesuai prosedur normal",
                "Pantau ulang saat mendekati 5 hari kadaluarsa",
                "Pastikan rotasi stok FIFO diterapkan",
            ]
        elif prob < 0.50:
            actions = [
                "Periksa kondisi suhu penyimpanan sekarang",
                "Pertimbangkan diskon 10–20% untuk percepat penjualan",
                "Pindahkan ke rak yang lebih terlihat pelanggan",
                "Cek ulang kondisi kemasan produk",
            ]
        else:
            actions = [
                "Berikan diskon 25–40% segera hari ini",
                "Lakukan flash sale atau program bundling",
                "Pindahkan ke area promosi / rak paling depan",
                "Periksa dan perbaiki sistem pendinginan",
                "Laporkan ke manajer toko untuk keputusan lanjut",
            ]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>💡 Rekomendasi Tindakan</h3>
</div>
""", unsafe_allow_html=True)
        for action in actions:
            st.markdown(f"- {action}")

        # shortcut button to ai assistant
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
<div class="ibox blue" style="text-align:center;">
    <b>Ingin analisis lebih mendalam?</b><br>
    <span style="font-size:.78rem;">Buka <b>AI Assistant</b> di menu navigasi untuk tanya-jawab
    seputar produk ini dengan Gemini AI.</span>
</div>
""", unsafe_allow_html=True)


# bottom section: contributing factors and ai report (full width)
if show_results and st.session_state.prediction_completed:
    st.divider()

    # contributing factors (stakeholder teknis only)
    if not is_retail:
        section_header("🔬 Faktor Penyebab Teknis")
        feat_df = st.session_state.last_prediction_feat_df
        if feat_df is not None:
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
                        format="%.1f%%",
                    ),
                    "Penyebab (Faktor Utama)": st.column_config.TextColumn(
                        "Faktor Penyebab Utama", width="large"
                    ),
                },
            )

    # ai analysis report
    section_header("🤖 AI Analysis Report")
    st.caption("Analisis mendalam dan rekomendasi berbasis Gemini AI")

    api_key = st.session_state.get("llm_api_key", "")
    input_data  = st.session_state.last_prediction_input_data
    prob        = st.session_state.last_prediction_prob
    user_inputs = st.session_state.last_user_inputs_display or {}

    if not api_key:
        st.markdown(f"""
<div class="ibox orange">
    <b>API Key belum dikonfigurasi.</b><br>
    Isi <b>Gemini API Key</b> di sidebar untuk mengaktifkan fitur AI Analysis Report.
</div>
""", unsafe_allow_html=True)
    else:
        col_gen, col_ref = st.columns([5, 1])
        with col_gen:
            if st.button(
                "📄 Generate AI Analysis Report",
                key="btn_gen_ai",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.generating_analysis = True
        with col_ref:
            if st.button("🔄", key="btn_ref_ai", help="Generate ulang (abaikan cache)", use_container_width=True):
                st.session_state.force_regenerate_analysis = True

        if st.session_state.get("generating_analysis") or st.session_state.get("force_regenerate_analysis"):
            with st.spinner("⏳ Menganalisis dengan Gemini AI..."):
                report = get_cached_or_generate_report(
                    input_data=input_data,
                    prob=prob,
                    user_inputs=user_inputs,
                    force_regenerate=st.session_state.get("force_regenerate_analysis", False),
                )
                if report:
                    st.session_state.ai_analysis_report = report
                    st.session_state.generating_analysis = False
                    st.session_state.force_regenerate_analysis = False
                    st.rerun()
                else:
                    st.error("❌ Gagal generate. Periksa API Key atau koneksi internet.")
                    st.session_state.generating_analysis = False
                    st.session_state.force_regenerate_analysis = False

        if st.session_state.get("ai_analysis_report"):
            st.markdown('<div class="ai-report-card">', unsafe_allow_html=True)
            display_analysis_report(st.session_state.ai_analysis_report)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption("✓ Hasil di-cache. Klik 🔄 untuk generate ulang.")
        else:
            st.markdown(f"""
<div class="ibox green" style="text-align:center;">
    Klik <b>Generate AI Analysis Report</b> untuk mendapatkan rekomendasi
    mendalam dari Gemini berdasarkan data produk ini.
</div>
""", unsafe_allow_html=True)
