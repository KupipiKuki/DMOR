# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 22:23:25 2025

@author: jmc53
"""

import pandas as pd
import numpy as np
from amplpy import AMPL


ampl = AMPL()
ampl.read("E:\\ufl\\OEM\\ESI 6314\\AMPL\\HW2\\Q3\\HW2_Q3.mod")
ampl.read_data("E:\\ufl\\OEM\\ESI 6314\\AMPL\\HW2\\Q3\\HW2_Q3.dat")

ampl.solve(solver="Gurobi", verbose=False)
print(ampl.solve_result)

solution = ampl.get_solution(flat=False, zeros=False)

nodes=list(solution['x'].keys())