# -*- coding: utf-8 -*-

import sys

f1 = open(sys.argv[1], 'r')
f2 = open('./output/' + sys.argv[1], 'w')

delete = False
for line in f1:
	if "<style>" in line:
		delete = True
		continue
	if "</style>" in line:
		delete = False
		continue
	if "<div style" in line:
		continue
	if "</div>" in line:
		continue
	if delete:
		continue

	f2.write(line)
