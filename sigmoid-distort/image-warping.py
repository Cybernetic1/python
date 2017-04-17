import cv2
import numpy as np
import math
import sys

# img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
rows, cols, _ = img.shape

print "rows = ", rows
print "cols = ", cols

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

for i in range(rows):
	blank = False
	q = rows / (i + 0.5)
	y = -k * math.log(q - 1.0)
	yy = int(y + rows/2.0)
	if yy >= rows:
		blank = True
		# yy = rows - 1
	if yy < 0:
		blank = True
		# yy = 0
	for j in range(cols):
		blank2 = False
		r = cols / (j + 0.00001)
		x = -k * math.log(r - 1.0)
		xx = int(x + cols/2.0)
		if xx >= cols:
			blank2 = True
			# xx = cols - 1
		if xx < 0:
			blank2 = True
			# xx = 0
		if not blank and not blank2:
			img_output[i,j] = img[yy,xx]
		else:
			img_output[i,j] = [255, 255, 255]

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
