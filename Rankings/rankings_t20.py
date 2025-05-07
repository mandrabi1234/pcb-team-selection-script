import numpy as np
import pandas as pd

from constants import *


def standardize_vals(df, col, min_percentile, max_percentile):
    
    val_min = df[col].quantile(min_percentile)
    val_max = df[col].quantile(max_percentile)
    val_range = val_max - val_min + 1

    # Set the floor.
    df.loc[df[col] < val_min, col] = val_min

    # Normalize
    df[col] = (df[col] - val_min) / val_range

    return df


def batting_rankings(df, runs_col, runs_avg_col):

    df_filtered = df[df[BATTING_INNINGS_PLAYED] >= T20_MIN_NUM_BATTING_INNINGS]

    # Standardize RunValues
    df_filtered = standardize_vals(
        df_filtered, runs_col, T20_RUNS_MIN_PERCENTILE, T20_RUNS_MAX_PERCENTILE)
    
    print(df_filtered)
    # Standardize RunValues_AVG
    df_filtered = standardize_vals(
        df_filtered, runs_avg_col, T20_RUNS_MIN_PERCENTILE, T20_RUNS_MAX_PERCENTILE)
    
    # Combine.
    df_filtered[BATTING_COMBINED_SCORE] = (
        (T20_BATTING_RUNSVALUE_TOTAL_PROP * df_filtered[runs_col]) +
        (T20_BATTING_RUNSVALUE_AVG_PROP * df_filtered[runs_avg_col])
    )

    df_filtered[BATTING_RANKING] = df_filtered[BATTING_COMBINED_SCORE].rank(method='dense')

    return df_filtered


def bowling_rankings(df, wickets_col, wickets_avg_col):

    df_filtered = df[df[BOWLING_INNINGS_PLAYED] >= T20_MIN_NUM_BOWLING_INNINGS]

    # Standardize WicketValues
    df_filtered = standardize_vals(
        df_filtered, wickets_col, T20_WICKETS_MIN_PERCENTILE, T20_WICKETS_MAX_PERCENTILE)
    
    print(df_filtered)
    # Standardize WicketValues_AVG
    df_filtered = standardize_vals(
        df_filtered, wickets_avg_col, T20_WICKETS_MIN_PERCENTILE, T20_WICKETS_MAX_PERCENTILE)
    
    # Combine.
    df_filtered[BOWLING_COMBINED_SCORE] = (
        (T20_BOWLING_WICKETSVALUE_TOTAL_PROP * df_filtered[wickets_col]) +
        (T20_BOWLING_WICKETSVALUE_AVG_PROP * df_filtered[wickets_avg_col])
    )

    df_filtered[BOWLING_RANKING] = df_filtered[BOWLING_COMBINED_SCORE].rank(method='dense')

    return df_filtered
