import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 1. LOAD RAW DATASET (with missing values)
# ------------------------------------------------------------
df = pd.read_csv("Steel_Industry_Raw_Unprocessed.csv")

print("\n----- Missing Values Before Cleaning -----")
print(df.isnull().sum())

# ------------------------------------------------------------
# 2. HANDLE CATEGORICAL MISSING VALUES (Fill with Mode)
# ------------------------------------------------------------
cat_cols = ['Load_Type', 'Day_of_week', 'WeekStatus']

for col in cat_cols:
    if col in df.columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

# ------------------------------------------------------------
# 3. HANDLE NUMERICAL MISSING VALUES (Fill with Median)
# ------------------------------------------------------------
num_cols = [
    'Usage_kWh','Lagging_Current_Reactive.Power_kVarh',
    'Leading_Current_Reactive_Power_kVarh','CO2(tCO2)',
    'Lagging_Current_Power_Factor','Leading_Current_Power_Factor',
    'NSM'
]

for col in num_cols:
    if col in df.columns:
        df[col].fillna(df[col].median(), inplace=True)

# ------------------------------------------------------------
# 4. HANDLE MISSING DATE VALUES (Drop corrupted timestamps)
# ------------------------------------------------------------
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df.dropna(subset=['date'], inplace=True)

# ------------------------------------------------------------
# 5. DROP UNNEEDED COLUMNS
# (Streamlit model already removes date column)
# ------------------------------------------------------------
df_clean = df.drop(columns=['date'])

# ------------------------------------------------------------
# 6. ONE-HOT ENCODING FOR CATEGORICAL FEATURES
# ------------------------------------------------------------
df_clean = pd.get_dummies(df_clean)

# ------------------------------------------------------------
# 7. PRINT FINAL CLEAN DATASET SHAPE
# ------------------------------------------------------------
print("\n----- Missing Values AFTER Cleaning -----")
print(df_clean.isnull().sum())

print("\nFinal Cleaned Dataset Shape:", df_clean.shape)

# ------------------------------------------------------------
# 8. SAVE CLEANED DATASET
# ------------------------------------------------------------
df_clean.to_csv("Steel_Industry_Cleaned_Final.csv", index=False)
print("\nCleaned dataset saved as Steel_Industry_Cleaned_Final.csv")
