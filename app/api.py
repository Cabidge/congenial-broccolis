from urllib import request
import requests
import urllib.parse
from urllib.error import HTTPError, URLError
import json

keys = {}
# keys.txt is a file containing all of the api keys
with open("keys.txt") as f:
	for line in f:
		# List destructuring
		[k, v] = line.rstrip().split("=")
		keys[k] = v

imdb_endpoint = "https://imdb-api.com/en/API"
ol_endpoint = "http://openlibrary.org"

#encode_plus = urllib.parse.quote_plus
encode_query = urllib.parse.quote


def imdb_search(expression):
	# Makes the expression safe to put into query string
	expression = encode_query(expression)

	req = request.Request(f"{imdb_endpoint}/SearchMovie/{keys['imdb']}/{expression}", headers={"User-Agent": "Mozilla/5.0"})
	try:
		page = request.urlopen(req)
	except (HTTPError, URLError) as e:
		print("Error ocurred fetching from api", e)
		return None
	url_dict = json.loads(page.read())
	return url_dict


def ol_search(title, limit=12):
	"""
	Searches for books on OpenLibrary.
	Returns the json response.
	https://openlibrary.org/developers/api
	"""
	# Makes the expression safe to put into query string
	title = encode_query(title)

	try:
		page = request.urlopen(f"{ol_endpoint}/search.json?title={title}&limit={limit}") #f string to add key to the url
	except (HTTPError, URLError) as e:
		print("Error ocurred fetching from api", e)
		return None
	url_dict = json.loads(page.read())
	return url_dict


def nyt_search(expression, type):
	"""
	Searches for reviews based on type movies or books.
	"""
	title = ""
	for c in expression:
		if c == " ":
			title += "+"
		else:
			title += c
	page = ""
	if type == "book":
		page = request.urlopen(f"https://api.nytimes.com/svc/books/v3/reviews.json?title={title}&api-key={keys['nyt']}") #f string to add key to the url
	else:
		page = request.urlopen(f"https://api.nytimes.com/svc/movies/v2/reviews/search.json?query={title}&api-key={keys['nyt']}")
	url_dict = json.loads(page.read())
	return url_dict
#print(nyt_search("titanic", "movie")["results"][0]["link"]["url"])
