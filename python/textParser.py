#!/usr/bin/python
"""
	@Author: Matt Murray
	@Description: visualize complex data in a simple quickly recognized representation
"""
import os,sys, random, json, re
import operator
from nltk.tokenize import RegexpTokenizer
import csv
import glob

#for csv parsing
import pandas as pd

#for lexical analysis
from textstat.textstat import textstat

ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = '../rawData'
PARSED_DATA_PATH = "../parsedData"
CSV_PATH = os.path.join(os.path.join(ROOT, DATA_PATH), 'links')

#http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
#http://sentiwordnet.isti.cnr.it/
#http://compstorylab.org/share/papers/reagan2016b/
sentimentDataPath = os.path.join(ROOT, 'sentiment.json')
sentimentData = {}
with open(sentimentDataPath) as f:
	sentimentData = json.loads(f.read())


def parse_text(fileName):

	
	filePath = os.path.join(DATA_PATH, fileName)
	parsedFilePath = os.path.join(PARSED_DATA_PATH, fileName)
	#path to read from
	fp = os.path.abspath(os.path.join(ROOT, filePath))
	#path to save to
	pfp = os.path.abspath(os.path.join(ROOT, parsedFilePath.replace('.txt', '.json')))
	#store words here
	words = {}
	chapters = {}
	sentimentCurveData = []
	tokenizer = RegexpTokenizer(r'\w+')
	chapterCount = 0
	with open(fp) as f:

		#parse line by line
		for ln in f:
			cleanLine = ln.decode('utf-8').strip().lower()
			if "chapter" in cleanLine:
				chapterCount += 1
			tokens = tokenizer.tokenize(cleanLine)
			#print(tokens)
			#add words to words dict
			chptr = "chapter{0}".format(chapterCount)
			if not chptr in chapters:
				chapters[chptr] = {}
			#print(chapters)
			for t in tokens:
				#increase score if in there
				t = t.lower()
				if t in words:
					words[t]['count'] += 1
					if t in chapters[chptr]:
						chapters[chptr][t] += 1
				else:
					#only do this once
					words[t] = {'count': 1, 'sentiment':check_sentiment(t)}
					chapters[chptr][t] = 1

	with open(fp) as f:
		#parse by paragraph
		content = f.read().decode('utf-8')
		paras = get_paragraphs(content)
		
		for p in paras:
			tokens = tokenizer.tokenize(p)
			sentimentCurveData.append(get_sentiment_score(tokens))
			

	#print(words)
	#sort words high to low
	sortedWords = sort_by_value(words)
	documentData = {
		"uniqueWordCount": len(words),
		"words": words,
		"chapters": chapters,
		"sorted": sortedWords,
		"sentimentCurve": sentimentCurveData
	}
	with open(pfp, 'w') as f:
		f.write(json.dumps(documentData))
	
	print("complete, saved results to {0}".format(pfp))

def check_sentiment(_word):
	#check for pos
	res = "unkown"
	pos = is_positive(_word.lower())
	neg = is_negative(_word.lower())
	if pos:
		res = "positive"
	if neg:
		res = "negative"
	return res

def get_sentiment_score(_tokens):
	"""
	return the overal score of sentiment for a given list of words aka tokens
	"""
	posScore = 0
	negScore = 0
	posVal = 1
	negVal = -1
	for t in _tokens:
		pos = is_positive(t)
		neg = is_negative(t)
		if pos:
			posScore += posVal
		if neg:
			negScore += negVal

	return posScore + negScore

def is_positive(_word):
	return _word in sentimentData['positives']
def is_negative(_word):
	return _word in sentimentData['negatives']

def sort_by_value(_dict):
	return sorted(_dict.items(), key=operator.itemgetter(1))

def sort_by_keys(_dict):
	return sorted(_dict.items(), key=operator.itemgetter(0))

def get_paragraphs(_content):
	p = []
	for match in re.finditer(r'(?s)((?:[^\n][\n]?)+)', _content):
		p.append(_content[match.start(): match.end()])
		#print match.start(), match.end()
	return p

