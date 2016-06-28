import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
%matplotlib inline

df = pd.read_csv('catcherr.csv')

df.columns
df.drop('Unnamed: 0', axis=1, inplace=True)

df[df.name=='Darren Sproles']
df.ix[3248].years_in_league = 2
# Reset Jordan Reed's years in league
df.years_in_league[3248] = 2
# Reset Jarvis Landry
df.years_in_league[1757] = 1
# Reset John Brown
df.years_in_league[1594] = 1

df[(df.years_in_league == 0)&(df.season !=1999)].sort('compilation', ascending=False)

plt.style.use('ggplot')
rookie_graph = df[(df.season !=1999)& (df.years_in_league == 0)].plot(kind='scatter', x = 'receptions', y = 'compilation', figsize=(20,18))
for i, player in enumerate(df[(df.season !=1999)& (df.years_in_league == 0)&(df.receptions >=50)].name):
    rookie_graph.annotate(player, (df[(df.season !=1999)& (df.years_in_league == 0)&(df.receptions >=50)].iloc[i].receptions, df[(df.season != 1999)& (df.years_in_league == 0)&(df.receptions>=50)].iloc[i].compilation), fontsize=12)
plt.savefig('all_time_rookies.png')

graph = df[(df.season == 2015)&(df.targets >=60)].plot(kind='scatter', x='receptions', y= 'compilation', figsize=(25,23))
for i, player in enumerate(df[(df.season == 2015)&(df.targets >=65)].name):
    graph.annotate(player, (df[(df.season == 2015)&(df.targets >=65)].iloc[i].receptions, df[(df.season == 2015)&(df.targets >=65)].iloc[i].compilation), fontsize=15)
plt.title('Receptions Vs. CATCHERR')
plt.xlabel('Number of Receptions')
plt.ylabel('CATCHERR Score')
plt.savefig('top_2015.png')
plt.show()


df.columns
df2 = df[(df.rookie_season <2013)& (df.years_in_league<=3)]
cols_df = df2.drop('name', axis = 1)
cols_df = df2.drop('years_in_league', axis = 1)

piv_df = df2.pivot_table(index=df2.name, columns='years_in_league', values=cols_df.columns)
piv_df.head()

mi = piv_df.columns
new_cols = pd.Index([x[0]+'_'+str(x[1]) for x in mi.tolist()])
piv_df.columns = new_cols

piv_df.head()
