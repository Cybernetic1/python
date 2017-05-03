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
	k = 60.0

for y in range(Y):
	outsideY = False
	y0 = Y / (y + 0.5)
	y1 = -k * math.log(y0 - 1.0)
	y2 = int(y1 + Y/2.0)
	if y2 >= Y or y2 < 0:
		outsideY = True

	for x in range(X):
		outsideX = False
		x0 = X / (x + 0.5)
		x1 = -k * math.log(x0 - 1.0)
		x2 = int(x1 + X/2.0)
		if x2 >= X or x2 < 0:
			outsideX = True
		if not (outsideX or outsideY):
			img_output[y,x] = img[y2,x2]
		else:
			img_output[y,x] = [255, 255, 255]

cv2.imshow('Input', img)
cv2.imshow('Sigmoid distort', img_output)

cv2.imwrite(sys.argv[1][:-4] + "-distort.jpg", img_output)

#####################
# Vertical wave

#img_output = np.zeros(img.shape, dtype=img.dtype)

#for i in range(rows):
    #for j in range(cols):
        #offset_x = int(25.0 * math.sin(2 * 3.14 * i / 180))
        #offset_y = 0
        #if j+offset_x < rows:
            #img_output[i,j] = img[i,(j+offset_x)%cols]
        #else:
            #img_output[i,j] = 0

#cv2.imshow('Input', img)
#cv2.imshow('Vertical wave', img_output)

#####################
# Horizontal wave

#~ img_output = np.zeros(img.shape, dtype=img.dtype)
#~ 
#~ for i in range(rows):
    #~ for j in range(cols):
        #~ offset_x = 0
        #~ offset_y = int(16.0 * math.sin(2 * 3.14 * j / 150))
        #~ if i+offset_y < rows:
            #~ img_output[i,j] = img[(i+offset_y)%rows,j]
        #~ else:
            #~ img_output[i,j] = 0
#~ 
#~ cv2.imshow('Horizontal wave', img_output)

#####################
# Both horizontal and vertical 

#~ img_output = np.zeros(img.shape, dtype=img.dtype)
#~ 
#~ for i in range(rows):
    #~ for j in range(cols):
        #~ offset_x = int(20.0 * math.sin(2 * 3.14 * i / 150))
        #~ offset_y = int(20.0 * math.cos(2 * 3.14 * j / 150))
        #~ if i+offset_y < rows and j+offset_x < cols:
            #~ img_output[i,j] = img[(i+offset_y)%rows,(j+offset_x)%cols]
        #~ else:
            #~ img_output[i,j] = 0
#~ 
#~ cv2.imshow('Multidirectional wave', img_output)

#####################
# Concave effect

#~ img_output = np.zeros(img.shape, dtype=img.dtype)
#~ 
#~ for i in range(rows):
    #~ for j in range(cols):
        #~ offset_x = int(128.0 * math.sin(2 * 3.14 * i / (2*cols)))
        #~ offset_y = 0
        #~ if j+offset_x < cols:
            #~ img_output[i,j] = img[i,(j+offset_x)%cols]
        #~ else:
            #~ img_output[i,j] = 0
#~ 
#~ cv2.imshow('Concave', img_output)

cv2.waitKey()
