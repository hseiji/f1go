import fastf1
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

# Enable caching for faster loading
fastf1.Cache.enable_cache('cache')

# 1. IMPORTING DATA ------------------------------------------------------------------------------

# Load season 2024
# schedule24 = fastf1.get_event_schedule(2024)
session_2024 = fastf1.get_session(2024, 6, "R")
session_2024.load()

# # Print all race names with dates
# print("2024 F1 Race Calendar:\n")
# for round_num, event in schedule24['RoundNumber'].items():
#     date = schedule24.loc[round_num, 'Session5Date'].date()
#     location = schedule24.loc[round_num, 'Location']
#     country = schedule24.loc[round_num, 'Country']
#     print(f"Round {round_num}: {country} - {location} - {date}")
# print("\n")

# RACE 2024 -------------------------------------------------
# Get Lap Time Data from 2024
laps_2024 = session_2024.laps[["Driver", "LapTime"]].copy()
laps_2024.dropna(subset=["LapTime"], inplace=True)
laps_2024["LapTime (s)"] = laps_2024["LapTime"].dt.total_seconds()
print(f"\nLap Time Data for 2024:\n{laps_2024}\n")

# Load the latest season and round info
season25 = 2025
round_number = 6  # Change this to GP round number you want to analyze > Miami GP = 6

# QUALY 2025 ------------------------------------------------
# Load qualifying session
session = fastf1.get_session(season25, round_number, 'Q')
session.load()

# Get results
results = session.results[['FullName', 'Abbreviation', 'TeamName', 'Position', 'Q1', 'Q2', 'Q3']]

print(f"\n🏁 Qualifying Results - {session.event['EventName']} 🏁\n")

data = []
for _, row in results.iterrows():
    pos = int(row['Position'])
    name = row['FullName']
    abbr = row['Abbreviation']
    team = row['TeamName']
    q1 = str(row['Q1']).split('0 days ')[-1][:12] if pd.notna(row['Q1']) else '-'
    q2 = str(row['Q2']).split('0 days ')[-1][:12] if pd.notna(row['Q2']) else '-'
    q3 = str(row['Q3']).split('0 days ')[-1][:12] if pd.notna(row['Q3']) else '-'
    q3_seconds = row['Q3'].total_seconds() if pd.notna(row['Q3']) else '-'

    data.append({'Abbreviation': abbr, 'Q3_seconds': q3_seconds})
    print(f"P{pos}: {abbr} - Q1: {q1} | Q2: {q2} | Q3: {q3} | Q3(s): {q3_seconds} ({name} - {team})")

q3_df = pd.DataFrame(data)
print(f"\nQ3 DataFrame:\n{q3_df}\n")

# Merging 2025 Quali with 2024 Race
merged_df = q3_df.merge(laps_2024, left_on='Abbreviation', right_on='Driver')
merged_df['Q3_seconds'] = pd.to_numeric(merged_df['Q3_seconds'], errors='coerce') # Convert to numeric
merged_df.dropna(subset=['Q3_seconds', 'LapTime (s)'], inplace=True)  # Drop rows with NaN
print(f"\nMerged DataFrame:\n{merged_df}\n")

# Feature and target variables
X = merged_df[['Q3_seconds']]
y = merged_df['LapTime (s)']
print(X)
print(y)

# 2. SPLITTING DATASET ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# 3. TRAIN GRADIENT BOOSTING MODEL ---------------------------------------------------------------
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# 4. PREDICTION ----------------------------------------------------------------------------------
q3_df['Q3_seconds'] = pd.to_numeric(q3_df['Q3_seconds'], errors='coerce') # Convert to numeric
q3_df.dropna(subset=['Q3_seconds'], inplace=True)  # Drop rows with NaN

pred_lap_times = model.predict(q3_df[['Q3_seconds']])
q3_df['Predicted_LapTime (s)'] = pred_lap_times

# Sort by predicted lap time
q3_df.sort_values(by='Predicted_LapTime (s)', ascending=True, inplace=True)

# Print the predictions
print("\nPredicted Lap Times and GP Winner:\n")
print(q3_df[['Abbreviation', 'Q3_seconds', 'Predicted_LapTime (s)']])

# 5. EVALUATION ----------------------------------------------------------------------------------
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"\nMean Absolute Error: {mae:.2f} seconds\n")

# 6. VISUALIZATION -------------------------------------------------------------------------------