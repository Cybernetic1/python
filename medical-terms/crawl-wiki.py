# crawl Wikipedia

# 1. crawl Wikipedia purposefully, given English term
# 2. locate said term in Wikipedia text or entry
# 3. go to Chinese version of same page
# 4. guess corresponding Chinese term based on textual location etc
# 5. validate correspondence, by scoring, how?
# 6. repeat actions

# Scoring:
# 1. if same term occurs in web page title
# 2. if same term occurs sentences that are translations
#		-- how to determine sentence-level translations?

# Simplified version:
# 1. open Wikitionary entry
# 2. get Chinese translation of entry

# Base code is copied from /ime/crawler.py

from BeautifulSoup import BeautifulSoup

import codecs
import requests
from lxml import etree

# Output for Chinese texts
fo = codecs.open("cn-symptoms.txt", "w", "utf-8")

url = "https://en.wikipedia.org/wiki/List_of_medical_symptoms"
print url
r = requests.get(url, stream=True)

index = 0
for line in r.iter_lines():
	#print line

	soup = BeautifulSoup(line)
	#print soup
	a = soup.find("a")							# find HTML anchors
	if not (a is None):
		#print a
		stuff = a.contents
		if len(stuff) > 0:
			index = index + 1
			if index >= 9 and index <= 203:
				print index, stuff[0], a['href']
				fo.write(a['href'])
				fo.write('\n')

fo.close()
