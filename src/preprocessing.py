"""Feature preparation for the Titanic survival model.

Mirrors notebooks/02_preprocessing.ipynb. The fill values (median Age by Title and
the Embarked mode) must always be calculated from the training set only.
"""
import numpy as np
import pandas as pd

TITLE_MAP = {"Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"}
COMMON_TITLES = ["Mr", "Mrs", "Miss", "Master"]
TITLE_VALUES = ["Master", "Miss", "Mr", "Mrs", "Rare"]
SEX_VALUES = ["female", "male"]
EMBARKED_VALUES = ["C", "Q", "S"]

# Final model input (same 15 columns, same order as in the modeling notebook)
FEATURE_COLUMNS = [
    "Pclass", "Age", "FamilySize", "has_cabin", "Fare_log",
    "Sex_female", "Sex_male",
    "Embarked_C", "Embarked_Q", "Embarked_S",
    "Title_Master", "Title_Miss", "Title_Mr", "Title_Mrs", "Title_Rare",
]


def extract_title(names):
    """Get the title from names like 'Braund, Mr. Owen Harris' (NaN if not found)."""
    return names.str.extract(r",\s*([^\.]+)\.", expand=False).str.strip()


def add_features(data):
    """Row-wise features. Each value depends only on that passenger's own row."""
    data = data.copy()
    title = extract_title(data["Name"]).replace(TITLE_MAP)
    data["Title"] = title.where(title.isin(COMMON_TITLES), "Rare")
    data["FamilySize"] = data["SibSp"] + data["Parch"] + 1
    data["has_cabin"] = data["Cabin"].notnull().astype(int)
    return data


def compute_fill_values(train_raw):
    """Learn the fill values from the TRAINING set only."""
    feats = add_features(train_raw)
    return {
        "age_median_by_title": feats.groupby("Title")["Age"].median().to_dict(),
        "age_median_overall": float(feats["Age"].median()),
        "embarked_mode": feats["Embarked"].mode()[0],
    }


def fill_missing(data, fill_values):
    data = data.copy()
    age_by_title = data["Title"].map(fill_values["age_median_by_title"])
    data["Age"] = data["Age"].fillna(age_by_title).fillna(fill_values["age_median_overall"])
    data["Embarked"] = data["Embarked"].fillna(fill_values["embarked_mode"])
    return data


def build_features(raw, fill_values):
    """Raw passenger rows -> the 15 numeric model features, in a fixed column order."""
    data = fill_missing(add_features(raw), fill_values)

    out = pd.DataFrame(index=data.index)
    out["Pclass"] = data["Pclass"]
    out["Age"] = data["Age"].astype(float)
    out["FamilySize"] = data["FamilySize"]
    out["has_cabin"] = data["has_cabin"]
    out["Fare_log"] = np.log1p(data["Fare"])

    # Fixed category lists, so a single passenger still gets all columns
    for sex in SEX_VALUES:
        out[f"Sex_{sex}"] = (data["Sex"] == sex).astype(int)
    for port in EMBARKED_VALUES:
        out[f"Embarked_{port}"] = (data["Embarked"] == port).astype(int)
    for title in TITLE_VALUES:
        out[f"Title_{title}"] = (data["Title"] == title).astype(int)

    return out[FEATURE_COLUMNS]