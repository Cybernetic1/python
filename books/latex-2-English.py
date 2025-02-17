# -*- coding: utf-8 -*-

# Translate Latex Chinese file into English using Google Translate web page

# TO-DO:
# * Replace sections
# * Sometimes \textbf, \uline unbalanced

# DONE:
# * use \cc{}{} format
# * the last line \end{document} always missing

from subprocess import call, check_output, getoutput
import time
import re
import pyperclip
import sys
from os import path

print("\n**** 建议你一定要去 Google Translate 的正式网站！")
print("**** 注意 terminal window 不要遮住 Translation column")
print("**** Your NumLock will be automatically set to ON.")
print("**** Edit near the beginning of 'for' loop to skip lines!\n")

if len(sys.argv) < 2:
	print("usage: latex-2-English in-file [out-file]")
	exit(0)
elif len(sys.argv) == 2:
	f1 = open(sys.argv[1], 'r')
	path = path.dirname(sys.argv[1])
	outfile = path + '/english.tex'
	print("NOTE: output file =", outfile)
	f2 = open(outfile, 'w')
else:
	f1 = open(sys.argv[1], 'r')
	f2 = open(sys.argv[2], 'w')

print("\nSetting terminal to be always on top...")
call(['wmctrl', '-r', ':ACTIVE:', '-b', 'add,above'])

# **** Read mouse positions
input("郁燃隻 mouse屎 去左边 clear text ❎ 果度，然後噤 enter！")
out = check_output(["xdotool", "getmouselocation"]).decode('utf-8')
x_clear = out[out.index('x:') +2 : out.index(' y:')]
y_clear = out[out.index('y:') +2 : out.index(' screen:')]
print("X, Y =", x_clear, y_clear)

input("郁燃隻 mouse屎 去左边 paste 嘅位置，然後噤 enter！")
out = check_output(["xdotool", "getmouselocation"]).decode('utf-8')
x_paste = out[out.index('x:') +2 : out.index(' y:')]
y_paste = out[out.index('y:') +2 : out.index(' screen:')]
print("X, Y =", x_paste, y_paste)

input("郁燃隻 mouse屎 去右邊 window 嘅邊緣（但並不是 “copy” icon 的位置，因爲佢會變），然後噤 enter！")
out = check_output(["xdotool", "getmouselocation"]).decode('utf-8')
x_copy = out[out.index('x:') +2 : out.index(' y:')]
y_copy = out[out.index('y:') +2 : out.index(' screen:')]
print("X, Y =", x_copy, y_copy)

call(["numlockx", "on"])
print("\n開始 翻譯！！ --- 注意： 可以噤 Num Lock = off 停止！！\n")

line_num = 0
in_eqn = False
last_line = ""

for line in f1:
	line_num += 1

	# skip beginning lines, comment out if not needed
	if line_num < 90 or \
	   line_num > 10000:
		continue

	f2.write(last_line)
	last_line = line

	if len(line) <= 2:			# line too short
		continue
	if line[0] == '%':			# line starts with comment
		continue

	# **** Skip inside of equations

	if line.startswith("\\end{eq") or \
			line.startswith("\\end{verbatim}"):
		in_eqn = False
		continue

	if in_eqn:
		continue

	if line.startswith("\\begin{eq") or \
			line.startswith("\\begin{verbatim}"):
		in_eqn = True
		continue

	# **** Skip possibly latex commands

	line2 = line.lstrip()
	if len(line2) < 3:
		continue
	if line2[0] == '\\' and not ( \
			line2.startswith("\\textbf{") or \
			line2.startswith("\\textit{") or \
			line2.startswith("\\item") or \
			line2.startswith("\\uline{") ):
		continue

	# **** Skip lines that have no Chinese
	if not re.search(u'[\u4e00-\u9fff]', line):
		continue

	# **** Pass the line to Google

	# clear text
	call(["xdotool", "mousemove", x_clear, y_clear, "click", "1"])
	time.sleep(0.5)

	# paste 上去!
	pyperclip.copy(line)
	call(["xdotool", "mousemove", x_paste, y_paste, "click", "1", "key", "ctrl+v"])

	# translate 佢!
	time.sleep(2)

	# copy text
	call(["xdotool", "mousemove", x_copy, y_copy, "click", "1", "key", "Tab", "Tab", "Tab", "Return"])
	time.sleep(1.5)

	# 写鸠佢落file佬!
	translated = pyperclip.paste()

	# 如果好似唔撚掂，停低一阵：
	if re.search(u'[\u4e00-\u9fff]', translated):
		call(["beep", "-l", "500", "-f", "512"])
		print("Error in this line:")
		print('**** ' + last_line)
		input("你可以自己手動翻譯，将文本放在剪贴板内 ....")
		translated = pyperclip.paste()

	last_line = "\\cc{" + line + "}{\n" + translated + "\n}\n"

	print('\x1b[31m⏹ ' + line, end='\x1b[0m\n')
	print('\x1b[32m● ' + translated, end='\n\x1b[0m\n')
	call(["beep", "-l", "50", "-f", "3000", "-n", "-l", "50", "-f", "2500"])

	numLock = getoutput("xset q | grep 'Num Lock' | tr -s ' ' | cut -d ' ' -f 9")
	if numLock == 'off':
		break

f2.write(last_line)
f1.close()
f2.close()

call(["beep", "-l", "500", "-f", "512"])

print("\nSetting terminal window to be normal...")
call(['wmctrl', '-r', ':ACTIVE:', '-b', 'remove,above'])

print("\nSetting Num Lock back to OFF...")
call(["numlockx", "on"])
