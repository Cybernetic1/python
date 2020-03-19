import numpy as np
from pywt import dwt, dwtn, idwtn

data = [0] * 200
data[10] = 1
data[73] = -1

(cA, cD) = dwt(data, 'haar')

print("len = ", len(cA), len(cD))
print(cA)
print(cD)

exit(0)

"""
data = [[1,0,0,0], [-1,0,1,0], [0,0,0,1], [0,0,0,-1]]

coeffs = dwtn(data, 'db1')

print(coeffs)

data2 = idwtn(coeffs, 'db1')

print(data2)
"""
