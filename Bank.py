#load required libraries
import pandas as pd
import numpy as np
import seaborn as sns
import sklearn 
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots

#load the data
df_main= pd.read_csv("C:/Users/bhavy/Downloads/main_data.csv")
df_old= pd.read_csv("C:/Users/bhavy/Downloads/prior_campaigns.csv")
df_main.head()
df_old.head()
df= df_main.merge(df_old, on="cust_id", how= "inner")
df.head()

#first glance of data
df.info()
df.describe()
df.isnull().sum(axis = 0)
for col in df.select_dtypes(include= 'object').columns:
    print(col)
    print(df[col].unique())

#clean the data
#impute missing values
#missing values - previous, pdays, poutcome
df['poutcome'].fillna('unknown', inplace= True)
df['pdays'].fillna(int(50), inplace= True)
df['previous'].fillna(int(0), inplace= True)
df.describe()
df.head()
#check for duplicates
df_dup = df[df.duplicated(keep="last")]
df_dup

#exploratory data analysis and visualizations
#histogram of all numeric variables
df.hist(bins=50, figsize=(20,15))
#pairplot to see how numerical variables vary 
sns.pairplot(df)
#compare how many customers subscribed (subscribed=yes)
sns.countplot(x='subscribed', data=df)
#count the percentage of subscribers
df['subscribed'].value_counts(normalize=True)
#univariate analysis
#boxplot for age
sns.boxplot(data=df, x="subscribed", y="age")
#subscribed vs contacted
lst = [df]
for column in lst:
    column.loc[column["age"] < 30,  'age_group'] = 20
    column.loc[(column["age"] >= 30) & (column["age"] <= 39), 'age_group'] = 30
    column.loc[(column["age"] >= 40) & (column["age"] <= 49), 'age_group'] = 40
    column.loc[(column["age"] >= 50) & (column["age"] <= 59), 'age_group'] = 50
    column.loc[column["age"] >= 60, 'age_group'] = 60
count_age_response_pct = pd.crosstab(df['subscribed'],df['age_group']).apply(lambda x: x/x.sum() * 100)
count_age_response_pct = count_age_response_pct.transpose() 
age1 = pd.DataFrame(df['age_group'].value_counts())
age1['% Contacted'] = age1['age_group']*100/age1['age_group'].sum()
age1['% Subscription'] = count_age_response_pct['yes']
age1.drop('age_group',axis = 1,inplace = True)
age1['age'] = [30,40,50,20,60]
age1 = age1.sort_values('age',ascending = True)
plot_age1 = age1[['% Subscription','% Contacted']].plot(kind = 'bar',
                                              figsize=(8,6), color = ('green','red'))
