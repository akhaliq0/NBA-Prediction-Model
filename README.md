# NBA-Prediction-Model
**NBA Stats Prediction Project**
Using NBA API data (2003–2004 to 2024–2025) to forecast the 2025–2026 season

 **Overview**
This project uses NBA API data from the 2003–2004 season through the 2024–2025 season to train regression models that forecast:
  *Team game scores
  *Player stats (points, rebounds, assists, steals, blocks, turnovers, 3-pointers made)

For the 2025–2026 schedule, the project allows you to:
  *Select an upcoming game.
  *View the predicted final score.
  *Choose multiple players from that matchup and see their projected stat lines.

Injury reports, lineup data, and playoff games are included to make predictions more realistic.

**Features**
  *Pulls 20+ years of NBA stats via the NBA API (Insert Link).
  *Predicts team-level scores with regression models.
  *Predicts player-level stats for multiple targets:
  *Points (PTS)
  *Rebounds (REB)
  *Assists (AST)
  *Steals (STL)
  *Blocks (BLK)
  *Turnovers (TOV)
  *3-Pointers Made (3PM)
  *Adjusts forecasts with injury reports and lineup data.

**Project Structure**
nba-prediction-project/
│── data/               # Raw + processed NBA API datasets
│── notebooks/          # Jupyter notebooks for exploration & modeling
│── src/                # Scripts for data, features, modeling, evaluation
│── models/             # Saved regression models (joblib/pickle)
│── results/            # Prediction outputs + evaluation metrics
│── README.md           # Project documentation


**Tech Stack**
  *Python 3.10+
  *Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn, xgboost/lightgbm, Jupyter
  *Data Source: nba_api (Insert Link)

****Methodology****

**1. Data Collection**
  *Historical stats (2003–2025 seasons) via NBA API.
  *2025–2026 schedule loaded for future predictions.
  *Integrated injury and lineup data where available.
**2. Feature Engineering**
  *Rolling averages (last 5, 10, 20 games).
  *Opponent offensive/defensive context.
  *Game context (home/away, rest days, back-to-back).
  *Player context (age, career stage, starter/bench role).
**3. Modeling (Regression)**
 *Baseline: Linear Regression.
  *Regularized: Ridge & Lasso.
  *Advanced: Random Forest, XGBoost.
**4. Evaluation**
  *Metrics: RMSE & MAE.
  *Season-based train/test splits (no data leakage).
**5.Prediction**
  *Game-level: Predicted team scores.
  *Player-level: PTS, REB, AST, STL, BLK, TOV, 3PM.

****Example Predictions****
**Predicted Game Score**

{
  "game": "LAL vs BOS",
  "date": "2025-11-12",
  "predicted_score": {
    "LAL": 113.1,
    "BOS": 108.7
  }
}

**Predicted Player Stats**
[
  {
    "player": "LeBron James",
    "team": "LAL",
    "predicted_stats": {
      "pts": 24.1,
      "reb": 6.8,
      "ast": 7.3,
      "stl": 1.1,
      "blk": 0.6,
      "tov": 3.2,
      "3pm": 1.9
    }
  },
  {
    "player": "Jayson Tatum",
    "team": "BOS",
    "predicted_stats": {
      "pts": 27.5,
      "reb": 8.2,
      "ast": 4.1,
      "stl": 1.2,
      "blk": 0.8,
      "tov": 2.7,
      "3pm": 3.0
    }
  }
]

**License**
This project is licensed under the MIT License – see the LICENSE(inset link) file for details.
