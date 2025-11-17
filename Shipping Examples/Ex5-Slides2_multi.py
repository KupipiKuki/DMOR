# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 14:35:57 2025

@author: jmc53
"""

import numpy as np
from pulp import *

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

c=c.transpose()

d=np.array([
    1,5,5,2,10,2,4,6,2,1
    ])

k=np.array([
    10,12,5,5,20
    ])

stores=list(range(5))
customers=list(range(10))

prob = LpProblem("DistributionProblem",LpMinimize)

#Create the decision variables for the store selected to meet demand
#By designating integer and speficying a bounds of 0 and 1 it
#will create the binary constraint
y = LpVariable.dicts("y",(stores,customers),0,None,LpInteger)

#Specify the objective statement
prob += lpSum([c[i][j]*y[i][j] for i in stores for j in customers]), "Sum of Transporting Costs"

# Add the constraint that the maximum store count to meet demand must be equal to 1
for j in customers:
    prob += lpSum([y[i][j] for i in stores]) == d[j], "Customer %s served from stores"%j

# Add the constraint that the total customers demand from each store does not
# exceed the total inventory
for i in stores:
    prob += lpSum([y[i][j] for j in customers]) <= k[i], "Sum of Products out of Store %s"%i

prob.solve()
#print('Optimal Solution: ', value(prob.objective))

for i in stores:
    for j in customers:
        if y[i][j].varValue > 0:
            print(f'y {i},{j}:',y[i][j].varValue)