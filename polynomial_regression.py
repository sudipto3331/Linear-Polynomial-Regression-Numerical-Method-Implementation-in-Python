# -*- coding: utf-8 -*-
"""
@author: Sudipto
"""

import numpy as np
import xlrd
from matplotlib import pyplot as plt
 
def brcond_Seidel(E,err,n):
    
    a=0
    for i in range(n):  
        if E[i]<err:
            a=a+1
    return a/n
def Gauss_Seidel(a):

    err=10**-15         #Assumed percentage relative error
    ite=10**4          #Assumed number of iterations
    
    n=np.shape(a)[0]
    #Initialize variables
    E=np.zeros([n])
    rel_err=np.zeros([ite,n])
    X=np.zeros([n])
    x=np.zeros([ite,n])
    itern=np.zeros([ite])
    p=np.zeros([n])
    
    #Iteration for Gauss Seidel begins here.
    for j in range(ite):
        #storing the values of iteration
        itern[j]=j+1
                 
        for i in range(n):
            summation=0
            
            for k in range(n):
                
                if k>i or k<i:
                    summation=summation+a[i,k]*x[j,k]
            
            x[j,i]=(a[i,n]-summation)/a[i,i]   #Determining the values of unknown variables
            
            #Error calculation
            if j>0:
                rel_err[j,i]=((x[j,i]-x[j-1,i])/x[j,i])*100
                E[i]=rel_err[j,i]
        if j>0:
            Q=brcond_Seidel(E,err,n)
            
            if Q==1:
                break

        if j==ite-1:
            break
         
        x[j+1,:]=x[j,:]
    
    #num_of_iter=j
    X=x[j,:]
    
    #Result Verification    
    for i in range(n):
        summation=0
        for j in range(n):
            summation=summation+a[i,j]*X[j]
        
        p[i]=summation-a[i,j+1]
        
    return X, p

m=int(input('Enter the order of the regression polynomial: ' ))

#Reading data from excel file
loc = ('Regression.xls')

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(3)

N=sheet.ncols-1   
#initialize variables
x=np.zeros([N])
y=np.zeros([N])
Y=np.zeros([N])
a=np.zeros([m+1,m+2])

#creating matrix from the data 
for i in range(1,sheet.ncols):
    #print(sheet.cell_value(1, i))
    x[i-1]=sheet.cell_value(0, i)
    y[i-1]=sheet.cell_value(1, i)

for p in range(m+1):
    for q in range(m+2):
        if all([p==0, q==0]):
            a[p,q]=N
        if all([p==0, q>0]):
            a[p,q]=sum(x**q)
        if all([p>0, q<m+1]):
            a[p,q]=sum(x**(q+p))
        if q==m+1:
            a[p,q]=sum(x**(p)*y)

X, p=Gauss_Seidel(a)

for Z in range(N):
    addition=0
    for v in range(m+1):
        addition=addition+X[v]*x[Z]**(v)

    Y[Z]=addition

plt.figure(1)
plt.plot(x,y,'o') 
plt.plot(x,Y)
plt.xlabel('Values of x')
plt.ylabel('Values of y')
plt.title('Curve fitting using polynomial regression')
plt.legend(['Measured','Estimated'], loc='upper left')
plt.show()
