# -*- coding: utf-8 -*-
"""Vectorised_logistic_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X5iNFLGtZ5xirFLFo_r6oWiCetcNXQJs
"""

#IMPORTING_LIBRARIES
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

#IMPORTING_MNIST_DATASET
df=pd.read_csv("/content/sample_data/mnist_train_small.csv")
df.head()

x=df.drop(["6"],axis=1)
y=df["6"]
x.head()

def feature_normalize(X):
    n_features = X.shape[1]
    means = np.array([np.mean(X.iloc[i,:]) for i in range(n_features)])
    stddevs = np.array([np.std(X.iloc[i,:]) for i in range(n_features)])
    normalized = (X - means) / stddevs
    return normalized

X=feature_normalize(x)

X=np.column_stack((np.ones(len(X)),X))

#HYPOTHESIS WITH INBUILT SIGMOID
def hypothesis(theta,X):
  return 1/(1+np.exp(-np.dot(X,theta)))

#DEFINING HYPOTHESIS
def hypothesisn(theta,X):   #USED FOR PROBABILITY FINDING
  return np.dot(X,theta)

def compute_cost(h,y):
  return (-1/len(y))*(sum(y*np.log(h)+(1-y)*np.log(1-h)))

#MATRIX_Ycoll
ycoll=np.ones((X.shape[0],9))
for i in range(0,X.shape[0]):
  if y[i]!=1:
    ycoll[i][0]=0
  if y[i]!=2:
    ycoll[i][1]=0
  if y[i]==2:
    ycoll[i][1]=1
  if y[i]!=3:
    ycoll[i][2]=0
  if y[i]==3:
    ycoll[i][2]=1
  if y[i]!=4:
    ycoll[i][3]=0
  if y[i]==4:
    ycoll[i][3]=1
  if y[i]!=5:
    ycoll[i][4]=0
  if y[i]==5:
    ycoll[i][4]=1
  if y[i]!=6:
    ycoll[i][5]=0
  if y[i]==6:
    ycoll[i][5]=1
  if y[i]!=7:
    ycoll[i][6]=0
  if y[i]==7:
    ycoll[i][6]=1
  if y[i]!=8:
    ycoll[i][7]=0
  if y[i]==8:
    ycoll[i][7]=1
  if y[i]!=9:
    ycoll[i][8]=0
  if y[i]==9:
    ycoll[i][8]=1

theta = np.zeros(X.shape[1])

def gradient_descent_multi(X, y, theta, alpha,lam, iterations):
    theta = np.zeros(X.shape[1])
    m = len(X)
    cost=[]
    
    for i in range(iterations):
        h=hypothesis(theta,X)
        gradient = -(1/m) *( np.dot(X.T,y*(1-h))+np.dot(X.T,(y-1)*h))
        c=theta[0]
        theta = theta - alpha * (gradient+(1/m)*lam*sum(theta))
        theta[0]=c-alpha*(gradient[0])
        cost.append(compute_cost(h,y))
    return theta,cost

theta1,cost1=gradient_descent_multi(X,ycoll[:,0],theta,0.001,10,6000)

theta2,cost2=gradient_descent_multi(X,ycoll[:,1],theta,0.001,10,6000)

theta3,cost3=gradient_descent_multi(X,ycoll[:,2],theta,0.001,10,6000)

theta4,cost4=gradient_descent_multi(X,ycoll[:,3],theta,0.001,10,6000)

theta5,cost5=gradient_descent_multi(X,ycoll[:,4],theta,0.001,10,6000)

theta6,cost6=gradient_descent_multi(X,ycoll[:,5],theta,0.001,10,6000)

theta7,cost7=gradient_descent_multi(X,ycoll[:,6],theta,0.001,10,6000)

theta8,cost8=gradient_descent_multi(X,ycoll[:,7],theta,0.001,10,6000)

theta9,cost9=gradient_descent_multi(X,ycoll[:,8],theta,0.001,10,6000)

#IMPORTING TESTSET
dft=pd.read_csv("/content/sample_data/mnist_test.csv")
dft.head()

xt=dft.drop(["7"],axis=1)
yt=dft["7"]

X_test=feature_normalize(xt)
X_test=np.column_stack((np.ones(len(X_test)),X_test))

#CALCULATING THE PARAMETERS REQUIRED FOR PROBABILITY MEASUREMENT
RHS1=hypothesisn(theta1,X_test) 
RHS2=hypothesisn(theta2,X_test)
RHS3=hypothesisn(theta3,X_test)
RHS4=hypothesisn(theta4,X_test)
RHS5=hypothesisn(theta5,X_test)
RHS6=hypothesisn(theta6,X_test)
RHS7=hypothesisn(theta7,X_test)
RHS8=hypothesisn(theta8,X_test)
RHS9=hypothesisn(theta9,X_test)

#BASE_PROBABILITY(P_ZERO)
Pzero=1/(1+np.exp(RHS1)+np.exp(RHS2)+np.exp(RHS3)+np.exp(RHS4)+np.exp(RHS5)+np.exp(RHS6)+np.exp(RHS7)+np.exp(RHS8)+np.exp(RHS9))

#OBTAINING OTHER PROBABILITIES USING BASE_PROBABILITY
P1=np.exp(RHS1)*Pzero
P2=np.exp(RHS2)*Pzero
P3=np.exp(RHS3)*Pzero
P4=np.exp(RHS4)*Pzero
P5=np.exp(RHS5)*Pzero
P6=np.exp(RHS6)*Pzero
P7=np.exp(RHS7)*Pzero
P8=np.exp(RHS8)*Pzero
P9=np.exp(RHS9)*Pzero

Pmat=np.vstack((Pzero,P1,P2,P3,P4,P5,P6,P7,P8,P9))
Pmat=Pmat.transpose()

y_pred=Pmat.argmax(axis=1)

def accuracy(y_pred,y_test):
  count=0
  for i in range(X_test.shape[0]):
    if y_pred[i]==y_test[i]:
      count+=1
  return (count/X_test.shape[0])*100

print(accuracy(y_pred,yt))

