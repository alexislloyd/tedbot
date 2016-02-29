# -*- coding: utf-8 -*-
from __future__ import print_function
from jinja2 import Environment, PackageLoader
import sys
import os
from time import strftime, gmtime
import json
import yaml
from tedbot import createTalk
from bs4 import BeautifulSoup

DEBUG = True

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
    outputdir = cfg['export']['root']
    talkdir = cfg['export']['talkdir']
    siteurl = cfg['export']['siteurl']


def makeNewPage():
	talk = createTalk()
	if DEBUG: print("Got a talk. Writing to speech.html", file=sys.stderr)
	
	#tedbot is the current package, and templates is the directory where templates live
	env = Environment(loader=PackageLoader('tedbot', 'templates'))
	template = env.get_template('talk.html')
	page = template.render(talk=talk)

	#create a filename with the current date/time
	filepath = outputdir + talkdir

	filename = strftime("%Y%m%d%H%M", gmtime())
	filename += ".html"

	filepath += filename

	with open(filepath, "w") as speechfile:
		speechfile.write(page)

	retobj = {}
	retobj['url'] = siteurl + talkdir + filename
	retobj['title'] = talk['title']

	return retobj

def rebuildIndex():
	#open the talks folder
	searchdir = outputdir + talkdir
	
	talklist = []
	#get a list of all the files inside
	for root, dirs, files in os.walk(searchdir):
		if DEBUG: print(root, file=sys.stderr)
		for filename in reversed(files):
			if DEBUG: print(filename, file=sys.stderr)
			#for each file, get its filename, title, and lead image
			with open(root+filename, "r") as currentpage:
				pagetext = currentpage.read()
				soup = BeautifulSoup(pagetext, "html5lib")
				talk = {}
				resulttags = soup.find_all("meta") 
				for tag in resulttags:
					if tag['name'] == 'title':
						talk['title'] = tag['content']
					elif tag['name'] == 'thumb':
						talk['image'] = tag['content']
					if DEBUG: print("tag: " + str(tag.attrs), file=sys.stderr)
				
				#put in some error checking here to make sure you have an image / title!
				talk['url'] = talkdir+filename
				if DEBUG: print(talk['url'], file=sys.stderr)
				talklist.append(talk)

	#pass that object to the template renderer
	filename = outputdir + "index.html"
	if DEBUG: print("index file will be " + filename, file=sys.stderr)
	env = Environment(loader=PackageLoader('tedbot', 'templates'))
	template = env.get_template('index.html')
	index = template.render(talklist=talklist)

	with open(filename, "w") as indexfile:
		indexfile.write(index)

def main():
	print(strftime("%a, %d %b %Y %H:%M:%S %Z", gmtime()), file=sys.stderr)
	print("Generating new talk", file=sys.stderr)
	
	talk = makeNewPage()

	print("Tweeting link to new talk at " + talk['url'], file=sys.stderr)

	#Tweet link here -- title is in talk['title']

	print("Regenerating index file", file=sys.stderr)

	rebuildIndex()
	
	print("Done.", file=sys.stderr)

if __name__ == "__main__":
    main()