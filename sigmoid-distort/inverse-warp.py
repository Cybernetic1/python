import cv2
import numpy as np
import math
import sys

# img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
Y, X, _ = img.shape

print "Y = ", Y
print "X = ", X

#####################
# Sigmoid distort by YKY

img_output = np.zeros(img.shape, dtype=img.dtype)

# s0 = 1.0 / (math.exp(rows/2.0) + 1.0)
# s1 = 1.0 / (math.exp(-rows/2.0) + 1.0)
# print s0, s1

try:
	k = float(sys.argv[2])
except:
	k = 80.0

for y2 in range(Y):
	outsideY = False
	y1 = y2 - Y / 2.0
	y0 = math.exp(- y1 / k) + 1.0
	y = int(Y / y0 - 0.5)
	if y >= Y or y < 0:
		outsideY = True

	for x2 in range(X):
		outsideX = False
		x1 = x2 - X / 2.0
		x0 = math.exp(- x1 / k) + 1.0
		x = int(X / x0 - 0.5)
		if x >= X or x < 0:
			outsideX = True
		if not (outsideX or outsideY):
			img_output[y2,x2] = img[y,x]
		else:
			img_output[y2,x2] = [255, 255, 255]

cv2.imshow('Input', img)
cv2.imshow('inverse distort', img_output)

cv2.imwrite(sys.argv[1][:-4] + "-inverse.jpg", img_output)
cv2.waitKey()
