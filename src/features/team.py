import pandas as pd
import numpy as np

def basic_context(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["HOME"] = out["MATCHUP"].str.contains("vs.")
    out = out.sort_values(["TEAM_ID","GAME_DATE"])
    return out

def add_four_factors(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["POSS_proxy"] = df["FGA"] + 0.44*df["FTA"] - df["OREB"] + df["TOV"]
    df["eFG"] = (df["FGM"] + 0.5*df["FG3M"]) / df["FGA"].replace(0, np.nan)
    df["FTr"] = df["FTA"] / df["FGA"].replace(0, np.nan)
    df["TOV_rate"] = df["TOV"] / df["POSS_proxy"].replace(0, np.nan)
    return df

def attach_opponent(df: pd.DataFrame) -> pd.DataFrame:
    opp_cols = ["TEAM_ID","FGM","FGA","FG3M","FTM","FTA","OREB","DREB","REB","TOV","PTS","POSS_proxy","eFG","FTr","TOV_rate"]
    opp = df[["GAME_ID"] + opp_cols].rename(columns={c: f"OPP_{c}" for c in opp_cols})
    m = df.merge(opp, on="GAME_ID")
    m = m[m["TEAM_ID"] != m["OPP_TEAM_ID"]].copy()
    m["ORB_pct"] = m["OREB"] / (m["OREB"] + m["OPP_DREB"]).replace(0, np.nan)
    m["eFG_allowed"] = m["OPP_eFG"]
    m["TOV_rate_forced"] = m["OPP_TOV_rate"]
    return m

def add_rolling(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    g = df.groupby("TEAM_ID", group_keys=False)
    for c in ["PTS","POSS_proxy","eFG","FTr","TOV_rate","ORB_pct","eFG_allowed","TOV_rate_forced"]:
        df[f"{c}_r{window}"] = g[c].rolling(window, min_periods=3).mean().reset_index(level=0, drop=True)
    df["days_rest"] = g["GAME_DATE"].diff().dt.days
    df["is_b2b"] = (df["days_rest"] == 1).astype(int)
    return df


def add_home_away_rolling_pts(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    out = df.sort_values(["TEAM_ID","GAME_DATE"]).copy()
    if "HOME" not in out.columns:
        out["HOME"] = out["MATCHUP"].str.contains("vs.")
    home = (
        out[out["HOME"]].groupby("TEAM_ID")["PTS"]
        .rolling(window, min_periods=1).mean()
        .reset_index(level=0, drop=True)
    )
    away = (
        out[~out["HOME"]].groupby("TEAM_ID")["PTS"]
        .rolling(window, min_periods=1).mean()
        .reset_index(level=0, drop=True)
    )
    out[f"PTS_r{window}_home"] = home
    out[f"PTS_r{window}_away"] = away

    # carry latest computed value forward so the team's last row always has a value
    out[f"PTS_r{window}_home"] = out.groupby("TEAM_ID")[f"PTS_r{window}_home"].ffill()
    out[f"PTS_r{window}_away"] = out.groupby("TEAM_ID")[f"PTS_r{window}_away"].ffill()
    return out



def build_matchup_frame(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """
    Build a dataset where each row represents one team in one game,
    containing both its own offensive rolling stats and the opponent's defensive rolling stats.
    """
    df = df.sort_values(["TEAM_ID", "GAME_DATE"]).copy()

    # pick columns that describe offense & defense
    off_cols = [f"eFG_r{window}", f"FTr_r{window}", f"TOV_rate_r{window}",
                f"ORB_pct_r{window}", f"PTS_r{window}"]
    def_cols = [f"eFG_allowed_r{window}", f"TOV_rate_forced_r{window}"]

    # offensive frame
    off = df[["GAME_ID","TEAM_ID","TEAM_NAME","HOME"] + off_cols].copy()
    # defensive frame (rename with _opp_)
    opp = df[["GAME_ID","TEAM_ID"] + def_cols].rename(
        columns={c: f"{c}_opp" for c in def_cols}
    )

    # merge each team row with its opponent's defensive features
    merged = off.merge(opp, on="GAME_ID", suffixes=("","_x"))
    merged = merged[merged["TEAM_ID"] != merged["TEAM_ID_x"]].drop(columns=["TEAM_ID_x"])

    # bring in target (actual points scored)
    pts = df[["GAME_ID","TEAM_ID","PTS"]]
    merged = merged.merge(pts, on=["GAME_ID","TEAM_ID"])

    return merged.reset_index(drop=True)