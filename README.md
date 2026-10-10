# Titanic Survival Prediction

A machine learning project that predicts whether a Titanic passenger survived, built as a university class assignment. It covers exploratory data analysis, leakage-safe preprocessing, model comparison with cross-validation, a final evaluation on a held-out test set, and a small prediction script.

**Final result:** a tuned Logistic Regression model reaches **83.8% accuracy** and **0.867 ROC-AUC** on the test set (179 passengers), compared with 77.7% for the simple rule "women survive, men do not".

**Run on Kaggle:** [Kaggle notebook](https://www.kaggle.com/code/tariqul1/titanic-survival-prediction/edit)

## Problem and Data

- **Task:** binary classification of `Survived` (0 = did not survive, 1 = survived).
- **Data:** `data/titanic_data.csv`, with 891 passengers and 12 columns (Titanic passenger data in the format of Kaggle's Titanic training set).
- **Target balance:** 342 passengers survived (38.4%) and 549 did not (61.6%).
- **Missing values:** `Cabin` 77.1%, `Age` 19.9%, `Embarked` 0.2%. There are no duplicate rows.

## Project Structure

```
titanic-survival-prediction/
├── data/
│   ├── titanic_data.csv          # raw data (never edited)
│   └── processed/                # train/test sets created by notebook 02
├── notebooks/
│   ├── 01_eda.ipynb              # exploratory data analysis
│   ├── 02_preprocessing.ipynb    # feature engineering, split, missing values, encoding
│   └── 03_modeling.ipynb         # baselines, cross-validation, tuning, test evaluation, interpretation
├── src/
│   ├── preprocessing.py          # reusable feature preparation
│   ├── train.py                  # trains and saves the final model
│   └── predict.py                # predicts survival for new passengers
├── models/
│   ├── best_model.pkl            # trained model (pipeline with scaler)
│   └── fill_values.json          # values used to fill missing Age and Embarked
├── requirements.txt
└── README.md
```

## Approach

1. **EDA** (`01_eda.ipynb`): `Sex` and `Pclass` are the strongest factors and they work together. Women in 1st and 2nd class survived more than 90% of the time, but 3rd-class women only 50%, and men survived 13-37% in every class. Children and small families (2-4 people) also survived more. `Age` is missing mostly for 3rd-class passengers.
2. **Preprocessing** (`02_preprocessing.ipynb`):
   - New features: `Title` (from `Name`), `FamilySize`, `has_cabin`, and `Fare_log` (log transform, skewness 4.79 reduced to 0.39).
   - The data is split first (80/20, stratified, `random_state=42`). Missing `Age` is filled with the median age of each `Title`, and missing `Embarked` with the mode. **Both values are learned from the training set only**, so no test information leaks into training.
   - Categories are one-hot encoded, giving 15 numeric features.
3. **Modeling** (`03_modeling.ipynb`):
   - Two baselines: always "did not survive", and the Sex rule.
   - Logistic Regression, Random Forest and Gradient Boosting are compared with 5-fold stratified cross-validation on the training set only. The scaler for Logistic Regression is inside a `Pipeline`, so it is fitted only on each training fold.
   - Feature sets (family features, `has_cabin`) were compared with the same cross-validation, and `FamilySize` and `has_cabin` were kept.
   - Each model was tuned with a small grid search selected by ROC-AUC. The selection rule was fixed before tuning: if the best model is not clearly better than Logistic Regression (gap smaller than one fold standard deviation), keep Logistic Regression. The rule selected Logistic Regression.
   - The test set was used once, for the final model.

## Results

**Baselines and cross-validation** (training set, 5-fold; baselines use the training set):

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Always "did not survive" | 0.617 | - |
| Sex rule (female = survive) | 0.789 | - |
| Logistic Regression (tuned) | 0.829 | 0.877 |
| Random Forest (tuned) | 0.824 | 0.885 |
| Gradient Boosting (tuned) | 0.823 | 0.896 |

The fold-to-fold standard deviation of accuracy is about 0.02-0.03, which is larger than the differences between the three models, so they perform about the same.

**Final test set** (179 passengers):

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression (final) | 0.838 | 0.786 | 0.797 | 0.791 | 0.867 |
| Sex rule | 0.777 | 0.738 | 0.652 | 0.692 | - |
| Always "did not survive" | 0.615 | 0.000 | 0.000 | 0.000 | - |

- Confusion matrix: 95 correct "did not survive", 55 correct "survived", 15 false alarms and 14 missed survivors.
- The 95% bootstrap interval for test accuracy is **0.782 to 0.888**.
- Test results match cross-validation (accuracy 0.829 vs 0.838, ROC-AUC 0.877 vs 0.867), so there is no sign of overfitting.

## Key Findings

- `Sex` and `Title` are the strongest signals (permutation importance: ROC-AUC drops by 0.089 and 0.082 when shuffled), followed by `FamilySize` (0.051), `Pclass` (0.026) and `Age` (0.021). `Sex` and `Title` overlap, so each is underestimated when shuffled alone.
- In the coefficients, `Title_Master` (young boys), `Sex_female`, `has_cabin` and `Title_Mrs` raise the odds of survival. `Title_Mr`, `Sex_male`, `FamilySize`, `Pclass` and `Age` lower them.
- The model is least accurate for 1st-class men (0.67) and 3rd-class women (0.68). Most of its confident mistakes are men who survived although the model gave them a low probability.

## Limitations

- The test set is small (179 passengers), so the accuracy estimate is uncertain (about ±5 points). The model is about 6 points better than the Sex rule, but this gain is small and the models are not clearly different from each other.
- Logistic Regression is linear and has no `Sex` x `Pclass` interaction, although the EDA shows that class matters differently for men and women. It also treats `FamilySize` as a straight line, although families of 2-4 did best.
- Hyperparameter tuning gave almost no gain, and the tuned CV scores are slightly optimistic because the settings were chosen on the same folds.
- `has_cabin` overlaps with `Pclass`, and cabin records may depend on how the data was collected, so its effect should be read with care.
- The model learned from only 891 passengers and shows association, not cause.

## How to Run

```bash
git clone https://github.com/Tariqul-stack/titanic-survival-prediction
cd titanic-survival-prediction

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Train the model and print the test results (this recreates `models/best_model.pkl`):

```bash
python src/train.py
```

Predict three example passengers:

```bash
python src/predict.py
```

Use it as a function:

```python
import sys
sys.path.insert(0, "src")
from predict import predict_survival

predict_survival({
    "Pclass": 3, "Name": "Smith, Mrs. Anna", "Sex": "female",
    "SibSp": 1, "Parch": 2, "Fare": 20.0,   # Age, Cabin and Embarked are optional
})
```

`Name` is required and must look like `"Surname, Title. Given names"`, because the title is used as a feature. `Sex` must be `male` or `female`, and `Pclass` must be 1, 2 or 3.

To reproduce the analysis, run the notebooks in order: `01_eda`, `02_preprocessing`, `03_modeling`.

**Note:** `models/best_model.pkl` depends on the scikit-learn version in `requirements.txt`. If it fails to load in another environment, run `python src/train.py` to recreate it.
**Reproducibility:** the pipeline was also run on Kaggle (Python 3.13, pandas 2.3.3, scikit-learn 1.6.1) and gave the same test results (accuracy 0.838, ROC-AUC 0.867) as the local run.

## Possible Improvements

- Add a `Sex` x `Pclass` interaction feature, or test a tree-based model with a stricter selection process.
- Use nested cross-validation for a less optimistic estimate after tuning.
- Submit predictions for the Kaggle competition test set.

## Author

Tariqul ([GitHub](https://github.com/Tariqul-stack))