def build_curve():
	"""
	You can make the sentiment time series from those 10,222x200 matrices, let me explain how quickly.
	Take each column (10,222 long), and normalize it to have a sum of 1 (divide by the sum).
	Then take a the dot product (a dot b = a_1 * b_1 + ... + a_10222 * b_10222) of each of the 200 columns with the sentiment vector.
	Those 200 numbers are the time series.
	Here's that vector that you need to multiply by:
	http://hedonometer.org/data/labMT/labMTscores-english.csv

	I'm excited to see what you come up with!

	Here's a link to the "mode" for each book:
	http://compstorylab.org/share/papers/reagan2016b/
	actual link:
	http://compstorylab.org/share/papers/reagan2016b/mode-lists.zip
	"""
	#load word scores
	scoresFile = os.path.join(ROOT, "labMTscores-english.csv")
	sentimentScores = []
	with open(scoresFile, 'rb') as sfData:
		rdr = csv.reader(sfData, delimiter=';')
		for row in rdr:
			sentimentScores.append(float(row[0]))
	
	#print sentimentScores

	#get list of .csv files
	print("reading files from: {0}".format(CSV_PATH))
	flz = glob.glob('{0}/*.csv'.format(CSV_PATH))

	print(flz)
	#print flz
	i=0
	#process only x number of files
	while(i < 3):
		csvfile = flz[i]
		gID = os.path.basename(csvfile).split('.')[0]

		txtfile = csvfile.replace('.csv', '.txt')
		
		

		print csvfile
		colnames = range(200)
		df = pd.read_csv(csvfile, names=colnames)
		columns = []
		timeSeries = []
		for i in colnames:
			columns.append(df[i].tolist())
		#print columns
		#print("col len: " + str(len(columns)))
		for col in columns:
			#normalizes the values in this column
			normed = [(c/float(len(col))) for c in col]
			#get dot product of normalized values to sentiment scores
			#which is timeseries of the 200 sliding window blocks of text
			timeSeries.append(dot(normed, sentimentScores))
		#print(timeSeries)
		#print(len(timeSeries))

		#map to plot / arc type
		plots = {
			'1': 'Rags-to-riches',
			'2': 'Tragedy',
			'3': 'Man-in-a-hole',
			'4': 'Icarus',
			'5': 'Cindarella',
			'6': 'Oedipus'
		}
		#somehow map this out

		#load text and parse (https://pypi.python.org/pypi/textstat)
		txt = None
		statData = {}
		lns = []
		with open(txtfile, 'r') as tf:
			lns = tf.readlines()

		#parse out true text and meta data
		stats = ["Title", "Author", "Language"]
		txtTitle = "n/a"
		trueTxt = []
		canStart = False
		canEnd = False
		for ln in lns:
			
			#only process the true body text
			#and not the gutenburg meta crap
			if not canStart and '*** START' in ln:
				canStart = True

			if not canEnd and '*** END' in ln:
				canEnd = True

			if canStart:
				trueTxt.append(ln)
			else:
				print(ln)
				for stat in stats:
					if (stat + ":") in ln:
						statData[stat.lower()] = ln.split(':')[1].strip()

			#if canEnd:
			#	break

		txt = ''.join(trueTxt)

		#get daleschall rating
		ds = textstat.dale_chall_readability_score(txt)
		#get grade level rating
		ts = textstat.text_standard(txt)
		#get word count
		lxCnt = textstat.lexicon_count(txt)
		
		#concat new data in dict
		textData = dict(statData)
		textData.update({
			"lexiconCount":lxCnt,
			"timeSeries":timeSeries,
			"daleChallScore":ds,
			"gradeLevel":ts,
			"gutenburgID":gID
		})

		resultFile = csvfile.replace(gID, "{0}_{1}".format(gID,textData['title'])).replace('.csv', '.json')

		#save resulting data
		with open(resultFile, 'w') as f:
			f.write(json.dumps(textData))

		print("saving complete: {0}".format(txtfile))

		#increment the iterator
		i += 1



def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(float(i[0]) * float(i[1]) for i in zip(K, L))

def main():
	#do arg parsing
	#parse_text('aliceInWonderland.txt')

	#take the sentiment and smooth it to get
	#general story arc curve
	build_curve()


if __name__ == "__main__":
	main()