import numpy as np
from pywt import dwtn,idwtn

data = [[1,0,0,0], [-1,0,1,0], [0,0,0,1], [0,0,0,-1]]

coeffs = dwtn(data, 'db1')

print(coeffs)

data2 = idwtn(coeffs, 'db1')

print(data2)
