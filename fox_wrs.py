import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep


base_url = 'http://www.foxsports.com/nfl/stats?season=1999&week=100&category=RECEIVING&opp=0&sort=2&qualified=1&sortOrder=0&page='
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
        year_urls = ['http://www.foxsports.com/nfl/stats?season='+str(x)+'&week=100&category=RECEIVING&opp=0&sort=2&qualified=1&sortOrder=0&page=' for x in range]
        print year_urls
        loc = 0
        for year in year_urls:
            rec_stats(year, range[loc])
            loc +=1
years = range(1999,2016)
years

sixteen_years(years)


stats[-10:]
columns = ['name', 'games', 'receptions', 'yards', 'yds_per_ctch', 'yds_per_game',
            'yac', 'td', 'long_ctch', 'recs_ovr_25', '100yd_gms', 'targets', 'drops',
            'ctch_pct', 'fumbles', 'fumbles_lost', 'first_down_ctchs', 'first_down_ctchpct',
            'season']


df = pd.DataFrame(stats, columns = columns)
print range(2013,2016)
len(stats)


df.head()


import re

# Add a team column using regex and the contents of the full name columns
df['team'] = df['name'].str.extract('([A-Z][A-Z]+)', expand=True)



# pull the phone book style name out of the name column
df['real_name'] = df['name'].str.extract('([A-Z]\w+, \w+)', expand = False)




test = df.proper_name[0]
df = df.drop('proper_name', axis = 1)
df.head()
# dump it up into a csv to try and figure out the name thing tomorrow
df.to_csv('fox_receiving')
