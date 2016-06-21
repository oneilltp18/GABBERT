import pandas as pd
import re
import numpy as np


df = pd.read_csv('https://raw.githubusercontent.com/cl65610/GABBERT/master/wide_receivers/wr_master_join.csv')
df.tail()

df.dtypes


# Create a column that has a player's height in inches
df['height_inches'] = pd.to_numeric(df.height.str.extract(r"([0-9])", expand = False))*12 + pd.to_numeric(df.height.str.extract(r"-([0-9]+)", expand = False))
# Now that we have the height in inches, we don't need this comlumn
df.drop('height', axis=1, inplace=True)


# Create a ratio of games played to games started
df['start_ratio'] = df['games_started']/df['games']
#With the starts ratio, we don't need the games_started column
df.drop('games_started', axis=1, inplace = True)


# Create two new columns: one for dpis_drawn, and one for dpi_yards
df['dpis_drawn'] = pd.to_numeric(df.DPI.str.extract(r"([0-9]+)", expand=False))
df['dpi_yards'] = pd.to_numeric(df.DPI.str.extract(r"/([0-9]+)", expand=False))

# There will be many values that are null here. They can be safely filled with zeroes.
df.dpis_drawn.fillna(0, inplace=True)
df.dpi_yards.fillna(0, inplace=True)
# we can now drop the useless DPI column
df.drop('DPI', axis=1, inplace = True)

# Find out what the deal is with the 40-yard dash columns
df['40 Yard'] = df['40 Yard'].apply(lambda x: str(x).strip('*'))
df['40 Yard'].replace('nan', 0, inplace=True)
# It doesn't seem like this totally works yet. Can't yet take an average
pd.to_numeric(df['40 Yard'])

df.columns
# Drop a lot of the unnecessary columns
drop_cols = ['index', 'rk', 'league', 'av', 'years_in_league']
for col in drop_cols:
    df.drop(col, axis=1, inplace=True)


# There are several columns that are listed as percents, but don't serve that purpose. They need the % stripped and then to be converted to percent floats.
percent_columns = ['ctch_pct', 'first_down_ctchpct', 'DVOA', 'DYAR']
for col in percent_columns:
    df[col] = df[col].apply(lambda x: str(x).replace('%', ''))
    df[col] = df[col].apply(lambda x: float(x)/100)

###

# Fill null values on numeric columns
na_fills = ['rush_atts', 'rush_yds', 'rush_y/a', 'rush_tds', 'rush_ypg', 'targets',
            'receptions', 'rec_yards', 'yards/reception', 'rec_tds', 'rec_ypg',
            'ctch_pct', 'y/tgt', 'fumbles', 'fumbles_recovered', 'fum_ret_yds', 'fum_tds',
            'forced_fumbles', '100yd_gms', 'yac', 'first_down_ctchs', 'first_down_ctchpct', 'long_ctch',
            'recs_ovr_25', 'drops']
for col in na_fills:
    df[col].fillna(0, inplace=True)

# Fill null value on the draft position column
df.draft_pos.fillna('UDFA', inplace=True)
df.columns
# Engineer some columns that show what percentage of a team's total offense a player represents

# What percent of pass attempts were targed at a player?
df['pct_team_tgts'] = df['targets'] /df['team_pass_attempts']

# What percent of a team's total receptions is a player responsible for?

df['pct_team_receptions'] = df['receptions']/df['team_completions']

# What percent of a team's total offense was this player responsible for?

df['pct_of_team_passyards'] = df['rec_yards']/ df['team_pass_yards']

# What percent of a team's passing touchdowns was a player responsible for?

df['pct_team_touchdowns'] = df['rec_tds']] / df['team_pass_tds']


# Make a column that computes what season a player is in
df['years_in_league'] = df['season']-df['rookie_season']
df.head(25)

### This is to manually change values for certain missing columns
df.iloc[df[(df.name == 'Steve Smith') & ((df.team == 'NYG') | (df.team == 'PHI') | (df.team == 'STL'))].index, 54] = 2007

df.iloc[df[(df.name == 'Antonio Brown') & (df.team == 'PIT')].index, 54] = 2010

df.iloc[df[(df.name == 'Mike Williams') & ((df.team == 'DET') | (df.team == '2TM') | (df.team == 'SEA'))].index, 54] = 2005

df.iloc[df[(df.name == 'Chris Davis') & (df.team == 'TEN')].index, 54] = 2007

df.iloc[df[(df.name == 'Chris Harper')&(df.team == '2TM')].index, 54] = 2013

df.iloc[df[(df.name == 'Roy Williams')&(df.draft_pos == '1-8')].index, 54] = 2002

df.iloc[df[(df.name == 'Charles Johnson')&(df.draft_pos == 'UDFA')].index, 54] = 2013

df.iloc[df[(df.name == 'Chris Givens')&(df.draft_pos == 'UDFA')].index, 54] = 2012

## Now we can engineer a few features based on filled in data
df_clean['years_in_league'] = df_clean['season'] - df_clean['rookie_season']

df_clean['rookie_age'] = df_clean['age'] - df_clean['years_in_league']



# df.to_csv('cleaned_wrs.csv')

