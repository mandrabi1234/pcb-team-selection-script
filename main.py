# -- Main Script -- #

# Import Libraries
import numpy
import pandas as pd
from datetime import date
from utils import summaryStats, standardizedRuns, runValue_Calc, finalScore_Calc

# Read In Run Data For All Formats From Local Directory
fcStats = pd.read_csv(r"LOCAL DIRECTORY\data\Player Values - Last 3 Seasons.xlsx - FC Batting Value (1).csv")
t20Stats = pd.read_csv(r"LOCAL DIRECTORY\data\Player Values - Last 3 Seasons.xlsx - T20 Batting Value (1).csv")
listAStats = pd.read_csv(r"LOCAL DIRECTORY\data\Player Values - Last 3 Seasons.xlsx - LIST A Batting Value (1).csv")

summaryStats = pd.DataFrame(columns = ['FORMAT', 'STD_DEV', 'AVERAGE', 'SHIFT']) # empty dataframe, to be populated later with summary statistics for all formats

# Calculate run values, per player, for each format
fc_Stats, fc_default_stdV, fc_default_stdV_shifted, average_fc, std_fc, minV_fc = runValue_Calc('fc', 2, 150, 0, 0.5, 1.1, fcStats)
t20_Stats, t20_default_stdV, t20_default_stdV_shifted, average_t20, std_t20, minV_t20 = runValue_Calc('t20', 1, 150, 50, 0.3, 1.1, t20Stats)
listA_Stats, listA_default_stdV, lisA_default_stdV_shifted, average_listA, std_listA, minV_listA = runValue_Calc('list A', 1, 100, 100, 0.2, 1.1, listAStats)

# Append summaryStats dataframe with every format's data
summaryStats.loc[0] = ['FC', average_fc, std_fc, minV_fc] 
summaryStats.loc[1] = ['T20', average_t20, std_t20, minV_t20] 
summaryStats.loc[2] = ['List A', average_listA, std_listA, minV_listA] 

summaryStats.to_csv(f'Summary Statistics- {str(date.today())}.csv', index=False) # write the run value data to a .csv file, stored in the working directory

# Calculate the final scores for each player
finalRank = finalScore_Calc(fc_Stats, t20_Stats, listA_Stats, fc_default_stdV_shifted)
