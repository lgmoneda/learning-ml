import re
import unicodedata
import numpy as np
import math

sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A quick brown dog outpaces a quick fox."

def preproc(message):
	"""
	@param message the string to be cleaned from special chars and to lower case 
	@return pre-processed message
	"""
	message = str(message)
	message = message.lower()
	message = unicode(message, "utf-8")
	message = unicodedata.normalize("NFKD", message).encode('ascii', 'ignore').lower().replace(' ', '-')
	message = re.sub("[^a-zA-Z]", " ", message) 
	message = re.sub(" +", " ", message) 
	return message

def build_dict(sentencesList):
	"""
	@param sentencesList a list of setences to build a dictionary from
	@return a dictionary with key = word and value = word_id
	"""
	dictionary = dict()
	for sentence in sentencesList:
		for word in sentence.split():
			if word not in dictionary:
				dictionary[word] = len(dictionary) + 1

	return dictionary

def build_vec(dictionary, sentence):
	"""
	@param dictionary the dictionary we're working with, containing all possible words and its ids
	@param sentence a string to be encoded based on the dictionary
	@return a sparse representation of that setence (a dict)
	"""
	vec = dict()
	for word in sentence.split():
		if dictionary[word] in vec:
			vec[dictionary[word]] += 1
		else:
			vec[dictionary[word]] = 1

	return vec

def dict_to_ndarray(dict1, dict2, dictionary):
	"""
	@param dict1 and dict2 are two sparse representations of setences
	@param dictionary is the dictionary we're working with
	@return the representations in a numpy array form
	"""
	length = len(dictionary)
 	vec1 = np.zeros(length)
	vec2 = np.zeros(length)

	item = 0
	for key, value in dictionary.iteritems():
		vec1[item] = dict1.get(value, 0) 
		vec2[item] = dict2.get(value, 0)
		item += 1

	return (vec1, vec2)

def euclidean_distance(dict1, dict2, dictionary):
	"""
	@param dict1, dict2 two sparse representations
	@param dictionary is the dictionary we're working with
	@return euclidean distance from the two represented sentences
	"""
	vectors = dict_to_ndarray(dict1, dict2, dictionary)
	dif = vectors[0] - vectors[1]
	return math.sqrt(np.dot(dif, dif))


def cosine_distance(dict1, dict2, dictionary):
	"""
	@param dict1, dict2 two sparse representations
	@param dictionary is the dictionary we're working with
	@return dosine distance from the two represented setences
	"""
	vectors = dict_to_ndarray(dict1, dict2, dictionary)
	return 1 - (np.dot(vectors[0], vectors[1])) / (math.sqrt(np.dot(vectors[0], vectors[0])) * math.sqrt(np.dot(vectors[1], vectors[1])))


sentence1 = preproc(sentence1)
sentence2 = preproc(sentence2)

dictionary = build_dict([sentence1, sentence2])

vec1 = build_vec(dictionary, sentence1)
vec2 = build_vec(dictionary, sentence2)

print "Euclidean distance: ",
print "%.3f" % euclidean_distance(vec1, vec2, dictionary)
print "Cosine distance: ",
print "%.3f" % cosine_distance(vec1, vec2, dictionary)