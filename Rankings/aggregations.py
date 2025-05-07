import numpy as np
import pandas as pd


def add_runvalues(df, run_avg_col, runvalue_col, runvalue_avg_col, total_played_col, player_col, runs_col, dismissed_col, factor_cols):
    """Aggregate the "value of runs" for each player.

    Args:
        df: the filtered dataframe for a format.
        run_avg_col: the column name of the new raw runs average column.
        runvalue_col: the column name of the new runvalue column.
        runvalue_avg_col: the column name of the new runvalue average column.
        total_played_col: the column name of the new total innings played column.
        player_col: the column name for player ID.
        runs_col: the column name for (raw) runs made.
        dismissed_col: the column name for whether the player was dismissed.
        factor_cols: a list with column names for all factors.

    Returns:
        A dataframe which has columns:
            player_col, runs_col (summed), runvalue_col (summed), runvalue_avg_col, run_avg_col
    """
    cols = factor_cols + [player_col, runs_col, dismissed_col]
    df_filtered = df[cols]
    df_filtered[runvalue_col] = df_filtered[runs_col]

    for c in factor_cols:
        df_filtered[runvalue_col] *= df_filtered[c]
    
    # Set total_played_col to 0 if Nan, else set to 1.
    df_filtered[total_played_col] =  np.where(df_filtered[runs_col].isna(), 0, 1)

    # Now group by and sum.
    cols_to_sum = [runs_col, runvalue_col, dismissed_col, total_played_col]
    df_filtered = df_filtered.groupby(player_col)[cols_to_sum].sum(numeric_only=True).reset_index()

    # If dismissed = 0 but total_played_col > 0, set dismissed = 1.0.
    df_filtered.loc[
        (df_filtered[dismissed_col] == 0.0) & (df_filtered[total_played_col] > 0.0), 
        dismissed_col] = 1.0
    
    # Also add the average columns.
    df_filtered[runvalue_avg_col] = df_filtered[runvalue_col] / df_filtered[dismissed_col]
    df_filtered[run_avg_col] = df_filtered[runs_col] / df_filtered[dismissed_col]


    return df_filtered


def add_wicketvalues(df, wickets_avg_col, wicketvalue_col, wicketvalue_avg_col, player_col, total_played_col, balls_bowled, wickets_col, factor_cols):
    """Aggregate the "value of runs" for each player.

    Args:
        df: the filtered dataframe for a format.
        wickets_avg_col: the column name of the new RAW wickets AVG column.
        wicketvalue_col: the column name of the new wickets value column.
        wicketvalue_avg_col: the column name of the new wickets value AVG column.
        player_col: the column name for player ID.
        total_played_col: the column name of the new total innings played column.
        balls_bowled: the column name for the number of balls bowled.
        wickets_col: the column name for (raw) number of wickets.
        factor_cols: a list with column names for all factors.

    Returns:
        A dataframe which has columns:
            player_col, wickets_col (summed), wicketvalue_col (summed), wickets_avg_col, wicketsvalue_avg_col
    """
    cols = factor_cols + [player_col, wickets_col, balls_bowled]
    df_filtered = df[cols]
    df_filtered[wicketvalue_col] = df_filtered[wickets_col]

    for c in factor_cols:
        df_filtered[wicketvalue_col] *= df_filtered[c]
    
    # Set total_played_col to 0 if Nan, else set to 1.
    df_filtered[total_played_col] =  np.where(
        (df_filtered[balls_bowled].isna() | df_filtered[balls_bowled] == 0) , 0, 1)

    # Now group by and sum.
    cols_to_sum = [wickets_col, wicketvalue_col, total_played_col]
    df_filtered = df_filtered.groupby(player_col)[cols_to_sum].sum(numeric_only=True).reset_index()
    
    # Also add the average columns.
    df_filtered[wicketvalue_avg_col] = df_filtered[wicketvalue_col] / df_filtered[total_played_col]
    df_filtered[wickets_avg_col] = df_filtered[wickets_col] / df_filtered[total_played_col]


    return df_filtered