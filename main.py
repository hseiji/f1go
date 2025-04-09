import fastf1
from fastf1 import plotting
import pandas as pd

# Enable caching for faster loading
fastf1.Cache.enable_cache('cache')

# Load event schedule for 2024
schedule = fastf1.get_event_schedule(2024)

# Print all race names with dates
print("2024 F1 Race Calendar:\n")
for round_num, event in schedule['RoundNumber'].items():
    date = schedule.loc[round_num, 'Session5Date'].date()
    location = schedule.loc[round_num, 'Location']
    country = schedule.loc[round_num, 'Country']
    print(f"Round {round_num}: {country} - {location} - {date}")
print("\n")

# Load the latest season and round info
season = 2024
round_number = 4  # Change this to latest round number or loop through rounds

# Load qualifying session
session = fastf1.get_session(season, round_number, 'Q')
session.load()

# Get results
results = session.results[['FullName', 'Abbreviation', 'TeamName', 'Position', 'Q1', 'Q2', 'Q3']]

print(f"\n🏁 Qualifying Results - {session.event['EventName']} 🏁\n")

for _, row in results.iterrows():
    pos = int(row['Position'])
    name = row['FullName']
    abbr = row['Abbreviation']
    team = row['TeamName']
    q1 = str(row['Q1']).split('0 days ')[-1][:12] if pd.notna(row['Q1']) else '-'
    q2 = str(row['Q2']).split('0 days ')[-1][:12] if pd.notna(row['Q2']) else '-'
    q3 = str(row['Q3']).split('0 days ')[-1][:12] if pd.notna(row['Q3']) else '-'

    print(f"P{pos}: {abbr} - Q1: {q1} | Q2: {q2} | Q3: {q3} ({name} - {team})")

pole_sitter = results.loc[results['Position'] == 1, 'FullName'].values[0]
pole_abbr = results.loc[results['Position'] == 1, 'Abbreviation'].values[0]

print(f"\nPole Position: {pole_sitter} ({pole_abbr})")