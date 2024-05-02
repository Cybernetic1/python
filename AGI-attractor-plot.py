import matplotlib.pyplot as plt 
import numpy as np 
import random

fig, ax = plt.subplots(1, 1)

U = np.linspace(0, 50, 256, endpoint=True)

def f(x):
	return .03*x**2 - 0.6*x + 10

W = f(U)
#W = np.maximum(np.minimum(V, [51]*256), [-1]*256)
#W = np.sin(2*U)
ax.plot(U, W, color='red', alpha=1.0)
ax.fill_between(U, W, 100, color='red', alpha=.2)

feature_x = np.arange(0, 50, 0.1) 
feature_y = np.arange(0, 50, 0.1) 
  
# Creating 2-D grid of features 
[X, Y] = np.meshgrid(feature_x, feature_y) 
# print(X)

i = 0
while i < 130:
	x = random.randint(0,50)
	y = random.randint(0,50)
	if y < f(x) and random.random() > 0.03:
		continue
	z = np.exp(-0.6 * ((X-x)**2 + (Y-y)**2))
	if i == 0:
		Z = z
	else:
		Z += z
	i += 1

# plots contour lines 
ax.contour(X, Y, Z, levels=np.arange(0,6,0.15), linewidths=0.4) 

ax.set_title('') 
ax.set_xlabel('') 
ax.set_ylabel('')
# ax.axis('off')
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim((0,50))
ax.set_ylim((0,50))

plt.show() 
