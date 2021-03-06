# -*- coding: utf-8 -*-
"""Neural_network_N_layer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YLEoJM6ihmYSA2I_kwfw9VuBNk1ybw5K
"""

#IMPORTING IMPORTANT LIBRARIES
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

#IMPORTING DATASET
df=pd.read_csv("/content/sample_data/mnist_train_small.csv")
df.head()

x=df.drop(["6"],axis=1)

y=df["6"]

layer=[784,40,40,40,10]#input for the number of hidden units and their dimensions

#NORMALISING 
def feature_normalize(X):
    mean=np.array(np.mean(X,axis=1)).reshape(X.shape[0],1)
    std=np.array(np.std(X,axis=1)).reshape(X.shape[0],1)
    normalized=(X-mean)/(std+1e-7)
    return normalized

X=feature_normalize(x)

#HYPOTHESIS WITH INBUILT SIGMOID FOR FORWARD PROPAGATION
def relu(X):
  return np.maximum(X,0)
def softmax_out(theta,arr,bias):
  mul=np.exp(np.dot(arr,theta)+bias)
  suma=np.sum(mul,axis=1).reshape(mul.shape[0],1)
  return mul/suma

def loss(h,params,y,reg):
  loss=0
  square=0
  for o in range(len(layer)-1):
    square+=np.sum(params['W'+str(o+1)])
  loss -= np.sum(np.log(out[np.arange(len(y)), y]))
  loss += 0.5 * reg * square #square is for regularisation
  return loss/len(y)

params={}
for i in range(len(layer)-1):
  params['W'+str(i+1)]=np.random.rand(layer[i],layer[i+1])*0.001
  params['b'+str(i+1)]=np.random.rand((1))

def forward_relu(arr1,arr2,bias):
  return relu(np.dot(arr1,arr2)+bias)
def forward_softmax(theta,arr,bias):
  return softmax_out(arr,theta,bias)

#LOOP FOR UPDATING THE PARAMETERS
cost=[]
z=0
num_iter=350
batch_size=500
lr=0.006
reg=0.8
for i in range(num_iter):
  l=0
  for j in range(X.shape[0]//batch_size):#USE 500 EXAMPLES AT A TIME AND UPDATE
    X1=x[l:l+batch_size]
    Y1=y[l:l+batch_size]
    fwd={'f0':X1}  
    for o in range(len(layer)-2):
      fwd['f'+str(o+1)]=forward_relu(fwd['f'+str(o)],params['W'+str(o+1)],params['b'+str(o+1)])
    out=forward_softmax(fwd['f'+str(len(layer)-2)],params['W'+str(len(layer)-1)],params['b'+str(len(layer)-1)])
    Dout=np.copy(out)
    Dout[np.arange(len(Y1)),Y1]-=1
    bp={}
    bp['bp1']=Dout
    for o in range(len(layer)-2):
      bp['bp'+str(o+2)]=np.dot(bp['bp'+str(o+1)], params['W'+str(len(layer)-o-1)].T) * (fwd['f'+str(len(layer)-o-2)] > 0)
    #Gradients
    grads={}
    for o in range(len(layer)-1):
      grads['W'+str(o+1)]=np.dot(fwd['f'+str(o)].T,bp['bp'+str(len(layer)-o-1)])/batch_size
      grads['b'+str(len(layer)-o-1)]=np.sum(bp['bp'+str(len(layer)-o-1)],axis=0)/batch_size
      grads['W'+str(o+1)]+=reg*params['W'+str(o+1)]
    #UPDATING PARAMETERS
    for o in range(len(layer)-1):
      params['W'+str(o+1)]-=lr*grads['W'+str(o+1)]
      params['b'+str(o+1)]-=lr*sum(grads['b'+str(o+1)])

    l+=batch_size  #INCREMENT IN VALUE OF L 
    z+=1
    cost.append(loss(out,params,Y1,reg))
  if i%50==0:
    print(f'i={i},cost={cost[i]}')

#Plotting Cost VS Iteration:
n_iterations = [x for x in range(1,z+1)]
plt.plot(n_iterations, cost)
plt.xlabel('No. of iterations')
plt.ylabel('Cost')

dft=pd.read_csv("/content/sample_data/mnist_test.csv")

x_test=dft.drop(["7"],axis=1)
y_test=dft["7"]
X_test=feature_normalize(x_test)

fwd_test={'f0':X_test}  
for o in range(len(layer)-2):
  fwd_test['f'+str(o+1)]=forward_relu(fwd_test['f'+str(o)],params['W'+str(o+1)],params['b'+str(o+1)])
output=forward_softmax(fwd_test['f'+str(len(layer)-2)],params['W'+str(len(layer)-1)],params['b'+str(len(layer)-1)])

y_pred=np.argmax(output,axis=1)

print(np.mean(y_pred==y_test))#accuracy

