import pandas as pd
import re
import numpy as np
# """ SQL query to pull this df:
# "SELECT wide_receivers.*, fox_receiving."100yd_gms", fox_receiving."yac", fox_receiving."first_down_ctchs", fox_receiving."first_down_ctchpct", fox_receiving."long_ctch", fox_receiving."recs_ovr_25", fox_receiving."drops", fo_wrs."EYds", fo_wrs."DPI", fo_wrs."DVOA", fo_wrs."DYAR", fo_wrs."position", combine_stats."Hand Size in", combine_stats."Arm Length in", combine_stats."40 Yard", combine_stats."Vert Leap in", combine_stats."Broad Jump in", combine_stats."Shuttle", combine_stats."3Cone", combine_stats."60Yd Shuttle"
# FROM wide_receivers
# LEFT JOIN fox_receiving
# ON CONCAT(wide_receivers."name", wide_receivers."team") = CONCAT(fox_receiving."name", fox_receiving."team")
# AND wide_receivers."season" = fox_receiving."season"
# LEFT JOIN fo_wrs
# ON CONCAT(lower(wide_receivers."name"), wide_receivers."team") = CONCAT(lower(fo_wrs."name"), fo_wrs."Team")
# and wide_receivers."season" = fo_wrs."season"
# left JOIN combine_stats
# ON wide_receivers."name" = combine_stats."Name"
# AND LOWER(fo_wrs."position") = LOWER(combine_stats."POS")
# WHERE wide_receivers."position" = 'wr'


df = pd.read_csv('/Users/codylaminack/Documents/Practice/GABBERT/sql_wrs.csv')
df.tail()

df.dtypes
df.height.head()


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


# There are several columns that are listed as percents, but don't serve that purpose. They need the % stripped and then to be converted to percent floats.
percent_columns = ['ctch_pct', 'first_down_ctchpct', 'DVOA', 'DYAR']


df.head(25)
# Fill null values on certain columns
df.draft_pos.fillna('UDFA', inplace=True)
