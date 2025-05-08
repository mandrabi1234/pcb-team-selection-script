import sys
import os

import pandas as pd
import numpy as np
import datetime
from datetime import date
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt

# Get the absolute path to the required directories.
FOLDERS = ["Factor Calculations", "Base Calculations"]
for folder in FOLDERS:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", folder))

    # Add the parent directory to sys.path
    sys.path.append(parent_dir)

from data_cleaning import *
from constants import *
from constants_t20 import *
import aggregations as agg 
import factors_t20 as ft20
import rankings_t20 as rank_t20


# Input data filename.
DATA_DIRECTORY = "data"
INPUT = "Filtered PCB Player Data - Final 582025"
INPUT2 = "player mapping.csv"

df_input = pd.read_csv(os.path.join("..", DATA_DIRECTORY, INPUT))

player_mapping = pd.read_csv(os.path.join("..", DATA_DIRECTORY, INPUT2))



# Data preprocessing (cleaning)
data_preprocessing(df_input)

# Only keep T20 data.
df_input = df_input[df_input["Tournament"].isin(["psl", "champions t20", "national t20"])]

# Set the SR factor.
ft20.strike_rate_factor(df_input, "Runs Made", "Balls Consumed", FACTOR_SR)

# Set the Tournament factor.
ft20.tournament_calibre_factor(df_input, "Tournament", FACTOR_TOURNAMENT)

# Set the Team Ranking diff (Opposition Quality) factor
ft20.opp_quality_factor(df_input, "Team Standing", "Opposition Standing", FACTOR_OPP_QUALITY)

# Set the Batting Position Factor
ft20.batting_position_factor(df_input, "Runs Made", "Batting Position", FACTOR_BAT_POSITION)

# Set the Special Batting Talent Factor
ft20.special_bat_talent_factor(df_input, "Special Batting Talent", FACTOR_SPECIAL_BAT_TALENT)

#print(df_input)
#print(len(df_input["Player ID"].unique()))


## BATTING

# Aggregation.
batting_factors = [FACTOR_SR, FACTOR_TOURNAMENT, FACTOR_OPP_QUALITY, FACTOR_BAT_POSITION, FACTOR_SPECIAL_BAT_TALENT]
df_bat_agg = agg.add_runvalues(
    df_input,
    RUN_AVG_COL, 
    RUNVALUE_COL,
    RUNVALUE_AVG_COL,
    BATTING_INNINGS_PLAYED,
    PLAYER_ID, 
    RUNS_MADE, 
    DISMISSED_COL,
    batting_factors
)

def player_map(df_map, df_input, player_name_col, player_id_col):
    id_to_name = pd.Series(df_map[player_name_col].values, index=df_map[player_id_col]).to_dict()
    df_input[player_name_col] = df_input[player_id_col].map(id_to_name)
    df_output = df_input.loc[:, [player_name_col] + [col for col in df_input.columns if col != player_name_col]]
    return df_output

#print(len(df_bat_agg["Player ID"].unique()))

# Batting Rankings
df_bat_rank = rank_t20.batting_rankings(df_bat_agg, RUNVALUE_COL, RUNVALUE_AVG_COL)
df_bat_rank = player_map(player_mapping, df_bat_rank, "Player Name", "Player ID")

print(df_bat_rank)
#print(len(df_bat_rank["Player ID"].unique()))

# Log test output in csv format: test_t20_batting_rankings_output.csv 
df_bat_rank.to_csv(f"test_t20_rankings_bat_output{str(date.today())}.csv", index=False)


## BOWLING
#Set the Special Bowling Talent Factor
ft20.special_bat_talent_factor(df_input, "Special Bowling Talent", FACTOR_SPECIAL_BOWL_TALENT)

#Batter dismissed factor.
ft20.batters_dismissed_position_factor(df_input, "Wickets Taken", "Batters Dismissed", FACTOR_WICKETS_BATTER_POS_DISMISSED)

#Economy Rate factor.
ft20.economy_rate_factor(df_input, "Runs Given", "Balls Bowled", FACTOR_ECON_RATE)

bowling_factors = [FACTOR_ECON_RATE, FACTOR_WICKETS_BATTER_POS_DISMISSED, FACTOR_TOURNAMENT, FACTOR_OPP_QUALITY, FACTOR_SPECIAL_BOWL_TALENT]
df_bowl_agg = agg.add_wicketvalues(
    df_input, 
    WICKETS_AVG_COL, 
    WICKETVALUE_COL, 
    WICKETVALUE_AVG_COL, 
    PLAYER_ID, 
    BOWLING_INNINGS_PLAYED, 
    BALLS_BOWLED, 
    WICKETS_COL, 
    bowling_factors
)
# print(df_bowl_agg)

# Bowling Rankings
df_bowl_rank = rank_t20.bowling_rankings(df_bowl_agg, WICKETVALUE_COL, WICKETVALUE_AVG_COL)
df_bowl_rank = player_map(player_mapping, df_bowl_rank, "Player Name", "Player ID")

print(df_bowl_rank)


# Log test output in csv format: test_t20_bowling_rankings_output.csv 
df_bowl_rank.to_csv(f"test_t20_rankings_bowl_output{str(date.today())}.csv", index=False)
