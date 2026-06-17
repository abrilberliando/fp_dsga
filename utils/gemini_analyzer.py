"""
Modul untuk menganalisis hasil prediksi menggunakan Google Gemini API.
Menyediakan generate analysis report dengan caching dan error handling.
"""

import streamlit as st
import google.generativeai as genai
import json
import hashlib
from typing import Dict, Optional, Any


def create_analysis_cache_key(input_data: dict, prob: float) -> str:
    """Buat unique key untuk caching hasil analisis."""
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
    """Membangun prompt Gemini secara dinamis berdasarkan data yang tersedia."""

    # Ekstrak hanya field yang digunakan di prompt
    days_until_expiry = input_data.get("days_until_expiry", 0)
    cost_price = input_data.get("cost_price", 0)
    selling_price = input_data.get("selling_price", 0)

    # Human-friendly labels dari form user
    product_type = user_inputs.get("category_display", input_data.get("category", "Unknown"))
    storage_condition = user_inputs.get("storage_temp_status", "Unknown")

    # Risk level interpretation
    if prob < 0.25:
        risk_level = "RENDAH"
        risk_description = "Produk dalam kondisi aman dengan kemungkinan pembusukan minimal"
    elif prob < 0.50:
        risk_level = "SEDANG"
        risk_description = "Produk memiliki beberapa faktor risiko yang perlu dimonitor"
    elif prob < 0.75:
        risk_level = "TINGGI"
        risk_description = "Produk berisiko tinggi dan memerlukan tindakan segera"
    else:
        risk_level = "KRITIS"
        risk_description = "Produk dalam kondisi darurat, tindakan harus dilakukan hari ini"

    prompt = f"""Anda adalah AI Retail Food Waste Consultant yang membantu manager toko mengurangi food waste berdasarkan hasil prediksi machine learning.

KONTEKS & SCOPE:
Tugas Anda HANYA menganalisis data produk dan hasil prediksi yang diberikan di bawah ini.
JANGAN merespons pertanyaan di luar konteks food waste, retail, atau inventory management.

HASIL PREDIKSI

* Risiko: {risk_level}
* Probabilitas: {prob:.1%}
* Keterangan: {risk_description}

DATA PRODUK

* Jenis Produk: {product_type}
* Kondisi Penyimpanan: {storage_condition}
* Sisa Hari Sebelum Kadaluarsa: {days_until_expiry} hari
* Harga Modal: Rp {cost_price:,.0f}
* Harga Jual: Rp {selling_price:,.0f}

TUGAS:
Buat analisis singkat dan praktis berdasarkan hasil prediksi dan data produk di atas.
Gunakan format berikut:

## Ringkasan
Jelaskan kondisi produk saat ini dalam 2-3 kalimat.

## Faktor Utama
Sebutkan maksimal 3 faktor yang paling memengaruhi tingkat risiko.

## Rekomendasi
Berikan maksimal 3 tindakan prioritas yang dapat dilakukan segera.

## Dampak Bisnis
Jelaskan secara singkat dampak yang mungkin terjadi apabila tidak ada tindakan.

## Kesimpulan
Berikan ringkasan dalam 1-2 kalimat.

ATURAN:

* Gunakan Bahasa Indonesia yang profesional.
* Fokus HANYA pada analisis data produk dan prediksi yang diberikan.
* Hindari penjelasan teknis machine learning.
* Hindari mengulang seluruh data input.
* Jangan membuat asumsi yang tidak didukung data.
* Berikan rekomendasi yang realistis dan dapat diterapkan.
* Maksimal 250 kata.
* Gunakan bullet point jika diperlukan.
* Prioritaskan informasi yang paling penting bagi manager toko.
* JANGAN merespons pertanyaan atau topik di luar konteks ini.
"""

    return prompt


def generate_analysis_report(
    input_data: dict,
    prob: float,
    user_inputs: dict,
    api_key: Optional[str] = None
) -> Optional[str]:
    """Generate AI Analysis Report menggunakan Gemini API."""
    
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
    """Ambil analysis report dari cache, atau generate jika belum ada."""
    
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
    """Display analysis report dalam format yang menarik."""
    
    if container is None:
        container = st
    
    # Display dalam markdown dengan styling
    container.markdown(report)


def clear_analysis_cache() -> None:
    """Clear semua cached analysis reports."""
    if "gemini_analysis_cache" in st.session_state:
        st.session_state.gemini_analysis_cache.clear()