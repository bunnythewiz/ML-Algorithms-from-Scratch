# -*- coding: utf-8 -*-
"""Linear-Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b3v01Ge81YQqqxCPXJmo_4PwRSvU0Lrd
"""

from sklearn.datasets import fetch_lfw_people
# min_faces_per_person signifies how many photos should atleast be there
# so as to include when extracting
lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)

images = lfw_people.images
images.shape

"""This shows we have 1288 images with size 50X37
* It basically is image representation in the form of matrix{PIXELS}
"""

# displaying multiple images as examples
fig = plt.figure(figsize=(10, 7))

# Say 4 images
for i in range(1, 5):
  fig.add_subplot(2, 2, i)
  plt.imshow(images[i])
  plt.axis('off')
  plt.title(lfw_people.target_names[lfw_people.target[i]])

# But for easy operations we will be using 1D form of these matrices
# We will be directly using the data function
# This here will be our feature variables
X = lfw_people.data
X.shape

"""* This shows that the entire 1288 images and 1850 features"""

# Visualisation
print(X[0])
print(X[0].shape)

# Now for target variable
y = lfw_people.target
y.shape

"""* Each image has a target that is their name which can be accesed via their categorcal encoded numbers .target"""

# Ex
y[1]

# Each category can be used to get their names
names = lfw_people.target_names
names[rand.randint(0, y[np.argmax(y)])]

# Now that we have got features and target
# Lets perform the split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8)

# KNN on original data before PCA
knn = KNeighborsClassifier()

# Model training
knn.fit(X_train,y_train)

# Testing
y_predict = knn.predict(X_test)

# Accuracy
acc_before_knn = accuracy_score(y_test,y_predict)

# Decision tree before PCA

model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_predict = model.predict(X_test)

acc_before_dt = accuracy_score(y_test, y_predict)

# Random Forest before PCA

model = RandomForestClassifier()
model.fit(X_train, y_train)
y_predict = model.predict(X_test)

acc_before_rf = accuracy_score(y_test, y_predict)

"""# PCA"""

# First we have to find the mean face
mean_face = np.mean(X_train, axis = 0)

# Converting 1D to pixel format
face = mean_face.reshape(50, 37)

# Checking
face.shape

# Mean face Visualisation
plt.imshow(face)

# # Now subtract each face with the mean face
X_train -= mean_face
X_test -= mean_face

class PCA:

  def __init__(self):

    # initializing eigenvalues, eigenvectors
    # and eigenfaces
    self.eigenvalues = None
    self.eigenvectors = None
    self.eigenfaces = None

  def Compute_eigenval_vec(self,X_train):

    # Get covarience matrix
    cov_matrix = np.cov(X_train.T)

    # Get Eigen values and Eigen vectors
    # The values and vectors are pair-wise related
    self.eigenvalues, self.eigenvectors = np.linalg.eigh(cov_matrix)

    # Sorting eigen vectors based on eigen values in descending order
    # As argsort gives ascending order we just have to reverse it
    sorted_indices = np.argsort(self.eigenvalues)[::-1]
    self.eigenvalues = self.eigenvalues[sorted_indices]
    self.eigenvectors = self.eigenvectors[:,sorted_indices]

    return

  def compute_eigenfaces(self, n_components):

    # In eigenvectors eigenfaces are arranged column wise
    self.eigenfaces = self.eigenvectors[:,:n_components]

    return

  def Feature_reduction(self, data, n_components):

    # Get the Projection matrix of required components
    projection_matrix = self.eigenfaces[:,:n_components]

    # Reduce the features by taking dot product between projection matrix
    # and original data
    new_data = np.dot(data, projection_matrix)

    return new_data

  def scree_plot(self):

    x = range(1, len(self.eigenvalues)+1)
    fig = px.scatter(x = x, y = self.eigenvalues,
               labels = {'x':'No.of features','y':'EigenValues'},
               title = 'Scree Plot'
    )

    fig.show()

    # return


    plt.plot(x, self.eigenvalues)
    plt.xlabel('No.of features')
    plt.ylabel('EigenValues')
    plt.title('Scree Plot')

    plt.show()

  def varience_graph(self):

    # varience here means eigenvalues
    varience_fraction = self.eigenvalues / (np.sum(self.eigenvalues))
    cummulative_variance = np.cumsum(varience_fraction)
    x = range(1, len(self.eigenvalues)+1)
    y = cummulative_variance
    fig = px.scatter(x = x, y = y,
               labels = {'x':'n_components','y':'Cummulative Variance'},
               title = 'varience_graph'
    )

    fig.show()

    plt.plot(x, y)
    plt.xlabel('n_components')
    plt.ylabel('Cummulative Variance')
    plt.title('varience_graph')

    plt.show()

    return

# Create object
pca = PCA()

