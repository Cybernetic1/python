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
# from bs4 import BeautifulSoup
import asyncio

print("\n開始 翻譯！！ --- 注意： 可以噤 Num Lock = off 停止！！\n")

from googletrans import Translator
translator = Translator(service_urls=['translate.googleapis.com'])

async def do_it():
	
	for d in range(95,119):
		f1 = open(f"/home/yky/Downloads/french/out{d:03d}.txt", 'r')
		f2 = open(f"/home/yky/Downloads/french/a{d:03d}.txt", 'w')
		print("****** Processing out{d:03d}.txt ...")

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

			# pyperclip.copy(line)

			# translate 佢!

			# check the "star" icon on the right, see if it is grey

			# copy text
			time.sleep(2)

			# 写鸠佢落file佬!
			# translated = pyperclip.paste()

			# 如果好似唔撚掂，停低一阵：
			"""
			if re.search(u'[\u4e00-\u9fff]', translated):
				call(["beep", "-l", "500", "-f", "512"])
				print("Error in this line:")
				print('**** ' + last_line)
				input("你可以自己手動翻譯....")
				translated = pyperclip.paste()
			"""

			translation = await translator.translate(line, src='fr', dest='en')
			# for translation in translations:
			print(translation.origin, '->', translation.text)
			f2.write(translation.text + "\n")

			# print('\x1b[31m⏹ ' + line, end='\x1b[0m\n')
			print('\x1b[33m● ' + translation.text, end='\n\x1b[0m\n')
			call(["beep", "-l", "50", "-f", "3000", "-n", "-l", "50", "-f", "2500"])

			numLock = getoutput("xset q | grep Caps | tr -s ' ' | cut -d ' ' -f 9")
			if numLock == 'off':
				break

		f1.close()
		f2.close()

		call(["beep", "-l", "500", "-f", "512"])

	print("\nSetting terminal to be normal...")
	# call(['wmctrl', '-r', ':ACTIVE:', '-b', 'remove,above'])

asyncio.run(do_it())
