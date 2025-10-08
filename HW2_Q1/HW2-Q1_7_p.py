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
x3 = pulp.LpVariable("Wing Ribs", 0, None, pulp.LpContinuous)

#Specify the objective statement
prob += pulp.lpSum(26500*x1+15900*x2+21200*x3), "Profit"

#Add Constraint
#prob += pulp.lpSum(x1+x2) <= 53, "Total Assembly Limit"
prob += pulp.lpSum(3*x1+2*x2+2.5*x3) <= 600, "Aluminum Supply"
prob += pulp.lpSum(0.5*x1+x2+0.3*x3) <= 200, "CNC Hours"

prob.solve()
print(x1.varValue)
print(x2.varValue)