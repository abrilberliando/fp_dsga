"""
utils/gemini_analyzer.py
========================
Modul untuk menganalisis hasil prediksi menggunakan Google Gemini API.

Fitur:
- Generate analysis report berdasarkan data produk dan hasil prediksi
- Format response dinamis sesuai data yang tersedia
- Caching hasil untuk menghindari request ulang
- Error handling dan fallback
"""

import streamlit as st
import google.generativeai as genai
import json
import hashlib
from typing import Dict, Optional, Any


def create_analysis_cache_key(input_data: dict, prob: float) -> str:
    """
    Buat unique key untuk caching hasil analisis.
    
    Args:
        input_data: Dictionary data input produk
        prob: Probability hasil prediksi
    
    Returns:
        Hash string untuk digunakan sebagai cache key
    """
    def normalize_value(value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, (str, bool, int, float)):
            return value
        if isinstance(value, dict):
            return {k: normalize_value(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [normalize_value(v) for v in value]
        try:
            if hasattr(value, "__float__"):
                return float(value)
        except (TypeError, ValueError):
            pass
        try:
            if hasattr(value, "__int__"):
                return int(value)
        except (TypeError, ValueError):
            pass
        return str(value)

    cache_payload = {
        "category": normalize_value(input_data.get("category")),
        "initial_quantity": normalize_value(input_data.get("initial_quantity")),
        "units_sold": normalize_value(input_data.get("units_sold")),
        "days_until_expiry": normalize_value(input_data.get("days_until_expiry")),
        "storage_temp": normalize_value(input_data.get("storage_temp")),
        "temp_deviation": normalize_value(input_data.get("temp_deviation")),
        "probability": round(float(prob), 4)
    }

    cache_string = json.dumps(cache_payload, sort_keys=True)
    return hashlib.md5(cache_string.encode()).hexdigest()


def build_analysis_prompt(input_data: dict, prob: float, user_inputs: dict) -> str:
    """
    Membangun prompt Gemini secara dinamis berdasarkan data yang tersedia.
    
    Args:
        input_data: Dictionary hasil preprocessing dengan semua feature
        prob: Probabilitas risiko dari model prediksi (0-1)
        user_inputs: Dictionary input original dari form user (untuk human-friendly names)
    
    Returns:
        Prompt string untuk dikirim ke Gemini
    """
    
    # Ekstrak data penting dengan safe defaults
    category = input_data.get("category", "Unknown")
    region = input_data.get("region", "Unknown")
    quality_grade = input_data.get("quality_grade", "B")
    storage_temp = input_data.get("storage_temp", 0)
    temp_deviation = input_data.get("temp_deviation", 0)
    initial_quantity = input_data.get("initial_quantity", 0)
    units_sold = input_data.get("units_sold", 0)
    days_until_expiry = input_data.get("days_until_expiry", 0)
    shelf_life_days = input_data.get("shelf_life_days", 0)
    cost_price = input_data.get("cost_price", 0)
    selling_price = input_data.get("selling_price", 0)
    base_price = input_data.get("base_price", 0)
    handling_score = input_data.get("handling_score", 5)
    packaging_score = input_data.get("packaging_score", 5)
    temp_abuse_events = input_data.get("temp_abuse_events", 0)
    spoilage_sensitivity = input_data.get("spoilage_sensitivity", 0.5)
    discount_pct = input_data.get("discount_pct", 0)
    profit = input_data.get("profit", 0)
    revenue = input_data.get("revenue", 0)
    
    # Hitung sisa stok dan data bisnis
    remaining_stock = initial_quantity - units_sold
    stock_value_at_cost = remaining_stock * cost_price
    potential_loss = stock_value_at_cost  # Jika seluruh stok rusak
    profit_margin_pct = (profit / revenue * 100) if revenue > 0 else 0
    
    # Kategori human-friendly dari user input
    user_category_display = user_inputs.get("category_display", category)
    user_quality_display = user_inputs.get("quality_display", quality_grade)
    user_temp_status = user_inputs.get("storage_temp_status", "Unknown")
    user_temp_stability = user_inputs.get("temp_deviation_status", "Unknown")
    user_temp_abuse_freq = user_inputs.get("temp_abuse_events_status", "Unknown")
    user_packaging_status = user_inputs.get("packaging_status", "Unknown")
    user_handling_status = user_inputs.get("handling_status", "Unknown")
    
    # Risk level interpretation
    if prob < 0.15:
        risk_level = "RENDAH"
        risk_description = "Produk dalam kondisi aman dengan kemungkinan pembusukan minimal"
    elif prob < 0.40:
        risk_level = "SEDANG"
        risk_description = "Produk memiliki beberapa faktor risiko yang perlu dimonitor"
    else:
        risk_level = "TINGGI"
        risk_description = "Produk berisiko tinggi dan memerlukan tindakan segera"
    
    # Build prompt dinamis
    prompt = f"""Anda adalah Senior Retail Operations Specialist yang ahli dalam food waste management dan inventory optimization.

KONTEKS HASIL PREDIKSI MODEL MACHINE LEARNING:
===============================================
Saya telah menjalankan model machine learning (XGBoost) untuk memprediksi risiko pembusukan produk retail.

HASIL PREDIKSI:
- Probabilitas Risiko Pembusukan: {prob*100:.2f}%
- Kategori Risiko: {risk_level}
- Interpretasi: {risk_description}

DATA PRODUK YANG DIANALISIS:
============================
Informasi Dasar:
- Jenis Produk: {user_category_display} ({category})
- Wilayah Toko: {region}
- Kualitas Produk: {user_quality_display}
- Sensitivitas Produk terhadap Pembusukan: {spoilage_sensitivity:.0%}

Kondisi Penyimpanan Saat Ini:
- Status Suhu: {user_temp_status} (Aktual: {storage_temp:.1f}°C)
- Stabilitas Suhu: {user_temp_stability} (Deviasi: ±{temp_deviation:.1f}°C)
- Frekuensi Gangguan Pendingin: {user_temp_abuse_freq} (Total: {temp_abuse_events} kali)
- Kondisi Kemasan: {user_packaging_status} (Score: {packaging_score}/10)
- Tingkat Kehati-hatian Penanganan: {user_handling_status} (Score: {handling_score}/10)

Masa Simpan & Inventory:
- Daya Tahan Total Produk: {shelf_life_days} hari
- Sisa Hari Sebelum Kadaluarsa: {days_until_expiry} hari
- Stok Awal: {initial_quantity} unit
- Stok Terjual: {units_sold} unit
- Sisa Stok Belum Terjual: {remaining_stock} unit

Analisis Finansial:
- Harga Modal per Unit: Rp {cost_price:,.0f}
- Harga Jual Normal: Rp {base_price:,.0f}
- Harga Jual Saat Ini: Rp {selling_price:,.0f}
- Diskon Saat Ini: {discount_pct:.1f}%
- Total Revenue (dari stok terjual): Rp {revenue:,.0f}
- Profit Saat Ini: Rp {profit:,.0f}
- Profit Margin: {profit_margin_pct:.1f}%
- Nilai Stok Sisa (di harga modal): Rp {stock_value_at_cost:,.0f}
- Potensi Kerugian Jika Semua Rusak: Rp {potential_loss:,.0f}

TUGAS ANDA:
===========
Berdasarkan data di atas dan hasil prediksi model, lakukan analisis mendalam dan berikan rekomendasi operasional.

OUTPUT HARUS DALAM FORMAT BERIKUT (Gunakan heading dan formatting yang jelas):

1. **RINGKASAN KONDISI PRODUK**
   - Berikan deskripsi terperinci kondisi produk saat ini.
   - Sorot setidaknya 2-3 risiko utama dan kondisi kritis.

2. **ANALISIS RISIKO**
   - Jelaskan mengapa probabilitas risiko mencapai {prob*100:.2f}%.
   - Identifikasi faktor utama yang mempengaruhi risiko.
   - Bandingkan dengan standar industri atau praktik terbaik jika relevan.

3. **FAKTOR YANG BERPENGARUH**
   - Tampilkan 4-6 faktor kritis yang memengaruhi risiko.
   - Jelaskan setiap faktor dengan dampak numerik atau level prioritas.

4. **REKOMENDASI TINDAKAN**
   - Berikan minimal 3 rekomendasi prioritas segera.
   - Sertakan 2-3 rekomendasi jangka menengah (2-7 hari).
   - Tambahkan 2-3 langkah preventif jangka panjang.
   - Jelaskan alasan dan hasil yang diharapkan untuk setiap rekomendasi.

5. **STRATEGI PENJUALAN**
   - Usulkan strategi diskon optimal dengan angka/rentang diskon.
   - Tentukan waktu pelaksanaan dan target segmen pelanggan.
   - Sarankan metode promosi atau bundling spesifik.
   - Sertakan proyeksi ROI atau dampak finansial singkat.

6. **SARAN PENGELOLAAN INVENTARIS**
   - Jelaskan cara terbaik menata dan menampilkan produk di rak.
   - Sebutkan monitoring kritis yang harus dilaksanakan.
   - Rekomendasikan koordinasi antar tim (warehouse, marketing, penjualan).
   - Berikan mekanisme early warning untuk mencegah pembusukan.

7. **KESIMPULAN**
   - Tuliskan ringkasan eksekutif 3-5 baris.
   - Tegaskan 3 prioritas utama yang harus dilakukan hari ini.

KETENTUAN PENULISAN:
- Gunakan Bahasa Indonesia yang profesional, jelas, dan komunikatif.
- Tulis minimal 700 kata.
- Jangan berhenti sebelum semua 7 bagian selesai.
- Sajikan setiap poin dalam bullet atau subheading yang terstruktur.
- Setiap rekomendasi harus memiliki dasar numerik atau alasan logis.
- Hindari jawaban sangat singkat; berikan konteks, data, dan justifikasi.
- Jika output tampak terputus, lanjutkan sampai semua bagian selesai.
- Jika perlu, gunakan contoh tindakan operasional yang realistis.
- Gunakan istilah yang mudah dipahami manajemen retail.

BERIKAN jawaban yang komprehensif, spesifik, dan actionable.

Mulai analisis sekarang:
"""
    
    return prompt


def generate_analysis_report(
    input_data: dict,
    prob: float,
    user_inputs: dict,
    api_key: Optional[str] = None
) -> Optional[str]:
    """
    Generate AI Analysis Report menggunakan Gemini API.
    
    Args:
        input_data: Dictionary hasil preprocessing dengan semua feature
        prob: Probabilitas risiko dari model (0-1)
        user_inputs: Dictionary input original dari form (untuk display names)
        api_key: API key untuk Gemini (jika None, ambil dari session state)
    
    Returns:
        String berisi analysis report, atau None jika gagal
    """
    
    # Ambil API key dari argument atau session state
    if api_key is None:
        api_key = st.session_state.get("llm_api_key", "")
    
    if not api_key:
        st.error("❌ API Key belum dikonfigurasi. Silakan isi API Key di sidebar.")
        return None
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Build prompt dinamis
        prompt = build_analysis_prompt(input_data, prob, user_inputs)
        
        # Generate content
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                top_p=0.92,
                top_k=40,
                max_output_tokens=4096,
            )
        )
        
        if response.text:
            return response.text
        else:
            return None
            
    except Exception as e:
        st.error(f"❌ Gagal generate analysis: {str(e)}")
        return None


