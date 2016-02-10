
import nltk
import codecs
import re
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
import requests

file_name = "E:\\repos_git\\megalearner\\tests\\google-10000-english\\words_not_found.csv"
file_handle = codecs.open(file_name, 'r', 'ISO-8859-1')
URL_DICT = "http://www.oxforddictionaries.com/translate/english-spanish/"
try:
	stream_file = file_handle.read()
	tokens = nltk.wordpunct_tokenize(stream_file)
	tokens = [word.lower() for word in tokens if not(re.search("[^a-zA-Z]", word))] 
	lmtzr = WordNetLemmatizer()
	porter_stemmer = PorterStemmer()
	lancaster_stemmer = LancasterStemmer()
	#result = requests.get(URL_DICT)
	#print(result.status_code)
	for token in tokens:	
		#print(token, lmtzr.lemmatize(token), porter_stemmer.stem(token), lancaster_stemmer.stem(token))
		token_lemma = lmtzr.lemmatize(token)
		result = requests.get(URL_DICT + token_lemma)
		#print(result)
		if result.status_code == 200:
			print(token, "exists!", token_lemma)
		else:
			token_lemma = lmtzr.lemmatize(token, "v")
			result = requests.get(URL_DICT + token_lemma)
			if result.status_code == 200:
				print(token, "exists!", token_lemma)
			else:
				print(token, "don't exist!", token_lemma)
finally:
	file_handle.close()