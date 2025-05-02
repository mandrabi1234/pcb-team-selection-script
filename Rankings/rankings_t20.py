import numpy as np
import pandas as pd

from constants import *


def standardize_runvals(df, col, min_percentile, max_percentile):
    
    runsval_min = df[col].quantile(min_percentile)
    runsval_max = df[col].quantile(max_percentile)
    runsval_range = runsval_max - runsval_min + 1

    # Set the floor.
    df.loc[df[col] < runsval_min, col] = runsval_min

    # Normalize
    df[col] = (df[col] - runsval_min) / runsval_range

    return df


def batting_rankings(df):

    df_filtered = df[df[BATTING_INNINGS_PLAYED] >= T20_MIN_NUM_BATTING_INNINGS]

    # Standardize RunValues
    df_filtered = standardize_runvals(
        df_filtered, RUNVALUE_COL, T20_RUNS_MIN_PERCENTILE, T20_RUNS_MAX_PERCENTILE)
    
    print(df_filtered)
    # Standardize RunValues_AVG
    df_filtered = standardize_runvals(
        df_filtered, RUNVALUE_AVG_COL, T20_RUNS_MIN_PERCENTILE, T20_RUNS_MAX_PERCENTILE)
    
    # Combine.
    df_filtered[BATTING_COMBINED_SCORE] = (
        (T20_BATTING_RUNSVALUE_TOTAL_PROP * df_filtered[RUNVALUE_COL]) +
        (T20_BATTING_RUNSVALUE_AVG_PROP * df_filtered[RUNVALUE_AVG_COL])
    )

    df_filtered[BATTING_RANKING] = df_filtered[BATTING_COMBINED_SCORE].rank(method='dense')

    return df_filtered
