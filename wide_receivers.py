import requests
from bs4 import BeautifulSoup
import time

url = 'http://www.pro-football-reference.com/play-index/psl_finder.cgi?request=1&match=single&year_min=1999&year_max=2016&season_start=1&season_end=-1&age_min=0&age_max=99&league_id=NFL&team_id=&is_active=&is_hof=&pos_is_wr=Y&c1stat=height_in&c1comp=gt&c1val=&c2stat=fumbles&c2comp=gt&c2val=&c3stat=rush_yds&c3comp=gt&c3val=&c4stat=pro_bowls&c4comp=gt&c4val=&c5comp=&c5gtlt=lt&c6mult=1.0&c6comp=&order_by=rec&draft=0&draft_year_min=1936&draft_year_max=2016&type=&draft_round_min=0&draft_round_max=99&draft_slot_min=1&draft_slot_max=500&draft_pick_in_round=0&draft_league_id=&draft_team_id=&college_id=all&conference=any&draft_pos_is_qb=Y&draft_pos_is_rb=Y&draft_pos_is_wr=Y&draft_pos_is_te=Y&draft_pos_is_e=Y&draft_pos_is_t=Y&draft_pos_is_g=Y&draft_pos_is_c=Y&draft_pos_is_ol=Y&draft_pos_is_dt=Y&draft_pos_is_de=Y&draft_pos_is_dl=Y&draft_pos_is_ilb=Y&draft_pos_is_olb=Y&draft_pos_is_lb=Y&draft_pos_is_cb=Y&draft_pos_is_s=Y&draft_pos_is_db=Y&draft_pos_is_k=Y&draft_pos_is_p=Y&offset=0'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

print soup.prettify()
