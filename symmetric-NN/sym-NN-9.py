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

def find_zxy(index):
	z = index // (N * N)
	y = (index % (N * N)) // N
	x = index % N
	return (z,x,y)

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

print("Colorful equations...")
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):

			if h < k:
				# 1 (CYAN in CYAN)
				if i > k:
					left = find_index(k,k,i)
					right = find_index(h,h,i)
					make_same_color(left, right)

				# 2 (OLIVE in OLIVE)
				if i > k:
					left = find_index(k,h,i)
					right = find_index(h,k,i)
					make_same_color(left, right)

				# 3 (RED in RED)
				if i < h:
					left = find_index(k,i,k)
					right = find_index(h,i,h)
					make_same_color(left, right)

				# 4 (BLUE in BLUE)
				if i < h:
					left = find_index(k,i,h)
					right = find_index(h,i,k)
					make_same_color(left, right)

				# 5 (RED in CYAN)
				if h < i and i < k:
					left = find_index(k,i,k)
					right = find_index(h,h,i)
					make_same_color(left, right)

				# 6 (OLIVE in BLUE)
				if h < i and i < k:
					left = find_index(k,h,i)
					right = find_index(h,i,k)
					make_same_color(left, right)

			elif k < h:
				# 1 (CYAN in CYAN)
				if i > h:
					left = find_index(k,k,i)
					right = find_index(h,h,i)
					make_same_color(left, right)

				# 2 (OLIVE in OLIVE)
				if i > h:
					left = find_index(k,h,i)
					right = find_index(h,k,i)
					make_same_color(left, right)

				# 3 (RED in RED)
				if i < k:
					left = find_index(k,i,k)
					right = find_index(h,i,h)
					make_same_color(left, right)

				# 4 (BLUE in BLUE)
				if i < k:
					left = find_index(k,i,h)
					right = find_index(h,i,k)
					make_same_color(left, right)

				# 5 (CYAN in RED)
				if k < i and i < h:
					left = find_index(k,k,i)
					right = find_index(h,i,h)
					make_same_color(left, right)

				# 6 (BLUE in OLIVE)
				if k < i and i < h:
					left = find_index(k,i,h)
					right = find_index(h,k,i)
					make_same_color(left, right)
print("so far: ", colors)

# ============ fill colors with values =============

A = np.zeros((N, N, N))

for group in colors:
	group.sort()					# sort the colors as well
	β = np.random.rand()
	for index in group:
		(z,x,y) = find_zxy(index)
		A[z][x][y] = β

for group in removed_colors:
	group.sort()					# sort the colors as well
	for index in group:
		(z,x,y) = find_zxy(index)
		A[z][x][y] = 0

print("\nColors = ", colors)

print("\nResult: A =\n", A)

print("\n# colors = ", len(colors))

num_colors = len(colors)
print("\n# colors = ", num_colors, "of", N**3, "=", "{:.1f}".format(num_colors * 100.0 / N**3),\
	end="%\n")

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

print("\nTesting....")
debugFlag = False

for t in range(0, 10):				# repeat test 10 times

	x = np.random.rand(N)

	# permute x
	σ = np.random.permutation(N)
	σx = x[σ]

	Y = np.zeros(N)
	Y2 = np.zeros(N)

	for k in range(0, N):
		Σ = 0.0
		for j in range(0, N):
			for i in range(0, N):
				if i <= j:
					Σ += A[k][j][i] * x[i] * x[j]
		Y[k] = Σ

		Σ = 0.0
		for j in range(0, N):
			for i in range(0, N):
				if i <= j:
					Σ += A[k][j][i] * σx[i] * σx[j]
		Y2[k] = Σ

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
