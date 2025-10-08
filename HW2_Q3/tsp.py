# python3
#Bellman Ford Shortest Path Algorithm
#jcheers
from itertools import combinations
INF=10**9

n=10

d= [
    [INF,6.14,10.54,5.93,10.46,10.73,6.08,9.22,11.02,3.96],
    [6.37,INF,14.52,3.91,10.50,12.11,4.37,5.99,4.84,10.22],
    [8.80,14.34,INF,10.76,7.99,4.93,11.82,19.14,18.88,6.71],
    [5.65,3.63,10.81,INF,5.65,7.89,1.43,11.18,9.04,7.92],
    [10.36,9.37,8.33,5.75,INF,2.68,6.37,15.93,14.75,9.49],
    [10.46,12.06,5.01,7.84,2.76,INF,8.17,17.06,16.23,9.55],
    [6.13,3.33,11.02,0.77,5.68,9.28,INF,9.49,7.76,8.73],
    [8.84,6.51,19.08,11.06,16.98,17.68,9.60,INF,6.77,12.63],
    [10.87,5.41,19.50,8.43,13.28,15.98,7.12,6.57,INF,14.99],
    [4.74,10.13,6.95,7.99,10.51,8.44,8.79,12.41,15.45,INF]
    ]

#HW2-Revision 4
d= [
    [INF,6.43,9.34,5.67,9.67,10.74,6.54,9.37,10.63,4.08],
    [5.97,INF,13.46,4.25,9.43,11.61,3.67,6.36,4.83,10.05],
    [10.27,13.10,INF,10.57,7.80,4.90,10.72,18.74,17.93,6.38],
    [5.55,4.42,10.32,INF,6.05,8.03,1.00,10.78,8.42,8.11],
    [10.40,9.70,7.94,5.89,INF,3.07,6.05,15.60,13.26,9.35],
    [10.11,11.47,4.87,7.94,2.95,INF,8.47,17.18,15.67,9.53],
    [6.52,3.65,10.74,1.03,6.14,8.48,INF,10.01,7.74,9.01],
    [9.14,6.58,18.48,9.96,15.22,17.41,9.57,INF,6.48,13.22],
    [10.86,4.89,18.14,8.43,13.54,15.88,7.40,6.50,INF,14.94],
    [4.01,10.15,7.03,7.96,9.52,9.60,8.95,12.36,14.22,INF]
    ]

def getSetNum(p):
    result=0
    for val in p:
        result+=1<<val
    return result

def getPath():
    C[1][0]=0
    for set_len in range(1,n):
        s_combos=[(0,)+p for p in combinations(range(1,n),set_len)]
        for s_combo in s_combos:
            k_val=getSetNum(s_combo)
            for i in s_combo:
                if i>0:
                    for j in s_combo:
                        if j!=i:
                            #if j==0:
                            #    print(i,j)
                            cmin=C[k_val^(1<<i)][j]+d[i][j]
                            if cmin<C[k_val][i]:
                                C[k_val][i]=cmin
                                node_paths[k_val][i]=[k_val^(1<<i),j]
    result_arr=[C[-1][j] + d[0][j] for j in range(n)]
    minval=min(list(enumerate(result_arr)), key = lambda t: t[1])
    if minval[1]>=INF:
        return -1
    else:
        j=minval[0]
        i=total_sets-1
        for k in range(n-1,-1,-1):
            path[k]=j+1
            if node_paths[i][j]:
                i,j=node_paths[i][j]
    return minval[1]
    
#initialize the path variable
path=[None]*n
total_sets=1<<n
C=[[INF]*n for _ in range(total_sets)]
node_paths=[[None]*n for _ in range(total_sets)]
m=getPath()
if m==-1:
    print('-1')
else:
    print(m)
    print(*path)
