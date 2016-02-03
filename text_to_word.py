###Phase 1 project megalearner

import nltk
import re
from urllib.request import urlopen
from urllib.request import urlretrieve
import codecs
from bs4 import BeautifulSoup
import pandas as pd
import os

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
	#print("--clean_words")
	file_name = args[0]
	file_handle = codecs.open(file_name, 'r', 'ISO-8859-1')
	try:
		stream_file = file_handle.read()
		tokens = nltk.wordpunct_tokenize(stream_file)
		#remove numbers and cast to lower
		tokens = [word.lower() for word in tokens if not(re.search("[^a-zA-Z]", word))] 
		tokens = set(tokens)
		print("Quantity of words: " + str(len(tokens)))
		#print(tokens)
		return tokens
	finally:
		file_handle.close()

def create_file(name_file, data):
	#print("create_file")
	words_df = pd.DataFrame(columns=["word", "mean", "phonetic", "path_mp3", "image_path"])
	for item in data:
		#print(item)
		#print("loop create file")
		words_df.loc[len(words_df) + 1]=[item.get_word(), item.get_mean(), item.get_phonetic(), item.get_path_mp3(), item.get_image_path()] 
	#print(words_df)

	#create file
	#print(name_file)
	words_df.to_csv(name_file, encoding='utf-8', index=False)

def get_phonetic(soup):
	#print("--get_phonetic")
	tags = soup.find_all("span", class_="prx")
	#print(tags)
	phonetic = ""
	if len(tags) != 0: 
		for link in tags[0].find_all("a"):
			phonetic = link.get_text()
			#print(phonetic)
			break
		return phonetic
	else:
		return phonetic

#note: some words doesn't appear, likely page was developed over other code, scrape will fail.
def get_translation(soup):
	#print("--get_translation")
	tags = soup.find_all("span", class_="tr trnoprecex")
	mean = ""
	#print(tags)
	if len(tags) != 0: 
		#print(tags)
		for link in tags[0].find_all("a"): 
			mean = link.get_text()
			print(mean)
			return mean	
		#print(mean)
	else:
		return mean

#get sound of word
def get_sound(soup, path_to_save):
	#print(path_to_save)
	mp3_tags = soup.find_all("span", class_="prx")
	file_name_mp3 = None
	if len(mp3_tags) != 0: 
		for link in mp3_tags[0].find_all("div"):
			file_name_mp3 = link.get('data-src-mp3')
			#print(file_name_mp3)
			#break
		#print(file_name_mp3)
		if file_name_mp3 is not None:	
			urlretrieve(file_name_mp3, path_to_save)

#scraping dictionary to obtain phonetic, translation and sound
#using oxford dictionary
def scrape_dict(tokens, args):
	URL_DICT = "http://www.oxforddictionaries.com/translate/english-spanish/"
	#print("--scrape_dict")
	#print(args)
	words = []
	words_not_found = []
	
	#create dir for sounds
	sounds_path = args[1] + "\sounds"
	if not os.path.exists(sounds_path):
		os.makedirs(sounds_path)

	for word in tokens:
		print(word)
		try:
			#print(URL_DICT + word)
			html = urlopen(URL_DICT + word).read()
		except Exception as e:
			print("***word: " + word + " doesn't exist***")
			print(e)
			word_spec = WordSpec(word, "", "", "", "")
			words_not_found.append(word_spec)
			continue
		
		#get soup
		soup = BeautifulSoup(html, 'html.parser')
		#print(soup)
		#tags = soup.find_all("span", class_="prx")
		#print(dir(soup))
		#get phonetic
		phonetic = get_phonetic(soup)
		#print(phonetic)
		mean = get_translation(soup)
		#print(mean)
		#print(word_spec)
		#get sound
		path_name_mp3 = "{0}\{1}.{2}".format(sounds_path, word, "mp3")
		get_sound(soup, path_name_mp3)
		image_path_name = "{0}\{1}\{2}.{3}".format(args[1], "images", word, "png")
		word_spec = WordSpec(word, phonetic, mean, path_name_mp3, image_path_name)
		words.append(word_spec)
		
	
	#write words into master file
	file_name = "{0}\{1}".format(args[1], "master.csv")
	create_file(file_name, words)
	#write words in doesn't exist
	file_name = "{0}\{1}".format(args[1], "words_not_found.csv")
	create_file(file_name, words_not_found)
	print("Total words: " + str(len(tokens)))
	print("Total words not found: " + str(len(words_not_found)))
	print("Percentage misses: " + str(len(words_not_found) / len(tokens)))

def main(args):
	print("--text_to_word")
	#get clean tokens
	tokens = clean_words(args)
	#create output with words
	scrape_dict(tokens,args)