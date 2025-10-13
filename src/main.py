import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import nba_api 

from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players


careers = players.find_players_by_full_name("Nikola Jokic")
career_id = careers[0]["id"]

df = playercareerstats.PlayerCareerStats(player_id=career_id).get_data_frames()[0]


print(df)

