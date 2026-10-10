"""Predict survival for new passengers.

Usage:
    python src/predict.py                 # runs three example passengers
    from predict import predict_survival  # use as a function
"""
import json
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from preprocessing import build_features, extract_title

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "best_model.pkl"
FILL_PATH = ROOT / "models" / "fill_values.json"

REQUIRED = ["Pclass", "Name", "Sex", "SibSp", "Parch", "Fare"]
OPTIONAL = ["Age", "Cabin", "Embarked"]


@lru_cache(maxsize=1)
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    with open(FILL_PATH) as f:
        fill_values = json.load(f)
    return model, fill_values


def _validate(raw):
    missing = [c for c in REQUIRED if c not in raw.columns]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    if raw[REQUIRED].isnull().any().any():
        raise ValueError(f"Required fields cannot be empty: {REQUIRED}")
    if not raw["Sex"].isin(["male", "female"]).all():
        raise ValueError("Sex must be 'male' or 'female'")
    if not raw["Pclass"].isin([1, 2, 3]).all():
        raise ValueError("Pclass must be 1, 2 or 3")
    if extract_title(raw["Name"]).isna().any():
        raise ValueError("Name must look like 'Surname, Title. Given names'")
    bad_port = raw["Embarked"].notnull() & ~raw["Embarked"].isin(["C", "Q", "S"])
    if bad_port.any():
        raise ValueError("Embarked must be 'C', 'Q' or 'S' (or left empty)")


def predict_dataframe(raw, model=None, fill_values=None):
    """Raw passenger rows (same columns as the original data) -> probability and label."""
    if model is None or fill_values is None:
        model, fill_values = load_artifacts()

    raw = raw.copy()
    for col in OPTIONAL:
        if col not in raw.columns:
            raw[col] = None
    raw["Age"] = pd.to_numeric(raw["Age"], errors="coerce")
    raw["Sex"] = raw["Sex"].astype(str).str.lower()
    _validate(raw)

    features = build_features(raw, fill_values)
    proba = model.predict_proba(features)[:, 1]
    return pd.DataFrame(
        {"probability": proba, "prediction": (proba >= 0.5).astype(int)},
        index=raw.index,
    )


def predict_survival(passenger):
    """Predict one passenger (a dict). Age, Cabin and Embarked are optional."""
    res = predict_dataframe(pd.DataFrame([passenger])).iloc[0]
    return {
        "prediction": "Survived" if res["prediction"] == 1 else "Did not survive",
        "probability_of_survival": round(float(res["probability"]), 3),
    }


if __name__ == "__main__":
    examples = [
        {"Pclass": 3, "Name": "Dawson, Mr. Jack", "Sex": "male", "Age": 20,
         "SibSp": 0, "Parch": 0, "Fare": 8.05, "Embarked": "S"},
        {"Pclass": 1, "Name": "DeWitt Bukater, Miss. Rose", "Sex": "female", "Age": 17,
         "SibSp": 1, "Parch": 1, "Fare": 100.0, "Cabin": "B52", "Embarked": "S"},
        {"Pclass": 3, "Name": "Smith, Mrs. Anna", "Sex": "female",
         "SibSp": 1, "Parch": 2, "Fare": 20.0},  # no Age and no Embarked: filled automatically
    ]
    for p in examples:
        print(p["Name"], "->", predict_survival(p))