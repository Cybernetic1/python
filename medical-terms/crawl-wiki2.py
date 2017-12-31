# crawl Wikipedia -- stage 2, get Chinese names from list of href's

from BeautifulSoup import BeautifulSoup

import requests
# from lxml import etree, html

# Output for Chinese texts
fo = codecs.open("cn-symptoms.txt", "w", "utf-8")

index = 0
with open("wiki-hrefs.txt") as infile:
	for term in infile:
		term0 = term[:-1]			# kill EOL \n character
		#print term0

		url = "https://en.wikipedia.org" + term0
		index += 1
		print index, url
		r = requests.get(url, stream=True)
		r.encoding = 'utf-8'

		soup = BeautifulSoup(r.content)
		found = False
		divs = soup.findAll("div")			# Chinese link is buried under 2 <div>'s
		for div in divs:
			div2 = div.find("div")
			if not (div2 is None):
				#ul = div2.find("ul")
				li = div2.findAll("li", "interlanguage-link interwiki-zh")
				if len(li) > 0:
					a = li[0].find("a")
					print a['title']
					fo.write(a['title'] + '\n')
					found = True

		if not found:
			fo.write("-\n")

fo.close()