plt.xlabel('Age Group')
plt.ylabel('Subscription Rate')
plt.xticks(np.arange(5), ('<30', '30-39', '40-49', '50-59', '60+'),rotation = 'horizontal')
plt.title('Subscription vs. Contact Rate by Age')
plt.show()
#boxplot for duration
sns.boxplot(data=df, x="subscribed", y="duration")
#boxplot for campaign
sns.boxplot(data=df, x="subscribed", y="campaign")
#boxplot for previous
sns.boxplot(data=df, x="subscribed", y="previous")
sns.countplot(x='previous', data=df, hue= "subscribed")
#emp.var.rate
sns.boxplot(data=df, x="subscribed", y="emp.var.rate")
#cons.price.idx
sns.boxplot(data=df, x="subscribed", y="cons.price.idx")
#cons.conf.idx
sns.boxplot(data=df, x="subscribed", y="cons.conf.idx")
#euribor3m
sns.boxplot(data=df, x="subscribed", y="euribor3m")
#nr.employed
sns.boxplot(data=df, x="subscribed", y="nr.employed")
#job categories and their count
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='job', data=df)
#job categories and count coloured by subscribed(yes or no)
sns.countplot(x='job', data=df, hue= "subscribed")
#repeat for all categorical variables
#marital
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='marital', data=df)
sns.countplot(x='marital', data=df, hue= "subscribed")
#education
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='education', data=df)
sns.countplot(x='education', data=df, hue= "subscribed")
#default
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='default', data=df)
sns.countplot(x='default', data=df, hue= "subscribed")
#housing
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='housing', data=df)
sns.countplot(x='housing', data=df, hue= "subscribed")
#loan
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='loan', data=df)
sns.countplot(x='loan', data=df, hue= "subscribed")
#contact
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='contact', data=df)
sns.countplot(x='contact', data=df, hue= "subscribed")
#month
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='month', data=df)
sns.countplot(x='month', data=df, hue= "subscribed")
#day_of_week
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='day_of_week', data=df)
sns.countplot(x='day_of_week', data=df, hue= "subscribed")
#poutcome
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x='poutcome', data=df)
sns.countplot(x='poutcome', data=df, hue= "subscribed")
#correlation matrix 
corr = df.corr()
f, ax = plt.subplots(figsize=(15,15))
cmap = sns.diverging_palette(220, 10, as_cmap=True)
_ = sns.heatmap(corr, cmap="YlGn", square=True, ax=ax, annot=True, linewidth=0.1)
plt.title("Correlation of Features", y=1.05, size=15)

#convert all categorical variables to binary
#one hot encoding
df = pd.get_dummies(df)
df.head()
#oversampling
count_class_0, count_class_1 = df.subscribed_yes.value_counts()
df_class_0 = df[df['subscribed_yes'] == 0]
df_class_1 = df[df['subscribed_yes'] == 1]
df_class_1_over = df_class_1.sample(count_class_0, replace=True)
df= pd.concat([df_class_0, df_class_1_over], axis=0)
print('Random over-sampling:')
print(df.subscribed_yes.value_counts())
df.subscribed_yes.value_counts().plot(kind='bar', title='Count (target)');

#splitting into train and test
# Labels are the values we want to predict
y = np.array(df['subscribed_yes'])
# Remove the labels from the features
# axis 1 refers to the columns
features= df.drop('subscribed_yes', axis = 1)
features= features.drop('subscribed_no', axis = 1)
features= features.drop('duration', axis = 1)
features= features.drop('cust_id', axis = 1)
# Saving feature names for later use
feature_list = list(features.columns)
# Convert to numpy array
features = np.array(features)
from sklearn.model_selection import train_test_split
train_features,test_features, train_y, test_y= train_test_split(features, y, test_size=0.2, random_state=42)
#check the length of each
print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_y.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_y.shape)
print(test_y)
#check if oversampling was done correctly
unique, counts = np.unique(train_y, return_counts=True)
dict(zip(unique, counts))
unique, counts = np.unique(test_y, return_counts=True)
dict(zip(unique, counts))

#random forest
from sklearn.ensemble import RandomForestRegressor
# Initiate model 
rf = RandomForestRegressor(n_estimators= 1000, random_state=42)
# Train the model on training data
rf.fit(train_features, train_y);
#predict on test data
predictions = rf.predict(test_features)
#make predictions categorical
ls = []
for i in predictions:
    if i<0.5:
        ls.append(0)
    else:
        ls.append(1)
