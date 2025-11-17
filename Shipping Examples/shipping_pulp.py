# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 08:53:25 2025

@author: jmc53
"""

import pandas as pd
import numpy as np
import pulp

branches=np.array([
    [ 1,  1,  0, 20,  1,  6],
    [ 2,  2,  0, 20,  2,  6],
    [ 3,  3,  0, 20,  3,  6],
    [ 4,  1,  0, 20,  4,  6],
    [ 5,  5,  0, 20,  5,  6],
    [ 6,  2,  0, 20,  1,  7],
    [ 7,  3,  0, 20,  2,  7],
    [ 8,  4,  0, 20,  3,  7],
    [ 9,  5,  0, 20,  4,  7],
    [10,  7,  0, 20,  5,  7],
    [11,  1,  0, 20,  1,  8],
    [12,  3,  0, 20,  2,  8],
    [13,  2,  0, 20,  3,  8],
    [14,  1,  0, 20,  4,  8],
    [15,  1,  0, 20,  5,  8],
    [16,  1,  0, 20,  1,  9],
    [17,  2,  0, 20,  2,  9],
    [18,  1,  0, 20,  3,  9],
    [19,  3,  0, 20,  4,  9],
    [20,  5,  0, 20,  5,  9],
    [21,  1,  0, 20,  1, 10],
    [22,  2,  0, 20,  2, 10],
    [23,  1,  0, 20,  3, 10],
    [24,  4,  0, 20,  4, 10],
    [25,  5,  0, 20,  5, 10],
    [26,  1,  0, 20,  1, 11],
    [27,  2,  0, 20,  2, 11],
    [28,  1,  0, 20,  3, 11],
    [29,  3,  0, 20,  4, 11],
    [30,  2,  0, 20,  5, 11],
    [31,  1,  0, 20,  1, 12],
    [32,  4,  0, 20,  2, 12],
    [33,  3,  0, 20,  3, 12],
    [34,  1,  0, 20,  4, 12],
    [35,  5,  0, 20,  5, 12],
    [36,  4,  0, 20,  1, 13],
    [37,  1,  0, 20,  2, 13],
    [38,  2,  0, 20,  3, 13],
    [39,  1,  0, 20,  4, 13],
    [40,  3,  0, 20,  5, 13],
    [41,  2,  0, 20,  1, 14],
    [42,  1,  0, 20,  2, 14],
    [43,  2,  0, 20,  3, 14],
    [44,  1,  0, 20,  4, 14],
    [45,  2,  0, 20,  5, 14],
    [46,  3,  0, 20,  1, 15],
    [47,  1,  0, 20,  2, 15],
    [48,  3,  0, 20,  3, 15],
    [49,  4,  0, 20,  4, 15],
    [50,  2,  0, 20,  5, 15],
    [51,  0,  0, 20,  1, 16],
    [52,  0,  0, 20,  2, 16],
    [53,  0,  0, 20,  3, 16],
    [54,  0,  0, 20,  4, 16],
    [55,  0,  0, 20,  5, 16]
    ])

nodes=np.array([
    [  1,  10],
    [  2,  12],
    [  3,   5],
    [  4,   5],
    [  5,  20],
    [  6,  -1],
    [  7,  -5],
    [  8,  -5],
    [  9,  -2],
    [ 10, -10],
    [ 11,  -2],
    [ 12,  -4],
    [ 13,  -6],
    [ 14,  -2],
    [ 15,  -1],
    [ 16, 0]
    ])

#Create the Slack Variable
nodes[15,1]=-1*(nodes[0:5,1].sum()+nodes[5:15,1].sum())

n_b=branches[:,0]
n_n=nodes[:,0]
c=branches[:,1]
lb=branches[:,2]
ub=branches[:,3]
i=branches[:,4]
j=branches[:,5]
b=nodes[:,1]

prob = pulp.LpProblem("InventoryProblem",pulp.LpMinimize)

x = pulp.LpVariable.dicts("x",(n_b),0,None,pulp.LpContinuous)

prob += pulp.lpSum([c[a-1]*x[a] for a in n_b]), 'cost'

for n in n_n:
    prob += pulp.lpSum([x[a+1] for a in np.where(i==n)[0]]+[-1*x[a+1] for a in np.where(j==n)[0]]) == b[n-1], f'inventory {n}'

for n in n_b:
    prob += pulp.lpSum(x[n]) >= lb[n-1], f'lower_b {n}'
    
for n in n_b:
    prob += pulp.lpSum(x[n]) <= ub[n-1], f'upper_b {n}'

prob.solve()
print(f'Solver: {prob.solver}')
print(pulp.value(prob.objective))

for n in n_b:
    if n<55:
        if x[n].varValue > 0:
            print(f'node: {i[n-1]} to {j[n-1]}',x[n].varValue)

for n in n_n:
    print(
        sum([x[a+1].varValue for a in np.where(i==n)[0]]),
        sum([-1*x[a+1].varValue for a in np.where(j==n)[0]]),
        b[n-1])