# TEST 9 -- symmetric quadratic NN, "colorful" i ≤ j version
# ==========================================================
# This version includes the i ≤ j condition, ie, the commutative xᵢxⱼ = xⱼxᵢ condition is built-in.
# This reduces the number of weights needed to represent the matrices.

import numpy as np

# The matrix A is 3-dimensional
# consisting of N blocks, each of size (N ⨉  N)
# satisfying the "colorful" constraints in my PDF file
# We want to show that this is EQUIVARIANT
# ********* Test result is ??? *********

print("N = ?", end="")
N = int(input())

def find_index(z,x,y):
	return z * N * N + y * N + x

def find_zyx(index):
	z = index // (N * N)
	y = (index % (N * N)) // N
	x = index % N
	return (z,y,x)

# There are N x N x N = N^3 weights in the 3D matrix A,
# but some weights are not used (those for which i ≤ j)
colors = []
for k in range(0, N):
	for j in range(0, N):
		for i in range(0, N):
			if i <= j:
				c = find_index(k,i,j)
				colors.append([c])

print(len(colors), "colors out of", N**3)
print("original colors = ", colors)

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

# =================================
# Remove a color from the 'colors' list
# this means the entire group should be removed
removed_colors = []

def remove_color(c):
	print("remove ", c)
	global colors

	def check(g):
		global removed_colors
		if c in g:
			removed_colors.append(g)
			return False
		else:
			return True

	colors2 = [group for group in colors if check(group)]
	print("colors2 = ", colors2)
	colors = colors2

print("1st equation (BLACK)...")
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			for i in range(0, N):
				if i <= j and i != h and i != k and j != h and j != k:
					left = find_index(h,i,j)
					right = find_index(k,i,j)
					make_same_color(left, right)
print("so far: ", colors)

print("diagonal equations (BLACK)...")
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
print("so far: ", colors)

print("CYAN & OLIVE equations, 1st pair...")
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j > max(h, k):
				# 1 (CYAN)
				left = find_index(h,h,j)
				right = find_index(k,k,j)
				make_same_color(left, right)

				# 2 (OLIVE)
				left = find_index(h,k,j)
				right = find_index(k,h,j)
				make_same_color(left, right)
print("so far: ", colors)

print("RED & BLUE equations, 1st pair...")
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			# (RED)
			if i <= k and i < h:
				left = find_index(h,i,h)
				right = find_index(k,i,k)
				make_same_color(left, right)

			# (BLUE)
			if i <= h and i < k:
				left = find_index(h,i,k)
				right = find_index(k,i,h)
				make_same_color(left, right)
print("so far: ", colors)

print("RED & BLUE equations, 2nd pair...")
for h in range(0, N):
	for k in range(0, N):
		# (RED)
		if k <= h:
			left = find_index(h,k,h)
			right = find_index(k,k,h)
			make_same_color(left, right)

		# (BLUE)
		if h <= k:
			left = find_index(h,h,k)
			right = find_index(k,h,k)
			make_same_color(left, right)
print("so far: ", colors)

print("======= pre-removal ======")

print("CYAN & OLIVE equations, 2nd pair...")
for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			# 1 (CYAN = OLIVE = 0)
			if k >= j and j > h:
				c = find_index(h,h,j)
				remove_color(c)
				c = find_index(k,h,j)
				remove_color(c)

			# 2 (OLIVE = CYAN = 0)
			if h >= j and j > k:
				c = find_index(h,k,j)
				remove_color(c)
				c = find_index(k,k,j)
				remove_color(c)

# ============ fill colors with values =============

A = np.zeros((N, N, N))

for group in colors:
	group.sort()					# sort the colors as well
	β = np.random.rand()
	for index in group:
		(z,y,x) = find_zyx(index)
		A[z][y][x] = β

for group in removed_colors:
	group.sort()					# sort the colors as well
	for index in group:
		(z,y,x) = find_zyx(index)
		A[z][y][x] = 0

print("\nColors = ", colors)
print("\nRemoved colors = ", removed_colors)

print("\nResult: A =\n", A)

print("\n# colors = ", len(colors), " - removed = ", len(removed_colors))

num_colors = len(colors) - len(removed_colors)
print("\n# colors = ", num_colors, "of", N**3, "=", "{:.1f}".format(num_colors * 100.0 / N**3),\
	end="%\n")

exit(0)
# =========== verifications =============

print("\nNumerically counting # colors = ", end="")
numeric_colors = []
for k in range(0, N):
	for i in range(0, N):
		for j in range(0, N):
			a = A[k,i,j]
			matched = False
			for x in numeric_colors:
				if abs(a - x) < 1.0e-14:
					matched = True
			if not matched:
				numeric_colors.append(a)

print(len(numeric_colors))
print(numeric_colors)

num_Errors = 0

print("\nVerifying 'missing' equations....")
def error_missing(typ, a1,a2,a3, b1,b2,b3):
	num_Errors += 1
	print("type {:d}  A[{:d}][{:d}][{:d}] ≠ A[{:d}][{:d}][{:d}]".format(typ, a1,a2,a3,b1,b2,b3),\
		end="   ")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3], A[b1][b2][b3]))

for h in range(0, N):
	for k in range(0, N):
		for j in range(0, N):
			if j != h and j != k:
				if A[h][k][j] != A[k][h][j]:
					error_missing(1, h,k,j,   k,h,j)
				if A[h][h][j] != A[k][k][j]:
					error_missing(2, h,h,j,   k,k,j)
				if A[h][j][k] != A[k][j][h]:
					error_missing(3, h,j,k,   k,j,h)
				if A[h][j][h] != A[k][j][k]:
					error_missing(4, h,j,h,   k,j,k)

print("\nVerifying 'additive' constraint....")

def error_additive(a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3):
	global num_Errors
	num_Errors += 1
	print("{:d},{:d},{:d} + {:d},{:d},{:d} ≠ {:d},{:d},{:d} + {:d},{:d},{:d}".\
		format(a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3), end="   ")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3] + A[b1][b2][b3], A[c1][c2][c3] + A[d1][d2][d3]))

for h in range(0, N):
	for k in range(0, N):
		if A[k][k][h] + A[k][h][k] != A[h][k][h] + A[h][h][k]:
			error_additive(k,k,h,  k,h,k,   h,k,h,   h,h,k)

print("\nVerifying 1st equation....")

def error_1st(a1,a2,a3, b1,b2,b3):
	num_Errors += 1
	print("{:d},{:d},{:d} ≠ {:d},{:d},{:d}".\
		format(a1,a2,a3, b1,b2,b3), end="   ")
	print("{:.5f} ≠ {:.5f}".format(A[a1][a2][a3], A[b1][b2][b3]))

for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					if A[k][i][j] != A[h][i][j]:
						error_1st(k,i,j, h,i,j)

print("\nErrors detected = ", num_Errors)

print("\nTesting....")
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
	print("RMS error = ", rms)
