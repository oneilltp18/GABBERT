import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep


# define a function to get the soup
def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

# define a function to increment the url to the next page

def next_page(base, player_count):
    url = base+str(player_count)
    return url

# define a function that will return a list of the rows of player stats on a page
def get_rows(soup):
    body = soup.findAll('tbody')
    rows = body[0].findAll('tr')
    stat_rows = [x for x in rows if x['class']==['']]
    return stat_rows

# define a function that will strip the stats out of a row of player html data
def strip_stats(rows):
    for x in range(0,len(rows)):
        player_stats = rows[x].findAll('td')
        stats.append([z.text for z in player_stats])



base = 'http://www.pro-football-reference.com/play-index/psl_finder.cgi?request=1&match=single&year_min=1999&year_max=2016&season_start=1&season_end=-1&age_min=0&age_max=99&league_id=NFL&team_id=&is_active=&is_hof=&pos_is_te=Y&c1stat=height_in&c1comp=gt&c1val=&c2stat=fumbles_rec&c2comp=gt&c2val=&c3stat=seasons&c3comp=gt&c3val=&c4stat=rush_att&c4comp=gt&c4val=&c5comp=&c5gtlt=lt&c6mult=1.0&c6comp=&order_by=targets&draft=0&draft_year_min=1936&draft_year_max=2016&type=&draft_round_min=0&draft_round_max=99&draft_slot_min=1&draft_slot_max=500&draft_pick_in_round=0&draft_league_id=&draft_team_id=&college_id=all&conference=any&draft_pos_is_qb=Y&draft_pos_is_rb=Y&draft_pos_is_wr=Y&draft_pos_is_te=Y&draft_pos_is_e=Y&draft_pos_is_t=Y&draft_pos_is_g=Y&draft_pos_is_c=Y&draft_pos_is_ol=Y&draft_pos_is_dt=Y&draft_pos_is_de=Y&draft_pos_is_dl=Y&draft_pos_is_ilb=Y&draft_pos_is_olb=Y&draft_pos_is_lb=Y&draft_pos_is_cb=Y&draft_pos_is_s=Y&draft_pos_is_db=Y&draft_pos_is_k=Y&offset='

# The master function will need to have a stats and counter that increments by 100
# and prints out how many players it has processed per loop
def get_te_stats(base_url, limit):
    player_count = 0
    while player_count <= limit:
        url = next_page(base, player_count)
        soup = get_soup(url)
        rows = get_rows(soup)
        strip_stats(rows)
        player_count +=100
        print '%d players processed' % player_count
        sleep(5)

# instantiate the list that the player stats will be added to. I've yet to figure
# out how to have this list exist inside the function and be returned by it.
stats = []

# after looking through the results of the search on pro-football-reference, this
# upper limit will capture all of the players in the search results.
get_te_stats(base, 2200)

# running a len on the stats column shows that we got all of the players we wanted
len(stats)
# manually create the column names that we'll need for this dataframe
te_cols = ['rk', 'name', 'year', 'age', 'drafted', 'team', 'league',
            'height', 'weight', 'bmi', 'games', 'starts', 'rush_atts',
            'rush_yds', 'rush_yds_peratt', 'rush_tds', 'rush_ypg',
            'rec_tgts', 'receptions', 'rec_yds', 'yds/rec', 'rec_tds',
            'rec_ypg', 'ctch_pct', 'yds_per_tgt', 'fumbles', 'fumbles_recovered', 'fum_ret_yds',
            'fum_tds', 'forced_fumbles', 'yrs', 'pro_bowl', 'all_pro', 'av']
df = pd.DataFrame(stats, columns = te_cols)


# identify the numeric columns so that they can be converted before adding to sql
numeric_columns = ['rk', 'age', 'weight', 'bmi', 'games', 'starts', 'rush_atts',
'rush_yds', 'rush_yds_peratt', 'rush_tds', 'rush_ypg',
'rec_tgts', 'receptions', 'rec_yds', 'yds/rec', 'rec_tds',
'rec_ypg', 'ctch_pct', 'yds_per_tgt', 'fumbles', 'fumbles_recovered', 'fum_ret_yds',
'fum_tds', 'forced_fumbles', 'yrs', 'pro_bowl', 'all_pro', 'av']

# this loop will force the numeric columns to integers and floats depending on their nature
for col in numeric_columns:
    df[col] = df[col].convert_objects(convert_numeric=True)

df.dtypes

# Put the database we've created into sql
from sqlalchemy import create_engine
engine = create_engine('postgresql://codylaminack@localhost:5432/nfl')

df.to_sql('tight_ends', engine)
