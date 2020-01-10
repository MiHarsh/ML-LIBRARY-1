# -*- coding: utf-8 -*-
"""K_means_Algorithm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Fz6o01Wxs_AkEiTVAzT5csJXXcDebsXG
"""

#IMPORTING_LIBRARIES
import numpy as np
import pandas as pd

#IMPORTING DATASET
df=pd.read_csv("/content/sample_data/mnist_train_small.csv")
df.head()

x=df.drop(["6"],axis=1)
y=df["6"]
y=np.array(y)

#APPLYING FEATURE NORMALISE
def feature_normalize(X):
  n_features=X.shape[1]
  means = np.array([np.mean(X.iloc[i,:]) for i in range(n_features)])
  stddevs = np.array([np.std(X.iloc[i,:]) for i in range(n_features)])
  normalized = (X - means) / stddevs
  return normalized

X=feature_normalize(x)

#DEFINING EUCLIDEAN_DISTANCE
def euclideanDistance(arr1,arr2):
  distance=sum(pow((arr1-arr2).T,2))
  return np.sqrt(distance)

m=X.shape[0] #number of training examples
n=X.shape[1] #number of features.Here n=784
n_iter=100

K=10 #since we are using it for number classsification
X=np.array(X)

#RAndom centroids are selected from the Dataset itself
Centroids=np.array([]).reshape(n,0) 
for i in range(K):
    rand=np.random.randint(0,m-1)
    Centroids=np.c_[Centroids,X[rand]]

#VECTORISING THE CENTROID VECTOR FOR EASE DISTANCE CALCULATION
def rep(arr):
  return np.tile(arr,(X.shape[0],1))

Output={} #For KEys as cluster and values as the assigned data points

for i in range(n_iter):
     #FINDING EUCLIDEAN DISTANCE
      EuclidianDistance=np.array([]).reshape(m,0)
      for k in range(K):
        repeated=rep(Centroids[:,k])
        tempDist=euclideanDistance(X,repeated)
        EuclidianDistance=np.c_[EuclidianDistance,tempDist]
      C=np.argmin(EuclidianDistance,axis=1)+1
     #CENTROID ASSIGNMENT STEP
      Y={}
      for k in range(K):
          Y[k+1]=np.array([]).reshape(n,0)
      for i in range(m):
          Y[C[i]]=np.c_[Y[C[i]],X[i]]
     
      for k in range(K):
          Y[k+1]=Y[k+1].T
    
      for k in range(K):
          Centroids[:,k]=np.mean(Y[k+1],axis=0)
      Output=Y

#MAKING CLASSIFIER THROUGH WHICH IT WILL EASY TO FIND WHICH CENTROID PREDICTS WHICH NUMBER
Classifier=[]
for i in range(K):
  Dist=euclideanDistance(X,rep(Centroids[:,i]))
  Dist2=np.vstack((Dist,y)).T
  Distf=sorted(Dist2,key=lambda x: (x[0]))
  lis=[]
  for j in range(40):
    lis.append(Distf[j][1])
  l=[]
  l.append(i+1)
  l.append(max(lis,key=lis.count))
  Classifier.append(l)

#IMPORTING TESTSET
dft=pd.read_csv("/content/sample_data/mnist_test.csv")

x_test=dft.drop(["7"],axis=1)

y_test=dft["7"]

X_test=feature_normalize(x_test)

X_test=np.array(X_test)
def reptest(arr):
  return np.tile(arr,(X_test.shape[0],1))

EuclidianDistance=np.array([]).reshape(X_test.shape[0],0)
for k in range(K):
        repeated=reptest(Centroids[:,k])
        tempDist=euclideanDistance(X_test,repeated)
        EuclidianDistance=np.c_[EuclidianDistance,tempDist]
C_test=np.argmin(EuclidianDistance,axis=1)+1

Y_pred=[]
for i in range(X_test.shape[0]):
  j=C_test[i]
  for o in range(K):
    if Classifier[o][0]==j:
      Y_pred.append(Classifier[o][1])

def accuracy(Y_pred,Y_test):
  count=0
  for i in range(len(Y_pred)):
    if Y_pred[i]==Y_test[i]:
      count+=1
  return (count/len(Y_test))*100

accuracy(Y_pred,y_test)

