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