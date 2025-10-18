from nba_api.stats.endpoints import TeamGameLogs
import pandas as pd
from nba_api.stats.static import teams as static_teams

def get_team_game_logs_season(season="2024-25", season_types=("Regular Season","Playoffs")) -> pd.DataFrame:
    frames = []
    for st in season_types:
        logs = TeamGameLogs(season_nullable=season,
                            season_type_nullable=st,
                            league_id_nullable="00",
                            date_from_nullable="2024-10-01",
                            date_to_nullable="2025-06-30")
        frames.append(logs.get_data_frames()[0])
    df = pd.concat(frames, ignore_index=True)
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    keep = ["SEASON_YEAR","TEAM_ID","TEAM_ABBREVIATION","TEAM_NAME","GAME_ID","GAME_DATE",
            "MATCHUP","WL","FGM","FGA","FG3M","FG3A","FTM","FTA","OREB","DREB","REB",
            "AST","TOV","STL","BLK","PF","PTS","PLUS_MINUS"]
    df = df[keep]
    nba_team_ids = {t["id"] for t in static_teams.get_teams()}
    df = df[df["TEAM_ID"].isin(nba_team_ids)]
    return df.sort_values(["GAME_DATE","TEAM_NAME"]).reset_index(drop=True)
