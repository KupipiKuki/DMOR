# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 13:32:31 2025

@author: jmc53
"""

import numpy as np
import pyomo.environ as pyo

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
    [51,  0,  0, 20, 16,  1],
    [52,  0,  0, 20, 16,  2],
    [53,  0,  0, 20, 16,  3],
    [54,  0,  0, 20, 16,  4],
    [55,  0,  0, 20, 16,  5],
    [56,  0,  0, 20,  1, 16],
    [57,  0,  0, 20,  2, 16],
    [58,  0,  0, 20,  3, 16],
    [59,  0,  0, 20,  4, 16],
    [60,  0,  0, 20,  5, 16]
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

model = pyo.ConcreteModel()

model.x = pyo.Var(n_b, domain = pyo.NonNegativeReals )

@model.Objective(sense=pyo.minimize)
def cost(m):
    return sum([c[a-1]*model.x[a] for a in n_b])

@model.Constraint(n_n)
def inventory(m, n):
    return sum([model.x[a+1] for a in np.where(i==n)[0]]+[-1*model.x[a+1] for a in np.where(j==n)[0]]) == b[n-1]
    
@model.Constraint(n_b)
def lower_b(m, n):
    return model.x[n] >= lb[n-1]
    
@model.Constraint(n_b)
def upper_b(m, n):
    return model.x[n] <= ub[n-1]

opt = pyo.SolverFactory('glpk') 
result_obj = opt.solve(model, tee=True)
print(result_obj['Problem'])

#model.pprint()

#minimize Cost: sum{a in ARCS} c[a]*x[a];
#s.t. balance {n in NODES}: sum{a in ARCS: i[a]=n}x[a]-sum{a in ARCS: j[a]=n}x[a]=b[n];
#s.t. lower_b {a in ARCS}: x[a] >= lb[a];
#s.t. upper_b {a in ARCS}: x[a] <= ub[a];

#a=[True,True,False,True]
#list(filter(lambda i: i != False, a))