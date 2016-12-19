args = ['/home/jasam/repositories/megalearner/tests/gotham/Gotham - 1x01.srt', '/home/jasam/repositories/megalearner/tests/gotham/']

import pysrt
from urllib.request import urlopen
from urllib.request import urlretrieve
import pandas as pd
import timeit
from yandex_translate import YandexTranslate
import urllib.parse

file_name = args[0]

# Text to speech using acapela
path_to_save = '/home/jasam/repositories/megalearner/tests/gotham/sentences/'

YANDEX_TOKEN = 'trnsl.1.1.20161206T131516Z.977502a78631e44a.ee6e6f5da9accef8571f04e123680e333d744149'
YANDEX_KEY_TTS = '11c5b64f-32ec-4252-a4f0-138132812068'
URL_YANDEX_TTS = 'https://tts.voicetech.yandex.net/generate?%s'

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

translate = YandexTranslate(YANDEX_TOKEN)

for item in subs:
    
    sentence = item.text
    sentence = sentence.replace('-', '')
    if sentence[-1] == '.':
        sentence = sentence[:-1]
    sentence = sentence.replace('"', '')
    sentence = sentence.replace(',', ';')
    sentence = sentence.replace('\n', ' ')
    sentence_cast = sentence
    print(index, sentence_cast)
    reponse = translate.translate(sentence_cast, 'en-es')
    sentence_translated = reponse['text'][0]
    sentence_translated = sentence_translated.replace(',', ';')
    
    if reponse['code'] == 200:
        print(sentence_translated)
    else:
        print('Problema con: ', sentence_cast)
    
    try:
        params = urllib.parse.urlencode({'text': sentence_cast, 
                                         'format': 'wav',
                                         'lang':'en-EN',
                                         'speaker':'zahar',
                                         'emotion':'good',
                                         'key':YANDEX_KEY_TTS})
        
        path_url_sound = URL_YANDEX_TTS % params
        #print(path_url_sound)
        #print(path_name_mp3)
        urlretrieve(path_url_sound, path_to_save+str(index)+'.mp3')
    except:
        print('problem text to speech: ', sentence)
    
    word_spec = WordSpec(index, sentence, sentence_translated, str(index)+'.mp3')
    sentences.append(word_spec)
    
    index += 1

# write words into master file
file_name = "{0}{1}".format(args[1], "master.csv")
create_file(file_name, sentences)    
print('finished')
elapsed = timeit.default_timer() - start_time
print('Elapsed time: ', elapsed, 'seconds')