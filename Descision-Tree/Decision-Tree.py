# -*- coding: utf-8 -*-
"""Decision-Tree.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b3v01Ge81YQqqxCPXJmo_4PwRSvU0Lrd
"""

# Import and mount to access drive
from google.colab import drive
drive.mount('/gdrive')

# Import required modules
import pandas as pd
import numpy as np

import warnings

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

#ignore warnings
warnings.filterwarnings('ignore')

# Creating a dataframe
data_set = pd.read_csv("/gdrive/MyDrive/titanic.csv")

# Data before pre-processing
data_set

# Info about data_set
data_set.info()

# Description about data_set
data_set.describe(include = 'all')

"""
-> We see that the count for the columns **'Age'**, **'Cabin'** and **'Embarked'** are less than actual which means we have some ***missing data*** in them

-> **Lets now start pre-processing the data**"""

# Amount of missing data
print("Percentage of missing values:")
print(((data_set.isna().sum())/data_set.shape[0])*100)

"""-> We can't ignore the 20% missing data of Age

-> Let's fill the missing values of age with the mean **but** categorised under which ***Pclass*** (passenger - class) they opted for as they are located at different locations in the Titanic and their **sex** as it matters in their biology
"""

# Lets groupby by sex and pclass only on age column
# Aggregated by their mean
# Finally rounding the age as float value is not that usefull
round(data_set.groupby(['Sex', 'Pclass'])['Age'].agg('mean'), 0)

# As Age can't be negative lets
# replace NaN with -1 for easy access
data_set["Age"].fillna(-1, inplace = True)

# Iterating over rows of age to handle missing data
for data_index in range(data_set.shape[0]):
  if data_set["Age"][data_index] == -1:
    if ((data_set["Sex"][data_index] == "female") and (data_set["Pclass"][data_index] == 1)):
      data_set["Age"][data_index] = 35
    elif((data_set["Sex"][data_index] == "female") and (data_set["Pclass"][data_index] == 2)):
      data_set["Age"][data_index] = 29
    elif((data_set["Sex"][data_index] == "female") and (data_set["Pclass"][data_index] == 3)):
      data_set["Age"][data_index] = 22
    elif((data_set["Sex"][data_index] == "male") and (data_set["Pclass"][data_index] == 1)):
      data_set["Age"][data_index] = 41
    elif((data_set["Sex"][data_index] == "male") and (data_set["Pclass"][data_index] == 2)):
      data_set["Age"][data_index] = 31
    elif((data_set["Sex"][data_index] == "male") and (data_set["Pclass"][data_index] == 3)):
      data_set["Age"][data_index] = 27

# Checking
data_set['Age'].isna().sum()

"""-> Now consider cabin (Room No : ), well it's pretty much obvious that it doesn't really depend on that so we can simply **drop this column**"""

# Dropping the column
data_set.drop(columns = 'Cabin', inplace = True)

# Checking
data_set.columns

"""-> Lastly coming to Embarked as the missing percentage is very low [0.22] we can just drop those and be done this"""

# Dropping the missing embarked values
data_set.dropna(inplace = True)
# As embarked are the only missing values left out



"""
-> Now we see that there are some columns with information which is redundant

*   PassengerId
*   Name
*   Ticket

-> As the survival doesn't depend on these we can simply drop them
"""

# Dropping
data_set.drop(columns = ["PassengerId", "Name", "Ticket"], inplace = True)

# Checking
data_set.columns

# Checking for outliers
# We will use boxplot method
figure, axes = plt.subplots(2, 2, figsize = (15, 8))
figure.suptitle("Outliers")
figure.delaxes(axes[1][1])

sns.boxplot(ax = axes[0, 0], data = data_set, x = "Survived", y = "Pclass", palette = "bwr")
sns.boxplot(ax = axes[0, 1], data = data_set, x = "Survived", y = "Age", palette = "bwr")
sns.boxplot(ax = axes[1, 0], data = data_set, x = "Survived", y = "Fare", palette = "bwr")

# Checking
data_set['Pclass'].unique()

"""We conclude,

-> Pclass has 3 discrete values 1, 2, and 3. Hence, no outliers

-> Age: The plots has some data values above 60. This indicates older people travelling in the ship Hence not outliers

-> Fare values can be large depending on the services alloted so this is also not an outlier

#### Categorical Encoding
"""

