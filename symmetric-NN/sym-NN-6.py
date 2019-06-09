# test 5 -- symmetric quadratic NN, corrected version

import numpy as np

# The matrix A is 3-dimensional
# consisting of N blocks, each of size (N ⨉ N)
# satisfying the constraints in my PDF file
# We want to show that this is EQUIVARIANT
# ********* Test result is ??? *********

print("N = ?", end="")
N = int(input())

A = np.random.rand(N, N, N)

# ======== "Diagonal" equations:
α = np.random.rand()
β = np.random.rand()
for i in range(0, N):
	np.fill_diagonal(A[i], α)
	A[i][i][i] = β

print("'Diagonal' constraints...")  # A =\n", A)

# ======== 1st equation:
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					# Which value will appear first?
					A[k][i][j] = A[h][i][j]

print("1st equation....")  # A =\n", A)

# ======== Last equation, "additive constraint":
for h in range(0, N):
	for k in range(0, N):
		A[k][k][h] = A[h][k][h] + A[h][h][k] - A[k][h][k]

print("Additive constraint....")  # A =\n", A)

# ======== "Missing" equations:
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				A[h][k][j] = A[k][h][j]
				A[h][h][j] = A[k][k][j]
				#A[h][j][k] = A[k][j][h]
				#A[h][j][h] = A[k][j][k]

# ======== "Missing" equations:
for h in range(N - 1, 0, -1):
	for k in range(N - 1, 0, -1):
		for j in range(N - 1, 0, -1):
			if j != h and j != k:
				A[h][j][h] = A[k][j][k]
				A[h][j][k] = A[k][j][h]
				#A[h][h][j] = A[k][k][j]
				#A[h][k][j] = A[k][h][j]

# ======== "Missing" equations:
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				A[h][k][j] = A[k][h][j]
				A[h][h][j] = A[k][k][j]
				A[h][j][k] = A[k][j][h]
				A[h][j][h] = A[k][j][k]

# ======== "Missing" equations:
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				A[k][h][j] = A[h][k][j]
				A[k][k][j] = A[h][h][j]
				A[k][j][h] = A[h][j][k]
				A[k][j][k] = A[h][j][h]

print("'Missing' constraints....")

print("A =\n", A)

def error(a1,a2,a3,b1,b2,b3):
	print("A[{:d}][{:d}][{:d}] ≠ A[{:d}][{:d}][{:d}]".format(a1,a2,a3,b1,b2,b3), end="\t")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3],A[b1][b2][b3]))

print("\nVerifying 'missing' equations....")
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				if A[h][k][j] != A[k][h][j]:
					error(k,k,j,   k,h,j)
					A[h][k][j] = A[k][h][j]
				if A[h][h][j] != A[k][k][j]:
					error(h,h,j,   k,k,j)
					A[h][h][j] = A[k][k][j]
				if A[h][j][k] != A[k][j][h]:
					error(h,j,k,   k,j,h)
					A[h][j][k] = A[k][j][h]
				if A[h][j][h] != A[k][j][k]:
					error(h,j,h,   k,j,k)
					A[h][j][h] = A[k][j][k]

print("\nVerifying 'missing' equations....")
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				if A[h][k][j] != A[k][h][j]:
					error(k,k,j,   k,h,j)
				if A[h][h][j] != A[k][k][j]:
					error(h,h,j,   k,k,j)
				if A[h][j][k] != A[k][j][h]:
					error(h,j,k,   k,j,h)
				if A[h][j][h] != A[k][j][k]:
					error(h,j,h,   k,j,k)

# =========== verifications =============

print("\nVerifying additive constraint....")
for h in range(0, N):
	for k in range(0, N):
		if A[k][k][h] + A[k][h][k] != A[h][k][h] + A[h][h][k]:
			error(k,k,h,  h,k,h)

print("\nVerifying 1st equation....")
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					if A[k][i][j] != A[h][i][j]:
						print("error: ", h, k, i, j)

x = np.random.rand(N)
print("\nx   =", x)

# permute x
σx = np.random.permutation(x)
print("σ·x =", σx)

Y = np.zeros(N)
σY = np.zeros(N)

for k in range(0, N):
	B_k = A[k].dot(x)
	# print("B_k = ", B_k)
	Y[k] = B_k.dot(x)

	C_k = A[k].dot(σx)
	σY[k] = C_k.dot(σx)

print("\nA x x   =", Y)
print("A σx σx =", σY)
