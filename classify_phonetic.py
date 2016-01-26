import pandas as pd
import re

#Identify all rules that apply for word
def identify_rules(phonetic, word):
	rules = []
	#Validate rules
	rule = "eɪ"
	rule_name = "long a : /eɪ/"
	if re.search(rule,str(phonetic)):
       	#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "i"
	rule_name = "long e : /i/"
	if re.search(rule,str(phonetic)) and re.search("ee",str(word)):
		rules.append(rule_name)
	rule = "ɑɪ"
	rule_name = "long i : /ɑɪ/"
	if re.search(rule,str(phonetic)):
       	#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "oʊ"
	rule_name = "long o : /oʊ/"
	if re.search(rule,str(phonetic)):
       	#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "ju"
	rule_name = "long u : /ju/"
	if re.search(rule,str(phonetic)):
       	#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "æ"
	rule_name = "short a : /æ/"
	if re.search(rule,str(phonetic)):
       	#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "ɛ"
	rule_name = "short  e : /ɛ/"
	if re.search(rule,str(phonetic)):
       	#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "ɪ"
	rule_name = "short  i : /ɪ/"
	if re.search(rule,str(phonetic)):
       	#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "ɑ"
	rule_name = "short  o : /ɑ/"
	if re.search(rule,str(phonetic)):
       	#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "ʊ"
	rule_name = "other u : /ʊ/"
	if re.search(rule,str(phonetic)) and not re.search("oʊ",str(phonetic)):
		#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)    
	rule = "ɔ"
	rule_name = "aw sound : /ɔ/"
	if re.search(rule,str(phonetic)):
		#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "ɑr"
	rule_name = "ar sound : /ɑr/"
	if re.search(rule,str(phonetic)):
		#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)
	rule = "ɔr"
	rule_name = "or sound : /ɔr/"
	if re.search(rule,str(phonetic)):
    	#print(rule_name  + str(word), phonetic)
		rules.append(rule_name)

	return rules

#rules taken from this site: http://pronuncian.com/Sounds/Default.aspx?
def cluster_word(args):
	print("--cluster_word")
	words_df = pd.read_csv(args[0], names=["word", "mean", "phonetic", "path_mp3", "image_path"])
	words_rules_df = pd.DataFrame(columns=["word", "mean", "phonetic", "rule", "path_mp3", "image_path"])
	#print(words_df)
	for i,r in words_df.iterrows():
		
		print(r["word"])

		rules = identify_rules(r["phonetic"] , r["word"])
		for rule in rules:
			words_rules_df.loc[len(words_rules_df) + 1] = [r["word"], r["mean"], r["phonetic"], rule, r["path_mp3"], r["image_path"]]

	file_name = "{0}\{1}".format(args[1], "master_words_rules.csv")
	#print(len(words_rules_df))
	words_rules_df.to_csv(file_name, encoding='utf-8', index=False)
	print("File: " + file_name + " created")

def main(args):
	print("--classify_phonetic")
	cluster_word(args)