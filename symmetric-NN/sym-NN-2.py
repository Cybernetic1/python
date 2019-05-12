# symmetric quadratic NN

import numpy as np

# The matrix M2 is of the form:
#	a b b
#	b a b
#	b b a
# symmetric test succeeds,
# 但这只是一层，一层来说，需要的是 equivariance 而不是 invariance (symmetric)

a = np.random.rand(1)
b = np.random.rand(1)

R1 = np.hstack((a, b, b))
R2 = np.hstack((b, a, b))
R3 = np.hstack((b, b, a))
M2 = np.vstack((R1, R2, R3))
print("M2 =\n", M2)

β = np.random.rand(1)
M1 = np.hstack((β, β, β))
print("M1 =\n", M1)

γ = np.random.rand(1)
print("γ = ", γ)

print()

x = np.random.rand(3)
print("x  =", x)

# permute x
σx = np.random.permutation(x)
print("σx =", σx)

print()

print("f(x)  =", γ + x.dot(M1) + (x.dot(M2)).dot(x))
print("f(σx) =", γ + σx.dot(M1) + (σx.dot(M2)).dot(σx))

print("M2(x)  =", x.dot(M2))
print("M2(σx) =", σx.dot(M2))

print("g(x)  =", γ + x.dot(M1))
print("g(σx) =", γ + σx.dot(M1))

exit(0)
# ============================= old code ==================================

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
