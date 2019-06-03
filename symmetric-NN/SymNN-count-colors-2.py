# Count Colors
# symmetric linear NN, folded in half

import numpy as np

# equation is of the form y = A x, where y is of dimension 1/2 x
# we want to count the number of colors in the (2D) matrix A

# There are 3 x 6 = 18 weights in the 2D matrix A
colors = [[i] for i in range(1,19)]

def find_index(x, y):
	return (x - 1) * 6 + y

# =================================
# find the left color in the list
# find the right color in the list
# join the 2 lists
def make_same_color(left, right):
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

for j in range(1,4):
	for k in range(1,7):
		for i in range(1,7):
			if i != j and i != k:
				left = find_index(j, i)
				right = find_index(k, i)
				print(left, "=", right, end=":   ")
				make_same_color(left, right)

for j in range(1,4):
	for k in range(1,7):
		left = find_index(j, k)
		right = find_index(k, j)
		print(left, "=", right, end=":   ")
		make_same_color(left, right)

		left = find_index(k,k)
		right = find_index(j,j)
		print(left, "=", right, end=":   ")
		make_same_color(left, right)

print("\nresults = ", colors)

print("\n# colors = ", len(colors), end="\n\n")

# Color-print the matrix A
for j in range(1,4):
	for k in range(1,7):
		idx = find_index(j,k)
		for num, c in enumerate(colors):
			if idx in c:
				print(num + 1, end=" ") 
	print()
