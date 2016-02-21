from __future__ import print_function
import flask
import sys
import json
from tedbot import createTalk

def main():
	talk = createTalk()
	print("Got a talk. Writing to speech.json", file=sys.stderr)
	with open("speech.json", "w") as speechfile:
		speechfile.write(json.dumps(talk))
	print("Done.", file=sys.stderr)

if __name__ == "__main__":
    main()