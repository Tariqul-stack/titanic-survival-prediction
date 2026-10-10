## 1. Data Overview
- The dataset has 891 rows and 12 columns, and there are no duplicate rows.
- The target variable is `Survived` (0 = did not survive, 1 = survived), so this is a binary classification problem.
- About 38.4% of passengers survived and 61.6% did not. The classes are moderately imbalanced, but not extreme.
- Most passengers were in 3rd class (the median `Pclass` is 3).
- Most passengers travelled alone: the median of both `SibSp` and `Parch` is 0.
- `Age` ranges from 0.42 (a baby) to 80. The mean is 29.7 and the median is 28.
- `Fare` is right-skewed: the mean (32.2) is much higher than the median (14.45), and the maximum is 512.3. This means there are a few very expensive tickets (outliers).
- 577 passengers (about 65%) are male and 314 (about 35%) are female.
- `Embarked` has 3 ports. Most passengers boarded at Southampton (S): 644 passengers, about 72%.
- `Name` is unique for every passenger, so it cannot be used directly, but a title (Mr, Mrs, Miss, Master) can be extracted from it.
- `Ticket` has 681 unique values, which means some passengers shared a ticket (likely families or groups).

## 2. Missing Values
- `Cabin` is missing in 687 rows (77.1%). It has too many missing values, so I will either drop it or convert it into a `has_cabin` flag (1 if cabin is known, 0 if not).
- `Age` is missing in 177 rows (19.87%). It will need to be filled (imputed). I will first check how missingness relates to `Pclass` and `Survived` before choosing a method.
- `Embarked` is missing in only 2 rows (0.22%), so I will fill them with the most common value (mode), which is S.
- All other columns have no missing values.

## Summary 
- The dataset has 891 passengers and about 38% survived. The main data quality issues are missing values: Cabin is mostly missing, Age is missing for about 20%, and Embarked for just 2 rows. Fare is highly skewed, so I will handle it during preprocessing. Next, I will study how features like Sex, Pclass and Age relate to survival.

## 3. Target Variable (Survived)
- 549 passengers (61.6%) did not survive and 342 (38.4%) survived.
- The classes are moderately imbalanced, so I will check precision and recall, not only accuracy.

## 4. Univariate Analysis

### 4a. Numeric Features
- `Age` is roughly bell-shaped, with most passengers between 20 and 30 years old.
- There is a small separate peak of babies and young children (0-5 years).
- `Age` has a few outliers above about 65, which are real elderly passengers, so I will keep them.
- `Fare` is heavily right-skewed: most tickets are cheap, with a long tail up to 512.
- `Fare` has many outliers, so I may apply a log transform or binning later.
- `SibSp` and `Parch` are mostly 0, which means most passengers travelled without family.

### 4b. Categorical Features
- `Sex`: 577 male (about 65%) and 314 female (about 35%).
- `Pclass`: 491 passengers in 3rd class, 216 in 1st, and 184 in 2nd.
- `Embarked`: 644 passengers boarded at S, 168 at C, and 77 at Q.

## 5. Bivariate Analysis (Feature vs Survived)

### 5a. Categorical Features
- `Sex` is the strongest factor: 74.2% of females survived, but only 18.9% of males.
- `Pclass` matters a lot: survival was 63.0% in 1st class, 47.3% in 2nd, and 24.2% in 3rd.
- `Embarked`: passengers from C (Cherbourg) survived most (55.4%), then Q (39.0%) and S (33.7%).
- The `Embarked` effect may be indirect, for example if more 1st-class passengers boarded at C. I will check this later.

### 5b. Numeric Features
- Children (0-12) had the highest survival rate (58.0%), which fits the "women and children first" rule.
- Survival was 42.9% for teens, about 39% for adults and middle-aged, and 22.7% for seniors (61-80).
- The senior group has only 22 passengers, so its rate is less reliable.
- The `Age` histogram shows a clear peak of survivors under age 10.
- Higher `Fare` means higher survival: about 20% in the lowest fare quartile and about 58% in the highest.
- `Fare` and `Pclass` are probably related, because 1st class tickets cost more.

