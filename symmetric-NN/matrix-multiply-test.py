# symmetric matrix test

import numpy as np

A = np.random.rand(2,2)
B = np.random.rand(2,2)

M1 = np.hstack((A,B,B))
M2 = np.hstack((B,A,B))
M3 = np.hstack((B,B,A))
M = np.vstack((M1,M2,M3))
print("M =\n", M)

x = np.random.rand(6)
print("x  =", x)

# permute x
x2 = np.array([x[2], x[3], x[0], x[1], x[4], x[5]])
print("x' =", x2)

print("M x  =", x.dot(M))
print("M x' =", x2.dot(M))
