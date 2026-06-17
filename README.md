# ♻️ Food Waste Recommendation System

Sistem prediksi dan rekomendasi AI untuk pengelolaan food waste di retail. Mengintegrasikan XGBoost untuk prediksi risiko pembusukan dan Google Gemini AI untuk rekomendasi operasional.

---

## 🎯 Fitur Utama

### Untuk Retail Manager (Mode Operasional)
- **Prediksi Risiko**: Input data produk dan dapatkan probabilitas risiko pembusukan real-time
- **AI Analysis Report**: Rekomendasi mendalam dari Gemini AI dengan 7 section insight
- **Chat Assistant**: Tanya jawab kontekstual dengan AI untuk keputusan operasional

### Untuk Stakeholder Teknis (Mode Analitik)
- **Dashboard & Data Exploration**: Statistik 100K records, trend analysis, distribusi kategori & region
- **Performa Model ML**: Evaluasi metrics, confusion matrix, ROC curve, feature importance
- **Gemini Documentation**: API configuration, system prompt, workflow architecture
- Akses penuh ke semua fitur Retail Manager

---

## 🗂️ Struktur Proyek

```
food_waste_app/
├── app.py                       ← Entry point, role-based navigation
│
├── pages/
│   ├── dashboard_awal.py        ← Dashboard statistik & visualisasi data
│   ├── prediksi.py              ← Form prediksi + AI Analysis Report
│   ├── deskripsi_model.py       ← Dokumentasi & evaluasi model ML
│   └── ai_gemini_model.py       ← Chat Assistant dengan konteks prediksi
│
├── utils/
│   ├── theme.py                 ← CSS global, color palette, Plotly config
│   ├── helpers.py               ← Utility functions & UI components
│   ├── predictor.py             ← Model loading & prediction logic
│   └── gemini_analyzer.py       ← Gemini API integration untuk AI reports
│
├── models/
│   ├── xgboost_model.pkl        ← Trained XGBoost model (SMOTE balanced)
│   ├── label_encoders.pkl       ← Encoders untuk categorical features
│   ├── feature_names.pkl        ← Feature names dari training
│   ├── metrics.json             ← Model performance metrics
│   ├── confusion_matrix.pkl     ← Confusion matrix untuk evaluation
│   ├── roc_data.pkl             ← ROC curve data (FPR, TPR, AUC)
│   ├── classification_report.json ← Detailed classification metrics
│   └── model_comparison.json    ← XGBoost vs CatBoost comparison
│
├── data/
│   └── perishable_goods_management.csv  ← Dataset (100K records)
│
├── notebooks/
│   └── XGBoost_CatBoost_Perishable_Goods.ipynb  ← EDA & training notebook
│
├── docs/
│   ├── skenario.md              ← Original requirements document
│   └── AI_ANALYSIS_REPORT.md    ← AI feature design documentation
│
├── train_model.py               ← Training script XGBoost + SMOTE
├── train_comparison.py          ← Comparison script XGBoost vs CatBoost
├── requirements.txt             ← Python dependencies
└── README.md                    ← Dokumentasi lengkap
```

---

## 🚀 Setup & Instalasi

### 1. Clone atau Extract Project
```bash
cd food_waste_app/
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
streamlit run app.py
```

### 4. Buka Browser
```
http://localhost:8501
```

