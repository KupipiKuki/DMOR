# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 22:21:08 2025

@author: jmc53
"""

import numpy as np
import pulp
import matplotlib.pyplot as plt

d= np.array([
    [1e8,6.14,10.54,5.93,10.46,10.73,6.08,9.22,11.02,3.96],
    [6.37,1e8,14.52,3.91,10.50,12.11,4.37,5.99,4.84,10.22],
    [8.80,14.34,1e8,10.76,7.99,4.93,11.82,19.14,18.88,6.71],
    [5.65,3.63,10.81,1e8,5.65,7.89,1.43,11.18,9.04,7.92],
    [10.36,9.37,8.33,5.75,1e8,2.68,6.37,15.93,14.75,9.49],
    [10.46,12.06,5.01,7.84,2.76,1e8,8.17,17.06,16.23,9.55],
    [6.13,3.33,11.02,0.77,5.68,9.28,1e8,9.49,7.76,8.73],
    [8.84,6.51,19.08,11.06,16.98,17.68,9.60,1e8,6.77,12.63],
    [10.87,5.41,19.50,8.43,13.28,15.98,7.12,6.57,1e8,14.99],
    [4.74,10.13,6.95,7.99,10.51,8.44,8.79,12.41,15.45,1e8]
    ])

#HW2-Revision 4
d= np.array([
    [1e8,6.43,9.34,5.67,9.67,10.74,6.54,9.37,10.63,4.08],
    [5.97,1e8,13.46,4.25,9.43,11.61,3.67,6.36,4.83,10.05],
    [10.27,13.10,1e8,10.57,7.80,4.90,10.72,18.74,17.93,6.38],
    [5.55,4.42,10.32,1e8,6.05,8.03,1.00,10.78,8.42,8.11],
    [10.40,9.70,7.94,5.89,1e8,3.07,6.05,15.60,13.26,9.35],
    [10.11,11.47,4.87,7.94,2.95,1e8,8.47,17.18,15.67,9.53],
    [6.52,3.65,10.74,1.03,6.14,8.48,1e8,10.01,7.74,9.01],
    [9.14,6.58,18.48,9.96,15.22,17.41,9.57,1e8,6.48,13.22],
    [10.86,4.89,18.14,8.43,13.54,15.88,7.40,6.50,1e8,14.94],
    [4.01,10.15,7.03,7.96,9.52,9.60,8.95,12.36,14.22,1e8]
    ])

n = 10
N = list(range(n))

prob = pulp.LpProblem("RoutingProblem",pulp.LpMinimize)

x = pulp.LpVariable.dicts("x",(N,N),0,1,pulp.LpInteger)
u = pulp.LpVariable.dicts("u",(N),1,10,pulp.LpInteger)


#Objective Statement
obj_smt = []
for i in N:
    for j in N:
        if i != j:
            obj_smt.append(d[i,j] * x[i][j])
prob += pulp.lpSum(obj_smt), "Sum of Routes"


for i in N:
    check=[]
    for j in N:
        if i != j:
            check.append(x[i][j])
    prob += pulp.lpSum(check) == 1, f'Check Out of Node {i}'
    

for j in N:
    check=[]
    for i in N:
        if i != j:
            check.append(x[i][j])
    prob += pulp.lpSum(check) == 1, f'Check In to Node {j}'

check=[]
for j in N:
    for i in N:
        if i != j and i != 0 and j !=0:
            prob += pulp.lpSum(u[i] - u[j] + n * x[i][j]) <= n - 1, f'Check MZT {i}{j}'

prob.solve()
print(pulp.value(prob.objective))  

path=[]
for i in N:
    for j in N:
        if x[i][j].varValue == 1:
            path.append((i+1,j+1))

coords={
        1:['Main Office',7,5,'right','top',-0.5],
        2:['C0092',13,7,'right','top',-0.5],
        3:['C0464',0,12,'right','bottom',0.5],
        4:['C0391',10,10,'right','top',-0.5],
        5:['C0322',7,15,'center','bottom',0.5],
        6:['C0202',4,15,'center','bottom',0.5],
        7:['C0412',11,10,'left','bottom',0.5],
        8:['C0273',15,1,'center','top',-0.5],
        9:['C0222',18,7,'center','bottom',0.5],
        10:['C0226',3,6,'right','top',-0.5]
        }

plt.figure(figsize=(10, 10))

for i in coords.keys():
    plt.plot(coords[i][1],coords[i][2],'ro',markersize=10)
    plt.text(coords[i][1],coords[i][2]+coords[i][5],coords[i][0],
             horizontalalignment=coords[i][3],
             verticalalignment=coords[i][4])

for i in N:
    c1=path[i][0]
    c2=path[i][1]
    xs=np.array([coords[c1][1],coords[c2][1]])
    ys=np.array([coords[c1][2],coords[c2][2]])
    plt.plot(xs,ys,'k--')
    xl=(xs[1]-xs[0])
    xsg=1 if xl>=0 else -1
    yl=(ys[1]-ys[0])
    ysg=1 if yl>=0 else -1
    ang=np.atan(abs(yl)/abs(xl))
    xm=xs.mean()-np.cos(ang)*xsg*0.25
    ym=ys.mean()-np.sin(ang)*ysg*0.25
    xo=np.cos(ang)*xsg*0.5
    yo=np.sin(ang)*ysg*0.5
    if xsg < 0 and ysg < 0:
        ang=np.pi+ang
    elif xsg < 0 and ysg > 0:
        ang=np.pi-ang
    elif xsg > 0 and ysg < 0:
        ang=2*np.pi-ang
    print(ang*180/np.pi,xl,yl,xsg,ysg)
    plt.annotate("",xytext=(xm,ym),xy=(xm+xo,ym+yo),arrowprops=dict(arrowstyle='wedge',mutation_scale=50))

plt.xlim(-2,22)
plt.ylim(-2,22)
plt.title('ESI 6314 HW2 Q.3.3')
plt.savefig('Q3_3.png')
plt.show()

#np.array([[x[i][j].varValue for i in n] for j in n])

'''
minimize totalDist: sum {i in N, j in N: i != j} d[i,j] * x[i,j];

s.t. outOfNode {i in N}: sum {j in N: j != i} x[i,j] = 1;
s.t. intoNode {j in N}: sum {i in N: i != j} x[i,j] = 1;
#Miller-Tucker-Zemlin Formula for simplified computation
s.t. shortestPath {i in N, j in N: i != j and i != 1 and j != 1}: u[i] - u[j] + n * x[i,j] <= n - 1;
'''
