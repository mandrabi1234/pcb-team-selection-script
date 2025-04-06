# Program Name: PCB Run Value Assessment (Preliminary Code)
# Program Function: assigning the value of runs for individual cricketers across three competitive formats: first class, t20, ODI
# Program Author: Mohi Andrabi, Jehangir Amjad PhD
# Creation Date: March 16, 2025
# Location: Los Angeles, CA

# NOTE: Formulas were adapted from those listed in Google Sheets, which differed slightly from those listed in Algorithm write-up

# -- Main Script -- #

# Import Libraries
import numpy
import pandas as pd
from datetime import date

# Read In Run Data For All Formats From Local Directory
fcStats = pd.read_csv(r"C:\Users\Mohi Andrabi\Documents\GitHub\pcb_teamSelection\pcb-team-selection-script\data\Player Values - Last 3 Seasons.xlsx - FC Batting Value (1).csv")
t20Stats = pd.read_csv(r"C:\Users\Mohi Andrabi\Documents\GitHub\pcb_teamSelection\pcb-team-selection-script\data\Player Values - Last 3 Seasons.xlsx - T20 Batting Value (1).csv")
listAStats = pd.read_csv(r"C:\Users\Mohi Andrabi\Documents\GitHub\pcb_teamSelection\pcb-team-selection-script\data\Player Values - Last 3 Seasons.xlsx - LIST A Batting Value (1).csv")

# Algorithm Reference
'''
• Player index: i
• Format index: j ∈ {F, A, T}, where F = First Class, A = List A, = T20
• xi,j : total runs made by a player i in format j
• ai,j : batting average of player i in format j
• si,j : strike rate of player i in format j
'''
summaryStats = pd.DataFrame(columns = ['FORMAT', 'STD_DEV', 'AVERAGE', 'SHIFT']) # empty dataframe, to be populated later with summary statistics for all formats

# -------------------------------------------------------------- #
#                      T20 Run Values                            #
#           Formula: ((xi,A) * (ai,A/150) * (si,A/150)) * 0.2    #
# -------------------------------------------------------------- #

players = t20Stats['Sr.'].nunique() # Get the length of the entire dataset
runValues = pd.DataFrame() # create an empty dataframe, to be populated later with run value data
names = []
values = []
valuesNorm = []

# iterate through the entire dataset, calculating the run value for each player on the roster, based on professor Amjad's formula
for i in range(0, players):
    name = t20Stats.at[t20Stats.index[i], 'Player']
    runValue = (t20Stats.at[t20Stats.index[i], 'Runs']) * ((t20Stats.at[t20Stats.index[i], 'Ave'])/150) * ((t20Stats.at[t20Stats.index[i], 'SR'])/50)* 0.2
    runValue_normalized = (t20Stats.at[t20Stats.index[i], 'Runs']) * ((t20Stats.at[t20Stats.index[i], 'Ave'])/150) * ((t20Stats.at[t20Stats.index[i], 'SR'])/50)
    names.append(name)
    values.append(runValue)
    valuesNorm.append(runValue_normalized)

# Add Player Names and Corresponding Runs Value to the runValues dataframe
runValues['Player'] = names
runValues['Run Value'] = values
runValues['Run Value - Normalized'] = valuesNorm
runValues = runValues.fillna(0) # replace any nan values with 0

# Summary Statistics 
average_t20 = runValues['Run Value'].mean() # Average Run Value for T20 Run Values
std_t20 = runValues['Run Value'].std() # Standard Deviation Across T20 Run Values
min_t20 = abs(runValues['Run Value'].min())*1.1 # Minimum value runs for T20 

summaryStats.loc[0] = ['T20', average_t20, std_t20, min_t20] # Append summaryStats dataframe

# Standardized Runs

stdRuns = []
for i in range(len(runValues['Player'])):
    stdRun = (runValues.at[runValues.index[i], 'Run Value'] - average_t20)/std_t20
    stdShift = stdRun + min_t20
    stdRuns.append(stdRun)
runValues['Standardized Runs'] = stdRuns

min_scale_shift = abs(runValues['Standardized Runs'].min())

default_stdV = round((35/100) * (len(runValues['Player']) - 1) + 1) #

default_stdV_shifted = default_stdV + (1.1 * min_scale_shift) # shift the default score

# Shift Standardized Scores
std_shift = []
for i in range(len(runValues['Player'])):
    std_score_shifted = runValues.at[runValues.index[i], 'Standardized Runs'] + (1.1 * min_scale_shift)
    std_shift.append(std_score_shifted)
    
runValues['Standardized Runs - Shifted'] = std_shift



runValues.to_csv(f't20 Run Values - {str(date.today())}.csv', index=False) # write the run value data to a .csv file, stored in the working directory


# -------------------------------------------------------------- #
#                   First Class Run Values                       #
#             Formula = ((xi,F/2) * (ai,F/150)) * 0.5            #
# -------------------------------------------------------------- #
players = listAStats['Sr.'].nunique() 
runValues = pd.DataFrame() 
names = []
values = []

for i in range(0, players):
    name = listAStats.at[listAStats.index[i], 'Player']
    runValue = (fcStats.at[fcStats.index[i], 'Runs'])/2 * ((fcStats.at[fcStats.index[i], 'Ave'])/150) * 0.5
    names.append(name)
    values.append(runValue)

runValues['Player'] = names
runValues['Run Value'] = values
runValues = runValues.fillna(0)

average_fc = runValues['Run Value'].mean() # Calculate the Average Run Value for T20 Run Values
std_fc = runValues['Run Value'].std() # Calculate the Standard Deviation For T20 Run Values
min_fc = abs(runValues['Run Value'].min())*1.1 # Calculate the minimum value runs for T20 

summaryStats.loc[1] = ['First Class', average_fc, std_fc, min_fc]

runValues.to_csv(f'First Class Run Values - {str(date.today())}.csv', index=False) 


# -------------------------------------------------------------- #
#                     List A Run Values                          #
#         Formula: ((xi,A) * (ai,A/100) * (si,A/100)) *0.2       #
# -------------------------------------------------------------- #

players = listAStats['Sr.'].nunique() 
runValues = pd.DataFrame() 
names = []
values = []

for i in range(0, players):
    name = listAStats.at[listAStats.index[i], 'Player']
    runValue = (listAStats.at[listAStats.index[i], 'Runs']) * ((listAStats.at[listAStats.index[i], 'Ave'])/100) * ((listAStats.at[listAStats.index[i], 'SR'])/100)
    names.append(name)
    values.append(runValue)

runValues['Player'] = names
runValues['Run Value'] = values
runValues = runValues.fillna(0)

average_listA = runValues['Run Value'].mean() # Calculate the Average Run Value for T20 Run Values
std_listA = runValues['Run Value'].std() # Calculate the Standard Deviation For T20 Run Values
min_listA = abs(runValues['Run Value'].min())*1.1 # Calculate the minimum value runs for T20 

summaryStats.loc[2] = ['List A', average_listA, std_listA, min_listA]

runValues.to_csv(f'List A Run Values - {str(date.today())}.csv', index=False) 

summaryStats.to_csv(f'Summary Statistics - All Formats - {str(date.today())}.csv', index=False) # write the summary statistics data for all formats to a .csv file in the working directory

