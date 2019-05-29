# symmetric quadratic NN

import numpy as np

# The matrix M is of the form:
#	a b c
#	b a d
#	c d a
# test result is that this is NOT equivariant

a = np.random.rand(1)
b = np.random.rand(1)
c = np.random.rand(1)
d = np.random.rand(1)

r1 = np.hstack((a, b, c))
r2 = np.hstack((b, a, d))
r3 = np.hstack((c, d, a))
M = np.vstack((r1,r2,r3))
print("M =\n", M)

x = np.random.rand(3)
print("x  =", x)

# permute x
σx = np.random.permutation(x)
print("σx =", σx)

print()

print("M x  =", x.dot(M))
print("M σx =", σx.dot(M))
