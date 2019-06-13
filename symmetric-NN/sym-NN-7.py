# TEST 7 -- symmetric quadratic NN, algebraic version
# ===================================================

import numpy as np

# The matrix A is 3-dimensional
# consisting of N blocks, each of size (N ⨉ N)
# satisfying the constraints in my PDF file
# We want to show that this is EQUIVARIANT
# ********* Test result is SUCCESS for all N !!! *********

print("N = ?", end="")
N = int(input())

# There are N x N x N = N^3 weights in the 3D matrix A
colors = [[i] for i in range(0, N **3)]

def find_index(z,y,x):
	return z * N * N + y * N + x

def find_zyx(index):
	z = index // (N * N)
	y = (index % (N * N)) // N
	x = index % N
	return (z,y,x)

# =================================
# find the left color in the list
# find the right color in the list
# join the 2 lists
def make_same_color(left, right):
	print(left, "=", right, end=":   ")
	global colors
	colors2 = []
	temp1 = temp2 = []
	for group in colors:
		if left in group:
			temp1 = group
		elif right in group:
			temp2 = group
		else:
			colors2.append(group)
	temp = temp1 + temp2
	print (temp)
	colors2.append(temp)
	colors = colors2

# 1st equation
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0, N):
				if i != h and i != k and j != h and j != k:
					left = find_index(h,i,j)
					right = find_index(k,i,j)
					make_same_color(left, right)

for h in range(0, N):
	for k in range(0, N):

		# diagonal equation #1
		left = find_index(h,h,h)
		right = find_index(k,k,k)
		make_same_color(left, right)

		# diagonal equation #2
		left = find_index(h,k,k)
		right = find_index(k,h,h)
		make_same_color(left, right)

# "missing" equations
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				# 1
				left = find_index(h,k,j)
				right = find_index(k,h,j)
				make_same_color(left, right)
				
				# 2
				left = find_index(h,h,j)
				right = find_index(k,k,j)
				make_same_color(left, right)

				# 3
				left = find_index(h,j,k)
				right = find_index(k,j,h)
				make_same_color(left, right)

				# 4
				left = find_index(h,j,h)
				right = find_index(k,j,k)
				make_same_color(left, right)

print("\nColors = ", colors)

print("\n# colors = ", len(colors), "of", N**3, "=", "{:.1f}".format(len(colors) * 100.0 / N**3),\
	end="%\n\n")

# ============ fill colors with values =============

A = np.zeros((N, N, N))

for group in colors:
	β = np.random.rand()
	for index in group:
		(z,y,x) = find_zyx(index)
		A[z][y][x] = β

def print_additive(a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3):
	print("{:d},{:d},{:d} + {:d},{:d},{:d} =? {:d},{:d},{:d} + {:d},{:d},{:d}".\
		format(a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3), end="   ")
	print("{:.5f} =? {:.5f}".format(A[a1,a2,a3] + A[b1,b2,b3], A[c1,c2,c3] + A[d1,d2,d3]))

# ============ enforce additive constraints while respecting colors ===============

print("Enforcing 'additive' constraint while respecting colors....")
for h in range(0, N):
	for k in range(0, N):
		if h != k and h < k:
			β = A[k,k,h] = A[h,k,h] + A[h,h,k] - A[k,h,k]

			# all entries of the same color as A[k,k,h] has to be changed as well
			i = find_index(k,k,h)
			for group in colors:
				if i in group:
					for j in group:
						(z,y,x) = find_zyx(j)
						A[z,y,x] = β

print("\nResult: A =\n", A)

# =========== verifications =============

errorFlag = False

def error(typ, a1,a2,a3, b1,b2,b3):
	errorFlag = True
	print("type {:d}  A[{:d}][{:d}][{:d}] ≠ A[{:d}][{:d}][{:d}]".format(typ, a1,a2,a3,b1,b2,b3),\
		end="   ")
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

print("\nTesting....")
debugFlag = True

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
	print("RMS error = ", rms)
