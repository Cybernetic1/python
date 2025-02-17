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
	outfile = path + '/out2.html'
	print("NOTE: output file =", outfile)
	f2 = open(outfile, 'w')
else:
	f1 = open(sys.argv[1], 'r')
	f2 = open(sys.argv[2], 'w')

print("\nDoing it...\n")

line_num = 0
number = None
span = None
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

	if line_num < 85:
		f2.write(line)
		continue

	# **** Extract HTML <p> paragraphs
	soup = BeautifulSoup(line, features="lxml")
	p = soup.find('p')		# find <p> paragraphs
	if p is None:
		f2.write(line)
		continue

	previous = { 'number': number, 'span': span }

	# check if p is a pure number
	if re.fullmatch("[0-9]+", p.text):
		number = int(p.text)
	else:
		number = None

	# check if p is a pure <span>
	span = None
	if len(p.contents) == 1:
		thing = p.contents[0]
		if thing.name == 'span':
			span = thing.text

	# check if p is a <span> + space + number
	elif len(p.contents) == 2:
		thing = p.contents[0]
		if thing.name == 'span':
			span = thing.text
			if p.contents[1].name == None and re.fullmatch("[0-9 ]+", p.contents[1]):
				number = int(p.contents[1])
			else:
				number = None
				span = None
		else:
			span = None
			number = None

	if previous['number'] and span:
		if span == 'The Angel of Grozny' and (previous['number'] != 6 or line_num < 200):
			print('\x1b[31m' + str(line_num), previous['number'], span, '\x1b[0m')
		else:
			print('\x1b[33m' + str(line_num), "****", previous['number'], span, '\x1b[0m')
			f2.write("<p class='Ch'>" + str(previous['number']) + "</p>\n")
			f2.write("<p><span class='Title'>" + span + "</span></p>")
		continue

	if previous['span'] and number:
		print('\x1b[32m' + str(line_num), previous['span'], number, '\x1b[0m')
		continue

	if span and number:
		print('\x1b[32m' + str(line_num), span, number, '\x1b[0m')
		continue

	if previous['span'] and number is None:
		f2.write("<p><span class='italic'>" + previous['span'] + "</span></p>")

	if not number and not span:
		f2.write(line)

	# if span and previous['number'] is None:
	#	f2.write(line)

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