### 5c. Family Features
- Passengers travelling alone (`IsAlone` = 1) survived 30.4% of the time (537 passengers), compared with 50.6% for those with family (354 passengers).
- Survival was highest for family sizes of 2-4 and lower for families of 5 or more.
- Family sizes 8 and 11 had 0% survival, but these groups are very small.
- This suggests `FamilySize` and `IsAlone` could be useful new features.

### 5d. Is Age Missing at Random?
- `Age` is missing for 27.7% of 3rd-class passengers, compared with 13.9% in 1st class and 6.0% in 2nd class.
- Missing rate by sex is closer: 21.5% for males and 16.9% for females.
- Survival was 29.4% when `Age` was missing, compared with 40.6% when `Age` was present.
- So the missing `Age` values are not completely random, and they depend mostly on `Pclass`.
- Decision: fill `Age` with the median grouped by `Pclass` and `Sex`, not one global median.

## summary 
- Sex and Pclass are the strongest factors: about 74% of women survived versus 19% of men, and 63% of 1st class versus 24% of 3rd class. Children and passengers with small families also survived more. Age is missing mostly for 3rd class passengers, so I will fill it using the median by Pclass and Sex.

## 6. Multivariate Analysis

### 6a. Sex and Pclass Together
- Women had very high survival in 1st class (96.8%) and 2nd class (92.1%), but only 50.0% in 3rd class.
- Men had low survival in every class: 36.9% in 1st, 15.7% in 2nd, and 13.5% in 3rd.
- So `Sex` and `Pclass` work together: being female helps in every class, but a 3rd-class woman survived far less often than a 1st or 2nd-class woman.
- The biggest group is 3rd-class men (347 passengers), and they had the lowest survival rate.

### 6b. Embarked and Pclass
- Passengers from C (Cherbourg) are 50.6% 1st class, while passengers from Q (Queenstown) are 93.5% 3rd class.
- This explains part of the earlier `Embarked` effect: C looked better because it had many more 1st-class passengers.
- Within the same class, C still has a higher rate than S: 69.4% vs 58.3% in 1st class and 37.9% vs 19.0% in 3rd class.
- S (Southampton) 3rd-class passengers had the lowest survival rate (19.0%).
- The Q results for 1st and 2nd class are based on only 2 and 3 passengers, so they are not reliable.
- `Embarked` is a weaker feature than `Sex` and `Pclass`, but it may still add a little information.

### 6c. Age and Fare vs Pclass
- 1st-class passengers are older (median age 35-40) than 3rd-class passengers (median age 21.5-25).
- Median `Fare` drops sharply with class: 60.29 in 1st, 14.25 in 2nd, and 8.05 in 3rd.
- `Age` depends on both `Pclass` and `Sex`, so I will fill missing `Age` with the median grouped by `Pclass` and `Sex`.

### 6d. Correlation Heatmap
- `Survived` correlates most with `Sex_female` (0.54), then `Pclass` (-0.34) and `Fare` (0.26).
- `Age` (-0.08), `SibSp` (-0.04) and `Parch` (0.08) have weak linear correlation with `Survived`.
- Weak correlation does not mean useless: survival by age group and by family size was non-linear (children and small families did best), and correlation only measures linear relationships.
- `Pclass` and `Fare` are fairly strongly related (-0.55), so they carry overlapping information.
- `SibSp` and `Parch` are correlated (0.41), which supports combining them into `FamilySize`.

### summary 
- Sex and Pclass together matter most. Women in 1st and 2nd class survived more than 90% of the time, but 3rd-class women only 50%, and men survived much less in every class. Embarked looked important at first, but a big part of it is just class mix. Age and family size have weak linear correlation, but the charts show non-linear patterns, so I will engineer features from them.

## 7. Feature Ideas for Preprocessing

