# -*- coding: utf-8 -*-

# Translate Latex Chinese file into English using Google Translate web page

# TO-DO:
# * Replace sections
# * Sometimes \textbf, \uline unbalanced

# DONE:
# * use \cc{}{} format
# * the last line \end{document} always missing

from subprocess import call
import time
import re
import pyperclip

f1 = open("../latex/2018/categorical-unification-old.tex", 'r')
f2 = open("../latex/2018/categorical-unification.tex", 'w')

line_num = 0
in_eqn = False
last_line = ""

for line in f1:

	f2.write(last_line)
	last_line = line

	line_num += 1
	if line_num <= 33:
		continue

	if len(line) <= 2:
		continue
	if line[0] == '%':
		continue

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

	if line[0] == '\\' and \
			not (line.startswith("\\textbf{") or \
				line.startswith("\\textit{") or \
				line.startswith("\\uline{")):
		continue

	# pass the line to Google

	# clear text
	call(["xdotool", "mousemove", "504", "283", "click", "3"])
	time.sleep(0.5)

	# paste 上去!
	pyperclip.copy(line)
	call(["xdotool", "mousemove", "60", "301", "click", "3", "key", "ctrl+v"])

	# translate 佢!
	time.sleep(2)

	# copy text
	call(["xdotool", "mousemove", "553", "287", "click", "3", "key", "Tab", "Tab", "Return"])
	time.sleep(1.5)

	# 写鸠佢落file佬!
	translated = pyperclip.paste()

	# 如果好似唔撚掂，停低一阵：
	if re.search(u'[\u4e00-\u9fff]', translated):
		call(["beep"])
		print("Error in this line:")
		print('**** ' + last_line)
		input()
		translated = pyperclip.paste()

	last_line = "\\cc{" + line + "}{\n" + translated + "\n}\n"

	print('● ' + translated)

f2.write(last_line)
f1.close()
f2.close()

call(["beep"])
