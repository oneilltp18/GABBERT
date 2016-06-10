import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep


# define a function to get the soup

def get_soup(a_url):
    r = requests.get(a_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def next_page(a_url, count):
    url = a_url+str(count)
    return url


# define a function that pulls all of the individual player rows from a page
def get_rows(a_soup):
    table = a_soup.find('section', {'class':'wisbb_body'})
    body = table.find('tbody')
    rows = body.findAll('tr', {'class':''})
    return rows

def strip_stats(some_rows, i):
    for x in range(0,len(some_rows)):
        player_stats = some_rows[x].findAll('td')
        player = [z.text for z in player_stats]
        player.append(i)
        stats.append(player)

# Define a funciton that will return the number of pages in the search.
def last_page(a_soup):
    pages = a_soup.find('div', {'class':'wisbb_paginator'})
    page_links = pages.findAll('a')
    final_page = page_links[-2].text.strip()
    return int(final_page)

# This function adds the season year onto the end of each player's stat list
def add_season(stat_list, year):
    for i in stat_list:
        i.append(year)


# for the compiler function, it'll need something increment the counter

def rec_stats(a_url, i):
    count = 1
    upper_limit = last_page(get_soup(a_url+str(count)))
    print i
    print upper_limit
    while count <= upper_limit:
        url = next_page(a_url, count)
        soup = get_soup(url)
        page_rows = get_rows(soup)
        strip_stats(page_rows, i)
        print '%d Players processed' % len(stats)
        count+=1
        sleep(5)

stats = []
# rec_stats(base_url)
stats
# The sixteen_years function will allow us to pull multiple years within the same function,
# and it will also append a value to the end of each stat row that contains the season year
def sixteen_years(range):
        year_urls = ['http://www.foxsports.com/nfl/stats?season='+str(x)+'&week=100&category=PASSING&opp=0&sort=2&qualified=0&sortOrder=0&page=' for x in range]
        print year_urls
        loc = 0
        for year in year_urls:
            rec_stats(year, range[loc])
            loc +=1
years = range(1999,2016)

sixteen_years(years)

columns = ['name', 'games', 'completions', 'pass_atts', 'comp_pct', 'att_pg',
            'pass_yards', 'pass_avg', 'avg_ypg', 'pass_tds', 'ints', 'qbr', 'throws_for_1down',
            '1down_pct', 'long_throw', 'passes_over_25', '300_ydg', 'sacks_taken',
            'sack_yds', 'fumbles', 'fumbles_lost', 'season']
df = pd.DataFrame(stats, columns = columns)

df.head()

# Add a team column using regex and the contents of the full name columns
df['team'] = df['name'].str.extract('([A-Z][A-Z]+)', expand=True)



# pull the phone book style name out of the name column
df['real_name'] = df['name'].str.extract('([A-Z]\w+, \w+)', expand = False)

# Apply regex to a colun in the data frame that puts the name in the proper order
df['real_name'] = df['real_name'].str.replace(r"([A-Z][\w|\W]*),\s([A-Z][\w|\W]+\b)", r"\2 \1")


# replace the wonky 'name' column with the new proper name
df['name'] = df['real_name']

# Drop the redundant 'real_name' column
df.drop('real_name', inplace = True, axis = 1)

numerics = ['games', 'completions', 'pass_atts', 'comp_pct', 'att_pg',
            'pass_yards', 'pass_avg', 'avg_ypg', 'pass_tds', 'ints', 'qbr', 'throws_for_1down',
            '1down_pct', 'long_throw', 'passes_over_25', '300_ydg', 'sacks_taken',
            'sack_yds', 'fumbles', 'fumbles_lost', 'season']
for col in numerics:
    df[col] = df[col].convert_objects(convert_numeric=True)

from sqlalchemy import create_engine
engine = create_engine('postgresql://codylaminack@localhost:5432/nfl')

df.to_sql('fox_passing', engine)
