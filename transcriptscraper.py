import sys
import urllib2
from bs4 import BeautifulSoup

def get_html(url):
	request = urllib2.Request(url)
	opener = urllib2.build_opener()
	try:
		result = opener.open(request).read()
		return result
	except urllib2.URLError, e:
		print 'Error: ' + str(e.reason)

def main():

	#read in all the links
	text_file = open("links.txt", "r")
	links = text_file.read().split('\n')
	print len(links)
	text_file.close()

	#open transcripts.txt for appending
	f = open('transcripts.txt', 'a')

	for link in links:
		html = get_html(link)	
		if html:
			print 'Parsing '+link
			output = ''
			soup = BeautifulSoup(html, "html.parser")
			paras = soup.find_all("span", class_="talk-transcript__para__text")
			for p in paras:
				for fragment in p.find_all("span", class_="talk-transcript__fragment"):
					output += fragment.string + " " 
				output += "\n\n"
			f.write(output.encode('ascii', 'ignore'))
			print ("success \n\n")
			

if __name__ == "__main__":
	main()