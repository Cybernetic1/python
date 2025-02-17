# -*- coding: utf-8 -*-

# reformat ePub HTML, with Beautiful Soup
# Some lines are specifically for ePub format.
# When finished, use this to re-pack the ePub file:
#     zip -rX ../my.epub mimetype . META-INF/ OEBPS/ ...

# TO-DO:
# * find <p>[0-9]+</p> <p><span class="italic">The Little Wolf</span></p>
# * find <span>'s after <p>[number]

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
	print("usage: reformat-ePub in-file [out-file]")
	exit(0)
elif len(sys.argv) == 2:
	f1 = open(sys.argv[1], 'r')
	path = path.dirname(sys.argv[1])
	outfile = path + '/out.html'
	print("NOTE: output file =", outfile)
	f2 = open(outfile, 'w')
else:
	f1 = open(sys.argv[1], 'r')
	f2 = open(sys.argv[2], 'w')

print("\nDoing it...\n")

line_num = 0
number = ""
inside = False
last_line = ""

"""  Skip HTML tags
"""

for line in f1:
	line_num += 1

	# **** skip empty lines
	if re.search("^[\ ]*$", line):
		print(line, end='')
		f2.write(line)
		continue

	# **** Extract HTML <p> paragraphs
	soup = BeautifulSoup(line, features="lxml")
	p = soup.find('p')		# find <p> paragraphs
	if p is None:
		f2.write(line)
		continue

	# check if p.text is a pure number
	if re.fullmatch("[0-9]+", p.text):
		inside = True
		number = p.text
		continue

	# check for a <p> with an only <span "italic"> inside
	thing = p.contents[0] if len(p.contents) == 1 else None
	if inside and thing and thing.name == 'span':
		if thing.text == "The Angel of Grozny" and line_num != 892:
			print('\x1b[31m' + str(line_num) + '\x1b[0m', number, thing.text)
			inside = False
			continue
		else:			# This is a real chapter
			f2.write("<p class='Ch'>" + number + "</p>\n")
	elif thing and thing.name != 'span':
		f2.write("<p>" + number + "</p>\n")
	f2.write(line)
	inside = False

	# extract <a> tags, append them afterwards
	# tags = soup.find_all('a')
	# print("<a>s =", len(tags))
	# print("tags =", len(soup.find_all()))

	# non-English texts
	# if re.search(u'[\u4e00-\u9fff]', line):
	#	continue

	# **** Pass the line to Google

	# 如果好似唔撚掂，停低一阵：
	"""
	if re.search(u'[\u4e00-\u9fff]', translated):
		call(["beep", "-l", "500", "-f", "512"])
		print("Error in this line:")
		print('**** ' + last_line)
		input("你可以自己手動翻譯....")
		translated = pyperclip.paste()
	"""

	#	call(["beep", "-l", "100", "-f", "512"])

	# print('\x1b[31m⏹ ' + line, end='\x1b[0m\n')
	# print('\x1b[33m● ' + p.text, end='\n\x1b[0m\n')
	# call(["beep", "-l", "50", "-f", "3000", "-n", "-l", "50", "-f", "2500"])

f1.close()
f2.close()

call(["beep", "-l", "500", "-f", "512"])
