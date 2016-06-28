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


cols_to_keep = []
for col in df2.columns:
    if df2[col].isnull().sum() == 0:
        cols_to_keep.append(col)

cols_to_keep.remove('years_in_league')
cols_to_keep.remove('team_pass_yds')
cols_to_keep.remove('team_pass_tds')
cols_to_keep.remove('team_pass_attempts')
cols_to_keep.remove('team_completions')
cols_to_keep.remove('total_points')
cols_to_keep.append('compilation')

pivoted = df2.pivot_table(index=df2.name, columns='years_in_league', values=cols_to_keep)
print pivoted.shape

zero_cols = ['games', 'rush_atts', 'rush_yds', 'rush_y/a', 'rush_tds', 'rush_ypg',
             'targets', 'receptions', 'rec_yards', 'yards/reception', 'rec_tds',
             'rec_ypg', 'ctch_pct', 'y/tgt', 'fumbles', 'fumbles_recovered', 'fum_ret_yds',
             'fum_tds', 'forced_fumbles', 'pro_bowls', 'all_pros', '100yd_gms',
             'first_down_ctchs', 'first_down_ctchpct', 'long_ctch', 'drops', 'EYds',
             'DVOA', 'DYAR', '40 Yard', 'start_ratio', 'dpis_drawn', 'dpi_yards',
             'pct_team_tgts', 'pct_team_receptions', 'pct_of_team_passyards',
             'pct_team_touchdowns', 'dropK', 'yacK', 'td_points', 'compilation']

add_cols = ['season', 'age']

backfill_cols = ['weight', 'bmi', 'rookie_age',
                 'rookie_season', 'height_inches']

team_cols = ['team_pass_tds', 'team_pass_yds', 'team_pass_attempts', 'team_completions',
             'total_points']

years = [0.0, 1.0, 2.0, 3.0]
back_years = [1.0, 2.0, 3.0]

for col in zero_cols:
    for i in years:
        pivoted[col][i].fillna(0, inplace = True)

for col in backfill_cols:
    for i in back_years:
        pivoted[col][i] = pivoted[col][0.0]


pivoted = pivoted[pivoted.season[0.0].isnull() == False]

mi = pivoted.columns
new_cols = pd.Index([x[0]+'_'+str(x[1]) for x in mi.tolist()])
pivoted.columns = new_cols

pivoted.rename(columns = lambda x: x.replace('.0', ''), inplace = True)

pivoted['season_1'] = pivoted['season_0']+1
pivoted['season_2'] = pivoted['season_0']+2
pivoted['season_3'] = pivoted['season_0']+3

for col in pivoted.columns:
    if col == 'compilation_3':
        pass
    elif str(col)[-2:] =='_3':
        pivoted.drop(col, axis=1, inplace=True)
pivoted['age_1'] = pivoted['age_0']+1
pivoted['age_2'] = pivoted['age_0']+2

from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import scale
X = pivoted.drop(['compilation_3', 'compilation_0', 'compilation_1', 'compilation_2'], axis = 1)
y = pivoted['compilation_3']

kbest = SelectKBest(k=100)
kbest.fit(scale(X),y)
# Show the feature importance for Kbest of 30
kbest_importance = pd.DataFrame(zip(X.columns, kbest.get_support()), columns = ['feature', 'important?'])

kbest_features = kbest_importance[kbest_importance['important?'] == True].feature
#Here's our dataframe
X_model = X[kbest_features]
net = ElasticNet(alpha=1.5)
lasso = Lasso(alpha=5)
ridge = Ridge(alpha=3)
lr = LinearRegression()
dtr = DecisionTreeRegressor(max_depth=17)
bagger = BaggingRegressor(net, verbose = 1)

X_train, X_test, y_train, y_test = train_test_split(X_model, y)

dtr.fit(X_train,y_train)
dtr.score(X_test, y_test)
pred = dtr.predict(X_test)
plt.scatter(y_test, (pred*0.8)-y_test)

net.fit(X_train, y_train)
net.score(X_test, y_test)
preds = net.predict(X_test)
plt.scatter(y_test, (preds) - y_test, alpha = 0.7)

scores = cross_val_score(net, scale(X_model), y, cv=12)
scores.mean()

X2 = pivoted[['compilation_0', 'compilation_1', 'compilation_2']]
y2 = pivoted.compilation_3

X_train, X_test, y_train, y_test = train_test_split(X2, y2, test_size=0.2)

lr.fit(X_train, y_train)
lr.score(X_test, y_test)
pivoted.head()
mapped_pivot = pd.DataFrame(pivoted)

mapped_pivot.compilation_3 = mapped_pivot.compilation_3.apply(lambda x: 1 if x >= 20 else 0)

mapped_pivot.head()

X3 = mapped_pivot[['compilation_0', 'compilation_1', 'compilation_2']]
y3 = mapped_pivot.compilation_3

from sklearn.linear_model import LogisticRegression
X_train, X_test, y_train, y_test = train_test_split(X3, y3, test_size=0.2)
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
log_reg.score(X_test, y_test)
