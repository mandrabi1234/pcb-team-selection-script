import sys
import os

sys.path.append(r'C:\Users\Mohi Andrabi\Documents\GitHub\pcb_teamSelection\pcb-team-selection-script\Factor Calculations')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import date

# Now import your project modules
from data_cleaning import *
from constants import *
from constants_t20 import *
import aggregations as agg 
import factors_t20 as ft20
import rankings_t20 as rank_t20



st.set_page_config(layout="wide")


# Sample data
df = pd.read_csv(r"C:\Users\Mohi Andrabi\Documents\GitHub\pcb_teamSelection\pcb-team-selection-script\data\Filtered PCB Player Data - Final 582025.csv")
player_mapping = pd.read_csv(r"C:\Users\Mohi Andrabi\Documents\GitHub\pcb_teamSelection\pcb-team-selection-script\data\player_mapping.csv")

data_preprocessing(df)

format = st.text_input("Bowling/B", help="Enter a name for the filtered view")
rankingSelect = st.selectbox(
    "What type of ranking would you like to generate?",
    ("Batting", "Bowling"),
)

def player_map(df_map, df_input, player_name_col, player_id_col):
    id_to_name = pd.Series(df_map[player_name_col].values, index=df_map[player_id_col]).to_dict()
    df_input[player_name_col] = df_input[player_id_col].map(id_to_name)
    df_output = df_input.loc[:, [player_name_col] + [col for col in df_input.columns if col != player_name_col]]
    return df_output



# Function to filter and calculate results
def filter_and_calculate(df_input, rankingSelect, SR_Factor, Tournament_Factor, Opponent_Factor, Bat_Pos_Factor, Special_Bat_Talent_Factor, Special_Bowling_Talent, Bowling_Factor, Wickets_Batter_Pos_Dismissed, Econ_Rate_Bowling):  
    # Only keep T20 data.
    df_input = df_input[df_input["Tournament"].isin(["psl", "champions t20", "national t20"])]

    if rankingSelect == "Batting":
        # Set the SR factor.
        ft20.strike_rate_factor(df_input, "Runs Made", "Balls Consumed", SR_Factor)

        # Set the Tournament factor.
        ft20.tournament_calibre_factor(df_input, "Tournament", Tournament_Factor)

        # Set the Team Ranking diff (Opposition Quality) factor
        ft20.opp_quality_factor(df_input, "Team Standing", "Opposition Standing", Opponent_Factor)

        # Set the Batting Position Factor
        ft20.batting_position_factor(df_input, "Runs Made", "Batting Position", Bat_Pos_Factor)

        # Set the Special Batting Talent Factor
        ft20.special_bat_talent_factor(df_input, "Special Batting Talent", Special_Bat_Talent_Factor)

        batting_factors = [SR_Factor, Tournament_Factor, Opponent_Factor, Bat_Pos_Factor, Special_Bat_Talent_Factor]
        df_bat_agg = agg.add_runvalues(
            df_input,
            RUN_AVG_COL, 
            RUNVALUE_COL,
            RUNVALUE_AVG_COL,
            BATTING_INNINGS_PLAYED,
            PLAYER_ID, 
            RUNS_MADE, 
            DISMISSED_COL,
            batting_factors
        )

        df_bat_rank = rank_t20.batting_rankings(df_bat_agg, RUNVALUE_COL, RUNVALUE_AVG_COL)
        df_bat_rank = player_map(player_mapping, df_bat_rank, "Player Name", "Player ID")
        return df_bat_rank
    else:
        #Set the Special Bowling Talent Factor
        ft20.special_bat_talent_factor(df_input, "Special Bowling Talent", Special_Bowling_Talent)

        #Batter dismissed factor.
        ft20.batters_dismissed_position_factor(df_input, "Wickets Taken", "Batters Dismissed", Wickets_Batter_Pos_Dismissed)

        #Economy Rate factor.
        ft20.economy_rate_factor(df_input, "Runs Given", "Balls Bowled", Econ_Rate_Bowling)

        bowling_factors = [Econ_Rate_Bowling, Wickets_Batter_Pos_Dismissed, Tournament_Factor, Opponent_Factor, Special_Bowling_Talent]
        df_bowl_agg = agg.add_wicketvalues(
            df_input, 
            WICKETS_AVG_COL, 
            WICKETVALUE_COL, 
            WICKETVALUE_AVG_COL, 
            PLAYER_ID, 
            BOWLING_INNINGS_PLAYED, 
            BALLS_BOWLED, 
            WICKETS_COL, 
            bowling_factors
        )
        # print(df_bowl_agg)

        # Bowling Rankings
        df_bowl_rank = rank_t20.bowling_rankings(df_bowl_agg, WICKETVALUE_COL, WICKETVALUE_AVG_COL)
        df_bowl_rank = player_map(player_mapping, df_bowl_rank, "Player Name", "Player ID")
        return df_bowl_rank


# Streamlit app
st.title("Compare Filtered Data")


title = st.text_input("Filter View Name", help="Enter a name for the filtered view")


# Initialize session state
if 'filtered_outputs' not in st.session_state:
    st.session_state.filtered_outputs = []


# User inputs
col1, col2, col3, col4 = st.columns(4)

with col1:
    param1 = st.slider("Strike Rate Factor", 0.0, 10.0, 1.0)
    param5 = st.slider("Tournament Weighting", 0.0, 10.0, 1.0)


with col2:
    param2 = st.slider("Opponent Quality Weighting", 0.0, 50.0, 10.0)
    param6 = st.slider("Batting Position Weighting", 0.0, 50.0, 10.0)


with col3:
    param3 = st.slider("Special Batting Talent Weighting", 0.0, 10.0, 1.0)
    param7 = st.slider("Special Bowling Talent Weighting", 0.0, 10.0, 1.0)


with col4:
    param4 = st.slider("Bowling Weighting", 0.0, 10.0, 1.0)
    param8 = st.slider("Batter Dismissal Position Weighting", 0.0, 10.0, 1.0)
    param9 = st.slider("Economy Rate Weighting", 0.0, 10.0, 1.0)



# Calculate button
if st.button("Calculate"):
    filtered_df = filter_and_calculate(df, rankingSelect, param1, param2, param3, param4, param5, param6, param7, param8, param9)
    if len(st.session_state.filtered_outputs) < 5:
        st.session_state.filtered_outputs.append({
            'title': title or f"Output {len(st.session_state.filtered_outputs) + 1}",
            'data': filtered_df
        })
    else:
        st.warning("You can only store up to 5 filtered outputs.")


# Display results side by side
cols = st.columns(5)


for i, output in enumerate(st.session_state.filtered_outputs):
    with cols[i]:
        st.subheader(output['title'])
        st.dataframe(output['data'])



