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



from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import BaggingRegressor, RandomForestClassifier
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
mapped_pivot = pd.read_csv('pivot_catcherr.csv')

mapped_pivot.compilation_3 = mapped_pivot.compilation_3.apply(lambda x: 1 if x >= 50 else 0)

mapped_pivot.head()

X3 = mapped_pivot[['compilation_0', 'compilation_1', 'compilation_2']]
y3 = mapped_pivot.compilation_3

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
X_train, X_test, y_train, y_test = train_test_split(X3, y3, test_size=0.2)
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
log_reg.score(X_test, y_test)

knn = KNeighborsClassifier(n_neighbors=12)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

bins = [-1, 17, 70, 200]
labels = ['below average', 'quality starter', 'all_pro']
len(labels)

categories = pd.cut(mapped_pivot['compilation_3'], bins, labels=labels)
categories.value_counts()

mapped_pivot['categories'] =  pd.cut(mapped_pivot['compilation_3'], bins, labels=labels)
mapped_pivot.head()
X3 = mapped_pivot.drop(['categories', 'name', 'compilation_3'], axis=1)
y3 = mapped_pivot.categories
kbest = SelectKBest(k=50)
kbest.fit(scale(X3),mapped_pivot['compilation_3'])
# Show the feature importance for Kbest of 30
kbest_importance = pd.DataFrame(zip(X3.columns, kbest.get_support()), columns = ['feature', 'important?'])

kbest_features = kbest_importance[kbest_importance['important?'] == True].feature

X_train, X_test, y_train, y_test = train_test_split(X3[kbest_features], y3, test_size=0.4)
dtc = DecisionTreeClassifier(max_depth=20)
dtc.fit(X_train, y_train)
dtc.score(X_test, y_test)
from sklearn.metrics import classification_report
print classification_report(y_test, dtc.predict(X_test))



# Using PCA to predict compilation_3
pca_df = pd.read_csv('pca_catcherr.csv')
mapped_pivot.tail(10)
pca_df = pca_df.join(mapped_pivot[['compilation_3', 'categories']])

pca_df.head()

X4 = pca_df.drop(['compilation_3', 'categories', 'name'], axis=1)
y4 = pca_df.categories
X_train, X_test, y_train, y_test = train_test_split(X4, y4, test_size=0.2)

rfc = RandomForestClassifier(max_depth=25)
rfc.fit(X_train, y_train)
rfc.score(X_test, y_test)
print classification_report(y_test, rfc.predict(X_test))
rfc.predict_proba(X_test)
