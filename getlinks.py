import sys
import urllib2
from bs4 import BeautifulSoup

def get_html(url):
	request = urllib2.Request(url)
	opener = urllib2.build_opener()
	return opener.open(request).read()

def main():

	for i in range(1,60):
		page_url = 'https://www.ted.com/talks?page='+str(i)
		html = get_html(page_url)
		soup = BeautifulSoup(html)
		divs = soup.find_all("h4", class_="h9 m5")
		for div in divs:
			link = div.find('a')['href']
			print 'http://www.ted.com' + link + '/transcript?language=en'

	

if __name__ == "__main__":
	main()