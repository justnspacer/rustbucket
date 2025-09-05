import nfl_data_py as nfl
import pandas as pd

#Returns seasonal data, including various calculated market share stats specific to receivers
#s_type (str) : optional (default 'REG') season type to include in average ('ALL','REG','POST')
seasonal_data = nfl.import_seasonal_data(years=[2024], s_type='POST')
print(f'seasonal_data: {seasonal_data.head()}')


seasonal_roster = nfl.import_seasonal_rosters(years=[2024], columns=['player_id', 'team', 'position', 'player_name'])
print(f'seasonal_roster: {seasonal_roster.head()}')


#officals
officials = nfl.import_officials()
print(f'officials: {officials.head()}')

#team descriptions
teams = nfl.import_team_desc()
print(f'teams: {teams.head()}')

#draft values
draft_values = nfl.import_draft_values()
print(f'draft_values: {draft_values.head()}')

#qbrs
qbrs = nfl.import_qbr()
print(f'qbrs: {qbrs.head()}')

#seasonal pfr
#('s_type variable must be one of "pass", "rec","rush", or "def".')
seasonal_pfr = nfl.import_seasonal_pfr(years=[2024], s_type='rush')
print(f'seasonal_pro-football-reference: {seasonal_pfr.head()}')

#snap counts
snap_counts = nfl.import_snap_counts(years=[2024])
print(f'snap_counts: {snap_counts.head()}')

#win totals
win_totals = nfl.import_win_totals(years=[2024])
print(f'win_totals: {win_totals.head()}')

#depth charts
depth_charts = nfl.import_depth_charts(years=[2024])
print(f'depth_charts: {depth_charts.head()}')

#injuries
injuries = nfl.import_injuries(years=[2024])
print(f'injuries: {injuries.head()}')