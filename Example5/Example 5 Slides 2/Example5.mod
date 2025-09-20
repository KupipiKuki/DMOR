set I;
set J;

param c {i in I, j in J};
param d {i in I};
param k {j in J};

var y {i in I, j in J} binary;

minimize totalCost: sum{i in I, j in J}d[i]*c[i,j]*y[i,j];
subject to allDemand {i in I}: sum{j in J}y[i,j]=1;
subject to capacity {j in J}: sum{i in I}d[i]*y[i,j] <= k[j];