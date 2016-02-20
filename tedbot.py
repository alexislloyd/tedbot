from __future__ import print_function
import markovify
import sys

def createTalk(seed):
	with open("./transcripts.txt") as f:
		text = f.read()

	markovmodel = markovify.Text(text)

	speech = ""

	if seed:
		beginning = seed
		words = seed.split()
		if len(words) > 2:
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
		speech = firstsentence
	else:
		speech = beginning + " " + firstsentence
	speechlength = len(speech.split())
	sentences = 1

	while speechlength < 1800:
		newsentence = markovmodel.make_sentence()
		speech += " " + newsentence
		speechlength += len(newsentence.split())
		sentences +=1
		print(str(speechlength) + " - " + str(sentences), file=sys.stderr)

	speech = speech + "\n\nThank you.\n\n(Applause)"

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
