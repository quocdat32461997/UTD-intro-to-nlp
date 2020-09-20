"""
program1.py - module to build and train n-gram models
"""

# import dependencies
import os
import re
import nltk
import pickle
import argparse
import numpy as np

def main(args):
	"""
	Read in and build bigram & unigram dictionaries for text files: English, French, Italian
	"""

	# retrieve file paths
	files = [text for text in os.listdir(os.path.join(os.getcwd(), args.files)) if text.startswith('LangId.train')]

	# read text file
	texts = {} 
	for file in files:
		with open(os.path.join(os.getcwd(), args.files, file)) as f:
			texts[file] = f.read() 

	# process and pickle text
	for k, text in texts.items():
		# process text
		ug, bg = text_process(text)	

		# pickle text
		with open(k+'_bg_dict.pickle', 'wb') as file:
			pickle.dump(bg, file)
		with open(k+'_ug_dict.pickle', 'wb') as file:
			pickle.dump(ug, file)


def text_process(text):
	"""
	Process text and build dictionary of bigrams and unigrams
	Inputs:
		- text : given text
	Outputs:
		- unigram_dict : unigram dictionary
		- bigram_dict : bigram dictionary 
	"""

	# remove newlines
	text = re.sub('\n', '', text)

	# tokenize text
	tokens = nltk.word_tokenize(text)

	# create bigram and unigram list
	bigrams = nltk.ngrams(tokens, 2)
	unigrams = nltk.ngrams(tokens, 1)

	# build bigram and unigram dictionary
	bigram_dict = {}
	for bg in bigrams:
		if bg not in bigram_dict:
			bigram_dict[bg] = 1
		else:
			bigram_dict[bg] += 1
	unigram_dict = {}
	for ug in unigrams:
		if ug[0] not in unigram_dict:
			unigram_dict[ug[0]] = 1
		else:
			unigram_dict[ug[0]] += 1

	return unigram_dict, bigram_dict 

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Argument parser to build dictionary")
	parser.add_argument('--files', default = 'homework_4_files', help='Path to directory of text files')
	main(parser.parse_args())
