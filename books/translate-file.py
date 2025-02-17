# -*- coding: utf-8 -*-

# Translate PLAIN text using Google Translate API

# TO-DO:

# DONE:

from subprocess import call, check_output, getoutput
import time
import re
import pyperclip
import sys
from os import path
import asyncio

from googletrans import Translator
translator = Translator(service_urls=['translate.googleapis.com'])

path = '/home/yky/Downloads/french/'
if len(sys.argv) < 2:
	print("usage: translate-plain number OR in-file out-file")
	exit(0)
elif len(sys.argv) == 2:
	f1 = open(path + 'fr' + sys.argv[1] + '.txt', 'r')
	outfile = path + 'b' + sys.argv[1] + '.html'
	print("NOTE: output file =", outfile, end='\n\n')
	f2 = open(outfile, 'w')
else:
	f1 = open(sys.argv[1], 'r')
	f2 = open(sys.argv[2], 'w')

with open("preamble.html") as f0:
	for line in f0:
		f2.write(line)

async def do_it():

	line_num = 0
	in_eqn = False
	last_line = ""

	for line in f1:
		line_num += 1

		# **** skip empty lines
		if re.search("^[\ ]*$", line):
			# print(line, end='')
			# f2.write(line)
			continue

		# **** skip '--'
		if re.search("^--$", line):
			print(line, end='')
			f2.write(line)
			continue

		# **** skip "0c 0a" where 0c = form feed = '\f'
		if re.search("^\f$", line):
			# print(line, end='')
			# f2.write(line)
			continue

		# non-English texts
		# if re.search(u'[\u4e00-\u9fff]', line):
		#	continue

		# **** Pass the line to Google
		translation = await translator.translate(line.rstrip(), src='fr', dest='en')
		# for translation in translations:
		print(translation.origin)
		f2.write("<p class='FR'>" + translation.origin + "</p>\n")
		english = translation.text
		f2.write("<p class='EN'>" + english + "</p>\n")

		translation = await translator.translate(line, src='fr', dest='zh')
		chinese = translation.text
		f2.write("<p class='CN'>" + chinese + "</p><br>\n")

		# print('\x1b[31m⏹ ' + line, end='\x1b[0m\n')
		print('\x1b[33m● ' + english, end='\n\x1b[0m')
		print('\x1b[36m● ' + chinese, end='\n\x1b[0m\n')

		call(["beep", "-l", "50", "-f", "3000", "-n", "-l", "50", "-f", "2500"])

	f1.close()
	f2.write("</body></html>")
	f2.close()

	call(["beep", "-l", "500", "-f", "512"])

asyncio.run(do_it())
