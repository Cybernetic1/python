# -*- coding: utf-8 -*-

import math

x = 4557.88

for i in range(0, 100):
	print(i, ":",  x)
	oldx = x
	x = math.cos(x)
	if oldx == x:
		print("no change!!!")

print("Finished!")
