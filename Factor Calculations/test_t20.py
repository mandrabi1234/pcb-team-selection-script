import os

import pandas as pd
import numpy as np
import datetime
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt

from data_cleaning import *
import factors_t20 as ft20
import constants_t20 as t20

# Input data filename.
DATA_DIRECTORY = "data"
INPUT = r"..\data\m_ali_sample.csv"


df_input = pd.read_csv(os.path.join(DATA_DIRECTORY, INPUT))

# Data preprocessing (cleaning)
data_preprocessing(df_input)

# Set the SR factor.
ft20.strike_rate_factor(df_input, "Runs made", "Balls consumed", t20.FACTOR_SR)

# Set the Tournament factor.
ft20.tournament_calibre_factor(df_input, "Tournament", t20.FACTOR_TOURNAMENT)

# Set the Team Ranking diff (Opposition Quality) factor
ft20.opp_quality_factor(df_input, "Team standing", "Opposition standing", t20.FACTOR_OPP_QUALITY)

ft20.batting_position_factor(df_input, "Runs made", "Batting position", t20.FACTOR_BAT_POSITION)

print(df_input)
