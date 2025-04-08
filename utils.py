# Import Libraries
import numpy
import pandas as pd 
from datetime import date


# Algorithm Reference
'''
• Player index: i
• Format index: j ∈ {F, A, T}, where F = First Class, A = List A, = T20
• xi,j : total runs made by a player i in format j
• ai,j : batting average of player i in format j
• si,j : strike rate of player i in format j
'''

# *summaryStats* - calculate the average runs, standard deviation, and minimum value runs for a given format
def summaryStats(dataFrame, minimumVal_mtplr):
    average = dataFrame['Run Value'].mean() # Average Run Value for T20 Run Values
    std = dataFrame['Run Value'].std() # Standard Deviation Across T20 Run Values
    minV = abs(dataFrame['Run Value'].min()) * minimumVal_mtplr # Minimum value runs for T20 
    
    return average, std, minV

# *standardizedRuns* - calculate the standardized run values for a given format
def standardizedRuns(dataFrame, average, std, minV):
    stdRuns = [] # declare an empty array, to be populated later

    # Iterate through the dataframe, and calculate the standardized runs for each player across the given format
    for i in range(len(dataFrame['Player'])):
        stdRun = (dataFrame.at[dataFrame.index[i], 'Run Value'] - average)/std
        stdShift = stdRun + minV
        stdRuns.append(stdRun)
    dataFrame['Standardized Runs'] = stdRuns

    min_scale_shift = abs(dataFrame['Standardized Runs'].min()) # calculate the minimum scale shift

    default_stdV = dataFrame['Standardized Runs'].quantile(0.35) # calculate the default value (35th percentile)

    default_stdV_shifted = default_stdV + (1.1 * min_scale_shift) # shift the default value

    # Shift Standardized Scores
    std_shift = []
    for i in range(len(dataFrame['Player'])):
        std_score_shifted = dataFrame.at[dataFrame.index[i], 'Standardized Runs'] + (1.1 * min_scale_shift)
        std_shift.append(std_score_shifted)

    dataFrame['Standardized Runs - Shifted'] = std_shift

    return dataFrame, default_stdV, default_stdV_shifted

# *runValue_Calc* - calculate the run values—raw and normalized—per player, for a given format
def runValue_Calc(format, runs_quotient, average_quotient, strikeRate_quotient, runValue_weight, minimumVal_mtplr, dataFrame): # if calculating FC stats, list strikeRate_quotient as 0
    
    runData = pd.DataFrame() # empty dataframe, to be populated later
    players = dataFrame['Sr.'].nunique() # Get the length of the entire dataset

    # Empty arrays, to be populated later
    names = []
    values = []
    valuesNorm = []

    # Calculate run values for First Class (fc) cricket
    if format == 'fc':
        for i in range(0, players):
            name = dataFrame.at[dataFrame.index[i], 'Player']
            runValue = ((dataFrame.at[dataFrame.index[i], 'Runs'])/runs_quotient) * ((dataFrame.at[dataFrame.index[i], 'Ave'])/average_quotient) * runValue_weight
            runValue_normalized = (dataFrame.at[dataFrame.index[i], 'Runs']/runs_quotient) * ((dataFrame.at[dataFrame.index[i], 'Ave'])/average_quotient)
            names.append(name)
            values.append(runValue)
            valuesNorm.append(runValue_normalized)

    # Calculate run values for List A and T20 cricket
    else:
        for i in range(0, players):
            name = dataFrame.at[dataFrame.index[i], 'Player']
            runValue = ((dataFrame.at[dataFrame.index[i], 'Runs'])) * ((dataFrame.at[dataFrame.index[i], 'Ave'])/average_quotient) * ((dataFrame.at[dataFrame.index[i], 'SR'])/strikeRate_quotient) * runValue_weight
            runValue_normalized = (dataFrame.at[dataFrame.index[i], 'Runs']) * ((dataFrame.at[dataFrame.index[i], 'Ave'])/average_quotient) * ((dataFrame.at[dataFrame.index[i], 'SR'])/strikeRate_quotient)
            names.append(name)
            values.append(runValue)
            valuesNorm.append(runValue_normalized)
    
    # Append the runData dataframe with player names, and their corresponding run values
    runData['Player'] = names
    runData['Run Value'] = values
    runData['Run Value - Normalized'] = valuesNorm

    runData = runData.fillna(0) # replace any NAN values with 0

    average, std, minV = summaryStats(runData, minimumVal_mtplr) # calculate summary statistics

    runData, default_stdV, default_stdV_shifted = standardizedRuns(runData, average, std, minV) # calculate standardized run values

    runData.to_csv(f'{format} Run Values - {str(date.today())}.csv', index=False) # write the run value data to a .csv file, stored in the working directory

    return runData, default_stdV, default_stdV_shifted, average, std, minV

# *scoreCalc* - generalized formula for calculating the final score per format
def scoreCalc(dataFrame, multpr, index):
    calcScore = (dataFrame.at[dataFrame.index[index], 'Standardized Runs - Shifted'] * multpr)
    return calcScore

# *rowMatch* - adjust the row length of a given dataframe to match another 
#   i.e. add empty rows to List A and FC dataframes to match the larger T20 dataframe
def rowMatch(dataFrame, length):
    dataFrame = dataFrame.reindex(list(range(0, length))).reset_index(drop=True)
    return dataFrame

# *finalScore_Calc* - calculate the final score for each player, across all three formats. 
#   - Calls functions rowMatch, and scoreCalc
def finalScore_Calc(runData_fc, runData_t20, runData_listA, fc_default_stdV_shifted):

    finalRank = pd.DataFrame()
    finalScores = []
    names = []

    # Adjust the row lengths of FC and List A dataframes to match the longer T20 dataframe
    runData_fc = rowMatch(runData_fc, len(runData_t20['Player']))
    runData_listA = rowMatch(runData_fc, len(runData_t20['Player']))

    # Iterate through the dataframes, running score calculations for each player
    for i in range(len(runData_t20['Player'])):
        name = runData_t20.at[runData_t20.index[i], 'Player']
        
        calcScore_fc = scoreCalc(runData_fc, 0.5, i)
        calcScore_listA = scoreCalc(runData_listA, 0.2, i)
        calcScore_t20 = scoreCalc(runData_t20, 0.3, i)
        calcScore_final = calcScore_fc + calcScore_listA + calcScore_t20 # add up the individual format scores to get a final score
        print(calcScore_final)
        print(fc_default_stdV_shifted)
        finalScore = max(fc_default_stdV_shifted, calcScore_final) # compare final score vs default score, take the larger value
        
        finalScores.append(finalScore) # append the finalScores array with the player's assigned final score
        names.append(name) # append the names array with the player's name

    # Append the finalRank dataframe with the player's name and their assigned final score
    finalRank['Player'] = names
    finalRank['Final Score'] = finalScores

    finalRank = finalRank.sort_values(by='Final Score', ascending=False) # sort the final rankings in descending order

    finalRank.to_csv(f'Final Player Rankings- {str(date.today())}.csv', index=False) # write the run value data to a .csv file, stored in the working directory

    return finalRank