#measure accuracy
from sklearn import metrics
errors = abs(ls - np.array(test_y,float))
# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors *test_y)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:',round(metrics.accuracy_score(test_y, ls), 2), )
#Count predicted number of subscribers
(unique, counts) = np.unique(ls, return_counts=True)
frequencies = np.asarray((unique, counts)).T
print(frequencies)
#confusion matrix
from sklearn import metrics
print(metrics.confusion_matrix(test_y, ls))
#interpreting model results
#visualize a single decision tree
from sklearn.tree import export_graphviz
import pydot
# Pull out one tree from the forest
tree = rf.estimators_[5]
# Export the image to a dot file
export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)
# Use dot file to create a graph
(graph, ) = pydot.graph_from_dot_file('tree.dot')
# Write graph to a png file
graph.write_png('tree.png');
print('The depth of this tree is:', tree.tree_.max_depth)
# Limit depth of tree to 2 levels
rf_small = RandomForestRegressor(n_estimators=10, max_depth = 3, random_state=42)
rf_small.fit(train_features, train_y)
# Extract the small tree
tree_small = rf_small.estimators_[5]
# Save the tree as a png image
export_graphviz(tree_small, out_file = 'small_tree.dot', feature_names = feature_list, rounded = True, precision = 1)
(graph, ) = pydot.graph_from_dot_file('small_tree.dot')
graph.write_png('small_tree.png');
# Get numerical feature importances
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];
# list of x locations for plotting
x_values = list(range(len(importances)))
# Make a bar chart
plt.bar(x_values, importances, orientation = 'vertical')
# Tick labels for x axis
plt.xticks(x_values, feature_list, rotation='vertical')
# Axis labels and title
plt.ylabel('Importance'); plt.xlabel('Variable'); plt.title('Variable Importances');

#xgboost
import xgboost as xgb
#train the model
xg_reg = xgb.XGBRegressor(objective = 'binary:logitraw' ,colsample_bytree = 0.3, learning_rate = 0.001,
                max_depth = 10, alpha = 10, n_estimators = 100)
xg_reg.fit(train_features,train_y)
#predict
preds = xg_reg.predict(test_features)
#make predictions categorical
lsxg = []
for i in preds:
    if i<0.5:
        lsxg.append(0)
    else:
        lsxg.append(1)
#accuracy
errors = abs(lsxg - np.array(test_y,float))
# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors *test_y)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:',round(metrics.accuracy_score(test_y, lsxg), 2), )
#count predictions
(unique, counts) = np.unique(lsxg, return_counts=True)
frequencies = np.asarray((unique, counts)).T
print(frequencies)
#confusion matrix
from sklearn import metrics
print(metrics.confusion_matrix(test_y, lsxg))

#logistic regression
#scale data
from sklearn.preprocessing import StandardScaler
#Bring the data on same scale
scaleobj = StandardScaler()
Scaled_Data = scaleobj.fit_transform(df)
#Transform it back to dataframe
Scaled_Data = pd.DataFrame(Scaled_Data, index = df.index, columns = df.columns)
Scaled_Data.head()
# Labels are the values we want to predict
scaled_y = np.array(Scaled_Data['subscribed_yes'])
# Remove the labels from the features
# axis 1 refers to the columns
scaled_features= Scaled_Data.drop('subscribed_yes', axis = 1)
scaled_features= scaled_features.drop('subscribed_no', axis = 1)
scaled_features= scaled_features.drop('duration', axis = 1)
scaled_features= scaled_features.drop('cust_id', axis = 1)
# Saving feature names for later use
scaled_feature_list = list(scaled_features.columns)
# Convert to numpy array
scaled_features = np.array(scaled_features)
#split into train and test
from sklearn.model_selection import train_test_split
train_scaled_features,test_scaled_features, train_scaled_y, test_scaled_y= train_test_split(scaled_features, scaled_y, test_size=0.2, random_state=42)
print('Training Features Shape:', train_scaled_features.shape)
print('Training Labels Shape:', train_scaled_y.shape)
print('Testing Features Shape:', test_scaled_features.shape)
print('Testing Labels Shape:', test_scaled_y.shape)
#train model
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(train_scaled_features, train_y)
#predict
y_pred = logreg.predict(test_scaled_features)
#accuracy
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(test_scaled_features, test_y)))
#frequencies of outcomes
(unique, counts) = np.unique(y_pred, return_counts=True)
frequencies = np.asarray((unique, counts)).T
print(frequencies)
#confusion matrix
from sklearn import metrics
print(metrics.confusion_matrix(test_y, y_pred))
#report
from sklearn.metrics import classification_report
print(classification_report(test_y, y_pred))
