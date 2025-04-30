# Python file listing all constants used by factors.py.

# Factor Column Names.
FACTOR_SR = "Factor_Runs_SR"
FACTOR_TOURNAMENT = "Factor_Runs_Tournament"

# Opp Quality Factor can be used for Runs and Wickets.
FACTOR_OPP_QUALITY = "Factor_Opp_Quality"

FACTOR_BAT_POSITION = "Factor_Batting_Position"

############################################################
# Strike Rate Scaling Constants.
SR_FACTOR_DEFAULT = 1.0

# SR_BASELINE: 
#   the strike rate which will correspond to a factor multiplier of 1.0
SR_BASELINE = 110

# SR_FACTOR_MIN: 
#   The Normalized SR (with ref to SR_BASELINE) below which all factor 
#   values are set to this SR_FACTOR_MIN.
#   Example: for a SR_BASELINE of 110 and actual SR of 50,
#       The SR factor will be SR_FACTOR_MIN becayse 50/110 < SR_FACTOR_MIN.
SR_FACTOR_MIN = 0.5

# SR_FACTOR_MAX: 
#   The Normalized SR (with ref to SR_BASELINE) above which all factor 
#   values are set to this SR_FACTOR_MAX.
#   Example: for a SR_BASELINE of 110 and actual SR of 225,
#       The SR factor will be SR_FACTOR_MAX becayse 225/110 > SR_FACTOR_MAX.
SR_FACTOR_MAX = 2.0


############################################################
# Tournament Scaling Constants.
TOURNAMENT_FACTOR_DEFAULT = 1.0

# Set the factor values for various tournament names.
TOURNAMENT_FACTOR_DICT = {
    "Champions T20": 1.2,

    "Champions One Day": 1.2,
    "President's Cup One-Day": 1.0,

    "QAT": 1.2,
    "President's Trophy Grade-I": 1.0,

}


############################################################
# Opposition Quality Scaling Constants.

# Opp Quality Scaling Constants.
OPP_QUALITY_FACTOR_DEFAULT = 1.0

# OPP_QUALITY_RANKING_MAX_DIFF
#   The real maximum ranking difference between teams to consider.
#   All differences in ranking larger than this are set to the same.
OPP_QUALITY_RANKING_MAX_DIFF = 4.0

# OPP_QUALITY_FACTOR_MIN: 
#   Min possible value of Opposition Quality factor multiplier.
OPP_QUALITY_FACTOR_MIN = 0.8

# OPP_QUALITY_FACTOR_MAX: 
#   Max possible value of Opposition Quality factor multiplier.
OPP_QUALITY_FACTOR_MAX = 1.2


###############################################################
# Batting Position Scaling Constants

# Batting Factor Multiplier for Batting Positions 1-3
POS_1_3 = 0.9

# Batting Factor Multiplier for Batting Positions 4-5
POS_4_5 = 1.0

# Batting Factor Multiplier for Batting Positions 6-8
POS_6_8 = 1.1

# Batting Factor Multiplier for Batting Positions 9-11
POS_9_11 = 1.2