### 7a. Title from Name
- The title (Mr, Mrs, Miss, Master, etc.) can be extracted from `Name`. Rare titles (Dr, Rev, Major, Col, Lady, Sir, and others) are grouped into one `Rare` group, and Mlle/Ms/Mme are merged into Miss/Mrs.
- Survival rate by title: Mrs 79.4%, Miss 70.3%, Master 57.5%, Rare 34.8%, Mr 15.7%.
- `Title` carries information about both sex and age: `Master` (young boys) has a median age of 3.5, while Mr has 30.0, Mrs 35.0, and Rare 48.5.
- Because of this, the median age by `Title` is a better way to fill missing `Age` than the median by `Pclass` and `Sex`. In particular, young boys would otherwise get an adult male age.
- The `Rare` group has only 23 passengers, so its rate is less reliable.

### 7b. Cabin Flag
- Passengers with a known cabin survived 66.7% of the time (204 passengers), compared with 30.0% for those without one (687 passengers).
- But `has_cabin` is strongly linked to class: 81.5% of 1st-class passengers have a cabin recorded, versus only 8.7% in 2nd class and 2.4% in 3rd class.
- So `has_cabin` partly repeats the information in `Pclass`. It may also depend on how the records were collected.
- I will keep it as a candidate feature and check in the modeling stage whether it improves the results.

### 7c. Family Features
- `FamilySize` = `SibSp` + `Parch` + 1, and `IsAlone` = 1 when `FamilySize` is 1.
- Survival by family group: Alone 30.4% (537 passengers), Small family of 2-4 57.9% (292), Large family of 5+ 16.1% (62).
- Small families did best, while both travelling alone and being in a large family were worse. This non-linear pattern is not visible in the correlation heatmap.
- `FamilyGroup` (Alone / Small / Large) captures this pattern better than `IsAlone`. I will test both.

### 7d. Fare Transform
- Skewness of `Fare` is 4.79 before the log1p transform and 0.39 after it.
- After the transform the distribution is much more symmetric, although there is still a peak around the cheap 3rd-class fares and a few zero fares.
- I will use `Fare_log` for models that are sensitive to skew (such as Logistic Regression). Tree-based models do not need it.

## EDA Summary
- About 38.4% of passengers survived, so the classes are moderately imbalanced.
- `Sex` and `Pclass` are the strongest factors, and they work together (for example, 96.8% survival for 1st-class women vs 13.5% for 3rd-class men).
- Children and small families survived more, so `Age` and family size have non-linear effects.
- `Age` has 19.87% missing values, mostly in 3rd class. `Cabin` is 77.1% missing.
- `Title` is a strong new feature because it combines sex and age information.

## 3. Train/Test Split
- The data was split 80/20 with `stratify=y` and `random_state=42`: 712 training rows and 179 test rows.
- The survival rate is almost the same in both sets (38.3% in train, 38.5% in test).

## 4. Missing Values
- Missing `Age` values were filled with the median age of each `Title`, calculated from the training set only (Master 3.0, Miss 22.0, Mr 30.0, Mrs 35.0, Rare 49.0).
- Missing `Embarked` values were filled with the training-set mode (S).
- The same training-set values were applied to the test set, so no test information leaked into training.
- After filling, `Age` and `Embarked` have 0 missing values in both sets.

## 5. Transform and Encode
- `Fare` was log-transformed into `Fare_log`.
- `PassengerId`, `Name`, `Ticket`, `Cabin`, `SibSp`, `Parch` and `Fare` were dropped.
- `Sex`, `Embarked`, `Title` and `FamilyGroup` were one-hot encoded.
- The test set was aligned to the training columns, so both have the same 19 features and all values are numeric.

## 6. Save Processed Data
- The processed train/test sets and the fill values (`fill_values.json`) were saved to `data/processed/`.
- The modeling notebook will load these files directly. `fill_values.json` will be used to prepare new passengers for prediction.

## 2. Baselines
- Always predicting "did not survive" gives 61.7% accuracy and an F1 of 0.
- The simple rule "females survive, males do not" gives 78.9% accuracy and an F1 of 0.715. This is a strong baseline, because `Sex` alone carries a lot of information.

