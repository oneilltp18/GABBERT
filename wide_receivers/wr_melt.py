import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
df = pd.read_csv('final_wr.csv')
df.head()
df.drop(['Unnamed: 0'], axis = 1, inplace = True)

df.reset_index(inplace=True, drop=True)

df.columns


values = ['name','age', 'team', 'weight', 'games', 'targets', 'first_down_ctchs', 'receptions', 'yac', 'team']




# Define a function that splits a pivoted dataframe into its training and target set
cols = ['years_in_league', 'name', 'season', 'team']
df[cols].head(15)

# This will create a dataframe that has all the players who were rookies three seasons ago, and are therefore entering their fourth seasons.
x = df[((df.years_in_league == 0)&(df.season==2013))|((df.years_in_league==1)&(df.season==2014))|((df.years_in_league==2)&(df.season==2015))|((df.years_in_league==3)&(df.season==2016))]


cols = [ 'season', 'age', 'team', 'yac', 'receptions']
df2 = df[(df.years_in_league>=0)&(df.years_in_league<=3)]

df2.shape

df3 = df[(df.rookie_season <2013)& (df.years_in_league<=3)]
df3.head()
pivoted = df3.pivot_table(index=df3.name, columns='years_in_league', values=cols)




pivoted.shape

pivoted.head()
zero_cols = ['season', 'yac']
seasons = [0.0, 1.0, 2.0, 3.0]

for col in zero_cols:
    for i in seasons:
        pivoted[col][i].fillna(0,inplace=True)

pivoted['season'][1.0] = pivoted['season'][0.0]+1

pivoted.head()

df2 = pd.read_csv('catcherr.csv')
df2.receptions.plot(kind='hist')
plt.show()
