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
INPUT = "PCB Player Data - Filtered.csv"

df_input = pd.read_csv(os.path.join("..", DATA_DIRECTORY, INPUT))

# Data preprocessing (cleaning)
data_preprocessing(df_input)

# Only keep T20 data.
#df_input = df_input[df_input["Tournament"] == "Champions T20"]

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

print(df_input)

# Aggregation.
batting_factors = [FACTOR_SR, FACTOR_TOURNAMENT, FACTOR_OPP_QUALITY, FACTOR_BAT_POSITION, FACTOR_SPECIAL_BAT_TALENT]
df_agg = agg.add_runvalues(
    df_input, 
    RUNVALUE_COL,
    RUNVALUE_AVG_COL,
    BATTING_INNINGS_PLAYED,
    PLAYER_ID, 
    RUNS_MADE, 
    DISMISSED_COL,
    batting_factors
)

print(df_agg)

# Rankings
df_rank = rank_t20.batting_rankings(df_agg)

print(df_rank)

# Log test output in csv format: test_t20_rankings_output.csv 
df_rank.to_csv(f"test_t20_rankings_output{str(date.today())}.csv", index=False)