# For sex
data_set["Sex"].replace("female", 0, inplace = True)
data_set["Sex"].replace("male", 1, inplace = True)

# Checking
data_set['Sex']

# For embarked
# First lets see the uniques values in it
data_set['Embarked'].unique()

data_set['Embarked']

#function to encode 'Embarked'
def encode_embarked(column):

  for data in column:
    if data == 'S':
      column[column.index(data)] = 0
    elif data == 'C':
      column[column.index(data)] = 1
    else:
      column[column.index(data)] = 2

  return column

#implement function
print("Column 'Embarked' before encoding:")
print(data_set["Embarked"][0:5])

data_set["Embarked"] = encode_embarked(list(data_set["Embarked"]))

print("Column 'Embarked' after encoding:")
print(data_set["Embarked"][0:5])

# Checking
data_set['Embarked']

"""* Now we are done with the data pre-processing and the final data looks like"""

data_set.sample(10)

# Converting data in numpy array
x1 = data_set.drop(columns = 'Survived')
y1 = data_set['Survived']

x1

# Correlation Matrix
correlation_matrix = data_set.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='viridis', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()
print()

# Splitting the data
x1_train, x1_test, y1_train, y1_test = train_test_split(x1, y1, train_size = 0.9, random_state = 1)
x1_train, x1_vali, y1_train, y1_vali = train_test_split(x1_train, y1_train, train_size = 7 / 9, random_state = 1)

# Checking
print(len(x1_train), len(x1_vali), len(x1_test))

"""* Implementing the entropy as the cost function to calculate the split."""

# In the code the traininig data is given in the form where both
# target an feature are both required
x1_train['Survived'] = list(y1_train)

# Here we given a column of data as the parameter
def entropy(col):
    # Get each unique class of the column and count for each class to calculate probabilites
    counts = np.unique(col, return_counts = True)
    # Now counts has the unique elements and the count of those unique values as well
    N = float(col.shape[0])
    # N is total rows in the column
    entropy = 0.0

    for idx in counts[1]:
      # counts[1] here is array of counts of diff uniq elem
        prob = idx/N
        # Formula for entropy
        entropy += -1 * prob * np.log2(prob)
    return entropy

# Ex
print(entropy(y1_train))

"""* It is mentioned that the split has to be into two categories
* meaning binary tree //
"""

def conTocat(x, feature, fval):
  # Splitting data meaning one node splits into left
  # and right child nodes considering there is an
  # information gain
    x_right = pd.DataFrame([], columns = x.columns)
    x_left = pd.DataFrame([], columns = x.columns)

  # x_right and x_left are two empty dataframes which will be
  # built base on the val, the splitting condition which accounts
  # for the best/ most information gain
    for index, row in x.iterrows():
        val = x[feature].loc[index]

        if val > fval:
            x_right = x_right.append(x.loc[index])
        else:
            x_left = x_left.append(x.loc[index])

    return x_left, x_right

# Ex
l, r = conTocat(x1_train, 'Sex', 0.5)
print(l)
print(r)

def info_gain(x, fkey, fval):

    # After splitting the data we have to calc their IG
    # To select the best column as the next child node
    left,right = conTocat(x, fkey, fval)

    # Calculate percentages of samples in left and right
    l = float(left.shape[0])/x.shape[0]
    r = float(right.shape[0])/x.shape[0]

    # If all samples are in one side
    if l == 0.0 or r == 0.0:
        return -1 # least IG

    # entropy of parent class - weighted entropy of child class
    i_gain = entropy(x['Survived']) - (l*entropy(left['Survived']) + r*entropy(right['Survived']))

    return i_gain

np.unique(x1_train['Pclass'])

print(info_gain(x1_train, 'Pclass', 1.5))

x1_train['Pclass'].loc[268]

x1_train

# ex
# consider splitting all columns about their mean as fkey and then calc their IG
for col in x1_train.columns:
    print(col, ": ", info_gain(data_set, col, x1_train[col].mean()))

def aid(indii):
  sum = 0
  for i in indii:
    sum += y1_train['Survived'].loc[i]
    meaan = sum / len(indii)
  return meaan

Dict = {'Pclass': 0, 'Sex' : 1, 'Age' : 2, 'SibSp' : 3, 'Parch' : 4, 'Fare' : 5, 'Embarked' : 6}

