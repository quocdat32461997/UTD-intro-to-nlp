"""
hw5.py - module for Web Scrapping project
"""

# import dependencies
import os
import requests
import argparse
from bs4 import BeautifulSoup

def main(args):
	# read urls
	with open(args.url_path) as file:
		urls = file.read()

	# iterate thru each url and query html
	for url in urls:
		# web scrape text relevant to given url
		web_scrape(url)
	return None	

def web_scrape(url):
	#query html
	html = requests.get(url)

	# check if request successful or not
	if html.status_code == 200: # valid request
		html = html.content
	else
		exit # if invalid request -> exit

	#

def clean_text(text):
	return None

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Arguments for web-scrapping projects')
	parser.add_argument('--url-path', default = 'urls.txt', type=str)
	main(parser.arg_parse())
