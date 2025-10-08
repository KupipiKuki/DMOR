# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 10:52:01 2025

@author: jmc53
"""

import pandas as pd
import numpy as np
import pulp

d = np.array([
    [120,120,150,180,220,260],
    [50,70,80,80,80,80,],
    [15,10,5,30,55,55,],
    [300,320,350,380,440,420],
    [230,235,260,375,260,230]
    ])

N = list(range(5))
T = list(range(6))
C = np.array([
    [1.5,1.5,2,2,2,1.5],
    [0.5,0.5,0.75,1,0.75,0.50],
    [8,8,7,5,5,5],
    [3.5,3.5,2.5,2,2.5,2.5],
    [1,1,1.5,1.5,1.5,1.5]
    ])
s = np.array([0.5,1,3,0.25,0.3])
u = np.array([50,50,50,60,60,40])
k = np.array([195,100,180,200,185])
h = np.array([1, 1.5, 5, 0.5, 0.5])
L = np.array([
    [8.5,8.5,8.5,8.5,9,9],
    [10.5,10.5,11.75,11.75,11.75,10.50],
    [22,22,22,22,25,25],
    [23.5,23.5,22.5,22,22.5,22.5],
    [10,10,10.5,10.5,10.5,10.5]
    ])

#Variables
#x=np.zeros((5,6))
#I = np.zeros((5,7))
I0=np.array([15,17,2,25,50])

prob = pulp.LpProblem("InventoryProblem",pulp.LpMinimize)

x = pulp.LpVariable.dicts("x",(N,T),0,None,pulp.LpInteger)
I = pulp.LpVariable.dicts("I",(N,T+[6]),0,None,pulp.LpContinuous)

prob += pulp.lpSum([C[n,t]*I[n][t+1]+L[n,t]*x[n][t] for n in N for t in T]), "Sum of labor and storage cost"

for n in N:
    prob += pulp.lpSum(I0[n]) == I[n][0], f'subject to initial inventory [{n}]'

#for n in N:
#    for t in T:
#        prob += pulp.lpSum(d[n,t]-I[n][t+1]) <= x[n][t], f'subject to supply [{n},{t}]'
         
for n in N:
    for t in T:
        prob += pulp.lpSum(I[n][t]+(x[n][t]-d[n,t])) == I[n][t+1], f'subject to inventory [{n},{t}]'

for t in T:
    prob += pulp.lpSum([I[n][t+1]*s[n] for n in N]) <= u[t], f'subject to inventory check [{t}]'

for n in N:
    for t in T:
        prob += pulp.lpSum(h[n]*x[n][t]) <= k[n], f'subject to labor [{n},{t}]'

prob.solve()
print(pulp.value(prob.objective))  
  
#np.array([[I[i][j].varValue for i in N] for j in T+[6]])
#np.array([[x[i][j].varValue for i in N] for j in T])

#subject to initial {n in 1..N}: (I[n,0] = I0[n]);
#subject to supply {n in 1..N, t in 1..T}: d[n,t]-I[n,t-1] <= x[n,t];
#subject to inventory {n in 1..N, t in 1..T}: I[n,t] = I[n,t-1]+(x[n,t]-d[n,t]);
#subject to inventory_check {t in 1..T}: sum{n in 1..N}I[n,t]*s[n]<=u[t];
#subject to hours {n in 1..N, t in 1..T}: h[n]*x[n,t]<=k[n];