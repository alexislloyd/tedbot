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
from twython import Twython

DEBUG = True

with open("config.yml", 'r') as ymlfile:
	cfg = yaml.load(ymlfile)
	outputdir = cfg['export']['root']
	talkdir = cfg['export']['talkdir']
	siteurl = cfg['export']['siteurl']
	twitter_api = cfg['twitter']['api_key']
	twitter_secret = cfg['twitter']['secret']
	twitter_access = cfg['twitter']['access_token']
	twitter_access_secret = cfg['twitter']['access_token_secret']
	aws_key = cfg['aws']['key']
	aws_secret = cfg['aws']['secret']
	aws_bucket = cfg['aws']['bucket']

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

def s3upload():
	# move everything in the output directory, including all in the talks directory, using os.walk

	from boto.s3.connection import S3Connection, OrdinaryCallingFormat
	from boto.s3.key import Key

	conn = S3Connection(aws_key, aws_secret, calling_format=OrdinaryCallingFormat())
	bucket = conn.get_bucket(aws_bucket)

	for root, dirs, files in os.walk(outputdir):
		for filename in files:
			path = root[len(outputdir):]
			if DEBUG: print("Saving " + os.path.join(path,filename) + " from " + os.path.join(root,filename), file=sys.stderr)

			key = bucket.new_key(os.path.join(path,filename))
			key.set_contents_from_filename(os.path.join(root,filename), policy='public-read')

def main():
	print(strftime("%a, %d %b %Y %H:%M:%S %Z", gmtime()), file=sys.stderr)
	print("Generating new talk", file=sys.stderr)
	
	talk = makeNewPage()

	print("Regenerating index file", file=sys.stderr)

	rebuildIndex()

	print("Moving files to S3", file=sys.stderr)

	s3upload()

	print("Tweeting link to new talk at " + talk['url'], file=sys.stderr)

	#Tweet link here -- title is in talk['title']
	twitter = Twython(twitter_api, twitter_secret, twitter_access, twitter_access_secret)
	tweet = talk['title'] + ' ' + talk['url']
	twitter.update_status(status=tweet)
	
	print("Done.", file=sys.stderr)

if __name__ == "__main__":
	main()