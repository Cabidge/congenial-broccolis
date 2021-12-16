from urllib import request
import json

keys = {}
# keys.txt is a file containing all of the api keys
with open("keys.txt") as f:
	for line in f:
		# List destructuring
		[k, v] = line.rstrip().split("=")
		keys[k] = v


def imdb_search(expression):
	req = request.Request(f"https://imdb-api.com/en/API/SearchMovie/{keys['imdb']}/{expression}", headers={"User-Agent": "Mozilla/5.0"})
	page = request.urlopen(req)
	url_dict = json.loads(page.read())
	return url_dict


def nyt_search(expression):
	page = request.urlopen(f"https://api.nytimes.com/svc/books/v3/reviews.json?author={author}&api-key={keys['nyt']}") #f string to add key to the url
	url_dict = json.loads(page.read())
	return url_dict
