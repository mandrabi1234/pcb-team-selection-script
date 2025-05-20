import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import *
from constants import *
from constants_t20 import *
import aggregations as agg 
import factors_t20 as ft20
import rankings_t20 as rank_t20
import sys
import os
import numpy as np
import datetime
from datetime import date


st.set_page_config(layout="wide")


# Sample data
df = pd.read_csv(r"C:\Users\Mohi Andrabi\Documents\GitHub\pcb_teamSelection\pcb-team-selection-script\data\Filtered PCB Player Data - Final 582025.csv")

data_preprocessing(df_input)


# Function to filter and calculate results
def filter_and_calculate(df, param1, param2, param3, param4, param5, param6, param7, param8):  
    return df[(df['parameter1'] == param1) &
              (df['parameter2'] == param2) &
              (df['parameter3'] == param3) &
              (df['parameter4'] == param4) &
              (df['parameter5'] == param5) &
              (df['parameter6'] == param6) &
              (df['parameter7'] == param7) &
              (df['parameter8'] == param8)]


# Streamlit app
st.title("Compare Filtered Data")


title = st.text_input("Filter View Name", help="Enter a name for the filtered view")


# Initialize session state
if 'filtered_outputs' not in st.session_state:
    st.session_state.filtered_outputs = []


# User inputs
col1, col2, col3, col4 = st.columns(4)


with col1:
    param1 = st.slider("Parameter 1 (min value)", 0.0, 10.0, 1.0)
    param5 = st.slider("Parameter 5 (min value)", 0.0, 10.0, 1.0)


with col2:
    param2 = st.slider("Parameter 2 (max value)", 0.0, 50.0, 10.0)
    param6 = st.slider("Parameter 6 (min value)", 0.0, 50.0, 10.0)


with col3:
    param3 = st.slider("Parameter 3 (max value)", 0.0, 10.0, 1.0)
    param7 = st.slider("Parameter 7 (min value)", 0.0, 10.0, 1.0)


with col4:
    param4 = st.slider("Parameter 4 (max value)", 0.0, 10.0, 1.0)
    param8 = st.slider("Parameter 8 (min value)", 0.0, 10.0, 1.0)


# Calculate button
if st.button("Calculate"):
    filtered_df = filter_and_calculate(df, param1, param2, param3, param4, param5, param6, param7, param8)
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



