from urllib.request import Request, urlopen
from urllib import request
import requests
import json

keys = {}
# keys.txt is a file containing all of the api keys
with open("keys.txt") as f:
	for line in f:
		# List destructuring
		[k, v] = line.rstrip().split("=")
		keys[k] = v


def imdb_search(expression):
	req = Request(f"https://imdb-api.com/en/API/SearchMovie/{keys['imdb']}/{expression}", headers={"User-Agent": "Mozilla/5.0"})
	page = urlopen(req)
	url_dict = json.loads(page.read())
	return url_dict

def nyt_search(expression):
	page = request.urlopen(f"https://api.nytimes.com/svc/books/v3/reviews.json?author={author}&api-key={keys['nyt']}") #f string to add key to the url
	url_dict = json.loads(page.read())
	return url_dict

author = ""
for c in "Marcel Proust":
	if (c == " "):
		author += "+"
	else:
		author += c
print(author)
#print(nyt_search(author)['results'])

urls = []
for d in nyt_search(author)['results']: #results is a dictionary of dictionaries of book review information
	urls.append(d['url']) #each dictionary has a url key
print(urls) #dictionary
