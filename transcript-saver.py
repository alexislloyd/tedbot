import sys
import urllib2
from BeautifulSoup import BeautifulSoup

__version__ = '0.1'
__project_name__ = 'TedTranscriptExtractor'
__project_link__ = 'http://gist.github.com/786849'

TED_TALK_URL = 'http://www.ted.com/index.php/talks/'

def get_html(url):
	request = urllib2.Request(url)
	request.add_header('User-Agent', '%s/%s +%s' % (
		__project_name__, __version__, __project_link__
	))
	opener = urllib2.build_opener()
	return opener.open(request).read()

def main(talk_url):
	if not talk_url.startswith('http://'):
		talk_url = TED_TALK_URL + talk_url
	
	html = get_html(talk_url)
	
	soup = BeautifulSoup(html)
	
	transcript = soup.find('div', attrs={'id': 'transcriptText'})
	
	for p in transcript.findAll('p'):
		print ''.join(p.findAll(text=True))
		print

if __name__ == "__main__":
	talk_url = sys.argv[-1]
	main(talk_url)  