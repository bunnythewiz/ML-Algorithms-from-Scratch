# -*- coding: utf-8 -*-
"""Linear-Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b3v01Ge81YQqqxCPXJmo_4PwRSvU0Lrd

# Modules
"""

import csv
import numpy as np
import pandas as pd

import math

import seaborn as sns
import matplotlib.pyplot as plt

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score

from sklearn.model_selection import train_test_split

# Import and mount to access drive
from google.colab import drive
drive.mount('/gdrive')

"""#Naive Bayes

## Data Pre-Processing & Visualisation
"""

# Create a data frame of data.csv
df = pd.read_csv('/gdrive/MyDrive/naive_bayes.csv', header = 0)

# Sample
df

# Information
df.info()

# Description
df.describe()

# Amount of missing data
print("Percentage of missing values:")
print(((df.isna().sum()) / df.shape[0]) * 100)

# Getting target and features
X = df.drop('Play', axis=1)
y = df['Play']

from sklearn.preprocessing import LabelEncoder

# Initialize LabelEncoder
label_encoder = LabelEncoder()

# Apply LabelEncoder to each categorical column
X['Outlook'] = label_encoder.fit_transform(df['Outlook'])
X['Temp'] = label_encoder.fit_transform(df['Temp'])
X['Humidity'] = label_encoder.fit_transform(df['Humidity'])
X['Windy'] = label_encoder.fit_transform(df['Windy'])

# Checking
X

# Data Distribution Plots
def plot_data_distribution(df):
    plt.figure(figsize=(12, 8))
    for i in range(len(X.columns)):
        plt.subplot(2, 2, i + 1)
        sns.histplot(df[df.columns[i]])
        plt.title(df.columns[i] + ' Distribution')
    plt.tight_layout()
    plt.show()

plot_data_distribution(df)

"""## TASK 0"""

# train-test Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.14,
                                                      random_state = 42)

# Checking
print(len(X_train), len(X_test))

"""## TASK 1"""

# Calculation of prior probabilities
yes = 0
no = 0
for i in y_train:
  if i == 'yes':
    yes += 1
  else:
    no += 1

p_yes = yes / (yes + no)
p_no = no / (yes + no)

plt.figure(figsize = (8, 6))
outcomes = ['yes', 'no']
probabilities = [p_yes, p_no]

sns.barplot(x = outcomes, y = probabilities, palette='pastel')
plt.title('Prior Probabilities', fontsize = 16)
plt.xlabel('Outcome', fontsize = 12)
plt.ylabel('Probability', fontsize = 12)

# Adding probability values on top of bars
for i in range(len(outcomes)):
    plt.text(i, probabilities[i] + 0.01, f"{probabilities[i]:.2f}",
             ha = 'center', fontsize = 10)

plt.ylim(0, 1)  # Setting y-axis limits
plt.show()

"""## TASK 2"""

# For this task I will first split the dataframe
# into two the yes one and the no one
yep = []
nah = []
for i in range(len(y_train)):
  if y_train.iloc[i] == 'yes':
    yep.append(i)
  else:
    nah.append(i)

X_yes = X_train.iloc[yep]
X_no = X_train.iloc[nah]

likelihood_yes = []

# Making individual list for each column
# then append it to likelihood
for col in X_yes.columns:
  diff_values = X[col].unique()
  li = [0] * len(diff_values)
  for val in X_yes[col]:
    li[val] += 1
  li = [x / len(X_yes[col]) for x in li]
  likelihood_yes.append(li)

likelihood_no = []

# Making individual list for each column
# then append it to likelihood
for col in X_no.columns:
  diff_values = X[col].unique()
  li = [0] * len(diff_values)
  for val in X_no[col]:
    li[val] += 1
  li = [x / len(X_no[col]) for x in li]
  likelihood_no.append(li)

df_1 = pd.DataFrame({ 'Outlook' : ['Overcast', 'Rainy', 'Sunny']
                     , 'P(yes)' : likelihood_yes[0]
                      , 'p(no)' : likelihood_no[0] })

df_2 = pd.DataFrame({    'Temp' : ['Cool', 'Hot', 'Mild']
                     , 'P(yes)' : likelihood_yes[1]
                      , 'p(no)' : likelihood_no[1] })

