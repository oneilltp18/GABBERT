import pandas as pd

df = pd.read_csv('cleaned_wrs.csv')

df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis = 1, inplace = True)

df.reset_index(inplace=True, drop=True)

df.columns


values = ['name','age', 'team', 'weight', 'games', 'targets', 'first_down_ctchs', 'receptions', 'yac']

df2 = pd.pivot_table(df[df.season>=2014], values=values, index='name', columns = 'season')
df2.head(50)

data = df[df.season == 2015]

### Trying to see how well you could impute YAC and other fox_receiving stats

data[data.yac <= 5][values]

test = data[data.yac == 0]
test.shape

train = data[data.yac != 0]

train.columns
features = ['targets', 'receptions', 'rec_yards', 'rec_tds', 'rec_ypg', 'pct_of_team_passyards', 'dpi_yards', 'height_inches']


# Define a function that splits a pivoted dataframe into its training and target set
cols = ['years_in_league', 'name', 'season', 'team']
df[cols].head(15)

# This will create a dataframe that has all the players who were rookies three seasons ago, and are therefore entering their fourth seasons.
x = df[((df.years_in_league == 0)&(df.season==2013))|((df.years_in_league==1)&(df.season==2014))|((df.years_in_league==2)&(df.season==2015))|((df.years_in_league==3)&(df.season==2016))]
x.head(25)

x[x.name == 'DeAndre Hopkins']
