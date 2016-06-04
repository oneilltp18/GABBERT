import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep


# define a function to get the soup of a page of stats
def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
# Returns the header columns
def get_headers(soup):
    table = soup.find('table', {'class':'sortable'})
    headers = (table.find('thead'))
    header_cols = headers.findAll('td')
    headers = [x.text for x in header_cols]
    return headers
# Returns the stats from the body of the soup
def get_stats(soup):
    table = soup.find('table', {'class':'sortable'})
    body = table.find('tbody')
    rows = body.findAll('tr', {'class':'tablefont'})
    stats = []
    for row in rows:
        row_stats = row.findAll('div')
        stats.append([x.text for x in row_stats])
    return stats
#combines the previous functions and returns their results to a dataframe
def combine_stats(url):
    soup = get_soup(url)
    header_cols = get_headers(soup)
    stats = get_stats(soup)
    df = pd.DataFrame(stats, columns = header_cols)
    return df

full_url = 'http://nflcombineresults.com/nflcombinedata_expanded.php?year=all&pos=&college='

df = combine_stats(full_url)
# Behind the scenes here, I updated the csv to modify the column headers
# The fact that there were some
final_df = pd.read_csv('combine_stats')

# At this point, we can send the full datafram to our sql database

from sqlalchemy import create_engine
engine = create_engine('postgresql://codylaminack@localhost:5432/nfl')
final_df.to_sql('combine_stats', engine)
