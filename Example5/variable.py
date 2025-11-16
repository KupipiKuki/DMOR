# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 08:53:08 2025

@author: jmc53
"""

import numpy as np

c=np.array([
    [1,2,3,1,5],
    [2,3,4,5,7],
    [1,3,2,1,1],
    [1,2,1,3,5],
    [1,2,1,4,5],
    [1,2,1,3,2],
    [1,4,3,1,5],
    [4,1,2,1,3],
    [2,1,2,1,2],
    [3,1,3,4,2]
    ])

d=np.array([
    1,5,5,2,10,2,4,6,2,1
    ])

k=np.array([
    10,12,5,5,20
    ])

n_stores=5
n_customers=10
n_branches=n_stores*n_customers

stores=range(1,n_stores+1)
customers=range(6,n_stores+n_customers+1)

branches=[]

for i in customers:
    for j in stores:
        branches.append([((i-6)*5)+j,int(c[i-6,j-1]),0,20,j,i])

for j in stores:
    branches.append([n_branches+j,0,0,20,n_stores+n_customers+1,j])

for j in stores:
    branches.append([n_branches+j,0,0,20,j,n_stores+n_customers+1])

nodes=[[j,int(k[j-1])] for j in stores]
nodes=nodes+[[i,-1*int(d[i-6])] for i in customers]
nodes.append([n_stores+n_customers+1,int(d.sum()-k.sum())])
    