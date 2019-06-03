# Count Colors
# symmetric quatratic NN

import numpy as np

# equation is of the form y = <A x, x>
# we want to count the number of colors in the 3D matrix A

# There are 3 x 3 x 3 = 27 weights in the 3D matrix A
colors = [[i] for i in range(1,28)]

def find_index(z,x,y):
	return (z - 1) * 9 + x + (y - 1) * 3

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

for h in range(1,4):
	for k in range(1,4):
		for i in range(1,4):
			for j in range(1,4):
				if i != h and i != k and j != h and j != k:
					left = find_index(h,i,j)
					right = find_index(k,i,j)
					print(left, "=", right, end=":   ")
					make_same_color(left, right)

for h in range(1,4):
	for k in range(1,4):
		left = find_index(h,h,h)
		right = find_index(k,k,k)
		print(left, "=", right, end=":   ")
		make_same_color(left, right)

		left = find_index(h,k,k)
		right = find_index(k,h,h)
		print(left, "=", right, end=":   ")
		make_same_color(left, right)

		left = find_index(k,k,h)
		right = find_index(k,h,k)
		print(left, "=", right, end=":   ")
		make_same_color(left, right)

		left = find_index(h,k,h)
		right = find_index(h,h,k)
		print(left, "=", right, end=":   ")
		make_same_color(left, right)

		# left = find_index(k,h,k)
		# right = find_index(h,h,k)
		# make_same_color(left, right)

print("\nresults = ", colors)

print("\n# colors = ", len(colors))
