import numpy as np
import pandas as pd


def add_runvalues(df, runvalue_col, runvalue_avg_col, total_played_col, player_col, runs_col, dismissed_col, factor_cols):
    """Aggregate the "value of runs" for each player.

    Args:
        df: the filtered dataframe for a format.
        runvalue_col: the column name of the new runvalue column.
        runvalue_avg_col: the column name of the new runvalue average column.
        total_played_col: the column name of the new total innings played column.
        player_col: the column name for player ID.
        runs_col: the column name for (raw) runs made.
        dismissed_col: the column name for whether the player was dismissed.
        factor_cols: a list with column names for all factors.

    Returns:
        A dataframe which has columns:
            player_col, runs_col (summed), runvalue_col (summed)
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
    
    # Also add the average column.
    df_filtered[runvalue_avg_col] = df_filtered[runvalue_col] / df_filtered[dismissed_col]

    return df_filtered