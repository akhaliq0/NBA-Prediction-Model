import pandas as pd

def predict_matchup_baseline(home_team: str, away_team: str, df: pd.DataFrame, col="PTS_r10"):
    last = df.sort_values("GAME_DATE").groupby("TEAM_ID").tail(1)
    id_by_name = df[["TEAM_ID","TEAM_NAME"]].drop_duplicates().set_index("TEAM_NAME")["TEAM_ID"]
    h = last[last["TEAM_ID"] == int(id_by_name[home_team])].iloc[0]
    a = last[last["TEAM_ID"] == int(id_by_name[away_team])].iloc[0]
    ph = float(h[col]); pa = float(a[col])
    return {
        "home": home_team, "away": away_team,
        "pred_home": round(ph,1), "pred_away": round(pa,1),
        "winner": home_team if ph > pa else away_team
    }


def predict_matchup_baseline_homeaway(home_team: str, away_team: str, frame: pd.DataFrame, window: int = 10):
    last = frame.sort_values("GAME_DATE").groupby("TEAM_ID").tail(1)
    id_by_name = frame[["TEAM_ID","TEAM_NAME"]].drop_duplicates().set_index("TEAM_NAME")["TEAM_ID"]
    h = last[last["TEAM_ID"] == int(id_by_name[home_team])].iloc[0]
    a = last[last["TEAM_ID"] == int(id_by_name[away_team])].iloc[0]
    ph = float(h[f"PTS_r{window}_home"])
    pa = float(a[f"PTS_r{window}_away"])
    return {
        "home": home_team, "away": away_team,
        "pred_home": round(ph,1), "pred_away": round(pa,1),
        "winner": home_team if ph > pa else away_team
    }