### 5. Setup Gemini API Key
Untuk mengaktifkan AI Analysis & Chat features:
1. Dapatkan API key dari [Google AI Studio](https://ai.google.dev)
2. Di sidebar aplikasi, masukkan key di field "Gemini API Key"
3. Klik tombol "Test Connection" di halaman AI Assistant untuk verifikasi
4. Fitur AI akan otomatis aktif setelah key tervalidasi

---

## 👥 Role-Based Access

Aplikasi mendukung 2 role pengguna yang dapat dipilih di sidebar:

### 🛒 Retail Manager (Mode Operasional)

**Target User**: Manager toko, staff operasional, decision maker harian

**Halaman yang Tersedia:**

**1. Prediksi Risiko** (`prediksi.py`)
- Form input data produk: kategori, kondisi storage, stok, harga, supplier
- Real-time prediction: probabilitas risiko pembusukan (0-100%)
- Risk categorization: AMAN, WASPADA, BAHAYA, KRITIS
- Rekomendasi tindakan berdasarkan risk level
- Estimasi kerugian potensial & strategi diskon otomatis
- Feature importance visualization untuk produk spesifik
- **AI Analysis Report**: 7 section mendalam dari Gemini AI
  - Ringkasan kondisi produk
  - Analisis risiko
  - Faktor yang berpengaruh
  - Rekomendasi tindakan (urgent, medium, long-term)
  - Strategi penjualan & diskon
  - Saran pengelolaan inventaris
  - Kesimpulan & prioritas

**2. AI Assistant** (`ai_gemini_model.py`)
- Chat dengan Gemini AI tentang produk & inventory management
- Context-aware: otomatis gunakan data dari prediksi terakhir
- Suggested questions berdasarkan risk level
- Rekomendasi operasional real-time
- API configuration & connection testing

---

### 🔬 Stakeholder Teknis (Mode Analitik)

**Target User**: Data scientist, ML engineer, technical stakeholder, management

**Halaman Tambahan:**

**1. Dashboard & Data** (`dashboard_awal.py`)
- **Overview Statistics**: 100K records, 42 features, class distribution
- **KPI Cards**: Spoilage rate, waste cost, profit margin, demand forecast
- **Trend Analysis**: Monthly spoilage trends dengan smoothing
- **Distribusi Kategori**: Bar chart dengan spoilage percentage
- **Distribusi Region**: Geographic analysis
- **Category × Region Heatmap**: Spoilage rate breakdown
- **EDA Features**: Boxplot, scatter, correlation heatmap
- **Feature Importance**: Top 15 features dari model

**2. Performa Model** (`deskripsi_model.py`)
- **Overview**: Model architecture, dataset info, training pipeline
- **Performance Metrics**: Accuracy, Precision, Recall, F1, AUC
- **Model Comparison**: XGBoost vs CatBoost side-by-side
- **Evaluation Curves**: Confusion matrix, ROC curve dengan Plotly
- **Classification Report**: Per-class metrics detail
- **Feature Analysis**: Top 10 feature importance + full ranking
- **Metadata**: Model files status, parameters, training info
- Link ke Jupyter notebook untuk deep dive

**3. Gemini Documentation** (`ai_gemini_model.py` - full access)
- Gemini model information & capabilities
- API configuration & live connection testing
- System prompt documentation
- AI workflow architecture & data flow
- Plus Chat Assistant feature

**4. Plus**: Semua fitur Retail Manager (Prediksi + AI Assistant)

---

## 🤖 AI Analysis Report (Gemini Integration)

### Apa itu AI Analysis Report?
Fitur yang mengintegrasikan hasil prediksi ML dengan Google Gemini AI untuk menghasilkan rekomendasi operasional yang actionable dan context-aware.

### Cara Kerja
1. User mengisi form prediksi produk di halaman **Prediksi Risiko**
2. Model XGBoost menghitung probabilitas risiko pembusukan
3. User klik tombol **"Generate AI Analysis Report"**
4. Data produk & hasil prediksi dikirim ke Gemini API dengan prompt terstruktur
5. Gemini AI menganalisis dan menghasilkan 7 section rekomendasi:
   - **Ringkasan Kondisi Produk**: Overview status & prognosis
   - **Analisis Risiko**: Interpretasi probabilitas & kategori risiko
   - **Faktor yang Berpengaruh**: Top 3-5 faktor kritis dari feature importance
   - **Rekomendasi Tindakan**: Aksi konkret berdasarkan urgency (immediate, short-term, long-term)
   - **Strategi Penjualan & Diskon**: Pricing recommendations dengan justifikasi bisnis
   - **Saran Pengelolaan Inventaris**: Inventory actions (reorder, clearance, promotion)
   - **Kesimpulan & Prioritas**: Executive summary & next steps

### Features
- **Smart Caching**: Hasil di-cache berdasarkan kombinasi data produk (menghindari duplicate API calls)
- **Dynamic Prompt**: Prompt disesuaikan dengan data aktual & feature importance
- **Context-Aware**: Menggunakan probabilitas model & feature contribution
- **Bahasa Indonesia**: Output profesional, praktis, dan actionable
- **Force Regenerate**: Tombol "Regenerate Report" untuk analisis ulang

### Model & Configuration
- **Model**: Gemini 2.5 Flash (latest generation)
- **Temperature**: 0.7 (balance between creativity & consistency)
- **Max Tokens**: 2048
- **Language**: Bahasa Indonesia
- **Provider**: Google AI (generativeai SDK)

### API Key Setup
1. Buka [Google AI Studio](https://ai.google.dev)
2. Klik "Get API Key" atau "Create API Key"
3. Copy API key yang muncul
4. Paste di sidebar aplikasi → field "Gemini API Key"
5. Test koneksi di halaman AI Assistant

---

## 🧠 Model Machine Learning

### XGBoost Binary Classification

**Objective**: Prediksi apakah produk akan membusuk sebelum terjual (`was_spoiled`: 0/1)

### Dataset
- **Source**: `data/perishable_goods_management.csv`
- **Size**: 100,000 records (simulasi data retail perishable goods)
- **Features**: 42 kolom mencakup:
  - Product attributes: kategori, quality score, packaging
  - Storage conditions: temperature, humidity, handling score
  - Supply chain: supplier score, location, transportation
  - Demand & sales: daily demand, units sold, markdown applied
  - Financial: base price, cost price, profit margin
- **Target**: `was_spoiled` (binary: 0=tidak busuk, 1=busuk)
- **Class Balance**: Imbalanced data, ditangani dengan **SMOTE** oversampling

### Jupyter Notebook
Exploratory Data Analysis (EDA) dan training process tersedia di:
```
notebooks/XGBoost_CatBoost_Perishable_Goods.ipynb
```

Notebook mencakup:
- Data loading & exploration
- Feature engineering & preprocessing
- SMOTE balancing
- XGBoost & CatBoost training
- Model comparison & evaluation
- Feature importance analysis
- Hyperparameter tuning experiments

---

## 📦 Requirements & Dependencies

### Core Dependencies
- **Python** >= 3.9
- **Streamlit** >= 1.36.0 (required untuk `st.navigation` API & role-based routing)
- **XGBoost** >= 2.0.0 (ML model)
- **scikit-learn** >= 1.3.0 (preprocessing, metrics, SMOTE)
- **pandas** >= 2.0.0 (data manipulation)
- **numpy** >= 1.24.0 (numerical operations)

### AI/LLM
- **google-generativeai** >= 0.4.0 (Gemini API integration)

### Visualization
- **plotly** >= 5.17.0 (interactive charts)
- **matplotlib** >= 3.7.0 (static plots)
- **seaborn** >= 0.12.0 (statistical visualization)

### Optional
- **imbalanced-learn** (SMOTE implementation)
- **joblib** (model persistence)

### Full Requirements
Lihat `requirements.txt` untuk daftar lengkap dengan versi pinned.

**Install semua dependencies**:
```bash
pip install -r requirements.txt
```

---

## 🏗️ Tech Stack

- **Frontend/UI**: Streamlit (Python web framework)
- **ML Framework**: XGBoost, scikit-learn
- **Data Processing**: pandas, numpy
- **Visualization**: Plotly (interactive), Matplotlib/Seaborn (static)
- **AI/LLM**: Google Gemini API (generative AI)
- **Imbalanced Learning**: SMOTE (imblearn)
- **Model Persistence**: joblib, pickle

---

## � Penggunaan

### Workflow Typical User (Retail Manager)

1. **Login & Role Selection**
   - Pilih role "Retail Manager" di sidebar

2. **Input Data Produk**
   - Buka halaman "Prediksi Risiko"
   - Isi form: kategori produk, kondisi storage, stok, harga, supplier info

3. **Prediksi Risiko**
   - Klik "Prediksi Risiko Pembusukan"
   - Review hasil: probabilitas (0-100%), kategori risiko (AMAN/WASPADA/BAHAYA/KRITIS)
   - Lihat rekomendasi tindakan & estimasi kerugian

4. **Generate AI Analysis**
   - Klik "Generate AI Analysis Report"
   - Review 7 section analisis dari Gemini AI
   - Implementasikan rekomendasi tindakan

5. **Chat Assistant (Opsional)**
   - Buka halaman "AI Assistant"
   - Tanyakan pertanyaan follow-up tentang produk
   - Context otomatis menggunakan data dari prediksi terakhir

### Workflow Typical User (Stakeholder Teknis)

1. **Exploratory Analysis**
   - Buka "Dashboard & Data"
   - Review KPI, trend, distribusi, dan feature importance

2. **Model Evaluation**
   - Buka "Performa Model"
   - Review metrics, confusion matrix, ROC curve
   - Compare XGBoost vs CatBoost performance

3. **Deep Dive (Opsional)**
   - Buka Jupyter notebook untuk EDA detail
   - Review training process & hyperparameter tuning

4. **Gemini Integration Review**
   - Buka "AI Assistant" → tabs documentation
   - Review system prompt, API config, workflow architecture

---

## 🔧 Troubleshooting

### Model Files Tidak Ditemukan
```
Error: File 'models/xgboost_model.pkl' not found
```
**Solusi**: Jalankan `python train_model.py` untuk generate model files

### API Key Gemini Tidak Valid
```
Error: Invalid API key
```
**Solusi**: 
- Verifikasi API key dari [Google AI Studio](https://ai.google.dev)
- Pastikan tidak ada spasi atau karakter hidden
- Test koneksi di halaman "AI Assistant" → tab "API Configuration"

### Import Error XGBoost/CatBoost
```
Error: No module named 'xgboost'
```
**Solusi Windows**:
```bash
pip install --upgrade pip setuptools wheel
pip install xgboost catboost --no-cache-dir
```

### Streamlit Navigation Error
```
Error: 'st.navigation' not found
```
**Solusi**: Upgrade Streamlit ke >= 1.36.0
```bash
pip install --upgrade streamlit>=1.36.0
```

---

## 📄 License

Project ini dibuat untuk keperluan edukasi dan research. Silakan gunakan dengan bijak dan sesuai kebutuhan.

---

## 🙏 Acknowledgments

- **Dataset**: Simulated perishable goods management data (100K records)
- **ML Framework**: XGBoost team
- **AI Integration**: Google Gemini AI
- **UI Framework**: Streamlit team

---

**Dibuat dengan ❤️ untuk mengurangi food waste di industri retail**
