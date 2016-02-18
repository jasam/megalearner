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
import re
from urllib.request import urlopen
from urllib.request import urlretrieve
import codecs
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
from nltk.stem import WordNetLemmatizer

class WordSpec:
 	
 	def __init__(self, word, phonetic, mean, path_mp3, image_path):
 		self.word = word
 		self.phonetic = phonetic
 		self.mean = mean
 		self.path_mp3 = path_mp3
 		self.image_path = image_path

 	def get_word(self):
 		return self.word

 	def get_phonetic(self):
 		return self.phonetic

 	def get_mean(self):
 		return self.mean

 	def get_path_mp3(self):
 		return self.path_mp3

 	def get_image_path(self):
 		return self.image_path

#clean and tokenize source file
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

#Create file with: word, mean, phonetic, path_mp3 and image_path
def create_file(name_file, data):
	words_df = pd.DataFrame(columns=["word", "mean", "phonetic", "path_mp3", "image_path"])
	for item in data:
		words_df.loc[len(words_df) + 1]=[item.get_word(), item.get_mean(), item.get_phonetic(), item.get_path_mp3(), item.get_image_path()] 
	
	words_df.to_csv(name_file, encoding='utf-8', index=False)

#Get phonetic using web scraping
def get_phonetic(soup):
	tags = soup.find_all("span", class_="prx")
	phonetic = ""
	if len(tags) != 0: 
		for link in tags[0].find_all("a"):
			phonetic = link.get_text()
			break
		return phonetic
	else:
		return phonetic

#Get meaning using web scraping
#note: some words doesn't appear, likely page was developed over other code, scrape will fail.
def get_translation(soup):
	tags = soup.find_all("span", class_="tr trnoprecex")
	mean = ""
	if len(tags) != 0: 
		for link in tags[0].find_all("a"): 
			mean = link.get_text()
			return mean	
	else:
		return mean

#get sound of word
def get_sound(soup, path_to_save):
	mp3_tags = soup.find_all("span", class_="prx")
	file_name_mp3 = None
	if len(mp3_tags) != 0: 
		for link in mp3_tags[0].find_all("div"):
			file_name_mp3 = link.get('data-src-mp3')
		if file_name_mp3 is not None:	
			urlretrieve(file_name_mp3, path_to_save)

#scraping dictionary to obtain phonetic, translation and sound
#using oxford dictionary
def scrape_dict(tokens, args):
	URL_DICT = "http://www.oxforddictionaries.com/translate/english-spanish/"
	words = []
	words_not_found = []
	
	#create dir for sounds
	sounds_path = args[1] + "\sounds"
	if not os.path.exists(sounds_path):
		os.makedirs(sounds_path)

	lmtzr = WordNetLemmatizer()
	for word in tokens:
		#print(word)
		token_lemma = word
		result = requests.get(URL_DICT + token_lemma)
		if result.status_code == 200:
			print(word, " --exists!")
			html = urlopen(URL_DICT + token_lemma).read()
		else:
			token_lemma = lmtzr.lemmatize(word)
			result = requests.get(URL_DICT + token_lemma)
			if result.status_code == 200:
				#Using from console, useful for see live log report
				print(word, " --exists!")
				html = urlopen(URL_DICT + token_lemma).read()
			else:
				token_lemma = lmtzr.lemmatize(word, "v")
				result = requests.get(URL_DICT + token_lemma)
				if result.status_code == 200:
					#Using from console, useful for see live log report
					print(word, " --exists!")
					html = urlopen(URL_DICT + token_lemma).read()
				else:
					#Using from console, useful for see live log report
					print("***word: " + word + " doesn't exist***")
					word_spec = WordSpec(word, "", "", "", "")
					words_not_found.append(word_spec)
					continue
		
		#get soup
		soup = BeautifulSoup(html, 'html.parser')
		#get phonetic
		phonetic = get_phonetic(soup)
		#print(phonetic)
		mean = get_translation(soup)
		#get sound
		path_name_mp3 = "{0}\ {1}.{2}".format(sounds_path, token_lemma, "mp3")
		get_sound(soup, path_name_mp3)
		image_path_name = "{0}\{1}\{2}.{3}".format(args[1], "images", token_lemma, "png")
		word_spec = WordSpec(token_lemma, phonetic, mean, path_name_mp3, image_path_name)
		words.append(word_spec)
		
	
	#write words into master file
	file_name = "{0}\{1}".format(args[1], "master.csv")
	create_file(file_name, words)
	#write words doesn't exist
	file_name = "{0}\{1}".format(args[1], "words_not_found.csv")
	create_file(file_name, words_not_found)
	#Using from console, useful for see live log report
	print("Total words: " + str(len(tokens)))
	print("Total words not found: " + str(len(words_not_found)))
	print("Percentage misses: " + str(len(words_not_found) / len(tokens)))

def main(args):
	#get clean tokens
	tokens = clean_words(args)
	#create output with words
	scrape_dict(tokens,args)