import os
import joblib
import pandas as pd
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "xgboost_model.pkl")
ENCODERS_PATH = os.path.join(MODEL_DIR, "label_encoders.pkl")
FEATURE_NAMES_PATH = os.path.join(MODEL_DIR, "feature_names.pkl")

class Predictor:
    def __init__(self):
        self.model = None
        self.encoders = None
        self.feature_names = None
        self.load_models()
        
    def load_models(self):
        if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODERS_PATH) or not os.path.exists(FEATURE_NAMES_PATH):
            raise FileNotFoundError("Model files not found. Please run train_model.py first.")
        
        self.model = joblib.load(MODEL_PATH)
        self.encoders = joblib.load(ENCODERS_PATH)
        self.feature_names = joblib.load(FEATURE_NAMES_PATH)
        
    def preprocess_input(self, data: dict) -> pd.DataFrame:
        df = pd.DataFrame([data])
        
        # Derived features
        df['temp_risk_score'] = df['storage_temp'] * df['temp_deviation']
        df['quality_handling'] = df['handling_score'] * df['packaging_score']
        df['price_ratio'] = df['base_price'] / (df['cost_price'] + 1e-6)
        df['demand_pressure'] = df['daily_demand'] / (df['initial_quantity'] + 1e-6)
        df['shelf_urgency'] = 1 / (df['days_until_expiry'] + 1)
        df['temp_abuse_rate'] = df['temp_abuse_events'] / (df['shelf_life_days'] + 1)
        df['supplier_quality'] = df['supplier_score'] * df['handling_score']
        df['sensitivity_exposure'] = df['spoilage_sensitivity'] * df['temp_deviation']
        
        # Label Encoding
        label_enc_cols = ['category', 'region', 'quality_grade']
        for col in label_enc_cols:
            if col in self.encoders:
                val = str(df[col].iloc[0])
                le = self.encoders[col]
                if val in le.classes_:
                    df[col] = le.transform([val])[0]
                else:
                    df[col] = 0
        
        # Ensure correct column order
        df = df[self.feature_names]
        
        # Convert all to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])
            
        return df
        
    def predict(self, data: dict):
        df_processed = self.preprocess_input(data)
        prob = self.model.predict_proba(df_processed)[0, 1]
        
        importances = self.model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'Fitur': self.feature_names,
            'Kepentingan': importances
        }).sort_values(by='Kepentingan', ascending=False)
        
        return prob, feature_importance_df.head(5)
        
    def get_global_importances(self):
        importances = self.model.feature_importances_
        return pd.DataFrame({
            'Fitur': self.feature_names,
            'Kepentingan': importances
        }).sort_values(by='Kepentingan', ascending=False)

_predictor_instance = None

def get_predictor():
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = Predictor()
    return _predictor_instance
