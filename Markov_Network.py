###########################################################################
#
# MARKOV CHAIN Network Implementation from Scratch
# -- Built for a WMP KTS --
#
# Author: Sam Showalter
# Date: January 2, 2018
#
###########################################################################

###########################################################################
# Module and library imports 
###########################################################################

#Module and system based packages
import os
import gzip
import sys
import copy
import pickle as pkl

#Random choice and regex packages
import random
import re

#Scientific Computing and stats libraries
from numpy import cumsum
import numpy as np
from operator import itemgetter

###########################################################################
# Class and Constructor
###########################################################################

class Markov_Network():
	'''
	Markov chain class from scratch for NLP. All you 
	have to enter is a filename and the network will
	learn the corpus.

	Attributes:

		filename:			Filename to the text
		corpus:				Cleaned text corpus
		network:			Markov network derived from corpus

	'''
	def __init__(self,
				 filename,
				 corpus = None):

		#Network and filename information
		self.network = {}
		self.filename = filename + ".txt"
		self.corpus = None

		#Temporary word variables to reference
		self.word = ""
		self.new_word = ""

		#Assign corpus if necessary
		if corpus is not None:
			self.corpus = corpus


	###########################################################################
	# Class-specific functions
	###########################################################################

	def clean_corpus(self, regex_string = " +", encoding = "UTF-16"):
		"""
		takes a file and cleans it based on a specific regex
		string and replaces all the matched values with " "

		Args:
			regex_string: 		String that identifies how the corpus
								will be parsed.

		"""

		#Opends the file and reads it
		file = open(self.filename, encoding = encoding)
		file_data = file.read()

		#Replaces the file information with a specific string
		file_data = re.sub(regex_string, " ", file_data).lstrip()
		self.corpus = file_data


	def make_markov_network(self):
		"""
		Creates a markov network by scanning through a corpus of text.

		"""

		# Corpus list variable converts all of the text into tokens
		self.corpus_list = self.corpus.split(" ")

		#Iterates through all of the available tokens, stores the following terms
		for token_index in range(len(self.corpus_list) - 1):

			#Does the token exist
			if self.network.get(self.corpus_list[token_index], None) is not None:

				#Does the succeeding token exist as a value for the key already
				if self.network[self.corpus_list[token_index]].get(self.corpus_list[token_index + 1], None) is not None:
					self.network[self.corpus_list[token_index]][self.corpus_list[token_index + 1]] = self.network[self.corpus_list[token_index]][self.corpus_list[token_index + 1]] + 1
				
				#Succeeding token does not yet exist
				else:
					self.network[self.corpus_list[token_index]][self.corpus_list[token_index + 1]] = 1

			#Token itself does not exist
			else:
				self.network[self.corpus_list[token_index]] = {self.corpus_list[token_index + 1]: 1}

	def make_cum_sum_network(self):
		'''
		Converts a random network with counts into a probabilistic network
		that can function as a full Markov chain. Probabilities for state 
		transfer are determined by the occurrence of different tokens in
		the corpus

		'''

		#Converts the current network into a probabilistic markov chain
		self.prob_network = copy.deepcopy(self.network)

		#Converts counts of each token occurrence into cumsum distributions
		for token in self.prob_network.keys():
			token_dict = self.network[token]
			keys, values = zip(*sorted(token_dict.items(), key=itemgetter(1)))
			self.prob_network[token] = dict(zip(keys, (subtotal / sum(values) for subtotal in cumsum(values))))

	def write_random_story(self, max_length):
		'''
		Write a random story. This Markov network crawl will not
		pay any attention to frequency of occurrence for different
		tokens, it is completely stochastic.

		Args:

			max_length:			Maximum length of the story, in tokens

		'''

		# Initialize story length and choose a random word
		# to add to the story. Initialize a random story string
		story_length = 1
		self.word = random.choice(list(self.network.keys()))
		self.story = self.word + " "

		#Keep adding random tokens in the chain/network until
		#you reach the maximum length
		while story_length < max_length:
			self.new_word = random.choice(list(self.network[self.word].keys()))
			self.story += self.new_word + " "
			self.word = self.new_word
			story_length += 1

	def write_prob_story(self, max_length):
		'''
		Create a story by traversing the Markov network
		while considering the probabilities of transferring
		to different states.

		Args:

			max_length:			Maximum length of a story, in tokens

		'''

		#Initialize story length and story string by choosing
		#a random token to start with
		story_length = 1
		self.word = random.choice(list(self.network.keys()))
		self.story = self.word + " "

		#While the story is under the maximum length
		while story_length < max_length:

			#Get random integer, and make lists of the potential
			#Subsequent tokens and their cumulative probabilities
			rand_num = np.random.rand()
			vals = list(self.prob_network[self.word].values())
			keys = list(self.prob_network[self.word].keys())

			#Choose the appropriate token based on the findings
			#of the cumulative dist function network (vals)
			for index in range(len(vals)):
				if vals[index] >= rand_num:
					self.new_word = keys[index - 1]
					break

			#Add the new word to the network
			self.story += self.new_word + " "
			self.word = self.new_word
			story_length += 1

	

###########################################################################
# Helper Functions (static)
###########################################################################




###########################################################################
# Main method
###########################################################################

if __name__ == '__main__':
	os.chdir(".\\data\\")
	print(os.getcwd())
	print(os.listdir())
	# data = gzip.open("gutenberg-poetry-v001.ndjson.gz")
	# file = data.read()
	# import json

	# all_lines = []
	# for line in gzip.open("gutenberg-poetry-v001.ndjson.gz"):
	# 	all_lines.append(json.loads(line.strip()))

	# big_poem = "\n".join(line['s'] for line in all_lines if re.search(r"\blove\b", line['s'], re.I))

	# model = Markov_Network("test file", corpus = big_poem)
	# model.make_markov_network()

	#model.make_cum_sum_network()
	filename = 'markov_network_gutenberg.pickle'
	model = pkl.load(open(filename, 'rb'))
	model.write_prob_story(100)
	print(model.story)

	#print(poetry(300, ["rupis/" + file for file in os.listdir(os.getcwd()+"/rupis/")]))
	#test = Markov_Network("C:\\Users\\sshowalter\\Desktop\\rupi-kaur-poetry\\rupis\\result")
	# test = Markov_Network("C:\\Users\\sshowalter\\Desktop\\ExcludeFromBackup\\Repos\\Recurrent_Story_Telling\\data\\shakespeare_all")
	
	# test = Markov_Network("C:\\Users\\sshowalter\\Desktop\\plath_neruda")
	# test.clean_corpus()
	# test.make_markov_network()
	# test.make_cum_sum_network()
	# # #print(test.prob_network)
	# test.write_prob_story(200)
	# print()
	# print(test.story)
	# print()
	#print(test.prob_network["to"])
	#print(test.prob_network)
	#print(random.choice(list(test.network.keys())))
	#print(test.corpus_list)