## 3. Model Comparison (5-fold CV on the training set)
- Cross-validated accuracy: Logistic Regression 0.827, Gradient Boosting 0.820, Random Forest 0.819.
- The standard deviation of accuracy is about 0.023-0.029, which is larger than the differences between the models. So the three models perform about the same, and none is clearly better.
- Gradient Boosting has the highest ROC-AUC (0.894, versus 0.878 for Logistic Regression and 0.874 for Random Forest), so it ranks passengers slightly better by survival probability.
- All three models beat the Sex-rule baseline by only about 3-4 accuracy points. This is a small gain, and it is close to one standard deviation.
- Conclusion: the extra features (`Title`, family features, `Pclass`, etc.) help a little, but most of the predictive power already comes from `Sex`.
- I will not pick a model yet. First I will compare feature sets, and then tune the best candidates.

## 4. Feature Set Comparison
- I compared 5 family-feature options, each with and without `has_cabin`, using 3 models (30 cross-validation runs).
- Mean CV accuracy ranges only from 0.809 to 0.827, while the fold-to-fold standard deviation is about 0.025. So the ranking between feature sets is not reliable.
- The best sets were FamilyGroup only + `has_cabin` (0.827), FamilySize only + `has_cabin` (0.824), and all three family features + `has_cabin` (0.822).
- `has_cabin` adds about 0.006-0.014 mean accuracy for every family option, and ROC-AUC is also slightly higher. The effect is clearest for Random Forest (0.819 vs 0.798 with FamilySize) and not consistent for Gradient Boosting.
- `has_cabin` overlaps with `Pclass` and may depend on how the records were collected, so this gain should be read with care.
- `FamilySize` and `FamilyGroup` give almost the same score (difference 0.003). `IsAlone` alone gives no gain, and using all three together is no better than using one, so they are redundant.
- Decision: keep `has_cabin` and `FamilySize`, and drop `IsAlone` and `FamilyGroup`. This is a close call, because the differences are within the noise.
- The test set was not used for this choice.

## 5. Hyperparameter Tuning
- Final features (15): `Pclass`, `Age`, `FamilySize`, `has_cabin`, `Fare_log`, and the one-hot columns for `Sex`, `Embarked` and `Title`.
- I tuned each model with a small grid search (5-fold CV, selected by ROC-AUC). Best settings: Logistic Regression `C=1` (same as default), Random Forest `max_depth=None` and `min_samples_leaf=3`, Gradient Boosting `learning_rate=0.1`, `max_depth=2` and `n_estimators=200`.
- Tuning helped very little: ROC-AUC changed from 0.877 to 0.877 (Logistic Regression), 0.875 to 0.885 (Random Forest) and 0.894 to 0.896 (Gradient Boosting). Accuracy did not improve.
- The tuned scores are slightly optimistic, because the settings were chosen on the same CV folds.
- Gradient Boosting has the highest ROC-AUC (0.896), and its gap to Logistic Regression (0.019) is smaller than the fold-to-fold standard deviation of Logistic Regression (0.022).
- By the rule I set before tuning, I selected **Logistic Regression**: it is simpler, its coefficients are easy to explain, and its accuracy is the same or better (0.829 vs 0.823-0.824).
- This is a close call, because the gap is only slightly below the standard deviation. Gradient Boosting would be a reasonable choice too.

## 6. Final Evaluation on the Test Set
- The test set (179 passengers) was used once, only for the final model.
- Logistic Regression: accuracy 0.838, precision 0.786, recall 0.797, F1 0.791, ROC-AUC 0.867.
- Sex rule baseline: accuracy 0.777, precision 0.738, recall 0.652, F1 0.692. Always predicting "did not survive": accuracy 0.615.
- The model beats the Sex rule by about 6 accuracy points, which is roughly 11 passengers. The biggest gain is recall for survivors (0.797 vs 0.652): the model finds more survivors than the simple rule.
- Confusion matrix: 95 correct "did not survive", 55 correct "survived", 15 false alarms (predicted survived, but died) and 14 missed survivors.
- The test results match cross-validation (accuracy 0.829 in CV, 0.838 on test, and ROC-AUC 0.877 vs 0.867), so there is no sign of overfitting.
- With only 179 test passengers, the 95% bootstrap interval for accuracy is wide: 0.782 to 0.888. The estimate is therefore uncertain, and a small difference between models would not be reliable.