# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 10:52:01 2025

@author: jmc53
"""

import pandas as pd
import numpy as np
from amplpy import AMPL


ampl = AMPL()
ampl.read("E:\\ufl\\OEM\\ESI 6314\\AMPL\\HW2_Q1\\HW2_Q2_3b.mod")
ampl.read_data("E:\\ufl\\OEM\\ESI 6314\\AMPL\\HW2_Q1\\HW2_Q2_3b.dat")

ampl.solve(solver="Gurobi", verbose=False)
print(ampl.solve_result)

solution = ampl.get_solution(flat=False, zeros=False)
solution_df = pd.DataFrame.from_dict(ampl.get_solution(flat=False))
#print(solution_df)
s=np.array(ampl.get_data('s').to_pandas())
u=np.array(ampl.get_data('u').to_pandas())
k=np.array(ampl.get_data('k').to_pandas())
h=np.array(ampl.get_data('h').to_pandas())

da=ampl.get_data('d').to_pandas()

d=np.zeros((6,5))
for i in range(1,7):
    for j in range(1,6):
        d[i-1,j-1]=da.at[(j,i),'d']

x=np.zeros((6,5))
for i in range(1,7):
    for j in range(1,6):
        x[i-1,j-1]=solution['x'][(j,i)]

I=np.zeros((7,5))
for i in range(0,7):
    for j in range(1,6):
        try:
            I[i,j-1]=solution['I'][(j,i)]
        except:
            I[i,j-1]=0

Is=np.zeros((6,5))
for i in range(5):
    Is[:,i]=I[1:,i]*s[i]

kx=np.zeros((6,5))
for i in range(1,7):
    for j in range(1,6):
        try:
            kx[i-1,j-1]=solution['kx'][(j,i)]
        except:
            kx[i-1,j-1]=0

print('Check Storage Constraints')
print(Is.sum(axis=1) <= u.transpose())

xh=np.zeros((6,5))
for i in range(5):
    xh[:,i]=x[:,i]*h[i]-kx[:,i]

print('Check Labor Constraints')
print(xh<=k.transpose())

dI=d-I[:6]

print('Check Supply Constraints')
print(dI<=x)

dIx=(x+I[:6])-d

print('Check Inventory Constraints')
print(dIx==I[1:])