import flickrapi
import yaml
from pattern.en import parse
from pattern.en import tag
import random

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
    flickr_key = cfg['flickr']['api_key']
    flickr_secret = cfg['flickr']['api_key']

tagged = tag("As a boy in Lima, my grandfather told me a legend of the Spanish conquest of Peru.")

nouns = [word for word,pos in tagged if pos == 'NNP' or pos == 'NP' or pos == 'NN']
query = random.choice(nouns)
print query

flickr = flickrapi.FlickrAPI(flickr_key, flickr_secret, format='parsed-json')

result = flickr.photos_search(api_key = flickr_key, text = query, privacy_filter = 1, safe_search=1, sort='interestingness-desc', orientation="landscape")

pick = random.choice(result['photos']['photo'])

url = 'https://farm' + str(pick['farm']) + '.staticflickr.com/' + str(pick['server']) + '/' + str(pick['id']) + '_' + str(pick['secret']) + '_z.jpg'
print url