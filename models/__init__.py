"""
Models Package
==============
Folder ini digunakan untuk menyimpan:

- File model terlatih  (.pkl, .h5, .pt, .onnx, dll)
- File konfigurasi     (model_config.json / config.yaml)
- File scaler/encoder  (scaler.pkl, label_encoder.pkl)
- Dokumentasi model    (model_card.md)

Struktur yang Disarankan
-------------------------
models/
├── __init__.py
├── model_config.json      ← metadata & hyperparameter
├── food_waste_model.pkl   ← model terlatih (sklearn)
├── scaler.pkl             ← StandardScaler / MinMaxScaler
├── label_encoder.pkl      ← LabelEncoder untuk target
└── model_card.md          ← dokumentasi model

Cara Memuat Model
------------------
    from utils.helpers import load_model
    model = load_model("models/food_waste_model.pkl")
"""
