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