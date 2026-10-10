"""Train the final Logistic Regression model and save it to models/."""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from preprocessing import build_features, compute_fill_values

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "titanic_data.csv"
MODEL_DIR = ROOT / "models"
RANDOM_STATE = 42


def build_model():
    prep = ColumnTransformer(
        [("scale", StandardScaler(), ["Age", "FamilySize", "Fare_log"])],
        remainder="passthrough",
    )
    return Pipeline([
        ("prep", prep),
        ("model", LogisticRegression(C=1, max_iter=1000, random_state=RANDOM_STATE)),
    ])


def main():
    raw = pd.read_csv(RAW_PATH)
    y = raw["Survived"]
    X = raw.drop(columns="Survived")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    fill_values = compute_fill_values(X_train)  # training set only
    X_train_f = build_features(X_train, fill_values)
    X_test_f = build_features(X_test, fill_values)

    model = build_model()
    model.fit(X_train_f, y_train)

    pred = model.predict(X_test_f)
    proba = model.predict_proba(X_test_f)[:, 1]
    print("Test set results (should match the modeling notebook):")
    print(f"  accuracy : {accuracy_score(y_test, pred):.3f}")
    print(f"  precision: {precision_score(y_test, pred):.3f}")
    print(f"  recall   : {recall_score(y_test, pred):.3f}")
    print(f"  f1       : {f1_score(y_test, pred):.3f}")
    print(f"  roc_auc  : {roc_auc_score(y_test, proba):.3f}")

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "best_model.pkl")
    with open(MODEL_DIR / "fill_values.json", "w") as f:
        json.dump(fill_values, f, indent=2)
    print(f"Saved model and fill values to {MODEL_DIR}")


if __name__ == "__main__":
    main()