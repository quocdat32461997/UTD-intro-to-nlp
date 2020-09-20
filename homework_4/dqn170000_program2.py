"""
program2.py - module to build and train n-gram models
"""

import os
import nltk
import pickle
import argparse
import numpy as np
import program1

def main(args):
	# read dictionary picle files
	files = [file for file in os.listdir(args.files) if file.endswith('.pickle')]
	dicts = {'English' : {}, 'French' : {}, 'Italian' : {}}
	for file in files:
		with open(os.path.join(os.getcwd(), file), 'rb') as f:
			file = file.replace('.pickle', '').split('_')
			lang = file[0][13:]
			dicts[lang][file[1]] = pickle.load(f)

	# read test file
	with open(args.test) as f:
		tests = f.read()
		tests = tests.split('\n') # split by new line

	# results
	results = []
	for idx in range(len(tests)):
		res = compute_prob(tests[idx], dicts)
		results.append(res[0])

	# write language for text
	with open('LangId.result', 'w') as f:
		f.writelines('\n'.join(results))

	# compare solutions and print accuracy
	with open(os.path.join(os.getcwd(), args.sol), 'r') as f:
		solutions = f.read()
		solutions = solutions.split('\n')
		solutions = [sol.split(' ')[1] for sol in solutions]
	wrongs = []
	for idx in range(len(solutions)):
		if solutions[idx] == results[idx]:
			continue
		else:
			wrongs.append(idx)
	print("Accuracy is {}".format(1 - (len(wrongs) / len(solutions))))
	print("Incorrectly classified lines are: {}".format(wrongs))

def compute_prob(text, dicts):
	"""
	Compute probability of the given text
	Inputs:
		- text : text input
		- dicts : dictionaries of bigram and ngram of training data
	Output: 
		- lang : tuple of (language, probability)
	"""
	# build unigram and bigram list
	input_ug, input_bg = program1.text_process(text)
	# vocab size
	vocab_size = sum([len(d['ug']) for d in dicts.values()]) 

	probs = {}
	for lang, v in dicts.items():
		probs[lang] = 1
		bg_dict, ug_dict = v['bg'], v['ug']
		for bg, count in input_bg.items():
			# bigram count
			b = bg_dict[bg] if bg in bg_dict else 0

			# unigram count
			u = ug_dict[bg[0]] if bg[0] in ug_dict else 0

			# Laplace smoothing
			# raise the smoothing probability to the count of bigram 
			probs[lang] *= ((b+1) / (u + vocab_size)) ** count

	# sort probabilities to find the language with the highest probability
	lang = sorted(probs.items(), key = lambda x: x[1], reverse=True)
	return lang[0]
	
			
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Argument parser to build dictionary")
	parser.add_argument('--files', default = '.', help='Path to dictionary picle files')
	parser.add_argument('--test', default='./homework_4_files/LangId.test', help = 'Path to test file')
	parser.add_argument('--sol', default='./homework_4_files/LangId.sol', help = 'Path to solutions')
	main(parser.parse_args())