class DecisionTree:

  def __init__(self, depth = 0):
    self.left = None
    self.right = None
    self.feature = None
    self.fval = None
    self.max_depth = None
    self.depth = depth
    self.target = None

  def train(self, X_train, max_depth):
    # Firstly fix the max depth
    self.max_depth = max_depth
      # Calc IG and fkey for all columns and then select the best
      # and then split ... PERFECTO
    features = X_train.columns
    info_gains = []
    indices = []
      # We iterate through each row and keep on trying with all fkey val
      # Till we get the best IG and then store it
    for feat in features:
      if(feat != "Survived"):
        i_gain = 0.0
        comp = 0.0
        ff = np.unique(X_train[feat])
        to_check = []
        for i in range(len(ff) - 1):
          to_check.append((ff[i] + ff[i + 1]) / 2)
        for t_c in to_check:
          i_g = info_gain(X_train, feat, t_c)
          if(i_g > i_gain):
            i_gain = i_g
            comp = t_c
        info_gains.append(i_gain)
        indices.append(comp)

    self.feature = features[np.argmax(info_gains)]
    self.fval = indices[np.argmax(info_gains)]

        # Split the data
    left, right = conTocat(X_train, self.feature, self.fval)
    # # Dropping the self.feature in the l and r df
    # left = left.drop(columns = self.feature)
    # right = right.drop(columns = self.feature)

    if left.shape[0] == 0 or right.shape[0] == 0:
      if X_train['Survived'].mean() >= 0.5:
        self.target = 'Survived'
      else:
        self.target = 'Dead'
      return



        # Stop early when max depth reached
    if self.depth >= self.max_depth:
      if X_train['Survived'].mean() >= 0.5:
        self.target = 'Survived'
      else:
        self.target = 'Dead'
      return

    self.left = DecisionTree(depth = self.depth+1)
    self.left.train(left, max_depth)
    self.right = DecisionTree(depth = self.depth+1)
    self.right.train(right, max_depth)

    if X_train['Survived'].mean() >= 0.5:
      self.target = 'Survived'
    else:
      self.target = 'Dead'
    return

  def Infer(self, y_test):
    # Base case
    if(self.left == None and self.right == None):
      if(self.target == 'Survived'):
        return 1
      elif(self.target == 'Dead'):
        return 0
    else:
      # We can still traverse
      if(y_test[Dict[self.feature]] < self.fval):
        if(self.left.feature == None):
          if(self.target == 'Survived'):
            return 1
          elif(self.target == 'Dead'):
            return 0
        else:
          return self.left.Infer(y_test)
      else:
        if(self.left.feature == None):
          if(self.target == 'Survived'):
            return 1
          elif(self.target == 'Dead'):
            return 0
        return self.right.Infer(y_test)

lol = DecisionTree()

"""* I have taken height to be 5"""

lol.train(x1_train, 5)

xx_test = list(x1_test.to_numpy())
yy = list(y1_test.to_numpy())

# list of pred data
y_pred = []
for i in range(len(x1_test)):
  y_pred.append(lol.Infer(xx_test[i]))

"""* For tasks 6, 7 and 8 I am gonna use sklearn"""

from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, ConfusionMatrixDisplay, recall_score, f1_score

# Confusion matrix

cm = confusion_matrix(yy, y_pred)
cm_display = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = ['Dead', 'Survived'])
cm_display.plot()
plt.show()

# Precision
print(precision_score(yy, y_pred))

# Recall
print(recall_score(yy, y_pred))

# F1 score
print(f1_score(yy, y_pred))

yyy_pred = []
for i in range(len(x1_train)):
  yyy_pred.append(lol.Infer(list(x1_train.to_numpy())[i]))

# accuracy score on train and test data
print("On train data : ", accuracy_score(list(y1_train.to_numpy()), yyy_pred))
print("On test data : ", accuracy_score(yy, y_pred))

# Class wise accuracy on test data
# we will compute this with the help
# of confusion matrix
print("survived accuracy : ", 28 / 40)
print("dead accuracy : ", 45 / 49)

# Similarly on train data
cm1 = confusion_matrix(list(y1_train.to_numpy()), yyy_pred)
cm1

# Class wise accuracy on train data
print("survived accuracy : ", 172 / (172 + 62))
print("dead accuracy : ", 358 / (358 + 30))