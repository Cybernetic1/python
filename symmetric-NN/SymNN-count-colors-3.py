# Count Colors
# symmetric quatratic NN

# import numpy as np

# equation is of the form y = <A x, x>
# we want to count the number of colors in the 3D matrix A

print("N = ?", end="")
N = int(input())
# N = 4
N1 = N + 1

# There are N x N x N = N^3 weights in the 3D matrix A
colors = [[i] for i in range(1, N **3 + 1)]

def find_index(z,x,y):
	return (z - 1) * N * N + x + (y - 1) * N

# =================================
# find the left color in the list
# find the right color in the list
# join the 2 lists
def make_same_color(left, right):
	print(left, "=", right, end=":   ")
	global colors
	colors2 = []
	temp1 = temp2 = []
	for c in colors:
		if left in c:
			temp1 = c
		elif right in c:
			temp2 = c
		else:
			colors2.append(c)
	temp = temp1 + temp2
	print (temp)
	colors2.append(temp)
	colors = colors2

# 1st equation
for h in range(1, N1):
	for k in range(1, N1):
		for i in range(1, N1):
			for j in range(1, N1):
				if i != h and i != k and j != h and j != k:
					left = find_index(h,i,j)
					right = find_index(k,i,j)
					make_same_color(left, right)

for h in range(1, N1):
	for k in range(1, N1):

		# diagonal equation #1
		left = find_index(h,h,h)
		right = find_index(k,k,k)
		make_same_color(left, right)

		# diagonal equation #2
		left = find_index(h,k,k)
		right = find_index(k,h,h)
		make_same_color(left, right)

# "missing" equations
for h in range(1, N1):
	for k in range(1, N1):
		for j in range(1, N1):
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

print("\nresults = ", colors)

print("\n# colors = ", len(colors), "of", N**3, "=", "{:.1f}".format(len(colors) * 100.0 / N**3), end="%\n\n")

# Color-print the matrix A
for n in range(1, N1):
	for j in range(1, N1):
		for k in range(1, N1):
			idx = find_index(n,j,k)
			for num, c in enumerate(colors):
				if idx in c:
					print("{:2d}".format(num + 1), end=" ") 
		print()
	print()
