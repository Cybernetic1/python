"""
Plot an illustrative diagram for the paper:
  "Measuring the size of hypothesis spaces from the perspective of No Free Lunch"
where a bunch of attractors are more densely distributed in a region (space B)
"""

import matplotlib.pyplot as plt 
import numpy as np 
import random

fig, ax = plt.subplots(1, 1)

# This is the function that defines 'space B' which is a roundish region
# inside the ambient space: 
def f(x):
	return .03*x**2 - 0.6*x + 10

# First, plot the roundish region = space B
U = np.linspace(0, 50, 256, endpoint=True)
W = f(U)
#W = np.maximum(np.minimum(V, [51]*256), [-1]*256)
#W = np.sin(2*U)
ax.plot(U, W, color='red', alpha=1.0)
ax.fill_between(U, W, 100, color='red', alpha=.2)	# fill with pink color

# Creating 2-D grid of features 
feature_x = np.arange(0, 50, 0.1) 
feature_y = np.arange(0, 50, 0.1) 
[X, Y] = np.meshgrid(feature_x, feature_y) 
# print(X)

i = 0
while i < 50:		# create a number of attractors
	x = random.randint(0,50)
	y = random.randint(0,50)
	# Below is the probability to IGNORE if a point falls outside of region B
	if y < f(x) and random.random() > 0.08:
		continue
	# This is the Gaussian radial basis function
	# the smaller coefficient, the more `spread out' the shape
	z = np.exp(-0.15 * ((X-x)**2 + (Y-y)**2))
	if i == 0:
		Z = z
	else:
		Z += z
	i += 1

# plots contour lines 
ax.contour(X, Y, Z, levels=np.arange(0,6,0.15), linewidths=0.5, colors=['black']) 

ax.set_title('') 
ax.set_xlabel('') 
ax.set_ylabel('')
# ax.axis('off')
ax.set_xticks([])
ax.set_yticks([])

ax.set_xlim((0,50))		# confine the plot to a rectangular region
ax.set_ylim((0,50))

plt.show() 
