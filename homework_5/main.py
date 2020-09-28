"""
hw5.py - module for Web Scrapping project
"""

# import dependencies
import re
import os
import json
import requests
import argparse
from nltk import word_tokenize
from bs4 import BeautifulSoup

def main(args):
	# read urls
	with open(args.url_path) as file:
		urls = file.read()
		urls = urls.split('\n')

	# iterate thru each url and query html
	count = 15
	while urls:
		if count < 1:
			break
		try:
			# retrieve the next url
			url = urls.pop(0)
			# web scrape text relevant to given url
			urls, text = web_scrape(url)

			# write text
			url = re.sub('[\./:]+', '', url)
			with open(os.path.join(os.getcwd(), docs, url+'.txt'), 'w') as file:
				file.writelines('\n' + t for t in text)
			count -= 1
		except:
			continue
	return None	

def web_scrape(url):
	#query html
	html = requests.get(url)

	# check if request successful or not
	if html.status_code == 200: # valid request
		html = html.content
	else:
		exit # if invalid request -> exit

	# parse html to soup
	soup = BeautifulSoup(html, 'html.parser')

	# find all urls
	urls = []
	for link in soup.find_all('a'):
		l = link.get('href')
		if not l:
			l = os.path.join(url, l[1:]) if not l.startswith('https') else l
			urls.append(l)

	# extract all text
	text = clean_text(soup.get_text())

	return urls, text
def clean_text(text):
	# tokenize sentences
	sents = sent_tokenize(text)

	sents = [re.sub('[\n\t]+', '', sent) for sent in sents]
	return sents

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Arguments for web-scrapping projects')
	parser.add_argument('--url-path', default = 'urls.txt', type=str)
	parser.add_argument('--docs', default='texts', type=str)
	main(parser.parse_args())
