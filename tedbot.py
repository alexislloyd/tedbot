from __future__ import print_function
import markovify
import sys
import math
import random
import re

GRAF_LENGTH = 8
GRAF_RANGE = 3
DEBUG = True

# generate a target length for a paragraph, of the range LENGTH +/- [0-RANGE]
def initTarget():
	return GRAF_LENGTH + int(math.floor(random.triangular(0-GRAF_RANGE, GRAF_RANGE)))

#given a list of sentences, create a long string broken up into paragraphs
def graphize(sentences):
	speech = ""
	counter = 0
	target = initTarget()

	for sentence in sentences:
		speech += sentence
		if counter == target:
			if DEBUG: print("Ending a graf after " + str(target) + " lines.", file=sys.stderr)
			speech += "\n\n"
			counter = 0
			target = initTarget()
		else:
			speech += " "
			counter += 1

	speech = speech + "\n\nThank you.\n\n(Applause)"

	return speech


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

	speech = graphize(sentences)

	return speech

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
