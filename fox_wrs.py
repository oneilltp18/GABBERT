import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep


base_url = 'http://www.foxsports.com/nfl/stats?season=1999&week=100&category=RECEIVING&opp=0&sort=2&qualified=1&sortOrder=0&page='
# define a function to get the soup

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def next_page(url, count):
    url = base_url+str(count)
    return url


# define a function that pulls all of the individual player rows from a page
def get_rows(soup):
    table = soup.find('section', {'class':'wisbb_body'})
    body = table.find('tbody')
    rows = body.findAll('tr', {'class':''})
    return rows

def strip_stats(rows, i):
    for x in range(0,len(rows)):
        player_stats = rows[x].findAll('td')
        player = [z.text for z in player_stats]
        player.append(i)
        stats.append(player)

# Define a funciton that will return the number of pages in the search.
def last_page(soup):
    pages = soup.find('div', {'class':'wisbb_paginator'})
    page_links = pages.findAll('a')
    final_page = page_links[-2].text.strip()
    return int(final_page)

# for the compiler function, it'll need something increment the counter

def rec_stats(base_url, i):
    count = 1
    upper_limit = last_page(get_soup(base_url+str(count)))
    while count <= upper_limit:
        url = next_page(base_url, count)
        soup = get_soup(url)
        rows = get_rows(soup)
        strip_stats(rows, i)
        print '%d Players processed' % len(stats)
        count+=1
        sleep(5)

stats = []
rec_stats(base_url)
stats
# The sixteen_years function will allow us to pull multiple years within the same function,
# and it will also append a value to the end of each stat row that contains the season year
def sixteen_years(range):
    for i in range:
        year_url = 'http://www.foxsports.com/nfl/stats?season='+str(i)+'&week=100&category=RECEIVING&opp=0&sort=2&qualified=1&sortOrder=0&page='
        rec_stats(year_url, i)
sixteen_years(range(1999,2000))
df = pd.DataFrame(stats)
df.tail()
len(stats)

stats2 = rec_stats(base_url)


# This function adds the season year onto the end of each player's stat list
def add_season(stat_list, year):
    for i in stat_list:
        i.append(year)

# This pulls the stats down just fine, but it doesn't have the season in the stats.
# I suppose we coudl add somethin in at the first position that was the season
# since we don't carea bout the player rank.
