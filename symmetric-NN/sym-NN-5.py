# test 5 -- symmetric quadratic NN

import numpy as np

# The matrix A is 3-dimensional,
# consisting of N blocks, each of size (N ⨉ N)
# satisfying the constraints in my PDF file
# We want to show that this is EQUIVARIANT
# ********* Test result is ??? *********

print("N = ?", end="")
N = int(input())

# ======== This takes care of the 2nd and 3rd equations:
A = np.random.rand(N, N, N)
β = np.random.rand()
for i in range(0, N):
	np.fill_diagonal(A[i], np.random.rand())
	A[i][i][i] = β

print("A =\n", A)

def find_index(z,x,y):
	return (z - 1) * N * N + x + (y - 1) * N

# ======== 1st equation:
for h in range(0, N):
	for k in range(0, N):
		for i in range(0, N):
			for j in range(0,  N):
				if i != h and i != k and j != h and j != k:
					# left = find_index(h,i,j)
					# right = find_index(k,i,j)
					# print(left, "=", right, end=":   ")
					# Which value will appear first?
					A[k][i][j] = A[h][i][j]

print("A =\n", A)

# ======== 2nd equation:
for h in range(0, N):
	for k in range(0, N):

		# # 2nd equation
		# left = find_index(h,h,h)
		# right = find_index(k,k,k)
		# print(left, "=", right, end=":   ")
		# make_same_color(left, right)

		# # 3rd equation
		# left = find_index(h,k,k)
		# right = find_index(k,h,h)
		# print(left, "=", right, end=":   ")
		# make_same_color(left, right)

		# 4th equation:
		# left = find_index(k,k,h)
		# right = find_index(k,h,k)
		# print(left, "=", right, end=":   ")
		A[k][k][h] = A[h][k][h] + A[h][h][k] - A[k][h][k]

print("A =\n", A)

x = np.random.rand(N)
print("\nx  =", x)

# permute x
σx = np.random.permutation(x)
print("σ·x =", σx)

Y = np.zeros(N)
σY = np.zeros(N)

for k in range(0, N):
	B_k = A[k].dot(x)
	Y[k] = B_k.dot(x)

	C_k = A[k].dot(σx)
	σY[k] = C_k.dot(σx)

print("\nA x  =", Y)
print("A σx =", σY)