def get_cached_or_generate_report(
    input_data: dict,
    prob: float,
    user_inputs: dict,
    force_regenerate: bool = False
) -> Optional[str]:
    """
    Ambil analysis report dari cache, atau generate jika belum ada.
    
    Args:
        input_data: Dictionary hasil preprocessing
        prob: Probabilitas risiko
        user_inputs: Dictionary input original
        force_regenerate: Force regenerate meskipun sudah ada di cache
    
    Returns:
        String berisi analysis report, atau None jika gagal
    """
    
    # Create cache key
    cache_key = create_analysis_cache_key(input_data, prob)
    
    # Initialize cache storage jika belum ada
    if "gemini_analysis_cache" not in st.session_state:
        st.session_state.gemini_analysis_cache = {}
    
    # Return cached result jika ada dan tidak force regenerate
    if not force_regenerate and cache_key in st.session_state.gemini_analysis_cache:
        return st.session_state.gemini_analysis_cache[cache_key]
    
    # Generate report baru
    report = generate_analysis_report(input_data, prob, user_inputs)
    
    # Cache hasil jika berhasil
    if report:
        st.session_state.gemini_analysis_cache[cache_key] = report
    
    return report


def display_analysis_report(report: str, container=None) -> None:
    """
    Display analysis report dalam format yang menarik.
    
    Args:
        report: String berisi analysis report dari Gemini
        container: Streamlit container untuk menampilkan (default: main)
    """
    
    if container is None:
        container = st
    
    # Display dalam markdown dengan styling
    container.markdown(report)


def clear_analysis_cache() -> None:
    """Clear semua cached analysis reports."""
    if "gemini_analysis_cache" in st.session_state:
        st.session_state.gemini_analysis_cache.clear()
