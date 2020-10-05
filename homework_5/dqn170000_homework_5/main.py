"""
hw5.py - module for Web Scrapping project
"""

# import dependencies
import re
import os
import math
import json
import numpy as np
import pandas as pd
import requests
import string
import argparse
import nltk
import pickle
from sqlalchemy import create_engine
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from bs4 import BeautifulSoup

# initialize sql engien
engine = create_engine('sqlite://', echo = False)

def main(args):
	# read urls
	with open(args.url_path) as file:
		urls = file.read()
		urls = urls.split('\n')

	# iterate thru each url and query html
	count = 10
	texts = []
	while urls:
		try:
			print("Count: {}".format(count))
			if count < 1:
				break
			# retrieve the next url
			url = urls.pop(0)
			print(url)

			# web scrape text relevant to given url
			links, text = web_scrape(url)

			# update urls, and text
			urls.extend(links)

			# write raw text
			url = re.sub('[\./:]*', '', url)
			with open(os.path.join(os.getcwd(), args.docs, url+'.txt'), 'w') as file:
				file.writelines('\n' + t for t in text)

			# preprocess text
			text = clean_text(text)
			with open(os.path.join(os.getcwd(), args.kb, url + '.txt'), 'w') as file:
				file.writelines('\n' + t for t in text)
		
			texts.extend(text)
			count -= 1
		except:
			continue

	# build tf-idf dictionary for each token/document and idf dictionary for important words
	tf_idf, idf = term_freq(texts)
	top_terms = sorted(idf.items(), key = lambda x : x[-1], reverse=False)

	# print top 40 terms
	print('Top 40 important terms', top_terms[:40])
	print()

	# build knowledge base 
	kb = create_kb(tf_idf, idf)
	kb.to_csv(args.kb + '.csv') # write knowledge base dataframe

	# convert to sql
	sql_kb = kb.to_sql('knowledge_base', con=engine)

	return None	

def create_kb(tf_idf, idf):
	"""
	create_kb - function to create knowledge base
	Inputs:
		- tf_idf : dictionary of key-doc and values - dictionary of token and its tf-idf score
		- idf : dictionary of key-token and value - idf score
	Output:
		- kb : pandas DataFrame
	"""
	properties = {}

	# fill all tokens to each document
	for doc in tf_idf.keys():
		for token in idf.keys():
			if not token in tf_idf[doc]:
				tf_idf[doc][token] = 0.0
		properties[doc] = list(tf_idf[doc].values())

	return pd.DataFrame.from_dict(properties, orient = 'index', columns = list(idf.keys())) 

def term_freq(inputs):
	"""
	term_freq - function to build frequencey dictionary, find important bi-gram terms, and build knowledge base
	Knowledge base, I define, is the dictionary of keys (bigrams to describe the text) and values (tokens of the text)
	Inputs:
		- inputs : list of String
			List of texts
	Outputs:
		- terms : frequencey dictioanry
		- top_terms : sorted important bigram terms
		- temp_docs : knowledge base as dictionary
	"""

	tf_idf_dict = {} # key - unqiue integer encoding each text, and values are dictionary of {key=token, vales=coutn} 
	idf_dict = {}

	# preprocess text, and build frequency dictionary
	for text, idx in zip(inputs, range(len(inputs))):
		# lowercase
		text = text.lower()

		# remove punctuations
		text = re.sub("[" + string.punctuation+"]*", '', text)
		
		# tokenize words
		tokens = word_tokenize(text)

		# remove stop words
		tokens = [token for token in tokens if not token in stop_words]

		# initialize idx documetn
		tf_idf_dict[idx] = {}

		# compute term-frequency
		for token in tokens:
			if not token in tf_idf_dict[idx]:
				tf_idf_dict[idx][token] = 1
			else:
				tf_idf_dict[idx][token] += 1
			if not token in idf_dict:
				idf_dict[token] = [idx]
			elif not idx in idf_dict[token]:
				idf_dict[token].append(idx)

	
	# comptue inverse-document-frequency
	for token in idf_dict.keys():
		idf_dict[token] = math.log((1 + len(inputs)) / (1 + len(idf_dict[token])))

	# compute tf-idf
	for doc in tf_idf_dict.keys():
		for token in tf_idf_dict[doc].keys():
			tf_idf_dict[doc][token] *= idf_dict[token]
			
	return tf_idf_dict, idf_dict
def web_scrape(url):
	#query html
	html = requests.get(url)

	# check if request successful or not
	if html.status_code == 200:
		html = html.content

	# parse html to soup
	soup = BeautifulSoup(html, 'html.parser')
	
	# find all urls
	urls = []
	for link in soup.find_all('a'):
		l = link.get('href')
		if l and not 'es' in l: 
			l = os.path.join(url, l[1:]) if not l.startswith('https') else l
			urls.append(l)

	return urls, soup.get_text()

def clean_text(text):
	# remove newlines and tabs
	text = re.sub('[\t\n]*', '', text)

	# tokenize sentences
	sents = sent_tokenize(text)

	return sents

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Arguments for web-scrapping projects')
	parser.add_argument('--url-path', default = 'urls.txt', type=str)
	parser.add_argument('--docs', default='texts', type=str)
	parser.add_argument('--kb', default='knowledge_base', type=str)

	main(parser.parse_args())
