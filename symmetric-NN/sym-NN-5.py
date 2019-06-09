# test 5 -- symmetric quadratic NN

import numpy as np

# The matrix A is 3-dimensional,
# consisting of N blocks, each of size (N ⨉ N)
# satisfying the constraints in my PDF file
# We want to show that this is EQUIVARIANT
# ********* Test result is ??? *********

print("N = ?", end="")
N = int(input())

A = np.random.rand(N, N, N)

# ======== 1st equation:
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					# Which value will appear first?
					A[k][i][j] = A[h][i][j]

print("\nAfter 1st equation, A =\n", A)

# ======== 4th equation:
for h in range(0, N):
	for k in range(0, N):
		A[k][k][h] = A[h][k][h] + A[h][h][k] - A[k][h][k]

print("\nAfter 4th equation, A =\n", A)

# ======== This takes care of the 2nd and 3rd equations:
α = np.random.rand()
β = np.random.rand()
for i in range(0, N):
	np.fill_diagonal(A[i], α)
	# A[i][i][i] = β

print("\nAfter 2nd and 3rd equation, A =\n", A)

# =========== verifications =============

print("\nVerifying 4th equation....")
for h in range(0, N):
	for k in range(0, N):
		if A[k][k][h] + A[k][h][k] != A[h][k][h] + A[h][h][k]:
			print("error: ", h, k)

print("\nVerifying 1st equation....")
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					if A[k][i][j] != A[h][i][j]:
						print("error: ", h, k, i, j)

x = np.random.rand(N)
print("\nx  =", x)

# permute x
σx = np.random.permutation(x)
print("σ·x =", σx)

Y = np.zeros(N)
σY = np.zeros(N)

for k in range(0, N):
	B_k = A[k].dot(x)
	print("B_k = ", B_k)
	Y[k] = B_k.dot(x)

	C_k = A[k].dot(σx)
	σY[k] = C_k.dot(σx)

print("\nA x x =", Y)
print("A σx σx =", σY)
