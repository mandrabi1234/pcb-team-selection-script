import pandas as pd
import numpy as np


def data_preprocessing(df):
    # TODO: use constants for column names instead of hardcoding

    # Ensure all Runs Made text values are set to NaNs.
    df.loc[df["Runs made"] == "DNB", "Runs made"] = np.nan
    df["Runs made"] = df["Runs made"].astype(float)

    # Ensure own team and opposition team rankings are floats.
    df["Team standing"] = df["Team standing"].apply(lambda x: ''.join(filter(str.isdigit, str(x))))
    df["Opposition standing"] = df["Opposition standing"].apply(lambda x: ''.join(filter(str.isdigit, str(x))))
    df["Team standing"] = df["Team standing"].astype(float)
    df["Opposition standing"] = df["Opposition standing"].astype(float)