#!/usr/bin/python
import os,sys, random, json


ROOT = os.path.abspath(os.path.dirname(__file__))


wordsPath = os.path.join(ROOT, 'labMTwords-english.csv')
scoresPath = os.path.join(ROOT, 'labMTscores-english.csv')
sentimentData = {}
words = []
scores = []

with open(wordsPath) as f:
	for ln in f:
		words.append(ln.strip())
print words

with open(scoresPath) as f:
	for ln in f:
		scores.append(float(ln.strip()))
print scores

for i in range(0, len(words)):
	w = words[i]
	s = scores[i]
	sentimentData[w] = s

with open('labMTwordScores.json', 'w') as f:
	f.write(json.dumps(sentimentData))

print ('complete')



