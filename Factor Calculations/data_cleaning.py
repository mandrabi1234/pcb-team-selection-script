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

    # Convert Dimissed Column from YES/NO to 1/0 (also correct some typos)
    df.loc[df["Dismissed"] == "YES", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "YSE", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "NO", "Dismissed"] = 0.0
    df.loc[df["Dismissed"].isna(), "Dismissed"] = 0.0    
    df["Dismissed"] = df["Dismissed"].astype(float)

    # Convert Special Batting Talent Column from YES/NO to 1/0 (also correct some typos)
    df.loc[df["Special Batting Talent"] == "YES", "Special Batting Talent"] = 1.0
    df.loc[df["Special Batting Talent"] == "Yes", "Special Batting Talent"] = 1.0
    df.loc[df["Special Batting Talent"] == "yes", "Special Batting Talent"] = 1.0
    df.loc[df["Special Batting Talent"] == "", "Special Batting Talent"] = 0.0
    df.loc[df["Special Batting Talent"] == "No", "Special Batting Talent"] = 0.0
    df.loc[df["Special Batting Talent"].isna(), "Special Batting Talent"] = 0.0    
    df["Special Batting Talent"] = df["Special Batting Talent"].astype(float)

    
    # Convert Special Bowling Talent Column from YES/NO to 1/0 (also correct some typos)
    df.loc[df["Special Bowling Talent"] == "YES", "Special Bowling Talent"] = 1.0
    df.loc[df["Special Bowling Talent"] == "Yes", "Special Bowling Talent"] = 1.0
    df.loc[df["Special Bowling Talent"] == "yes", "Special Bowling Talent"] = 1.0
    df.loc[df["Special Bowling Talent"] == "", "Special Bowling Talent"] = 0.0
    df.loc[df["Special Bowling Talent"] == "No", "Special Bowling Talent"] = 0.0
    df.loc[df["Special Bowling Talent"].isna(), "Special Bowling Talent"] = 0.0    
    df["Special Bowling Talent"] = df["Special Bowling Talent"].astype(float)