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
│   ├── prediksi.py           ← 🔮 Form prediksi & hasil rekomendasi
│   ├── deskripsi_model.py    ← 📖 Dokumentasi & evaluasi model
│   └── chatbot_model.py      ← 🤖 Chatbot interaktif
│
├── assets/
│   └── logo.png              ← Logo aplikasi (letakkan di sini)
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py            ← Helper functions & reusable components
│   └── chatbot.py            ← Integrasi LLM untuk chatbot
│
├── models/
│   └── __init__.py           ← Simpan model .pkl / .h5 di sini
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

## 🗺️ Navigasi Sidebar

| Menu             | Halaman               | Deskripsi                              |
|------------------|-----------------------|----------------------------------------|
| 🏠 Dashboard Awal | `dashboard_awal.py`   | Statistik utama & visualisasi data    |
| 🔮 Prediksi       | `prediksi.py`         | Form input & hasil prediksi ML        |
| 📖 Deskripsi Model| `deskripsi_model.py`  | Arsitektur, performa & metadata model |
| 🤖 Chatbot Model  | `chatbot_model.py`    | Tanya jawab interaktif dengan LLM     |

---

## ⚙️ Pengembangan Lanjutan

### Menambahkan Model ML
1. Simpan file model ke folder `models/` (contoh: `models/food_waste_model.pkl`)
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

### Menambahkan Logo
1. Letakkan file `logo.png` di folder `assets/`
2. Logo akan otomatis tampil di bagian atas sidebar

---

## 📦 Requirements Utama

- **Python** >= 3.9
- **Streamlit** >= 1.36.0 (diperlukan untuk `st.navigation` API)
- Lihat `requirements.txt` untuk daftar lengkap

---

## 🏗️ Teknologi

- **Frontend**: Streamlit
- **Backend/ML**: scikit-learn, pandas, numpy
- **Visualisasi**: Plotly, Matplotlib, Seaborn
- **LLM** *(opsional)*: OpenAI / Google Gemini / LangChain
