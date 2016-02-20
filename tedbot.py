from __future__ import print_function
import markovify
import sys
import math
import random
import re
import flickrapi
import yaml
import json
from pattern.en import parse
from pattern.en import tag

GRAF_LENGTH = 8
GRAF_RANGE = 3
DEBUG = True

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
    flickr_key = cfg['flickr']['api_key']
    flickr_secret = cfg['flickr']['api_key']

# generate a target length for a paragraph, of the range LENGTH +/- [0-RANGE]
def initTarget():
	return GRAF_LENGTH + int(math.floor(random.triangular(0-GRAF_RANGE, GRAF_RANGE)))

def getImage(refstring):
	tagged = tag(refstring)

	nouns = [word for word,pos in tagged if pos == 'NNP' or pos == 'NP' or pos == 'NN']
	try:
		query = random.choice(nouns)
	except IndexError:
		#somehow this string has no nouns!
		if DEBUG: print("Paragraph with no nouns:\n" + refstring, file=sys.stderr)
		return None
	
	if DEBUG: print(query, file=sys.stderr)

	flickr = flickrapi.FlickrAPI(flickr_key, flickr_secret, format='parsed-json')
	result = flickr.photos_search(api_key = flickr_key, text = query, privacy_filter = 1, safe_search=1, sort='interestingness-desc', orientation="landscape")
	try:
		pick = random.choice(result['photos']['photo'])
		url = 'https://farm' + str(pick['farm']) + '.staticflickr.com/' + str(pick['server']) + '/' + str(pick['id']) + '_' + str(pick['secret']) + '_z.jpg'
	except IndexError:
		# there were no results, so the random.choice call failed above. This is OK, we'll just move on.
		url = None

	return url

#given a list of sentences, return a list of paragraphs
def graphize(sentences):
	grafs = []
	currentgraf = ""
	counter = 0
	target = initTarget()

	for sentence in sentences:
		currentgraf += sentence
		if counter == target:
			if DEBUG: print("Ending a graf after " + str(target) + " lines.", file=sys.stderr)
			grafs.append(currentgraf)
			counter = 0
			target = initTarget()
			currentgraf = ""
		else:
			currentgraf += " "
			counter += 1

	grafs.append("Thank you.")
	grafs.append("(Applause)")

	return grafs


#get a list of sentences to make into a speech, then call a utility to format it
def createTalk(seed):
	with open("./transcripts.txt") as f:
		text = f.read()

	markovmodel = markovify.Text(text)

	speech = ""

	if seed:
		beginning = seed
		words = seed.split()
		if len(words) >= 2:
			end = len(words)
			seed = words[end-2] + " " + words[end-1]
		else:
			if len(words) == 1:
				seed += " " + seed
			else:
				seed = None
	print(seed, file=sys.stderr)
	try:
		firstsentence = markovmodel.make_sentence_with_start(beginning=seed)
	except KeyError: 
		firstsentence = None
	
	if firstsentence is None:
		print("Seed generated no results. Falling back.", file=sys.stderr)
		firstsentence = markovmodel.make_sentence()
	else:
		firstsentence = beginning + " " + firstsentence
	speechlength = len(firstsentence.split())
	sentences = [firstsentence]

	while speechlength < 1800:
		newsentence = markovmodel.make_sentence()
		speechlength += len(newsentence.split())
		sentences.append(newsentence)
		if DEBUG: print(str(speechlength) + " - " + str(len(sentences)), file=sys.stderr)

	grafs = graphize(sentences)
	slides = []
	for graf in grafs:
		slides.append({"image": getImage(graf), "text": graf})

	talk = {}
	talk['title'] = "title goes here"
	talk['slides'] = slides

	return json.dumps(talk)

def main():
	if len(sys.argv) == 1:
		print("TEDBot initiated without seed sentence. To start a speech with a specified opening, try " + sys.argv[0] + " \"Here is my opening sentence\".", file=sys.stderr)
		talk = createTalk(None)
	else:
		if len(sys.argv) > 2:
			print("usage: " + sys.argv[0] + "[\"opening sentence is optional\"]", file=sys.stderr)
			sys.exit()
		else:
			talk = createTalk(sys.argv[1])

	print(talk)


if __name__ == "__main__":
    main()