df_3 = pd.DataFrame({'Humidity' : ['High', 'Normal']
                     , 'P(yes)' : likelihood_yes[2]
                      , 'p(no)' : likelihood_no[2] })

df_4 = pd.DataFrame({   'Windy' : ['f', 't']
                     , 'P(yes)' : likelihood_yes[3]
                      , 'p(no)' : likelihood_no[3] })

# Concatenating DataFrames horizontally
result = pd.concat([df_1, df_2, df_3, df_4], axis=1)

# Displaying the result
result.style.hide()

"""##TASK 3"""

# To array conversion
X_test = X_test.to_numpy()
i , j = X_test.shape

p1_yes = p_yes
p1_no = p_no

for col in range(j):
  p1_yes *= likelihood_yes[col][X_test[0][col]]
  p1_no *= likelihood_no[col][X_test[0][col]]

print('For yes : ', p1_yes)
print('For no : ', p1_no)

p2_yes = p_yes
p2_no = p_no

for col in range(j):
  p2_yes *= likelihood_yes[col][X_test[1][col]]
  p2_no *= likelihood_no[col][X_test[1][col]]

print('For yes : ', p2_yes)
print('For no : ', p2_no)

"""##TASK 4"""

# Making predictions
print('For case 1')
if(p2_yes > p2_no):
  print('Playing')
else:
  print('Not Plating')

# Making predictions
print('For case 2')
if(p2_yes > p2_no):
  print('Playing')
else:
  print('Not Plating')

"""##TASK 5"""

# Laplace Smoothing
# Considering alpha  = 0.01
alpha = 0.01
# No of features k
k = None

likelihood_yes = []

# Making individual list for each column
# then append it to likelihood
for col in X_yes.columns:
  diff_values = X[col].unique()
  k = len(diff_values)
  li = [0] * len(diff_values)
  for val in X_yes[col]:
    li[val] += 1
  li = [(x + alpha) / (len(X_yes[col]) +
          (k * alpha)) for x in li]
  likelihood_yes.append(li)

likelihood_no = []

# Making individual list for each column
# then append it to likelihood
for col in X_no.columns:
  diff_values = X[col].unique()
  k = len(diff_values)
  li = [0] * len(diff_values)
  for val in X_no[col]:
    li[val] += 1
  li = [(x + alpha) / (len(X_no[col]) +
          (k * alpha)) for x in li]
  likelihood_no.append(li)

df_1 = pd.DataFrame({ 'Outlook' : ['Overcast', 'Rainy', 'Sunny']
                     , 'P(yes)' : likelihood_yes[0]
                      , 'p(no)' : likelihood_no[0] })

df_2 = pd.DataFrame({    'Temp' : ['Cool', 'Hot', 'Mild']
                     , 'P(yes)' : likelihood_yes[1]
                      , 'p(no)' : likelihood_no[1] })

df_3 = pd.DataFrame({'Humidity' : ['High', 'Normal']
                     , 'P(yes)' : likelihood_yes[2]
                      , 'p(no)' : likelihood_no[2] })

df_4 = pd.DataFrame({   'Windy' : ['f', 't']
                     , 'P(yes)' : likelihood_yes[3]
                      , 'p(no)' : likelihood_no[3] })

# Concatenating DataFrames horizontally
result = pd.concat([df_1, df_2, df_3, df_4], axis=1)

# Displaying the result
result.style.hide()

p1_yes = p_yes
p1_no = p_no

for col in range(j):
  p1_yes *= likelihood_yes[col][X_test[0][col]]
  p1_no *= likelihood_no[col][X_test[0][col]]

print('For yes : ', p1_yes)
print('For no : ', p1_no)

p2_yes = p_yes
p2_no = p_no

for col in range(j):
  p2_yes *= likelihood_yes[col][X_test[1][col]]
  p2_no *= likelihood_no[col][X_test[1][col]]

print('For yes : ', p2_yes)
print('For no : ', p2_no)

y_pred = []

# Making predictions
print('For case 1')
if(p1_yes > p1_no):
  print('Playing')
  y_pred.append('yes')
else:
  print('Not Playing')
  y_pred.append('no')

# Making predictions
print('For case 2')
if(p2_yes > p2_no):
  print('Playing')
  y_pred.append('yes')
else:
  print('Not Playing')
  y_pred.append('no')

accuracy_score(y_test, y_pred)