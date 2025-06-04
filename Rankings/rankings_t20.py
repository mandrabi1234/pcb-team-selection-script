import numpy as np
import pandas as pd

from constants import *


def standardize_vals(df, col, new_col, min_percentile, max_percentile):
    val_min = df[col].quantile(min_percentile)
    val_max = df[col].quantile(max_percentile)
    val_range = val_max - val_min + 1e-9  # add non-zero value to avoid division-by-zero situations

    df[new_col] = df[col]

    # Set the floor to min_percentile value
    df.loc[df[new_col] < val_min, new_col] = val_min

    # Normalize
    df[new_col] = (df[new_col] - val_min) / val_range

    # Add a floor and ceiling to avoid zeros and ones
    df[new_col] = df[new_col].clip(lower=0.05, upper=1.0)

    return df


def batting_rankings(df, runs_col, runs_avg_col):
    new_col_suffix = "_normed"
    new_runs_col = runs_col + new_col_suffix
    new_runs_avg_col = runs_avg_col + new_col_suffix

    df_filtered = df[df[BATTING_INNINGS_PLAYED] >= T20_MIN_NUM_BATTING_INNINGS]

    # Standardize RunValues
    df_filtered = standardize_vals(
        df_filtered, runs_col, new_runs_col, T20_RUNS_MIN_PERCENTILE, T20_RUNS_MAX_PERCENTILE)
    
    # Standardize RunValues_AVG
    df_filtered = standardize_vals(
        df_filtered, runs_avg_col, new_runs_avg_col, T20_RUNS_MIN_PERCENTILE, T20_RUNS_MAX_PERCENTILE)
    
    # Combine.
    df_filtered[BATTING_COMBINED_SCORE] = (
        (T20_BATTING_RUNSVALUE_TOTAL_PROP * df_filtered[new_runs_col]) +
        (T20_BATTING_RUNSVALUE_AVG_PROP * df_filtered[new_runs_avg_col])
    )

    df_filtered[BATTING_RANKING] = df_filtered[BATTING_COMBINED_SCORE].rank(method='dense', ascending=False)
    df_filtered = df_filtered.set_index(BATTING_RANKING).sort_index()
    return df_filtered


def bowling_rankings(df, wickets_col, wickets_avg_col):

    new_col_suffix = "_normed"
    new_wick_col = wickets_col + new_col_suffix
    new_wick_avg_col = wickets_avg_col + new_col_suffix

    df_filtered = df[df[BOWLING_INNINGS_PLAYED] >= T20_MIN_NUM_BOWLING_INNINGS]

    # Standardize WicketValues
    df_filtered = standardize_vals(
        df_filtered, wickets_col, new_wick_col, T20_WICKETS_MIN_PERCENTILE, T20_WICKETS_MAX_PERCENTILE)
    
    # Standardize WicketValues_AVG
    df_filtered = standardize_vals(
        df_filtered, wickets_avg_col, new_wick_avg_col, T20_WICKETS_MIN_PERCENTILE, T20_WICKETS_MAX_PERCENTILE)
    
    # Combine.
    df_filtered[BOWLING_COMBINED_SCORE] = (
        (T20_BOWLING_WICKETSVALUE_TOTAL_PROP * df_filtered[new_wick_col]) +
        (T20_BOWLING_WICKETSVALUE_AVG_PROP * df_filtered[new_wick_avg_col])
    )

    df_filtered[BOWLING_RANKING] = df_filtered[BOWLING_COMBINED_SCORE].rank(method='dense', ascending=False)
    df_filtered = df_filtered.set_index(BOWLING_RANKING).sort_index()
    return df_filtered
