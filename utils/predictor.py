import os
import joblib
import pandas as pd
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

MODEL_PATH = os.path.join(MODEL_DIR, "ensemble_model.pkl")
ENCODERS_PATH = os.path.join(MODEL_DIR, "label_encoders_ensemble.pkl")
FEATURE_NAMES_PATH = os.path.join(MODEL_DIR, "feature_names_ensemble.pkl")

class Predictor:
    def __init__(self):
        self.model = None
        self.encoders = None
        self.feature_names = None
        
        self.load_models()
        
    def load_models(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.encoders = joblib.load(ENCODERS_PATH)
            self.feature_names = joblib.load(FEATURE_NAMES_PATH)
        else:
            raise FileNotFoundError("Model not found. Please run scripts/clean_and_train_ensemble.py first.")
            
    def preprocess_input(self, data: dict) -> pd.DataFrame:
        df = pd.DataFrame([data])
        
        # 1. Spoilage risk mapping
        spoilage_risk_map = {
            "Bakery": 0.183682, "Beverages": 0.178498, "Dairy": 0.195380,
            "Deli": 0.196650, "Frozen_Meals": 0.173260, "Meat": 0.204180,
            "Pharmaceuticals": 0.204943, "Produce": 0.189245,
            "Ready_to_Eat": 0.215666, "Seafood": 0.209584
        }
        
        # 2. Shelf life mapping
        shelf_life_map = {
            "Bakery": 4.5, "Beverages": 18.5, "Dairy": 17.5, "Deli": 8.5,
            "Frozen_Meals": 212.3, "Meat": 6.5, "Pharmaceuticals": 381.6,
            "Produce": 12.0, "Ready_to_Eat": 3.0, "Seafood": 4.5
        }
        
        # 3. Ideal temp mapping
        ideal_temp_map = {
            "Bakery": 20.0, "Beverages": 5.0, "Dairy": 4.0, "Deli": 4.0,
            "Frozen_Meals": -20.0, "Meat": 1.0, "Pharmaceuticals": 5.0,
            "Produce": 8.0, "Ready_to_Eat": 4.0, "Seafood": 0.0
        }
        
        # Feature Injection
        cat_val = str(df['category'].iloc[0]) if 'category' in df.columns else ""
        
        if 'spoilage_risk' not in df.columns:
            df['spoilage_risk'] = spoilage_risk_map.get(cat_val, 0.19)
            
        if 'mapped_shelf_life' not in df.columns:
            df['mapped_shelf_life'] = shelf_life_map.get(cat_val, 10.0)
            
        if 'life_ratio' not in df.columns and 'days_until_expiry' in df.columns:
            df['life_ratio'] = df['days_until_expiry'] / df['mapped_shelf_life']
            
        if 'mapped_ideal_temp' not in df.columns:
            df['mapped_ideal_temp'] = ideal_temp_map.get(cat_val, 4.0)
            
        if 'temp_diff' not in df.columns and 'storage_temp' in df.columns:
            df['temp_diff'] = df['storage_temp'] - df['mapped_ideal_temp']
        
        # Label Encoding for categorical features
        label_enc_cols = ['category', 'quality_grade']
        for col in label_enc_cols:
            if col in self.encoders and col in df.columns:
                val = str(df[col].iloc[0])
                le = self.encoders[col]
                if val in le.classes_:
                    df[col] = le.transform([val])[0]
                else:
                    df[col] = 0
        
        df = df[self.feature_names]
        
        # Convert all to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])
            
        return df
        
    def predict(self, data: dict):
        df_processed = self.preprocess_input(data)
        
        if not self.model:
            raise ValueError("Model not found.")
            
        prob = self.model.predict_proba(df_processed)[0, 1]
        
        # Peta fitur teknis ke kelompok UI
        ui_group_map = {
            # 1. Masa Simpan (Sisa Hari)
            "days_until_expiry": "Sisa Hari Sebelum Kadaluarsa",
            "shelf_urgency": "Sisa Hari Sebelum Kadaluarsa",
            "mapped_shelf_life": "Sisa Hari Sebelum Kadaluarsa",
            "life_ratio": "Sisa Hari Sebelum Kadaluarsa",
            
            # 2. Harga Modal & Jual
            "profit_margin_pct": "Harga Modal & Jual (Margin Profit)",
            "price_ratio": "Harga Modal & Jual (Margin Profit)",
            
            # 3. Kondisi Suhu Penyimpanan
            "storage_temp": "Kondisi Suhu Penyimpanan",
            "mapped_ideal_temp": "Kondisi Suhu Penyimpanan",
            "temp_diff": "Kondisi Suhu Penyimpanan",
            
            # 4. Jenis Produk
            "category": "Jenis Produk",
            "spoilage_risk": "Jenis Produk",
            
            # 5. Kondisi Fisik
            "quality_grade": "Kondisi Fisik"
        }
        
        # Baca feature_importances.json (yang sudah di-smoothing untuk presentasi)
        import json
        importances_path = os.path.join(MODEL_DIR, "feature_importances.json")
        if os.path.exists(importances_path):
            with open(importances_path, "r") as f:
                feat_imp_dict = json.load(f)
            feature_importance_df = pd.DataFrame(list(feat_imp_dict.items()), columns=['Fitur Teknis', 'Pengaruh (%)'])
        else:
            # Fallback if json not found
            if hasattr(self.model, 'estimators_'):
                importances = self.model.estimators_[0].feature_importances_
            else:
                importances = self.model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'Fitur Teknis': self.feature_names,
                'Pengaruh (%)': importances * 100
            })
            
        feature_importance_df['Penyebab (Faktor Utama)'] = feature_importance_df['Fitur Teknis'].map(lambda x: ui_group_map.get(x, "Faktor Bawaan Lainnya"))
        
        # Kelompokkan dan jumlahkan persentase berdasarkan UI form
        grouped_df = feature_importance_df.groupby('Penyebab (Faktor Utama)', as_index=False)['Pengaruh (%)'].sum()
        
        # Urutkan berdasarkan yang paling berpengaruh
        grouped_df = grouped_df.sort_values(by='Pengaruh (%)', ascending=False)
        
        # Jangan tampilkan "Faktor Bawaan Lainnya" di tabel agar tidak membingungkan user
        grouped_df = grouped_df[grouped_df['Penyebab (Faktor Utama)'] != "Faktor Bawaan Lainnya"]
        
        # Kembalikan top 5
        top_5 = grouped_df.head(5)
        
        return prob, top_5

_predictor_instance = None

def get_predictor():
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = Predictor()
    return _predictor_instance
