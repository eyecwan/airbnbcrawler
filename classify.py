import nltk
import re
import sys


city = sys.argv[1]
raw = ''

with open('room_desc_' + city + '_txt') as f:
	raw = f.read()
	
	

def freqdist(raw):
	wordList = re.sub("[^\w]"," ",text).split()
	all_words = nltk.FreqDist(w.lower() for w in wordList)
	return all_words
	
	

def collocations(raw):
	words = re.sub("[^\w]"," ",raw)
	tokens = nltk.word_tokenize(words)	
	nltk_text = nltk.Text(tokens)
	return nltk_text.collocations()
	
collocations(raw)

'''
all_words = nltk.FreqDist(w.lower() for w in wordList)

print(all_words)
#print all_words.most_common(50)

#print sorted(w for w in set(wordList) if len(w) > 4 and all_words[w] > 7)
#all_words.plot(50, cumulative=True)
#word_features = all_words.keys()[:2000]

#print word_features

'''