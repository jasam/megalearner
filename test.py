args = ['/home/jasam/repositories/megalearner/tests/gotham/Gotham - 1x01.srt', '/home/jasam/repositories/megalearner/tests/gotham/']

import pysrt
from urllib.request import urlopen
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from urllib.request import urlretrieve
import pandas as pd
import timeit

file_name = args[0]

# Translate using yandex
YANDEX_TOKEN = 'trnsl.1.1.20161206T131516Z.977502a78631e44a.ee6e6f5da9accef8571f04e123680e333d744149'
URL_YANDEX = 'https://translate.yandex.net/api/v1.5/tr/translate?key={0}&text={1}&lang=en-es'

# Text to speech using acapela
path_to_save = '/home/jasam/repositories/megalearner/tests/gotham/sentences/'
path_name_mp3 = 'http://vaas.acapela-group.com/Services/Synthesizer?req_voice={0}&req_text={1}&cl_pwd={2}&req_asw_type=STREAM&cl_login=EVAL_VAAS&cl_app=EVAL_3530309'
voice = 'ryan22k'
pwd = 'sjyraicm' 

class WordSpec:
     
     def __init__(self, index, sentence, translation, audio_name):
         
         self.index = index
         self.sentence = sentence
         self.translation = translation
         self.audio_name = audio_name

     def get_index(self):
         return self.index

     def get_sentence(self):
         return self.sentence

     def get_translation(self):
         return self.translation

     def get_audio_name(self):
         return self.audio_name
     
# Create file with
def create_file(name_file, data):
    #words_df = pd.DataFrame(columns=["index", "sentence", "translation", "audio_name"])
    words_df = pd.DataFrame(columns=['index', 'sentence', 'translation', 'audio_name'])
    for item in data:
        #words_df.loc[len(words_df) + 1]=[item.get_index(), item.get_sentence(), item.get_translation(), item.audio_name()] 
        words_df.loc[len(words_df) + 1]=[item.get_index(), item.get_sentence(), 
                                         item.get_translation(), item.get_audio_name()]
    
    words_df.to_csv(name_file, encoding='utf-8', index=False)

start_time = timeit.default_timer()     
subs = pysrt.open(file_name)

index = 1

sentences = []
for item in subs[1:1000]:
    
    sentence = item.text.replace('-', '')
    sentence = item.text.replace('"', '')
    sentence = item.text.replace(',', ';')
    sentence = item.text.replace('.', '')
    sentence_cast = sentence.replace(' ', '+')
    print(index, sentence)
    url_to_use = URL_YANDEX.format(YANDEX_TOKEN, sentence_cast)
    try:
        response = urlopen(url_to_use).read()
        xmldoc = minidom.parseString(response)
        text = xmldoc.getElementsByTagName('text')
        sentence_translated = text[0].firstChild.nodeValue
        #print(sentence_translated)
    except:
        print('problem translating with: ', url_to_use)
    
    try:
        path_name_mp3 = 'http://vaas.acapela-group.com/Services/Synthesizer?req_voice={0}&req_text={1}&cl_pwd={2}&req_asw_type=STREAM&cl_login=EVAL_VAAS&cl_app=EVAL_3530309'
        path_name_mp3 = path_name_mp3.format(voice, sentence_cast, pwd)
        urlretrieve(path_name_mp3, path_to_save+str(index)+'.mp3')
    except:
        print('problem text to speech: ', text)
    
    word_spec = WordSpec(index, sentence.replace('"',''), sentence_translated, str(index)+'.mp3')
    sentences.append(word_spec)
    
    index += 1

# write words into master file
file_name = "{0}{1}".format(args[1], "master.csv")
create_file(file_name, sentences)    
print('finished')
elapsed = timeit.default_timer() - start_time
print('Elapsed time: ', elapsed, 'seconds')