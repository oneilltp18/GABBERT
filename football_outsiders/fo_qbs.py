import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
import re

# The goal of this thing is to pull the advanced analytics off football outsiders

# define a function to get the soup

def get_soup(a_url):
    r = requests.get(a_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


# Get the first two tables from the quarterbacks advanced stats. The third
# table is rushing stats, which don't exist in enough volume to be useful to us. this
# will pull in all the qbs who threw at least 10 passes in the given season.
def get_tables(this_soup):
    tables = this_soup.findAll('table')
    return tables[0], tables[1]



 # Pull all of the rows out of a given table and return them
def get_rows(a_table):
    rows = a_table.findAll('tr')
    return rows
# Define a function that strips the stats from the first table
def strip_stats_one(some_rows, i, pos):
    for x in range(0,len(some_rows)):
        player_stats = some_rows[x].findAll('td')
        player = [z.text for z in player_stats]
        player.append(i[-4:])
        player.append(pos)
        link = some_rows[x].findAll('a', href=True)
        player.append(link)
        table_1_stats.append(player)
# define a function that strips the stats from the second table.
def strip_stats_two(some_rows, i, pos):
    for x in range(0,len(some_rows)):
        player_stats = some_rows[x].findAll('td')
        player = [z.text for z in player_stats]
        player.append(i[-4:])
        player.append(pos)
        link = some_rows[x].findAll('a', href=True)
        player.append(link)
        table_2_stats.append(player)

def make_url_list(a_range, pos):
    urls = ["http://www.footballoutsiders.com/stats/"+pos+str(x) for x in a_range]
    return urls


# This list will fill with all of the advanced wr stats from the first table of our date range
table_1_stats = []
table_2_stats = []
table_1_stats[1]
df = pd.DataFrame(table_1_stats)
df.tail()

def tables(a_range, pos):
    urls = make_url_list(a_range, pos)
    print urls
    for year in urls:
        print year[-4:]
        soup = get_soup(year)
        table_one, table_two = get_tables(soup)
        rows1 = get_rows(table_one)
        rows2 = get_rows(table_two)
        strip_stats_one(rows1, year[-4:], pos)
        strip_stats_two(rows2, year[-4:], pos)
        sleep(3)


# Write a function that will turn our two tables into a single dataframe
def join_lists(first_table, second_table):
    first_table_df = pd.DataFrame(first_table, columns = first_table[0])
    first_table_df.drop('Rk', axis = 1, inplace = True)
    second_table_df = pd.DataFrame(second_table, columns = second_table[0])
    frames = [second_table_df, first_table_df]
    joined_df = pd.concat(frames)
    final_joined_df = joined_df[joined_df['Player']!='Player']
    renamed_df = final_joined_df.rename(columns = {'1999': 'season', 'wr':'position'})
    renamed_df = renamed_df.reset_index()
    return renamed_df

tables(range(1999,2016), 'qb')

df = join_lists(table_1_stats, table_2_stats)

df.head()
len(df.columns)

def cleaned_df(df):
    df['name'] = df.ix[:,18].apply(lambda x: re.findall(r"([A-Z|a-z]\w+-[A-Z|a-z]\w+)", str(x)))
    df['name'] = df['name'].apply(lambda x: str(x).replace('-', ' '))
    df['name'] = df['name'].astype(str)
    df['name'] = df['name'].str.extract(r"([A-Z|a-z]\w+\s[A-Z|a-z]\w+)", expand = False)
    df.drop(['index'], axis=1, inplace = True)
    df.drop(df.columns[-2], axis=1, inplace=True)
    return df
df = cleaned_df(df)
df.tail(10)
df.shape
