import cv2
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

# **** Print list of screenshot files sorted by time
import glob
path = input("Image path [/home/yky/Pictures/]: ") or '/home/yky/Pictures/'
prefix = input("Image prefix [Screenshot from ]: ") or 'Screenshot from '
files = glob.glob(path + prefix + "*.png")
files.sort()
for i, fname in enumerate(files):
	if i % 2:
		print(end="\x1b[7;32m")
	else:
		print(end="\x1b[0m")
	print("%2d %s" %(i, fname[len(prefix):]))
print(end="\x1b[0m")
seq = list(map(int, input("Enter file sequence [eg. 4,5,6,7]: ").split(',')))
print()

# **** Find the positions to stitch the images
rowses = []				# the heights of each image
bottoms = []			# the "skipped" amount for each image
img1 = None
for i in seq:
	img2 = cv2.imread(files[i])
	print("filename =", files[i])
	if img1 is None:
		img1 = img2
		rows1, cols1, _ = img1.shape
		print("img1 size = %d x %d"% (rows1, cols1))
		rowses.append(rows1)
		bottoms.append(0)
		continue
	
	if img1.shape[1] != img2.shape[1]:
		print("images are different widths")
		exit(0)

	rows2, cols2, _ = img2.shape
	print("\timg2 size = %d x %d"% (rows2, cols2))
	rowses.append(rows2)

	# **** This is the "matching template"
	# which is created from the last 15 rows of img1
	# the left and right 10 pixels are cut off to allow for edge align error
	tmp = img1[(rows1 - 15) : rows1, 10 : cols1 - 10]		# format: [y1:y2, x1:x2]
	h, w, _ = tmp.shape
	print("\tmatching template size = %d x %d"% (h, w))

	img = img2.copy()					# a copy of the image, for display

	# **** Use OpenCV's template matching function.  Please refer to its documentation.
	method = eval('cv2.TM_CCOEFF')		# 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED'
	res = cv2.matchTemplate(img2, tmp, method)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)			# Pick the best match
	# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
	if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
		top_left = min_loc
	else:
		top_left = max_loc
	bottom_right = (top_left[0] + w, top_left[1] + h)
	cv2.rectangle(img, top_left, bottom_right, 255, 2)		# draw the found region in red
	bottom = bottom_right[1]
	print("\tFound: bottom location =", bottom)
	if bottom >= 100:
		bottom = 0
		print("\t**** Position too low, bottom assumed = 0")
	bottoms.append(bottom)									# keep a record of it

	# **** Show the aligned image in a new window
	# plt.subplot(121),plt.imshow(res, cmap = 'gray')
	# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
	plt.imshow(img, cmap = 'gray')
	plt.title('Detected fragment'), plt.xticks([]), plt.yticks([])
	plt.show()
	
	img1 = img2				# Let img1 := current image; repeat
	rows1 = rows2
	cols1 = cols2

# **** Finally, combine images together:
# create empty matrix:
scroll = np.zeros((sum(rowses) - sum(bottoms), cols1, 3), np.uint8)

rows1 = 0
for (i, rows, bottom) in zip(seq, rowses, bottoms):
	img = cv2.imread(files[i])
	scroll[rows1 : rows1 + rows - bottom, :cols1, :3] = img[bottom : rows, 0 : cols1]
	rows1 += rows - bottom

cv2.imwrite(path + "scroll.png", scroll)
print("\nResult written to `scroll.png`, bye.")
