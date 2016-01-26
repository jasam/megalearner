import simplejson as json
#print(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))
#print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
dragon = {'people': ['goku','krilim','picoro','vegeta']}
#print(dragon)
#print(json.dumps(dragon))
document = dict()
document['rule']= list(dict())
document['words'] = list(dict())

document['words'].append({"seek": "sIk"})
document['words'].append({"green": "grIn"})


#document['words'].append({"tax": "tæks"})
#document['words'].append({"crab": "kræb"})
#document['rule'].append('short a : /æ/')


#print(document)
#print(json.dumps(document, indent=1))
#for item in document:
	#print(item)

#rules = {"type_rule": "words with g"}
rules = ['words with g', {'bar': ('baz', None, 1.0, 2)}]

#{ "one": 1, "two": { "list": [ {"item":"A"},{"item":"B"} ] } }'
#words = []
#words.append({"green" : "grin"})
#rules['words'].append(words)

#print(rules)

print(json.dumps(rules, sort_keys=True, indent=4))

