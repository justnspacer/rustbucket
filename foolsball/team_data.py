import nfl_data_py as nfl
import pandas as pd
import json

# Get team descriptions
teams = nfl.import_team_desc()
print("Team descriptions loaded successfully!")
print(f"Columns: {teams.columns.tolist()}")
print(f"Number of teams: {len(teams)}")
print(teams.head())

# Convert to JSON for frontend use
teams_json = teams.to_json(orient='records', indent=2)
with open('teams_data.json', 'w') as f:
    f.write(teams_json)

print("\nTeam data saved to teams_data.json")