# Get PC's
pca.Compute_eigenval_vec(X_train)

# compute eigenfaces
pca.compute_eigenfaces(162)

# Plot the top-10 eigenfaces
plt.figure(figsize=(10, 5))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(pca.eigenfaces[:,i].reshape(50, 37))
    plt.title(f"Eigenface {i + 1}")
    plt.xticks(())
    plt.yticks(())

plt.suptitle("Top-10 Eigenfaces")
plt.show()

# Scree plot
pca.scree_plot()

# Varience graph
pca.varience_graph()

# Plot the top-10 eigenfaces
plt.figure(figsize=(20, 20))
for i in range(10):
    if i == 0:
      plt.subplot(5, 5, i + 1)
      plt.imshow((X_train[0] + mean_face).reshape(50, 37))
      plt.axis('off')
      plt.title('original')
    else:
      plt.subplot(5, 5, i + 1)
      pca.compute_eigenfaces(i * 30)
      X_train_ = pca.Feature_reduction(X_train, i * 30)
      X_re = np.dot(X_train_, pca.eigenfaces.T)
      X_re += mean_face
      plt.imshow(X_re[0].reshape(50, 37))
      plt.axis('off')
      plt.title('n_comp = ' + str(i * 30))


plt.suptitle("Reconstruction")
plt.show()

# Projecting data on choosen number of n_comp
X_train_ = pca.Feature_reduction(X_train, 162)
X_test_ = pca.Feature_reduction(X_test, 162)
# compute eigenfaces
pca.compute_eigenfaces(162)

# Checking
X_train_.shape

# Now let's try reconstructing the data
X_re = np.dot(X_train_, pca.eigenfaces.T)

# adding mean to it
X_re += mean_face

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

target_names = []
for i in range(7):
  target_names.append(names[i])

# KNN on projected data
knn = KNeighborsClassifier()

# Model training
knn.fit(X_train_,y_train)

# Testing
y_predict_knn = knn.predict(X_test_)

# Accuracy
acc_after_knn = accuracy_score(y_test,y_predict_knn)

# variation in accuracy before and after PCA
print("Before PCA", acc_before_knn)
print("After PCA", acc_before_knn)
print("Difference", acc_before_knn - acc_after_knn)

# Confusion Matrix
cm = confusion_matrix(y_test,y_predict_knn)
cm_display = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = target_names)
cm_display.plot()
plt.xticks(rotation = 90)
plt.show()

# Classification Report
print(classification_report(y_test, y_predict_knn, target_names=target_names))

# Decision tree after PCA

model = DecisionTreeClassifier()
model.fit(X_train_, y_train)
y_predict_dt = model.predict(X_test_)

acc_after_dt = accuracy_score(y_test, y_predict_dt)

# variation in accuracy before and after PCA
print("Before PCA", acc_before_dt)
print("After PCA", acc_before_dt)
print("Difference", acc_before_dt - acc_after_dt)

# Confusion Matrix
cm = confusion_matrix(y_test,y_predict_dt)
cm_display = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = target_names)
cm_display.plot()
plt.xticks(rotation = 90)
plt.show()

# Classification Report
print(classification_report(y_test, y_predict_dt, target_names=target_names))

# Random Forest after PCA

model = RandomForestClassifier()
model.fit(X_train_, y_train)
y_predict_rf = model.predict(X_test_)

acc_after_rf = accuracy_score(y_test, y_predict_rf)

# variation in accuracy before and after PCA
print("Before PCA", acc_before_rf)
print("After PCA", acc_before_rf)
print("Difference", acc_before_rf - acc_after_rf)

# Confusion Matrix
cm = confusion_matrix(y_test,y_predict_rf)
cm_display = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = target_names)
cm_display.plot()
plt.xticks(rotation = 90)
plt.show()

# Classification Report
print(classification_report(y_test, y_predict_rf, target_names=target_names))

"""* It is possible that the accuracy of the model is better after PCA reasons being

1.   remove noise
2.   irrelevant information
"""

values, counts = np.unique(lfw_people.target, return_counts=True)

# Plot the top-10 eigenfaces
plt.figure(figsize=(20, 20))
for i in range(7):
    plt.subplot(5, 5, i + 1)
    for j in range(len(images)):
      if lfw_people.target[j] == i:
        plt.imshow(images[j].reshape(50, 37))
        plt.title(lfw_people.target_names[lfw_people.target[j]] + '- Count : '
                   + str(counts[i]))
        plt.xticks(())
        plt.yticks(())
        break

plt.suptitle("All Farget Faces")
plt.show()

# variartions in one target
plt.figure(figsize=(50, 50))

