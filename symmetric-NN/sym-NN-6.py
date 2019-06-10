# test 6 -- symmetric quadratic NN, corrected version

import numpy as np

# The matrix A is 3-dimensional
# consisting of N blocks, each of size (N ⨉ N)
# satisfying the constraints in my PDF file
# We want to show that this is EQUIVARIANT
# ********* Test result is SUCCESS for n = 3 *********
# Constraint enforcement fails for n = 4

print("N = ?", end="")
N = int(input())

A = np.random.rand(N, N, N)

print("Enforcing 'diagonal' constraints...")
α = np.random.rand()
β = np.random.rand()
for i in range(0, N):
	np.fill_diagonal(A[i], α)
	A[i][i][i] = β

print("Enforcing 1st equation....")
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					# Which value will appear first?
					A[k][i][j] = A[h][i][j]

print("Enforcing 'missing' constraints....")
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				A[h][k][j] = A[k][h][j]
				A[h][h][j] = A[k][k][j]
				A[k][j][h] = A[h][j][k] 	# swapped
				A[h][j][h] = A[k][j][k]

print("Enforcing 'additive' constraint....")
for h in range(0, N):
	for k in range(0, N):
		A[k][k][h] = A[h][k][h] + A[h][h][k] - A[k][h][k]

for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				A[h][k][j] = A[k][h][j]
				A[h][h][j] = A[k][k][j]
				A[k][j][h] = A[h][j][k] 	# swapped
				A[h][j][h] = A[k][j][k]

print("Enforcing 1st equation....")
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					# Which value will appear first?
					A[k][i][j] = A[h][i][j]

print("Enforcing 'missing' constraints....")
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				A[h][k][j] = A[k][h][j]
				A[h][h][j] = A[k][k][j]
				A[k][j][h] = A[h][j][k] 	# swapped
				A[h][j][h] = A[k][j][k]

print("Enforcing 1st equation....")
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					# Which value will appear first?
					A[k][i][j] = A[h][i][j]

print("Enforcing 'missing' constraints....")
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				A[h][k][j] = A[k][h][j]
				A[h][h][j] = A[k][k][j]
				A[k][j][h] = A[h][j][k] 	# swapped
				A[h][j][h] = A[k][j][k]

print("A =\n", A)

# =========== verifications =============

errorFlag = False

def error(typ, a1,a2,a3,b1,b2,b3):
	errorFlag = True
	print("type {:d}  A[{:d}][{:d}][{:d}] ≠ A[{:d}][{:d}][{:d}]".format(typ, a1,a2,a3,b1,b2,b3), end="   ")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3], A[b1][b2][b3]))

print("\nVerifying 'missing' equations....")
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				if A[h][k][j] != A[k][h][j]:
					error(1, h,k,j,   k,h,j)
				if A[h][h][j] != A[k][k][j]:
					error(2, h,h,j,   k,k,j)
				if A[h][j][k] != A[k][j][h]:
					error(3, h,j,k,   k,j,h)
				if A[h][j][h] != A[k][j][k]:
					error(4, h,j,h,   k,j,k)

def error_additive(a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3):
	errorFlag = True
	print("{:d},{:d},{:d} + {:d},{:d},{:d} ≠ {:d},{:d},{:d} + {:d},{:d},{:d}".\
		format(a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3), end="   ")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3] + A[b1][b2][b3], A[c1][c2][c3] + A[d1][d2][d3]))

print("\nVerifying 'additive' constraint....")
for h in range(0, N):
	for k in range(0, N):
		if A[k][k][h] + A[k][h][k] != A[h][k][h] + A[h][h][k]:
			error_additive(k,k,h,  k,h,k,   h,k,h,   h,h,k)

def error_1st(a1,a2,a3, b1,b2,b3):
	errorFlag = True
	print("{:d},{:d},{:d} ≠ {:d},{:d},{:d}".\
		format(a1,a2,a3, b1,b2,b3), end="   ")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3], A[b1][b2][b3]))

print("\nVerifying 1st equation....")
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					if A[k][i][j] != A[h][i][j]:
						error_1st(k,i,j, h,i,j)

if errorFlag:
	print("*** Constraints are not completely satisfied ***")
	exit(1)

debugFlag = False

for i in range(0, 10):				# repeat test 10 times

	x = np.random.rand(N)

	# permute x
	σ = np.random.permutation(N)
	σx = x[σ]

	Y = np.zeros(N)
	Y2 = np.zeros(N)

	for k in range(0, N):
		B_k = A[k].dot(x)
		# print("B_k = ", B_k)
		Y[k] = B_k.dot(x)

		C_k = A[k].dot(σx)
		Y2[k] = C_k.dot(σx)

	σY = Y[σ]					# real answer

	if debugFlag:
		print("\nx   =", x)
		print("σ·x =", σx)
		print("σ   =", σ)
		print("A x x   =", Y)
		print("A σx σx =", Y2)
		print("σ A x x =", σY)

	rms = 0.0					# root mean square error
	for j in range(0, N):
		rms += (Y2[j] - σY[j])**2
	rms = np.sqrt(rms / N)
	print("rms = ", rms)
