# -*- coding: utf-8 -*-
from __future__ import print_function
from jinja2 import Environment, PackageLoader
import sys
from time import strftime, gmtime
import json
from tedbot import createTalk

DEBUG = True

outputdir = "output/"
talkdir = "talks/"

def makeNewPage():
	talk = createTalk()
	if DEBUG: print("Got a talk. Writing to speech.html", file=sys.stderr)
	
	#tedbot is the current package, and templates is the directory where templates live
	env = Environment(loader=PackageLoader('tedbot', 'templates'))
	template = env.get_template('talk.html')
	page = template.render(talk=talk)

	#create a filename with the current date/time
	filename = outputdir + talkdir
	filename += strftime("%Y%m%d%H%M", gmtime())
	filename += ".html"

	with open(filename, "w") as speechfile:
		speechfile.write(page)

def rebuildIndex():
	#open the talks folder
	#get a list of all the files inside
	#for each file, get its filename, title, and lead image
	#pass that object to the template renderer
	filename = outputdir + "index.html"
	env = Environment(loader=PackageLoader('tedbot', 'templates'))
	template = env.get_template('index.html')
	index = template.render(talklist=talklist)

	with open(filename, "w") as indexfile:
		indexfile.write(index)

def main():
	print(strftime("%a, %d %b %Y %H:%M:%S %Z", gmtime()), file=sys.stderr)
	print("Generating new talk", file=sys.stderr)
	
	makeNewPage()

	print("Regenerating index file", file=sys.stderr)

	#rebuildIndex()
	
	print("Done.", file=sys.stderr)

if __name__ == "__main__":
    main()