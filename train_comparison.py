import os
import glob
import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

import xgboost as xgb
from catboost import CatBoostClassifier

# ─── FIND CSV ─────────────────────────
def find_csv():
    csv_files = glob.glob("**/*.csv", recursive=True)
    if not csv_files:
        print("❌ CSV tidak ditemukan")
        exit()

    return csv_files[0]


# ─── MAIN ─────────────────────────
def main():
    print("🔍 Load dataset...")
    path = find_csv()
    df = pd.read_csv(path)

    # ─── CLEANING ─────────────────
    drop_cols = [
        'record_id','product_id','product_name','store_id','supplier_id',
        'transaction_date','expiration_date','units_wasted','waste_pct','waste_cost'
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

    # ─── ENCODING ─────────────────
    for col in ['category','region','quality_grade']:
        if col in df.columns:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))

    # ─── FEATURE ENGINEERING ──────
    df['temp_risk'] = df['storage_temp'] * df['temp_deviation']
    df['price_ratio'] = df['base_price'] / (df['cost_price'] + 1e-6)
    df['shelf_urgency'] = 1 / (df['days_until_expiry'] + 1)

    X = df.drop(columns=['was_spoiled'])
    y = df['was_spoiled']

    # ─── SPLIT ────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ─── SMOTE ────────────────────
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_train, y_train)

    results = {}

    # ─────────────────────────────
    # 🌳 XGBOOST
    # ─────────────────────────────
    print("🚀 Training XGBoost...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        random_state=42
    )

    xgb_model.fit(X_res, y_res)

    y_pred = xgb_model.predict(X_test)
    y_prob = xgb_model.predict_proba(X_test)[:,1]

    results["XGBoost"] = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "auc": roc_auc_score(y_test, y_prob)
    }

    # ─────────────────────────────
    # 🐱 CATBOOST
    # ─────────────────────────────
    print("🚀 Training CatBoost...")
    cat_model = CatBoostClassifier(
        iterations=300,
        depth=6,
        learning_rate=0.05,
        verbose=0
    )

    cat_model.fit(X_res, y_res)

    y_pred = cat_model.predict(X_test)
    y_prob = cat_model.predict_proba(X_test)[:,1]

    results["CatBoost"] = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "auc": roc_auc_score(y_test, y_prob)
    }

    # ─── SAVE RESULT ──────────────
    os.makedirs("models", exist_ok=True)

    with open("models/model_comparison.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Comparison selesai!")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()