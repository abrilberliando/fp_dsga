# ♻️ Food Waste Recommendation System

Aplikasi Streamlit multipage untuk prediksi dan rekomendasi pengelolaan food waste.

---

## 🗂️ Struktur Proyek

```
food_waste_app/
├── app.py                    ← Entry point & konfigurasi navigasi
│
├── pages/
│   ├── dashboard_awal.py     ← 🏠 Dashboard & overview statistik
│   ├── prediksi.py           ← 🔮 Form prediksi & hasil rekomendasi + AI Analysis
│   ├── deskripsi_model.py    ← 📖 Dokumentasi & evaluasi model
│   ├── ai_gemini_model.py    ← 🤖 Gemini API configuration & testing
│   └── chatbot_model.py      ← 💬 Chatbot interaktif
│
├── assets/
│   └── logo.png              ← Logo aplikasi (letakkan di sini)
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py            ← Helper functions & reusable components
│   ├── predictor.py          ← ML model loading & prediction logic
│   ├── gemini_analyzer.py    ← 🔑 Google Gemini API integration untuk AI Analysis
│   └── chatbot.py            ← Integrasi LLM untuk chatbot
│
├── models/
│   ├── __init__.py           
│   ├── xgboost_model.pkl     ← Trained XGBoost model
│   ├── label_encoders.pkl    ← Feature encoders
│   └── feature_names.pkl     ← Feature names list
│
├── requirements.txt
└── README.md
```

---

## 🚀 Cara Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan aplikasi
```bash
streamlit run app.py
```

### 3. Buka di browser
```
http://localhost:8501
```

---

## 🗺️ Navigasi Sidebar & Fitur

| Menu             | Halaman               | Deskripsi                              |
|------------------|-----------------------|----------------------------------------|
| 🏠 Dashboard Awal | `dashboard_awal.py`   | Statistik utama & visualisasi data    |
| 🔮 Prediksi       | `prediksi.py`         | Form input & hasil prediksi ML + **🤖 AI Analysis Report** |
| 🤖 AI Model Description | `ai_gemini_model.py` | Setup & testing Gemini API |
| 📖 ML Model Description | `deskripsi_model.py` | Arsitektur, performa & metadata model |
| 💬 Chatbot Model  | `chatbot_model.py`    | Tanya jawab interaktif dengan LLM     |

### Fitur Utama per Halaman

**Prediksi (🔮)**
- Input data produk (kategori, kualitas, kondisi penyimpanan, stok, harga)
- ML prediction dengan XGBoost
- Business analysis (profit, loss potential, diskon rekomendasi)
- Feature importance visualization
- **🔑 NEW: AI Analysis Report** - Analisis mendalam berbasis Gemini AI

---

## 🔑 Konfigurasi Gemini API (AI Analysis Report)

Aplikasi menggunakan **Google Gemini AI** untuk menganalisis hasil prediksi dan memberikan rekomendasi operasional yang actionable.

### Setup Gemini API

#### 1. Dapatkan API Key
1. Kunjungi [Google AI Studio](https://ai.google.dev)
2. Klik **"Get API Key"** 
3. Pilih atau buat project baru
4. Copy API key yang dihasilkan

#### 2. Input API Key di Aplikasi
1. Jalankan aplikasi: `streamlit run app.py`
2. Buka sidebar di sebelah kiri
3. Masukkan API key di field **"🔑 API Key"**
4. Sistem akan menampilkan ✓ jika valid

#### 3. Gunakan Fitur AI Analysis Report
1. Buka halaman **🔮 Prediksi**
2. Isi form data produk (4 section)
3. Klik **"🔍 Cek Risiko Pembusukan Dari Seluruh Data"**
4. Setelah hasil prediksi muncul, scroll ke bawah
5. Klik **"📄 Generate AI Analysis Report"**
6. Tunggu AI menganalisis (~ 30-60 detik)
7. Hasil ditampilkan dalam card hijau dengan 7 section analisis

### Fitur AI Analysis Report

**Output mencakup:**
1. **Ringkasan Kondisi Produk** - Status produk saat ini
2. **Analisis Risiko** - Penjelasan probabilitas risk dari model
3. **Faktor yang Berpengaruh** - Top factors yang paling material
4. **Rekomendasi Tindakan** - Action items prioritas (urgent, medium, long-term)
5. **Strategi Penjualan** - Diskon optimal & timing penjualan
6. **Saran Pengelolaan Inventaris** - Display, monitoring, koordinasi
7. **Kesimpulan** - Executive summary & prioritas manager

**Karakteristik:**
- ✅ Menggunakan model **Gemini 2.5 Flash** untuk response cepat
- ✅ Prompt dinamis berdasarkan data aktual produk
- ✅ Tidak hardcode field names atau struktur data
- ✅ **Smart caching** - Tidak request ulang untuk data yang sama
- ✅ Bahasa Indonesia profesional & actionable
- ✅ Fokus pada impact finansial & operational efficiency

### Caching & Performance

- Hasil analisis di-cache secara otomatis
- Cache key berdasarkan: kategori, stok, hari kadaluarsa, suhu, probabilitas
- Refresh manual dengan tombol 🔄 (force regenerate)
- Session cache (hilang saat halaman di-refresh)

---

## ⚙️ Pengembangan Lanjutan

### Menambahkan Model ML
1. Simpan file model ke folder `models/` (contoh: `models/xgboost_model.pkl`)
2. Buat `models/model_config.json` berisi metadata model
3. Gunakan `load_model()` dari `utils/helpers.py`
4. Implementasikan logika prediksi di `pages/prediksi.py`

### Mengaktifkan Chatbot
1. Pilih provider LLM (OpenAI / Gemini / lainnya)
2. Tambahkan API key ke `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
3. Implementasikan `get_chat_response()` di `utils/chatbot.py`

### Customize AI Analysis Prompt
Edit file `utils/gemini_analyzer.py`:
- Fungsi `get_system_prompt()` - Ubah system instruction
- Fungsi `build_analysis_prompt()` - Ubah format atau section output
- Fungsi `generate_analysis_report()` - Ubah model atau parameters API

### Menambahkan Logo
1. Letakkan file `logo.png` di folder `assets/`
2. Logo akan otomatis tampil di bagian atas sidebar

---

## 📦 Requirements Utama

- **Python** >= 3.9
- **Streamlit** >= 1.36.0 (diperlukan untuk `st.navigation` API)
- **XGBoost** >= 2.0.0 (model ML)
- **Google Generative AI** >= 0.4.0 (untuk Gemini Analysis)
- Lihat `requirements.txt` untuk daftar lengkap

### Optional Dependencies
- **Plotly** - Interactive visualizations
- **Seaborn & Matplotlib** - Static plots
- **SHAP** - Model explainability

---

## 🏗️ Teknologi

- **Frontend**: Streamlit
- **Backend/ML**: scikit-learn, pandas, numpy, XGBoost
- **Visualisasi**: Plotly, Matplotlib, Seaborn
- **AI/LLM**: Google Gemini API (`google-generativeai`)
- **Model Explainability**: SHAP
