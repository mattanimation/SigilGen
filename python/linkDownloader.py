#!/usr/bin/python

"""
download all the links from the computational story lab
http://compstorylab.org/share/papers/reagan2016b/

url that contains links
http://hedonometer.org/data/bookdata/gutenberg-007/

"""
import os, sys, json
import mechanize
from time import sleep
import requests, gzip

ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = '../rawData'


def download_links():

	flPath = os.path.join(os.path.join(ROOT, DATA_PATH), 'hegnometerlinks.html')
	br = mechanize.Browser()

	#download and save if dont have it
	#if not os.path.isfile(flPath):
		
	br.open('http://hedonometer.org/data/bookdata/gutenberg-007/')

	#save for good measure
	with open(flPath, 'w') as f:
		f.write(br.response().read())
	print("file save complete: {0}".format(flPath))
	#else:
	#	br.open(flPath)

	filetypes = ['.zip', '.gz', '.tar.gz']
	lnks =[]
	for l in br.links():
		for t in filetypes:
			if t in str(l):
				lnks.append(l)

	print("processing links")
	
	for lnk in lnks:
		
		download_link(br, lnk)
	

def download_link(_br, _link):
	try:
		flName = os.path.join(os.path.join(os.path.join(ROOT, DATA_PATH), 'links'), _link.text)
		if not os.path.isfile(flName):
			print('downloading link:{0} to file: {0}'.format(_link.text, flName))
			#_br.click_link(_link)
			#zData = _br.response() #.read()
			print _link.absolute_url
			r = requests.get(_link.absolute_url, stream=True)
			r.raise_for_status()

			raw = r.raw
			with open(flName, 'wb') as out:
				for chunk in r.iter_content(1024):
					out.write(chunk)
			
			dld = gzip.open(flName)
			svName = flName.replace('.gz','')
			with open(svName, 'w') as out:
				for line in dld:
					out.write(line)

			sleep(1)
		else:
			print("skipping, {0} already exists".format(flName))

		#remove .zip when done to save space
		try:
			print("removing {0}".format(flName))
			os.remove(flName)
		except OSError:
		    pass
		
		"""
		with open(flName, 'w') as f:
			f.write(zData)
			print("{0} downloaded".format(_link.text))
		"""

	except:
		raise
	else:
		pass
	finally:
		pass


def main():
	print("starting download")
	download_links()


if __name__ == "__main__":
	main()





