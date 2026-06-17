import os
import sys
import io
import glob
import joblib
import json
import pandas as pd
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.metrics import roc_curve
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, recall_score, f1_score, 
roc_auc_score, precision_score, confusion_matrix, classification_report
)
from sklearn.metrics import classification_report

import warnings


# Fix for Windows console emoji printing
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

warnings.filterwarnings('ignore')

def find_csv():
    print("🔍 Mencari file dataset...")
    csv_files = glob.glob("**/*.csv", recursive=True)
    if not csv_files:
        print("❌ File CSV tidak ditemukan.")
        print("Pastikan file .csv berada di folder yang sama dengan file train_model.py ini, lalu coba lagi.")
        exit(1)
    
    if len(csv_files) == 1:
        return csv_files[0]
    
    print("Ditemukan beberapa file CSV:")
    for i, file in enumerate(csv_files, 1):
        print(f"[{i}] {file}")
    
    while True:
        try:
            choice = int(input("Ketik nomor file yang ingin digunakan: "))
            if 1 <= choice <= len(csv_files):
                return csv_files[choice - 1]
            print("Nomor tidak valid.")
        except ValueError:
            print("Harap masukkan angka yang valid.")

def main():
    try:
        csv_path = find_csv()
        print(f"✅ Dataset ditemukan: {csv_path}")
        
        print("📊 Membaca data...")
        df = pd.read_csv(csv_path)
        print(f"   (Membaca {len(df):,} baris)")
        
        required_cols = [
            'category', 'region', 'quality_grade', 'storage_temp', 'temp_deviation',
            'handling_score', 'packaging_score', 'base_price', 'cost_price',
            'daily_demand', 'initial_quantity', 'days_until_expiry', 'temp_abuse_events',
            'shelf_life_days', 'supplier_score', 'spoilage_sensitivity', 'was_spoiled'
        ]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"❌ Kolom berikut tidak ditemukan di dataset: {missing_cols}")
            print("Pastikan Anda menggunakan file CSV yang benar.")
            exit(1)
            
        print("🧹 Membersihkan kolom yang tidak diperlukan...")
        cols_to_drop = [
            'record_id', 'product_id', 'product_name', 'store_id', 'supplier_id',
            'transaction_date', 'expiration_date', 'units_wasted', 'waste_pct', 'waste_cost'
        ]
        df = df.drop(columns=[col for col in cols_to_drop if col in df.columns], errors='ignore')
        
        # Label Encoding
        label_enc_cols = ['category', 'region', 'quality_grade']
        encoders = {}
        for col in label_enc_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = df[col].astype(str)
                df[col] = le.fit_transform(df[col])
                encoders[col] = le
            
        print("⚙️  Membuat fitur tambahan (feature engineering)...")
        # Engineer features
        df['temp_risk_score'] = df['storage_temp'] * df['temp_deviation']
        df['quality_handling'] = df['handling_score'] * df['packaging_score']
        df['price_ratio'] = df['base_price'] / (df['cost_price'] + 1e-6)
        df['demand_pressure'] = df['daily_demand'] / (df['initial_quantity'] + 1e-6)
        df['shelf_urgency'] = 1 / (df['days_until_expiry'] + 1)
        df['temp_abuse_rate'] = df['temp_abuse_events'] / (df['shelf_life_days'] + 1)
        df['supplier_quality'] = df['supplier_score'] * df['handling_score']
        df['sensitivity_exposure'] = df['spoilage_sensitivity'] * df['temp_deviation']
        
        # Any other object columns should be converted or dropped. For safety, drop remaining non-numeric
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except Exception:
                    df = df.drop(columns=[col])
                    
        X = df.drop(columns=['was_spoiled'])
        y = df['was_spoiled']
        feature_names = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        print("⚖️  Menyeimbangkan data (SMOTE)... ini mungkin 1-2 menit")
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
        
        print("🚀 Melatih model XGBoost... harap tunggu")
        xgb_model = xgb.XGBClassifier(
            n_estimators=500,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            min_child_weight=3,
            gamma=0.1,
            tree_method='hist',
            random_state=42,
            early_stopping_rounds=30
        )
        
        xgb_model.fit(
            X_resampled, y_resampled,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        
        y_pred = xgb_model.predict(X_test)
        y_prob = xgb_model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)

        print("💾 Menyimpan model ke folder models/...")

        os.makedirs("models", exist_ok=True)
        print("📁 Folder 'models' dibuat otomatis.")
        
        joblib.dump(xgb_model, "models/xgboost_model.pkl")
        joblib.dump(encoders, "models/label_encoders.pkl")
        joblib.dump(feature_names, "models/feature_names.pkl")
        
         # METRICS
        metrics = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "auc": auc
        }

        with open("models/metrics.json", "w") as f:
            json.dump(metrics, f)

        # CONFUSION MATRIX
        cm = confusion_matrix(y_test, y_pred)
        joblib.dump(cm, "models/confusion_matrix.pkl")
         # CLASSIFICATION REPORT
        report = classification_report(y_test, y_pred, output_dict=True)
        with open("models/classification_report.json", "w") as f:
            json.dump(report, f)

        fpr, tpr, _ = roc_curve(y_test, y_prob)

        joblib.dump({
            "fpr": fpr,
            "tpr": tpr
        }, "models/roc_data.pkl")
        print("✅ Selesai! Model siap digunakan.")
        print("👉 Sekarang jalankan: streamlit run app.py")
        
        summary = f"""
        ╔══════════════════════════════════════╗
        ║       ✅ TRAINING BERHASIL!          ║
        ╠══════════════════════════════════════╣
        ║  Model    : XGBoost                  ║
        ║  Accuracy : {acc*100:5.1f}%          ║
        ║  Precision: {prec*100:5.1f}%         ║
        ║  Recall   : {rec*100:5.1f}%          ║
        ║  F1-Score : {f1*100:5.1f}%           ║
        ║  AUC-ROC  : {auc:.3f}                ║
        ╠══════════════════════════════════════╣
        ║  File tersimpan di folder: models/   ║
        ║                                      ║
        ║  Langkah selanjutnya:                ║
        ║  → streamlit run app.py              ║
        ╚══════════════════════════════════════╝
        """
        print(summary)
    except MemoryError:
        print("❌ Memori tidak cukup. Coba tutup aplikasi lain lalu jalankan ulang script ini.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
        print("Hubungi tim teknis jika masalah berlanjut.")

if __name__ == "__main__":
    main()
