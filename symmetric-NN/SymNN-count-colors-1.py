# symmetric linear NN -- count colors

import numpy as np

# equation is of the form y = A x
# we want to count the number of colors in the (2D) matrix A

# There are 3 x 3 = 9 weights in the 2D matrix A
colors = [[i] for i in range(1,10)]

def find_index(x,y):
	return x + (y - 1) * 3

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
	for k in range(1,4):
		for i in range(1,4):
			if i != j and i != k:
				left = find_index(i,j)
				right = find_index(i,k)
				print(left, "=", right)
				make_same_color(left, right)

for j in range(1,4):
	for k in range(1,4):
		left = find_index(k,j)
		right = find_index(j,k)
		make_same_color(left, right)

		left = find_index(k,k)
		right = find_index(j,j)
		make_same_color(left, right)

print("results = ", colors)

print("# colors = ", len(colors))

# Color-print the matrix A
for j in range(1,4):
	for k in range(1,4):
		if find_index(j,k) in colors[0]:
			print("α ", end="") 
		else:
			print("β ", end="")
	print()
