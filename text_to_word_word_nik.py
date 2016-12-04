# Phase 1 project megalearner: text to  word, data analysis pipe 1 (preprocessing)
# Author  : Javier Rey <jreyro@gmail.com>
# License : MIT

"""
Text to word is an utility to Is a utility to allow processing of any text, it is a firts step from pipeline to 
natural language procesing to assist to learn english language, including work: 
* tokenization, 
* web scraping (get mp3 sound), 
* standardization, 
* stemming, 
* meaning 
* regular expressions
obtaining synthesizing all of the above in a plain text output.
"""

import nltk
from urllib.request import urlopen
from urllib.request import urlretrieve
import codecs
import pandas as pd
import os
import json
import timeit

class WordSpec:
 	
 	def __init__(self, word, type_word, phonetic, mean, path_mp3):
 		self.word = word
 		self.phonetic = phonetic
 		self.mean = mean
 		self.path_mp3 = path_mp3
 		self.type_word = type_word

 	def get_word(self):
 		return self.word

 	def get_phonetic(self):
 		return self.phonetic

 	def get_mean(self):
 		return self.mean

 	def get_path_mp3(self):
 		return self.path_mp3

 	def get_type_word(self):
 		return self.type_word

key = 'a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'

# Clean and tokenize source file
def clean_words(args):
	file_name = args[0]
	file_handle = codecs.open(file_name, 'r', 'ISO-8859-1')
	try:
		stream_file = file_handle.read()
		tokens = nltk.wordpunct_tokenize(stream_file)
		#remove numbers and cast to lower
		tokens = [word.lower() for word in tokens if not(re.search("[^a-zA-Z]", word))] 
		tokens = set(tokens)
		print("Quantity of words: " + str(len(tokens)))
		return tokens
	finally:
		file_handle.close()

# Get type of word
def get_type_of_word(word):
    
    # To debug is possible to use: print(json.dumps(data, indent=4, sort_keys=True))
    url = 'http://api.wordnik.com:80/v4/word.json/{0}/definitions?limit=200&includeRelated=false&sourceDictionaries=wiktionary&useCanonical=false&includeTags=false&api_key={1}'
    url = url.format(word, key)
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    type_of_word = data[0]['partOfSpeech']
    return type_of_word
    
# Get meaning of word
def get_meaning_of_word(word):
    
    url = 'http://api.wordnik.com:80/v4/word.json/{0}/definitions?limit=200&includeRelated=false&sourceDictionaries=wiktionary&useCanonical=false&includeTags=false&api_key={1}'
    url = url.format(word, key)
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    meaning_of_word = data[0]['text']
    return meaning_of_word
    

# Create file with
def create_file(name_file, data):
	words_df = pd.DataFrame(columns=["word", "word_type", "mean", "phonetic", "path_mp3"])
	for item in data:
		words_df.loc[len(words_df) + 1]=[item.get_word(), item.get_type_word(), item.get_phonetic(), item.get_mean(), item.get_path_mp3()] 
	
	words_df.to_csv(name_file, encoding='utf-8', index=False)

# Get phonetic
def get_phonetic(word):
    
    url = 'http://api.wordnik.com:80/v4/word.json/{0}/pronunciations?useCanonical=false&limit=50&api_key={1}'
    url = url.format(word, key)
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    phonetic = data[0]['raw']
    return phonetic
     
#get sound of word
def get_sound(word, path_to_save):
    url = 'http://api.wordnik.com:80/v4/word.json/{0}/audio?useCanonical=false&limit=50&api_key={1}'
    url = url.format(word, key)
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    path_name_mp3 = data[0]['fileUrl']
    urlretrieve(path_name_mp3, path_to_save+'/'+word+'.mp3')
    return path_name_mp3 

# Create file with informationi about words
def create_file_resume(tokens, args):
	words = []
	words_not_found = []
	
	#create dir for sounds
	sounds_path = args[1] + "sounds"
	if not os.path.exists(sounds_path):
		os.makedirs(sounds_path)

	for word in tokens:
		word_spec = WordSpec(word, '', '', '', '')
		print(word)
		try:
	        # get phonetic
		    phonetic = get_phonetic(word)
		    # get meaning
		    mean = get_meaning_of_word(word)
		    # get sound
		    path_name_mp3 = get_sound(word, sounds_path)
		    # get type of word
		    type_of_word = get_type_of_word(word)
		    word_spec = WordSpec(word, type_of_word, phonetic, mean, 'none')
		    words.append(word_spec)
		except:
		    print('problem with: ', word)
		    word_spec = WordSpec(word, '', '', '', '')
		    words_not_found.append(word_spec)
	
	# write words into master file
	file_name = "{0}{1}".format(args[1], "master.csv")
	create_file(file_name, words)
	#write words doesn't exist
	file_name = "{0}{1}".format(args[1], "words_not_found.csv")
	create_file(file_name, words_not_found)
	#Using from console, useful for see live log report
	print("Total words: " + str(len(tokens)))
	print("Total words not found: " + str(len(words_not_found)))
	print("Percentage misses: " + str(len(words_not_found) / len(tokens)))

# Principal function
def main(args):
    
    start_time = timeit.default_timer()
    #get clean tokens
    tokens = clean_words(args)
    create_file_resume(list(tokens), args)
    elapsed = timeit.default_timer() - start_time
    print('Elapsed time: ', elapsed, 'seconds')

# to execute	
args = ['/home/jasam/repositories/megalearner/tests/gotham/Gotham - 1x01.srt', '/home/jasam/repositories/megalearner/tests/gotham/']	

main(args)

