# -*- coding: utf-8 -*-
from __future__ import print_function
from jinja2 import Environment, PackageLoader
import sys
import json
from tedbot import createTalk

def main():
	talk = createTalk()
	print("Got a talk. Writing to speech.html", file=sys.stderr)
	
	#tedbot is the current package, and templates is the directory where templates live
	env = Environment(loader=PackageLoader('tedbot', 'templates'))
	template = env.get_template('test.html')
	page = template.render(talk=talk)

	with open("speech.html", "w") as speechfile:
		speechfile.write(page)
	print("Done.", file=sys.stderr)

if __name__ == "__main__":
    main()