# -*- coding: utf-8 -*-

# Translate PLAIN text using Google Translate web page

# TO-DO:

# DONE:

from subprocess import call, check_output, getoutput
import time
import re
import pyperclip
import sys
from os import path
import mss			# for screen capture
import numpy		# for analyzing image
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
	print("usage: translate-plain in-file [out-file]")
	exit(0)
elif len(sys.argv) == 2:
	f1 = open(sys.argv[1], 'r')
	path = path.dirname(sys.argv[1])
	outfile = path + '/chingchong.txt'
	print("NOTE: output file =", outfile)
	f2 = open(outfile, 'w')
else:
	f1 = open(sys.argv[1], 'r')
	f2 = open(sys.argv[2], 'w')

print("\nSetting terminal to be always on top...")
call(['wmctrl', '-r', ':ACTIVE:', '-b', 'add,above'])

print("\n**** 建议你一定要去 Google Translate 的正式网站！")
print("**** Edit near the beginning of 'for' loop to skip lines!\n")

# **** Read mouse positions
print("首先, 噤 NumLock ON 先!")
input("郁燃隻 mouse屎 去 clear text 果度，然後噤 enter！")
out = check_output(["xdotool", "getmouselocation"]).decode('utf-8')
x_clear = out[out.index('x:') +2 : out.index(' y:')]
y_clear = out[out.index('y:') +2 : out.index(' screen:')]
print("X, Y =", x_clear, y_clear)

input("郁燃隻 mouse屎 去左邊 paste 嘅位置，然後噤 enter！")
out = check_output(["xdotool", "getmouselocation"]).decode('utf-8')
x_paste = out[out.index('x:') +2 : out.index(' y:')]
y_paste = out[out.index('y:') +2 : out.index(' screen:')]
print("X, Y =", x_paste, y_paste)

input("郁燃隻 mouse屎 去右邊 window（但並不是 copy 的位置，因爲佢會變），然後噤 enter！")
out = check_output(["xdotool", "getmouselocation"]).decode('utf-8')
x_copy = out[out.index('x:') +2 : out.index(' y:')]
y_copy = out[out.index('y:') +2 : out.index(' screen:')]
print("X, Y =", x_copy, y_copy)

print("\n開始 翻譯！！ --- 注意： 可以噤 Num Lock = off 停止！！\n")

line_num = 0
in_eqn = False
last_line = ""

for line in f1:
	line_num += 1

	# **** skip empty lines
	if re.search("^[\ ]*$", line):
		print(line, end='')
		f2.write(line)
		continue

	# non-English texts
	# if re.search(u'[\u4e00-\u9fff]', line):
	#	continue

	# **** Pass the line to Google

	# scroll to page's top, clear text
	call(["xdotool", "mousemove", "162", "459", "key", "Home", "sleep", "1", "mousemove", x_clear, y_clear, "click", "1"])
	time.sleep(1)

	# paste 上去!
	pyperclip.copy(line)
	call(["xdotool", "mousemove", x_paste, y_paste, "click", "1", "key", "ctrl+v"])

	# translate 佢!
	time.sleep(2)

	# check the "star" icon on the right, see if it is grey
	with mss.mss() as sct:
		monitor = {'top':301, 'left':1554, 'width':64, 'height':64}
		img = numpy.array(sct.grab(monitor))
		m1 = numpy.average(img, axis=0)
		m2 = numpy.average(m1, axis=0)
		# print("average=", m2)
		if numpy.greater(m2, numpy.array([245.0, 245.0, 245.0, 245.0])).all():
			# 2 tabs are needed, otherwise 3 tabs
			tabs = ["Tab", "Tab", "Return"]
		else:
			tabs = ["Tab", "Tab", "Tab", "Return"]

	# copy text
	call(["xdotool", "mousemove", x_copy, y_copy, "click", "1", "key"] + tabs)
	time.sleep(2)

	# 写鸠佢落file佬!
	translated = pyperclip.paste()

	# 如果好似唔撚掂，停低一阵：
	"""
	if re.search(u'[\u4e00-\u9fff]', translated):
		call(["beep", "-l", "500", "-f", "512"])
		print("Error in this line:")
		print('**** ' + last_line)
		input("你可以自己手動翻譯....")
		translated = pyperclip.paste()
	"""

	f2.write(translated + "\n")

	# print('\x1b[31m⏹ ' + line, end='\x1b[0m\n')
	print('\x1b[33m● ' + translated, end='\n\x1b[0m\n')
	call(["beep", "-l", "50", "-f", "3000", "-n", "-l", "50", "-f", "2500"])

	numLock = getoutput("xset q | grep Caps | tr -s ' ' | cut -d ' ' -f 9")
	if numLock == 'off':
		break

f1.close()
f2.close()

call(["beep", "-l", "500", "-f", "512"])

print("\nSetting terminal to be normal...")
call(['wmctrl', '-r', ':ACTIVE:', '-b', 'remove,above'])
