import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep

base_url = 'http://www.pro-football-reference.com/play-index/psl_finder.cgi?request=1&match=single&year_min=1999&year_max=2016&season_start=1&season_end=-1&age_min=0&age_max=99&league_id=NFL&team_id=&is_active=&is_hof=&pos_is_wr=Y&c1stat=height_in&c1comp=gt&c1val=&c2stat=fumbles&c2comp=gt&c2val=&c3stat=rush_yds&c3comp=gt&c3val=&c4stat=pro_bowls&c4comp=gt&c4val=&c5comp=&c5gtlt=lt&c6mult=1.0&c6comp=&order_by=rec&draft=0&draft_year_min=1936&draft_year_max=2016&type=&draft_round_min=0&draft_round_max=99&draft_slot_min=1&draft_slot_max=500&draft_pick_in_round=0&draft_league_id=&draft_team_id=&college_id=all&conference=any&draft_pos_is_qb=Y&draft_pos_is_rb=Y&draft_pos_is_wr=Y&draft_pos_is_te=Y&draft_pos_is_e=Y&draft_pos_is_t=Y&draft_pos_is_g=Y&draft_pos_is_c=Y&draft_pos_is_ol=Y&draft_pos_is_dt=Y&draft_pos_is_de=Y&draft_pos_is_dl=Y&draft_pos_is_ilb=Y&draft_pos_is_olb=Y&draft_pos_is_lb=Y&draft_pos_is_cb=Y&draft_pos_is_s=Y&draft_pos_is_db=Y&draft_pos_is_k=Y&draft_pos_is_p=Y&offset='

r = requests.get(base_url)
soup = BeautifulSoup(r.text, 'html.parser')

headers = []
# this loop finds all of the table headers
table_header = soup.findAll('th')
for i in table_header:
    headers.append(i.renderContents())

# this list provides the column headers for wr stats. Ideally, I could find a more pythonic
# way of pulling out an ordered set of the columns.
wr_cols = headers[7:41]
wr_cols
body = soup.findAll('tbody')
rows = body[0].findAll('tr')
len(rows)
#This pulls down 108 rows, that means that it's also grabbing the column headers# that are peppered throughout
# They have separate classes, so it should be easy to filter them out.

# stat_rows utilizes a list comprehension to make sure that our final list only contains actual players and not the column headers
stat_rows = [x for x in rows if x['class']==['']]

# 'stats' is the list that all of a position's stats from pro-football-reference will be appended to.
stats = []

#strip_stats is a function that can be applied to any list of pfr stat-rows and return lists of players individual stats. Those stats are then appended to the list 'stats'
def strip_stats(rows):
    for x in range(0,len(rows)):
        player_stats = rows[x].findAll('td')
        stats.append([z.renderContents() for z in player_stats])

# This function will pull the relevant records for a positional search, and append the results to a list 'stats'. It relies on the helper
# function 'strip_stats' to create s
def get_wr_stats():
    count = 1
    for x in range(0, 3500, 100):
        url = base_url+str(x)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        body = soup.findAll('tbody')
        rows = body[0].findAll('tr')
        stat_rows = [y for y in rows if y['class']==['']]
        strip_stats(stat_rows)
        print '%d page completed' % count
        count +=1
        sleep(5)
get_wr_stats()

len(stats)
test_df = pd.DataFrame(stats, columns = actual_wr_cols)
actual_wr_cols = ['rk', 'name', 'season', 'age', 'draft_pos', 'team', 'league', 'height', 'weight', 'bmi', 'games', 'games_started',
                    'rush_atts', 'rush_yds', 'rush_y/a', 'rush_tds', 'rush_ypg', 'targets', 'receptions', 'rec_yards',
                    'yards/reception', 'rec_tds', 'rec_ypg', 'ctch_pct', 'y/tgt', 'fumbles', 'fumbles_recovered', 'fum_ret_yds',
                    'fum_tds', 'forced_fumbles', 'years_in_league', 'pro_bowls', 'all_pros', 'av']


test_df.fillna(0.0, inplace=True)




import matplotlib.pyplot as plt
%matplotlib inline
test_df.columns
test_df.head()
test_df['Y/Tgt'].value_counts()
test_df.dtypes

numeric_columns = [ 'rk', 'season', 'age', 'weight', 'bmi', 'games', 'games_started',
                    'rush_atts', 'rush_yds', 'rush_tds', 'targets', 'receptions', 'rec_yards',
                    'rec_tds','fumbles', 'fumbles_recovered', 'fum_ret_yds',
                    'fum_tds', 'forced_fumbles', 'years_in_league', 'pro_bowls',
                    'all_pros', 'av', 'rush_y/a', 'rush_ypg', 'yards/reception', 'rec_ypg', 'y/tgt']

for col in numeric_columns:
    test_df[col] = test_df[col].convert_objects(convert_numeric=True)

test_df.dtypes

test_df.bmi[4]
plt.style.use('ggplot')
plt.scatter(test_df.height, test_df.rec_tds, alpha =0.4)

from sqlalchemy import create_engine
import psycopg2
engine = create_engine('postgresql://codylaminack@localhost:5432/nfl')

test_df.to_sql('wide receivers', engine)
