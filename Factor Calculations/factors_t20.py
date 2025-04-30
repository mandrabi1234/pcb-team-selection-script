import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_columns', None)

import constants_t20 as t20

# Compute the Strike Rate Factor for each (player, match, innings).
def strike_rate_factor(df, runs_made_col_name, balls_faced_col_name, sr_factor_col_name):

    # First set the Normalized Strike Rate:
    # Norm_SR = 100 * (Runs Made / Balls Faced) / SR_BASELINE
    df[sr_factor_col_name] = np.where(
        df[runs_made_col_name].isna() | df[balls_faced_col_name].isna(), 
        t20.SR_FACTOR_DEFAULT,
        (100 / t20.SR_BASELINE) * df[runs_made_col_name] / df[balls_faced_col_name]
    )

    # Now clip on the Min/Max.
    df.loc[df[sr_factor_col_name] < t20.SR_FACTOR_MIN, sr_factor_col_name] = t20.SR_FACTOR_MIN
    df.loc[df[sr_factor_col_name] > t20.SR_FACTOR_MAX, sr_factor_col_name] = t20.SR_FACTOR_MAX


# Compute the Tournament Calibre Factor for each (player, match, innings).
def tournament_calibre_factor(df, tournament_col_name, tournament_factor_col_name):

    df[tournament_factor_col_name] = df[tournament_col_name].apply(
        lambda x: t20.TOURNAMENT_FACTOR_DICT[x] if x in t20.TOURNAMENT_FACTOR_DICT else t20.TOURNAMENT_FACTOR_DEFAULT)



# Compute the Opposition Quality Factor for each (player, match, innings).
def opp_quality_factor(df, own_team_ranking, opposition_ranking, opp_quality_factor_col_name):

    # First set the ranking diffs. These need to be signed.
    # They are also normalized by the max range allowed.
    real_diff_allowed = 2 * t20.OPP_QUALITY_RANKING_MAX_DIFF
    df[opp_quality_factor_col_name] = (t20.OPP_QUALITY_RANKING_MAX_DIFF + df[own_team_ranking] - df[opposition_ranking]) / real_diff_allowed
    
    # Now normalize to lie in the factor's min/max range.
    factor_range = t20.OPP_QUALITY_FACTOR_MAX - t20.OPP_QUALITY_FACTOR_MIN
    df[opp_quality_factor_col_name] =  t20.OPP_QUALITY_FACTOR_MIN + (df[opp_quality_factor_col_name] * factor_range)

    # Now clip on the Min/Max.
    df.loc[df[opp_quality_factor_col_name] < t20.OPP_QUALITY_FACTOR_MIN, opp_quality_factor_col_name] = t20.OPP_QUALITY_FACTOR_MIN
    df.loc[df[opp_quality_factor_col_name] > t20.OPP_QUALITY_FACTOR_MAX, opp_quality_factor_col_name] = t20.OPP_QUALITY_FACTOR_MAX
'''
4. If the code and everything above makes sense, you could try your hand at encoding another batting factor. 
This could be the batting position factor where you could bucket batting positions in four buckets: POS 1-3, 
POS 4-5, POS 6-8, POS 9-11. This factor could simply be 0.9 for runs made by POS 1-3, 1.0 for runs made by 4-5,
1.1 for runs made by 6-8 and 1.2 for runs made by POS 9-11. Again, I am just using some starter factor constants
here. The key would be to code this up in a way that the code doesn't need to change to update any of the 
numbers here (factor values or position numbers).
'''
# Compute the batting position factor for each player (4 buckets- POS 1-3, 4-5, 6-8. 9-11)
def batting_position_factor(df, runs_made_col_name, batting_position_col_name, bat_pos_factor_col_name):
    
    for index in df.index:
            if 1 <= df.at[index, batting_position_col_name] <= 3:
                df.at[index, bat_pos_factor_col_name] = (df.at[index, runs_made_col_name] * t20.POS_1_3)
            if 4 <= df.at[index, batting_position_col_name] <= 5:
                df.at[index, bat_pos_factor_col_name] = (df.at[index, runs_made_col_name] * t20.POS_4_5)
            if 6 <= df.at[index, batting_position_col_name] <= 8:
                df.at[index, bat_pos_factor_col_name] = (df.at[index, runs_made_col_name] * t20.POS_6_8)
            if 9 <= df.at[index, batting_position_col_name] <= 11:
                df.at[index, bat_pos_factor_col_name] = (df.at[index, runs_made_col_name] * t20.POS_9_11)
