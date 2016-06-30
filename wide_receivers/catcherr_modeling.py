import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import BaggingRegressor, RandomForestClassifier, VotingClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
%matplotlib inline

pca_df = pd.read_csv('pca_catcherr.csv')
df = pd.read_csv('pivot_catcherr.csv')


# Create an average starts column
df['avg_starts'] = (df.start_ratio_0 + df.start_ratio_1 + df.start_ratio_2) / 3

#Create a column that adds up a player's dpi yards and penaltys drawn
df['dpis'] = df.dpis_drawn_0 + df.dpis_drawn_1 + df.dpis_drawn_2
df['dpi_yards'] = df.dpi_yards_0 + df.dpi_yards_1 + df.dpi_yards_2

features = ['age_2', 'weight_2', 'bmi_2', 'rush_atts_0', 'rush_atts_1',
            'rush_atts_2', 'rush_y/a_0', 'rush_y/a_1', 'rush_y/a_2', 'rush_tds_0',
            'rush_tds_1', 'rush_tds_2', 'receptions_0', 'receptions_1', 'receptions_2',
            'rec_yards_0', 'rec_yards_1','rec_yards_2', 'rec_tds_0', 'rec_tds_1',
            'rec_tds_2', 'ctch_pct_0', 'ctch_pct_1', 'ctch_pct_2', 'fumbles_0',
            'fumbles_1', 'fumbles_2', 'first_down_ctchpct_0', 'first_down_ctchpct_1',
            'first_down_ctchpct_2', 'long_ctch_0', 'long_ctch_1', 'long_ctch_2',
            'drops_0', 'drops_1', 'drops_2', 'EYds_0', 'EYds_1', 'EYds_2', 'DVOA_0',
            'DVOA_1', 'DVOA_2', 'height_inches_2', 'avg_starts', 'dpis', 'dpi_yards',
             'pct_team_tgts_0', 'pct_team_tgts_1',
            'pct_team_tgts_2', 'compilation_1', 'compilation_2', 'yacK_1', 'yacK_2']

features_no_year_1 = ['age_2', 'weight_2', 'bmi_2',
             'rush_y/a_1', 'rush_y/a_2',
             'receptions_1', 'receptions_2',
            'rec_yards_1','rec_yards_2', 'rec_tds_1',
            'rec_tds_2', 'ctch_pct_1', 'ctch_pct_2',
             'first_down_ctchpct_1',
            'first_down_ctchpct_2',  'long_ctch_1', 'long_ctch_2',
             'drops_1', 'drops_2',  'EYds_1', 'EYds_2',
            'DVOA_1', 'DVOA_2', 'height_inches_2', 'avg_starts', 'dpis', 'dpi_yards',
             'pct_team_tgts_1',
            'pct_team_tgts_2', 'compilation_0', 'compilation_1', 'compilation_2', 'yacK_2']
len(features)

# Create categories for player season_3 ratings

bins = [-1, 10, 30, 65, 200]
labels = ['below average', 'league_average', 'quality starter', 'all_pro']
df['categories'] =  pd.cut(df['compilation_3'], bins, labels=labels)

df[df.compilation_3 >0].compilation_3.mean()

X = scale(df[features_no_year_1])
y = df.categories

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
cat_weights = {'below average':0.9, 'league_average':3, 'quality starter':2.5, 'all_pro':4}



svc = SVC(C = 0.95, class_weight=cat_weights, probability = True, kernel='rbf')
svc.fit(X_train, y_train)
svc.score(X_test, y_test)
preds = svc.predict(X_test)
print classification_report(y_test, preds)




# A Random Forest, and seemingly most tree-based models are not well suited to this type of problem. logistic regression seems
# to be performing better.
cat_weights = {'below average':0.9, 'league_average':3, 'quality starter':2.5, 'all_pro':4.5}
lr = LogisticRegression(C=2, solver = 'lbfgs', multi_class = 'multinomial', penalty='l2', class_weight = cat_weights, random_state=11)
lr.fit(X_train, y_train)
lr.score(X_test, y_test)
preds = lr.predict(X_test)
print classification_report(y_test, preds)

ab = AdaBoostClassifier(base_estimator = lr, n_estimators = 15, random_state=11)
ab.fit(X_train, y_train)
ab.score(X_test, y_test)
preds = ab.predict(X_test)
print classification_report(y_test, preds)
labels = svc.predict(X)

df['predicts'] = labels
df[((df.predicts == 'quality starter')|(df.predicts == 'all_pro'))]
df[(df.compilation_2 <=30) & (df.predicts == 'quality starter')]
# Voting Classifier won't work for this data. The category weights can't be used.



knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)
preds = knn.predict(X_test)
print classification_report(y_test, preds)
lables = knn.predict(X)
