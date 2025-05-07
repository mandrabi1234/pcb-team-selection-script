import pandas as pd
import numpy as np


def data_preprocessing(df):
    # TODO: use constants for column names instead of hardcoding


    print(df.columns)
    # Ensure all Runs Made text values are set to NaNs.
    df.loc[df["Runs Made"] == "DNB", "Runs Made"] = np.nan

    # Clean Up Runs Made column to remove * 
    df["Runs Made"] = pd.to_numeric(df["Runs Made"].str.replace('*', '', regex=False), errors='coerce')

    # df["Runs Made"] = df["Runs Made"].str.replace('*', '', regex=False).astype(float)
    # df["Runs Made"] = df["Runs Made"].str.replace('Retired Hurt', '', regex=False).astype(float)

    df["Runs Made"] = df["Runs Made"].astype(float)

    # Ensure own team and opposition team rankings are floats.
    df["Team Standing"] = df["Team Standing"].apply(lambda x: ''.join(filter(str.isdigit, str(x))))
    df["Team Standing"] = pd.to_numeric(df["Team Standing"], errors="coerce")
    
    df["Opposition Standing"] = df["Opposition Standing"].apply(lambda x: ''.join(filter(str.isdigit, str(x))))
    df["Opposition Standing"] = pd.to_numeric(df["Opposition Standing"], errors="coerce")
    
    df["Team Standing"] = df["Team Standing"].astype(float)
    df["Opposition Standing"] = df["Opposition Standing"].astype(float)

    # Convert Batters Dimissed to string (since it is comma separated).
    df["Batters Dismissed"] = df["Batters Dismissed"].astype(str)
    df.loc[df["Batters Dismissed"] == "nan", "Batters Dismissed"] = "0"

    # Convert Dimissed Column from YES/NO to 1/0 (also correct some typos)
    # Dismissed Tags
    df.loc[df["Dismissed"] == "YES", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "Yes", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "YSE", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "yes", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "ye", "Dismissed"] = 1.0    
    df.loc[df["Dismissed"] == "Caught", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "LBW", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "Runout", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "Bowled", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "LWB", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "Hit Wicket", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "Cuaght", "Dismissed"] = 1.0
    df.loc[df["Dismissed"] == "Run out", "Dismissed"] = 1.0
    
    # Not Dismissed Tags
    df.loc[df["Dismissed"] == "Nout out", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "ABSENT HURT", "Dismissed"] = 0.0    
    df.loc[df["Dismissed"] == "Absent Hurt", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "ABND", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "Did not play", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "Did Not Play", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "Did not Play", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "no", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "Did not", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "NO", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "No", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "DNP", "Dismissed"] = 0.0
    df.loc[df["Dismissed"].isna(), "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "Retired Hurt", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "Abandoned", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "Not out", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "*", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "Did Not play", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "Not Out", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "not Out", "Dismissed"] = 0.0
    df.loc[df["Dismissed"] == "DNB", "Dismissed"] = np.nan
    df["Dismissed"] = df["Dismissed"].astype(float)

    # Convert Special Batting Talent Column from YES/NO to 1/0 (also correct some typos)
    df.loc[df["Special Batting Talent"] == "YES", "Special Batting Talent"] = 1.0
    df.loc[df["Special Batting Talent"] == "Yes", "Special Batting Talent"] = 1.0
    df.loc[df["Special Batting Talent"] == "yes", "Special Batting Talent"] = 1.0
    df.loc[df["Special Batting Talent"] == "", "Special Batting Talent"] = 0.0
    df.loc[df["Special Batting Talent"] == "No", "Special Batting Talent"] = 0.0
    df.loc[df["Special Batting Talent"] == "NO", "Special Batting Talent"] = 0.0
    df.loc[df["Special Batting Talent"] == "no", "Special Batting Talent"] = 0.0
    df.loc[df["Special Batting Talent"].isna(), "Special Batting Talent"] = 0.0 
    df.loc[df["Special Batting Talent"] == "DNB", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "ABND", "Special Batting Talent"] = np.nan

    df.loc[df["Special Batting Talent"] == "DNP", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "*", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "Abandoned", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "Did Not Play", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "Did not Play", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "Did Not play", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "Did not play", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "-", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "N/a", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "N/A", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "n/a", "Special Batting Talent"] = np.nan
    df.loc[df["Special Batting Talent"] == "n/A", "Special Batting Talent"] = np.nan
    df["Special Batting Talent"] = df["Special Batting Talent"].astype(float)


    df.loc[df["Balls Consumed"] == "DNP", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "*", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "��7", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "ABSENT HURT", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "ABND", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "Retired Hurt", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "Time Out", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "Abandoned", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "Did Not Play", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "Did not Play", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "Did Not play", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "Did not play", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "-", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "N/a", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "N/A", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "n/a", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "n/A", "Balls Consumed"] = np.nan
    df.loc[df["Balls Consumed"] == "No", "Balls Consumed"] = np.nan
    #df["Balls Consumed"] = pd.to_numeric(df["Balls Consumed"].str.replace('`', '', regex=False), errors='coerce')
    df["Balls Consumed"] = df["Balls Consumed"].astype(float)

    # # Convert Special Bowling Talent Column from YES/NO to 1/0 (also correct some typos)
    # df.loc[df["Special Bowling Talent"] == "YES", "Special Bowling Talent"] = 1.0
    # df.loc[df["Special Bowling Talent"] == "Yes", "Special Bowling Talent"] = 1.0
    # df.loc[df["Special Bowling Talent"] == "yes", "Special Bowling Talent"] = 1.0
    # df.loc[df["Special Bowling Talent"] == "", "Special Bowling Talent"] = 0.0
    # df.loc[df["Special Bowling Talent"] == "No", "Special Bowling Talent"] = 0.0
    # df.loc[df["Special Bowling Talent"].isna(), "Special Bowling Talent"] = 0.0 
    # df.loc[df["Special Bowling Talent"] == "Abandoned", "Special Bowling Talent"] = np.nan
    # df.loc[df["Special Bowling Talent"] == "Did Not Play", "Special Bowling Talent"] = np.nan
    # df.loc[df["Special Bowling Talent"] == "Did not Play", "Special Bowling Talent"] = np.nan
    # df.loc[df["Special Bowling Talent"] == "Did Not play", "Special Bowling Talent"] = np.nan
    # df.loc[df["Special Bowling Talent"] == "Did not play", "Special Bowling Talent"] = np.nan
    # df.loc[df["Special Bowling Talent"] == "-", "Special Bowling Talent"] = np.nan
    # df.loc[df["Special Bowling Talent"] == "N/a", "Special Bowling Talent"] = np.nan
    # df.loc[df["Special Bowling Talent"] == "N/A", "Special Bowling Talent"] = np.nan
    # df.loc[df["Special Bowling Talent"] == "n/a", "Special Bowling Talent"] = np.nan
    # df.loc[df["Special Bowling Talent"] == "n/A", "Special Bowling Talent"] = np.nan 
    # df.loc[df["Special Bowling Talent"] == "ABND", "Special Bowlilng Talent"] = np.nan
  
    # df["Special Bowling Talent"] = df["Special Bowling Talent"].astype(float)

