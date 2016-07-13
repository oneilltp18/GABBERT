## Summary of Resuts

Our data collection efforts allowed us to train a model with over 800 wide receiver seasons from the past 17 years. Our model is based on traditional statistics as well as unique features created to provide more insight into player performance.

### Data Wrangling and Feature Engineering

Some amount of clearning was required to get our data to a state where it could be modeled. Much of this clearning occurred in SQL. Team name acronyms are not standard across the various sites we mined our data from. The same is true, oddly enough, for player names. Once the SQL transformations were complete, the five different tables were joined together, and pulled down as a CSV for more cleaning and feature engineering in Python. The majority of this additional cleaning involved imputing features that had a significant number of missing values (primarily advanced statistics). 

In order to more accurately predict future performance, we created several new features in our data. Some of these were very simple (things like the percentage of games a player appeared in that he started, and the percentage of his team's offense he represents), but others involved slightly more advanced machine learning techniques. In order to maximize the amount of career data we were able to train our model on while maintaining a lower-dimensional feature space, we performed principal component on a player's stats from their first and second years. We were able to reduce around 50 features to a much more manageable 15 while still capturing virtually all of the variance in that data. 

Once these features were created, we selected the most important ones to our target variable. After experimenting with several methods, we decided finally to use a Select K-Best features and begin modelling. 

### Model Creation

Given the extreme variance in player performance from year to year, a regression-based model wouldn't have been as useful as a classfication problem. We therefore binned players into four categories based on their CATCHERR score. These bins were as follows: below average, league average, quality starter, and all-pro. Initially we modeled on just two categories, above and below average. That model was highly accurate (96% accuracy), but we felt that the amount of insight it provided was minimal. Breaking players into four bins allows for more distinction between high-performing players while still reliably separating out players unworthy of extensions/resigning. 

Multiple classification models were tested and tuned. Each performed at different levels for different player groups. For exmaple, a Linear-Kernel SVC was able to accurately pick out all-pro players at a relatively high rate, but performed poorly with league average and quality starters. Alternatively, K-Neighbors Classifiers picked out quality starters reliablly but failed to predict some othe categories as well. After tuning these models by testing custom category weights and different parameters, we realized that there would be no one model reliably performing at a higher level than the others. As a result, we decided to use a Voting Classifier in the hopes that it would more accurately classify more players. Multiple voting weights were tested until our optimal model was found. 

This model had an overall precision score of 0.85, and a recall score of 0.83, giving us an F1 score of 0.84. 

### Predicting 2016 

The highest-performing model was used to predict fourth-year performance for players who will be entering their fourth year in 2016. In addition to showing the category our model predicts a player will perform at, we also felt it was useful to include probabilities of a player performing at any of the four levels we had outlined. 

Below is an image of our results. These players are sorted by their likelihood of performing at an all-pro level. 

![2016 Projections](https://raw.githubusercontent.com/cl65610/GABBERT/master/visualization/top_15_rooks.png "2016 WR Projections")

Deandre Hopkins is the most likely receiver to perform at an all-pro level, and this makes sense given his performance to this point in his career. The model is a little bullish on some wide receivers that analysts and pundits are a little more lukewarm on. Perhaps our model is correct, and Chris Hogan is due for a breakout. It's also possible that for some reason, he future performance sits right on the boundary between being a quality starter and an all-pro. Only time will tell. 

* The code associated with our modeling and predictions can be found [here](https://github.com/oneilltp18/GABBERT/blob/master/wide_receivers/csv_update_model_build.ipynb).

### Room for Improvement

Undobtedly, this model could be imporved on with a larger sample size and more robust features. We will continually update our model as new information becomes available with the goal of more accurately predicting future classes of of wide receivers.
