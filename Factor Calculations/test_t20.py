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
INPUT = "PCB Player Data - Filtered.csv"
df_input = pd.read_csv(os.path.join("..", DATA_DIRECTORY, INPUT))

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


print(df_input)

# Log test output in csv format: test_t20_output.csv 
df_input.to_csv(f"test_t20_output{str(date.today())}.csv", index=False)
