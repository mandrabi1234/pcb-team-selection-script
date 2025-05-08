# Python file listing all constants used by factors.py.

# Factor Column Names.
FACTOR_SR = "Factor_Runs_SR"
FACTOR_TOURNAMENT = "Factor_Runs_Tournament"

# Opp Quality Factor can be used for Runs and Wickets.
FACTOR_OPP_QUALITY = "Factor_Opp_Quality"

FACTOR_BAT_POSITION = "Factor_Batting_Position"

FACTOR_SPECIAL_BAT_TALENT = "Factor_Special_Batting_Talent"

FACTOR_SPECIAL_BOWL_TALENT = "Factor_Special_Bowling_Talent"

FACTOR_WICKETS_BATTER_POS_DISMISSED = "Factor_Wickets_Batter_Pos_Dimissed"

FACTOR_ECON_RATE = "Factor_Wickets_Economy_rate"
############################################################
# Strike Rate Scaling Constants.
SR_FACTOR_DEFAULT = 1.0

# SR_BASELINE: 
#   the strike rate which will correspond to a factor multiplier of 1.0
SR_BASELINE = 1.1
SR_RANGE_MIN = 0.5
SR_RANGE_MAX = 2.0

# SR_FACTOR_MIN: 
#   The min value for the  Normalized SR (with ref to SR_BASELINE).
SR_FACTOR_MIN = 0.85

# SR_FACTOR_MAX: 
#   The max value for the  Normalized SR (with ref to SR_BASELINE).
SR_FACTOR_MAX = 1.25


############################################################
# Tournament Scaling Constants.
TOURNAMENT_FACTOR_DEFAULT = 1.0

# Set the factor values for various tournament names.
TOURNAMENT_FACTOR_DICT = {
    "psl": 1.2,
    "champions t20": 1.0,
    "national t20": 0.8,

    "champions one day": 1.05,
    "president's cup one-day": 1.0,

    "qat": 1.05,
    "president's trophy grade-I": 1.0,

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

BATTING_POS_DEFAULT = 1.0

# Batting Factor Multiplier for Batting Positions 1-3
POS_1_3 = 0.95

# Batting Factor Multiplier for Batting Positions 4-5
POS_4_5 = 1.0

# Batting Factor Multiplier for Batting Positions 6-8
POS_6_8 = 1.05

# Batting Factor Multiplier for Batting Positions 9-11
POS_9_11 = 1.1


###############################################################
# Wickets Taken Batter Positions Scaling Constants

WICKET_BAT_POS_DEFAULT = 1.0

# Factor for Batter Dimissed at Positions 1-3
WICKET_BAT_POS_FACTOR_DICT = {
    0: 1.0,

    1: 1.1,
    2: 1.1,
    3: 1.1,
    4: 1.05,
    5: 1.05,
    6: 1.0,
    7: 1.0,
    8: 1.0,
    9: 0.95,
    10: 0.95,
    11: 0.95
}


############################################################
# Bowling Economy Rate Scaling Constants.
ECON_RATE_FACTOR_DEFAULT = 1.0

# ECON_RATE_BASELINE: 
#   the economy rate which will correspond to a factor multiplier of 1.0
ECON_RATE_BASELINE = 1.1
ECON_RATE_RANGE_MIN = 0.8
ECON_RATE_RANGE_MAX = 2.0

# ECON_RATE_FACTOR_MIN: 
#   The min value for the  Normalized ECON_RATE (with ref to ECON_RATE_BASELINE).
ECON_RATE_FACTOR_MIN = 0.85

# ECON_RATE_FACTOR_MAX: 
#   The max value for the  Normalized ECON_RATE (with ref to ECON_RATE_BASELINE).
ECON_RATE_FACTOR_MAX = 1.25


###############################################################
# Special Factor Scaling Constants

# Factor Multiplier for tagged Special Batting/Bowling Talents
BAT_TALENT_SPECIAL = 1.1
BOWL_TALENT_SPECIAL = 1.1

# Factor Multiplier for everyone else
BAT_TALENT_DEFAULT = 1.0
BOWL_TALENT_DEFAULT = 1.0