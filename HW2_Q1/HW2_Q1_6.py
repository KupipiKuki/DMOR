# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 20:41:55 2025

@author: jmc53
"""
import numpy as np
import matplotlib.pyplot as plt
from sympy.solvers import solve
from sympy import Symbol
import sympy.core.numbers as scn

def f1(x):
    return (750-3*x)/2
def f2(x):
    return 200-0.5*x
def fo(x,z,x3=0,x4=0):
    return (z-26500*x+800*x3+150*x4)/15900
def limits(x1,y1):
    a=solve([3*x+2*y<=750,0.5*x+y<=200,x>=0,y<=x,y>=0], x)
    return a.subs({'y': y1,'x' : x1})
    
x = Symbol('x')
y = Symbol("y")
x1, =  solve(f1(x)-f2(x))
x01, = solve(f1(x))
x02 = 0
x03 = 0

y1 = f1(x1)
y01 = f1(x01)
y02 = 200
y03 = 0

xs=[]
ys=[]

arr=[
    limits(x1,y1),
    limits(x01,y01),
    limits(x02,y02)]

plt.figure(figsize=(8, 6))

plt.plot(x01,y01,'ro',markersize=10)
plt.plot(x1,y1,'ro',markersize=10)
plt.plot(x02,y02,'ro',markersize=10)

plt.fill([x01,x1,x02,x03,x01],[y01,y1,y02,y03,y01],'blue',alpha=0.5)

xr = np.linspace(0,400,100)
y1r = f1(xr)
y2r = f2(xr)

plt.plot(xr,y1r,'k--')
plt.plot(xr,y2r,'k--')
#plt.plot(xr,y3r,'k--')

xo = np.linspace(0,1000,100)
yo = fo(xo,6505000,x3=150)
plt.plot(xo,yo,'k--',color='r')

def convert_sympy(value,string=False):
    if type(value) == scn.Rational:
        value=value.evalf()
    if type(value) == scn.Zero or type(value) == scn.Integer or type(value) == int:
        if string:
            return f'{int(value):,d}'
        return int(value)
    if type(value) == scn.Float or type(value) == float:
        if string:
            return f'{float(value):,.1f}'
        return float(value)
    
plt.annotate(convert_sympy(x01,True)+','+convert_sympy(y01,True),(convert_sympy(x01)+5,convert_sympy(y01)+5))
plt.annotate(convert_sympy(x02,True)+','+convert_sympy(y02,True),(convert_sympy(x02)+5,convert_sympy(y02)+5))
plt.annotate(convert_sympy(x1,True)+','+convert_sympy(y1,True),(convert_sympy(x1)+5,convert_sympy(y1)))
plt.annotate('26500*x1+15900*x2-800*x3-150*x4=6505000',(150,200),color='red')
plt.annotate('3*x1+2*x2<=750',(100,250),color='black')
plt.annotate('0.5*x1+x2<=200',(275,75),color='black')

plt.xlim(0,400)
plt.ylim(0,300)
plt.title('ESI 6314 HW2 Q.1.6')
plt.savefig('Q1_6.png')
plt.show()