"""
main.py - a module for homework 2
"""

# import dependencies
import argparse
import re
import nltk
import random
from collections import Counter
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.text import Text
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stopwords = stopwords.words()
wnl = WordNetLemmatizer()

def main(args):
    file_path = args.file

    # step 1
    try:
        with open(file_path, 'r') as f:
            text = f.read()
    except:
        print("{} file does not exist or is empty".format(file_path))
        exit()

    # tokenize words
    tokens = word_tokenize(text)

    # step 2: lexical dviersity
    lexical_diversity(tokens)

    # step 3: process text
    tokens, nouns = text_process(text)

    # step 4:
    # build dictionary of tokens and nouns, sort dicts byu count
    word_dict = Counter(tokens)
    word_dict = {k:v for k, v in word_dict.most_common()}
    noun_dict = Counter(nouns)
    noun_dict = {k:v for k, v in noun_dict.most_common()}
    # 50 most common words and their counts
    commons_50 = list(word_dict.keys())[:50]
    print("50 most common words: ")
    for key in commons_50:
        print("Word \"{}\" has count: {}".format(key, word_dict[key]))

    # step 5 :
    # guessing game
    guessing_game(commons_50)

def lexical_diversity(tokens):
    """
    lexical_diversity - function to compute lexical diversity
    Inputs:
        - tokens : list of tokens
    Outputs:
        - None
    """
    # unique tokens
    words = set(tokens)

    # lexical diversity
    lexdiv = len(words) / len(tokens)

    # display result
    print("\nLexical diversity of the given text is {:.2f}".format(lexdiv))

def text_process(text):
    """
    text_process - function to process text
    Inputs:
        - text : text input
    Ouputs:
        - tokens ; list of processed tokens
    """
    # step a
    # tokenize, lowercase tokens and filter tokens less than 5 characters
    tokens = [t.lower() for t in word_tokenize(text) if len(t) > 5]
    # filter non-alpha and stopwords tokens
    tokens = [t for t in tokens if (not t in stopwords) & t.isalpha()]

    # step b
    # lemmatize
    lemmas = [wnl.lemmatize(t) for t in tokens]
    # get unique lemmas
    lemmas = list(set(lemmas))

    # step c
    # do pos-tags for lemmas
    tags = nltk.pos_tag(lemmas)
    print("\nFirst 20 Pos-Tagged lemmas: {}".format(tags[:20]))

    # step d
    # get noun lemmas only
    noun_pattern = "^NN"
    noun_lemmas = [l for l in tags if re.match(noun_pattern, l[-1])]
    # print number of tokens and nouns
    print("\nNumber of tokens: {}. Number of nounds: {}".format(len(tokens), len(noun_lemmas)))

    return tokens, noun_lemmas

def guessing_game(commons50):
    """
    guessing_game - function to run guessing game
    Inputs:
        - commons50 : list of 50 most common words
    Outputs:
    """
    print("\nLey's play a word guessing game")
    score = 5

    # pick randomly in top 50 commons
    pick = random.randint(0, 50)
    word = commons50[pick]
    holders = ['_']*len(word)

    while True:
        print((' ').join(holders)) # print underscores for the word
        # prompt input
        guess = input("Guess a letter: ")

        if guess in word:
            if guess in holders:
                continue
            else:
                score += 1
                print('Right! Score is {}'.format(score))
                for i in range(len(word)):
                    if word[i] == guess:
                        holders[i] = guess
        else:
            score -= 1
            print('Sorry, guess agin. Score is {}'.format(score))

        if score < 0 or guess == '!':
            print("End of game.")
            break
        elif not '_' in holders:
            print('You solved it!')
            print("Current score is: {}".format(score))
            print("Guesss another word")
            pick = random.randint(0, 50)
            word = commons50[pick]
            holders = ['_']*len(word)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Argument Parser")

    parser.add_argument('--file', type = str, default = None, help = 'File name or path to text file')

    main(parser.parse_args())
