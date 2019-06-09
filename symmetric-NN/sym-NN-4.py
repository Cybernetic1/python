# test 4 -- symmetric linear NN, half-folded

import numpy as np

# The matrix A is of size (N ⨉ 2N) and of the form:
# 	e a a b c d
#	a e a b c d
#	a a e b c d
# which has (N + 2) different parameters
# We want to show that this is EQUIVARIANT
# ********* Test result is FAIL *********

print("N = ?", end="")
N = int(input())

A = np.full((N, N), np.random.rand())
np.fill_diagonal(A, np.random.rand())
for i in range(0, N):
	B = np.full((N, 1), np.random.rand())
	A = np.hstack((A, B))

print("A =\n", A)

x = np.random.rand(2 * N)
print("\nx  =", x)

# permute x
σx = np.random.permutation(x)
print("σ·x =", σx)

print("\nA x  =", A.dot(x))
print("A σx =", A.dot(σx))
