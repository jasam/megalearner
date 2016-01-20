###Phase 1 project megalearner

import nltk
import re
from urllib.request import urlopen
import codecs
from bs4 import BeautifulSoup
import pandas as pd

class WordSpec:
 	
 	def __init__(self, word, phonetic, mean):
 		self.word = word
 		self.phonetic = phonetic
 		self.mean = mean

 	def get_word(self):
 		return self.word

 	def get_phonetic(self):
 		return self.phonetic

 	def get_mean(self):
 		return self.mean

#clean and tokenize source file
def clean_words(args):
	#print("--clean_words")
	file_name = args[0]
	file_handle = codecs.open(file_name, 'r', 'utf-8')
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
	words_df = pd.DataFrame(columns=["word", "mean", "phonetic"])
	for item in data:
		#print(item)
		words_df.loc[len(words_df)+1]=[item.get_word(), item.get_mean(), item.get_phonetic()] 
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
		for link in tags[0].find_all("a"): 
			mean = link.get_text()
			#print(phonetic)
			#break
		#print(mean)
		return mean	
	else:
		return mean
	
#scraping dictionary to obtain phonetic, translation and sound
#using oxford dictionary
def scrape_dict(tokens, args):
	URL_DICT = "http://www.oxforddictionaries.com/translate/english-spanish/"
	#print("--scrape_dict")
	#print(args)
	words = []
	words_not_found = []
	
	for word in tokens:
		print(word)
		try:
			#print(URL_DICT + word)
			html = urlopen(URL_DICT + word).read()
		except Exception as e:
			print("***word: " + word + " doesn't exist***")
			print(e)
			word_spec = WordSpec(word, "", "")
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
		word_spec = WordSpec(word, phonetic, mean)
		words.append(word_spec)
		#print(word_spec)
		
	
	#write words in master file
	file_name = "{0}\{1}".format(args[1], "master.csv")
	create_file(file_name, words)
	#write words in doesn't exist
	file_name ="{0}\{1}".format(args[1], "words_not_found.csv")
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