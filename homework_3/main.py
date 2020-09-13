"""
main.py - main module for homework_3
"""
import os
import re
import argparse
import nltk
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()
stopwords = stopwords.words('english') # get list of stop words

def main(args):
    """
    main - function to execute homework-3
    """
    # step 1
    with open(args.file, 'r') as file:
        text = file.read()

    # step 2
    text = text_process(text)
    print()

    # step 3
    tokens = word_tokenize(text)
    print("Number of tokens", len(tokens))
    print()

    # step 4
    distinct_tokens = set(tokens)
    print("Number of distinct tokens", len(distinct_tokens))
    print()

    # step 5
    important_tokens = [token for token in distinct_tokens if not token in stopwords]
    print("Number of important tokens", len(important_tokens))
    print()

    # step 6
    stems = [(w, stemmer.stem(w)) for w in important_tokens]
    print("Top 5 stemmed tuples", stems[:5])
    print()

    # step 7
    stem_dict = {}
    for item in stems:
        if not item[1] in stem_dict.keys():
            # initialize list of relevant words to stem key
            stem_dict[item[1]] = [item[0]]
        else:
            # add a relevant word to list of stem key
            stem_dict[item[1]].append(item[0])
    key = list(stem_dict.keys())[0]
    print("Stemmed dictionary {}:{}".format(key, stem_dict[key]))
    print()

    # step 8
    print("Stemmed Dictionary has {} keys and {} values".format(len(stem_dict), sum(len(v) for v in stem_dict.values())))
    print()

    # step 9
    # sort by length
    sorted_list = sorted(stem_dict, key=lambda k: len(stem_dict[k]), reverse = True)
    print("List of 25 Stems which have longest list of stemmed words")
    for idx in range(25):
        print("Stem {} - List {}".format(sorted_list[idx], stem_dict[sorted_list[idx]]))
    print()

    # step 10
    # compute edit_distance with "continue" and "continu"
    for word in stem_dict['continu']:
        print("Edit distance between continue and {}: {}".format(word, levenshtein_distance("continue", word)))
    print()

    # step 11
    pos_tags = nltk.pos_tag(tokens) # assign POS Tags

    # step 12
    pos_dict = {}
    for _, tag in pos_tags:
        if not tag in pos_dict.keys():
            pos_dict[tag] = 1
        else:
            pos_dict[tag] += 1
    print("Dictionary of POS Tag", pos_dict)

def levenshtein_distance(source, target):
    """
    levenshtein_distance - function to compute evenshtein_distance or edit_distance
    Inputs:
        -- source : string
                Source text to compare with target text
        -- target : string
                Target text to be compared with source text
    Outputs:
        -- _ : integer
            Final/shortest edit distance
    """
    # declare zero-filled matrix of source x target
    matrix = np.zeros([len(source) + 1, len(target) + 1])

    # add default cost
    # dropping characters into empty string
    matrix[0, :] = range(len(target) + 1)
    # inserting characters into empty string
    matrix[:, 0] = range(len(source) + 1)

    # fill substitution cost
    for i in range(1, len(source) + 1):
        for j in range(1, len(target) + 1):
            if source[i-1] == target[j-1]: # if same character, ignore
                substitution_cost = 0
            else: # if different character, add cost by 1
                substitution_cost = 1

            # compute cost
            matrix[i, j] = min(matrix[i-1, j] + 1, # delete a character of source to target
                                matrix[i, j-1] + 1, # insert a charcter of source to target
                                matrix[i-1, j-1] + substitution_cost) # substitution
    return matrix[-1, -1] # get the final distance

def text_process(inputs):
    """
    text_process - function to process text following rules:
        * lower case
        * replace all '--' with ''
        * remove all digits
        * replace punctuation with a single space
    Inputs:
        -- input : text/corpus
    Outputs:
        -- TBD  : processed text
    """

    # lower case
    inputs = inputs.lower()

    # replace all '--' with ''
    inputs = re.sub('--', '', inputs)

    # remove all digits
    inputs = re.sub('[\d]*', '', inputs)

    # remove punctuations
    inputs = re.sub("[!&^*,./;:\"\\\[\]\{\}\(\)\''\`\-\_\?\<\>\$]", ' ', inputs)

    return inputs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Argument Parser from command lines')
    parser.add_argument('--file', type=str, default = 'moby_dick.txt')
    main(parser.parse_args())
