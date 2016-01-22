import pandas as pd
import re

#rules taken from this site: http://pronuncian.com/Sounds/Default.aspx?
def cluster_word(args):
	print("--cluster_word")
	words_df = pd.read_csv(args[0], names=["word", "mean", "pronunciation"])
	words_rules_df = pd.DataFrame(columns=["word", "rule", "pronunciation"])
	#print(words_df)
	for i,r in words_df.iterrows():
		word = r["word"] 
    	#print(word)
		phonetic = r["pronunciation"] 
    	#print(word)

    	#Validate rules
		rule = "eɪ"
		rule_name = "long a : /eɪ/"
		if re.search(rule,str(phonetic)):
        	#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "i"
		rule_name = "long e : /i/"
		if re.search(rule,str(phonetic)) and re.search("ee",str(word)):
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "ɑɪ"
		rule_name = "long i : /ɑɪ/"
		if re.search(rule,str(phonetic)):
        	#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "oʊ"
		rule_name = "long o : /oʊ/"
		if re.search(rule,str(phonetic)):
        	#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "ju"
		rule_name = "long u : /ju/"
		if re.search(rule,str(phonetic)):
        	#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "æ"
		rule_name = "short a : /æ/"
		if re.search(rule,str(phonetic)):
        	#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "ɛ"
		rule_name = "short  e : /ɛ/"
		if re.search(rule,str(phonetic)):
        	#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "ɪ"
		rule_name = "short  i : /ɪ/"
		if re.search(rule,str(phonetic)):
        	#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "ɑ"
		rule_name = "short  o : /ɑ/"
		if re.search(rule,str(phonetic)):
        	#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]

		rule = "ʊ"
		rule_name = "other u : /ʊ/"
		if re.search(rule,str(phonetic)) and not re.search("oʊ",str(phonetic)):
			#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]    
		rule = "ɔ"
		rule_name = "aw sound : /ɔ/"
		if re.search(rule,str(phonetic)):
			#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "ɑr"
		rule_name = "ar sound : /ɑr/"
		if re.search(rule,str(phonetic)):
			#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]
		rule = "ɔr"
		rule_name = "or sound : /ɔr/"
		if re.search(rule,str(phonetic)):
      		#print(rule_name  + str(word), phonetic)
			words_rules_df.loc[len(words_rules_df)+1]=[word, rule_name, phonetic]

	 #words_rules_df        
	#words_rules_df.groupby(['word']).size()
	#grouped = words_rules_df.groupby(['word'])
	#grouped.filter(lambda x: len(x) > 1)
	words_rules_df[words_rules_df["rule"] == "short  i : /ɪ/"]
	#grouped = words_rules_df.groupby(['rule'])
	#grouped.size()
	#grouped.filter(lambda x: len(x) > 1)

def main(args):
	print("--classify_phonetic")
	cluster_word(args)