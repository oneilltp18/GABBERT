import pandas as pd

df = pd.read_csv('team_data_df')

from sqlalchemy import create_engine
engine = create_engine('postgresql://codylaminack@localhost:5432/nfl')

df.to_sql('team_data', engine)
