# -*- coding: utf-8 -*-
"""K-nearest-neighbours.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ycv3mtEOOjNFrzsq4eJqw62h4izC1FeP
"""

#IMPORTING_LIBRARIES
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

#IMPORTING_DATASET
df=pd.read_csv("/content/sample_data/mnist_train_small.csv")
df.head()

xa=(df.drop(["6"],axis=1))/255  #APPLYING NORMALISATION
ya=df[["6"]]

#IMPORTING_TESTSET
dftest=pd.read_csv("/content/sample_data/mnist_test.csv")
dftest.head()

xatest=(dftest.drop(["7"],axis=1))/255  #APPLYING NORMALISATION
xatest.head()
yatest=dftest[["7"]]

dfn1=np.concatenate((xa,ya),axis=1)
dfn2=np.concatenate((xatest,yatest),axis=1)

def euclideanDistance(arr1,arr2,length):
  distance=0
  for i in range(length):
    distance+=pow((arr1[i]-arr2[i]),2)
  return np.sqrt(distance)

import operator
def getNeighbours(trainingset,testarr,k):
  distances=[]
  length=len(testarr)-1
  for x in range(len(trainingset)):
    dist=euclideanDistance(testarr,trainingset[x],length)
    distances.append((trainingset[x],dist))
  distances.sort(key=operator.itemgetter(1))
  neighbors=[]
  for x in range(k):
    neighbors.append(distances[x][0])
  return neighbors

import operator
def getResponse(neighbors):
  classVotes={}
  for x in range(len(neighbors)):
    response=neighbors[x][-1]
    if response in classVotes:
      classVotes[response]+=1
    else:
      classVotes[response]=1
  sortedVotes=sorted(classVotes.items(),key=operator.itemgetter(1),reverse=True)
  return sortedVotes[0][0]

def getAccuracy(testarr,predictions):
  correct=0
  for x in range(len(testarr)):
    if testarr[x][-1] is predictions[x]:
      correct+=1
  return(correct/float(len(testarr)))*100

def main(trainingset,testarr):
  prediction=[]
  k=9
  for i in range(len(testarr)):
    neighbors=getNeighbours(trainingset,testarr[i],k)
    result=getResponse(neighbors)
    prediction.append(result)
    print("> predicted-"+repr(result)+",actual-"+repr(testarr[i][-1]))
  accuracy=getAccuracy(testarr,prediction)
  print("Accuracy:"+repr(accuracy)+"%")

main(dfn1,dfn2)

