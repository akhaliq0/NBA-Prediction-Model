import nba_api
import matplotlib
import math
import pandas as pd
import numpy as np

# Adding 25 -26 Season and Extracting Home vs Away

from nba_api.stats.endpoints import leaguegamefinder 
gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable='2025-26')
games_df = gamefinder.get_data_frames()[0]

def extract_home_away(row):
    matchup = row['MATCHUP']
    team = row['TEAM_ABBREVIATION']
    if 'vs.' in matchup:
        home_team = team
        away_team = matchup.split('vs. ')[1]
    else:
        away_team = team
        home_team = matchup.split('@ ')[1]
    return pd.Series([home_team, away_team])

games_df[['HOME_TEAM', 'AWAY_TEAM']] = games_df.apply(extract_home_away, axis=1)

print(games_df[['GAME_DATE', 'TEAM_ID', 'TEAM_ABBREVIATION', 'MATCHUP']].head())