count  = -1
for j in range(len(images)):
  if lfw_people.target[j] == 0:
    count += 1
    plt.subplot(5, 10, count + 1)
    plt.imshow(images[j].reshape(50, 37))
    plt.title(str(count + 1))
    plt.xticks(())
    plt.yticks(())
    if count == 49:
      break


plt.suptitle("variartions in Arial Sharon")
plt.show()

# variartions in one target
plt.figure(figsize=(50, 50))

count  = -1
for j in range(len(images)):
  if lfw_people.target[j] == 3:
    count += 1
    plt.subplot(5, 10, count + 1)
    plt.imshow(images[j].reshape(50, 37))
    plt.title(str(count + 1))
    plt.xticks(())
    plt.yticks(())
    if count == 49:
      break


plt.suptitle("variartions in George W Bush")
plt.show()

"""# Reasons For Misclassification


1.   The count of George W-Bush is 530 which is like 52% of data {More Weight}
      and for Hugo Chavez it is only 7% {Less weights}
  *   Overfitting on George W-Bush
  *   Underfitting on Hugo Chavez
2.   The images provided are not uniform, meaning :

  *   Few images have glasses
  *   Face is covered by hands
  *   Eyes are closed
  *   Teeth is visible
  *   Few are way darker and other more brighter {CONTRAST}
  *   Entire head is visible
  *   Clothes are visible
  *   Some are left dominant and other right dominant poses
  *   In some lips are closed
  *   Some are happy, sad, Excited, scared


"""

# Checking for OUTLIERS via Z-SCORE
data = lfw_people.data
mean = np.mean(data, axis = 0)
stand_dev = np.std(data, axis = 0)

min = mean - 3 * stand_dev
max = mean + 3 * stand_dev
final = []

for i in data:
  if (i > min).all and (i < max).all:
    final.append(i)
print(len(final), len(data))

"""* We see that there are no outliers in the data

# To see how accuracy is dependent on n_components
"""

# varience here means eigenvalues

x = range(1, 300)
y = []

for i in x:
  # compute eigenfaces
  pca.compute_eigenfaces(i)
  # Projecting data on choosen number of n_comp
  X_train_ = pca.Feature_reduction(X_train, i)
  X_test_ = pca.Feature_reduction(X_test, i)
  # KNN on projected data
  knn = KNeighborsClassifier()
  # Model training
  knn.fit(X_train_,y_train)
  # Testing
  y_predict_knn = knn.predict(X_test_)
  # Accuracy
  y.append(accuracy_score(y_test,y_predict_knn))

fig = px.scatter(x = x, y = y,
                labels = {'x':'n_components','y':'Accuracy'},
                title = 'Dependence on n_comp for KNN'
                )

fig.show()
plt.plot(x, y)
plt.xlabel('n_components')
plt.ylabel('Accuracy')
plt.title('Dependence on n_comp for KNN')

plt.show()

# varience here means eigenvalues

x = range(1, 300)
y = []

for i in x:
  # compute eigenfaces
  pca.compute_eigenfaces(i)
  # Projecting data on choosen number of n_comp
  X_train_ = pca.Feature_reduction(X_train, i)
  X_test_ = pca.Feature_reduction(X_test, i)
  # dt on projected data
  dt = DecisionTreeClassifier()
  # Model training
  dt.fit(X_train_,y_train)
  # Testing
  y_predict_dt = dt.predict(X_test_)
  # Accuracy
  y.append(accuracy_score(y_test,y_predict_dt))

fig = px.scatter(x = x, y = y,
                labels = {'x':'n_components','y':'Accuracy'},
                title = 'Dependence on n_comp for Decision Tree'
                )

fig.show()
plt.plot(x, y)
plt.xlabel('n_components')
plt.ylabel('Accuracy')
plt.title('Dependence on n_comp for Decision Tree')

plt.show()

# varience here means eigenvalues

x = range(1, 300)
y = []

for i in x:
  # compute eigenfaces
  pca.compute_eigenfaces(i)
  # Projecting data on choosen number of n_comp
  X_train_ = pca.Feature_reduction(X_train, i)
  X_test_ = pca.Feature_reduction(X_test, i)
  # rf on projected data
  rd = RandomForestClassifier()
  # Model training
  rd.fit(X_train_,y_train)
  # Testing
  y_predict_rd = rd.predict(X_test_)
  # Accuracy
  y.append(accuracy_score(y_test,y_predict_rd))

fig = px.scatter(x = x, y = y,
                labels = {'x':'n_components','y':'Accuracy'},
                title = 'Dependence on n_comp for Random Forest'
                )

fig.show()
plt.plot(x, y)
plt.xlabel('n_components')
plt.ylabel('Accuracy')
plt.title('Dependence on n_comp for Random Forest')

plt.show()

import random as rand
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import warnings
# Ignore warnings
warnings.filterwarnings('ignore')

import time

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt
from matplotlib.image import imread

import plotly.express as px