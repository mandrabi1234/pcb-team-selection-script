import os

import pandas as pd
import numpy as np
from datetime import date
import datetime
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt

from data_cleaning import *
import factors_t20 as ft20
import constants_t20 as c_t20

# Input data filename.
DATA_DIRECTORY = "data"
INPUT = "Filtered PCB Player Data - Final 582025"
INPUT2 = "player mapping.csv"

df_input = pd.read_csv(os.path.join("..", DATA_DIRECTORY, INPUT))

player_mapping = pd.read_csv(os.path.join("..", DATA_DIRECTORY, INPUT2))

# Data preprocessing (cleaning)
data_preprocessing(df_input)

# Set the SR factor.
ft20.strike_rate_factor(df_input, "Runs Made", "Balls Consumed", c_t20.FACTOR_SR)

# Set the Tournament factor.
ft20.tournament_calibre_factor(df_input, "Tournament", c_t20.FACTOR_TOURNAMENT)

# Set the Team Ranking diff (Opposition Quality) factor
ft20.opp_quality_factor(df_input, "Team Standing", "Opposition Standing", c_t20.FACTOR_OPP_QUALITY)

# Set the Batting Position Factor
ft20.batting_position_factor(df_input, "Runs Made", "Batting Position", c_t20.FACTOR_BAT_POSITION)

# Set the Special Batting Talent Factor
ft20.special_bat_talent_factor(df_input, "Special Batting Talent", c_t20.FACTOR_SPECIAL_BAT_TALENT)

# Set the Special Bowling Talent Factor
ft20.special_bat_talent_factor(df_input, "Special Bowling Talent", c_t20.FACTOR_SPECIAL_BOWL_TALENT)

# Batter dismissed factor.
ft20.batters_dismissed_position_factor(df_input, "Wickets Taken", "Batters Dismissed", c_t20.FACTOR_WICKETS_BATTER_POS_DISMISSED)

# Economy Rate factor.
ft20.economy_rate_factor(df_input, "Runs Given", "Balls Bowled", c_t20.FACTOR_ECON_RATE)

df_input = df_input.drop('Player Name', axis=1)

def player_map(df_map, df_input, player_name_col, player_id_col):
    id_to_name = pd.Series(df_map[player_name_col].values, index=df_map[player_id_col]).to_dict()
    df_input[player_name_col] = df_input[player_id_col].map(id_to_name)
    df_output = df_input.loc[:, [player_name_col] + [col for col in df_input.columns if col != player_name_col]]
    return df_output

df_input = player_map(player_mapping, df_input, "Player Name", "Player ID")


print(df_input)


# Log test output in csv format: test_t20_output.csv 
df_input.to_csv(f"test_t20_output{str(date.today())}.csv", index=False)
