# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 20:08:47 2025

@author: jmc53
"""

import numpy as np
import pulp

prob = pulp.LpProblem("Parts",pulp.LpMaximize)

x1 = pulp.LpVariable("Fuselage Panels", 0, None, pulp.LpContinuous)
x2 = pulp.LpVariable("Wing Spars", 0, None, pulp.LpContinuous)
x3 = pulp.LpVariable("Extra Aluminum", 0, None, pulp.LpContinuous)
x4 = pulp.LpVariable("Extra CNC Hours", 0, None, pulp.LpContinuous)

#Specify the objective statement
prob += pulp.lpSum(26500*x1+15900*x2), "Profit"

#Add Constraint
#prob += pulp.lpSum(x1+x2) <= 53, "Total Assembly Limit"
prob += pulp.lpSum(3*x1+2*x2-x3) <= 600, "Aluminum Supply"
prob += pulp.lpSum(0.5*x1+x2-x4) <= 200, "CNC Hours"
prob += pulp.lpSum(800*x3+150*x4) <=120000, "Extra Material"

prob.solve()
print(x1.varValue)
print(x2.varValue)
print(x3.varValue)
print(x4.varValue)