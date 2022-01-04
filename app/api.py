from urllib import request
import urllib.parse
from urllib.error import HTTPError, URLError
import json

keys = {}
for key_name in ["imdb", "nyt", "google"]:
	with open("keys/key_" + key_name + ".txt") as f:
		keys[key_name] = f.read().strip()

imdb_endpoint = "https://imdb-api.com/en/API"
ol_endpoint = "http://openlibrary.org"

#encode_plus = urllib.parse.quote_plus
encode_query = urllib.parse.quote


def imdb_search(expression):
	"""
	Searches for movies on IMBD.
	Returns the json response.
	https://imdb-api.com/
	"""
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
	Returns a dictionary with a summary and link to the review.
	"""
	title = encode_query(expression)

	reviews = {}
	if type == "book":
		try:
			page = request.urlopen(f"https://api.nytimes.com/svc/books/v3/reviews.json?title={title}&api-key={keys['nyt']}") #f string to add key to the url
		except (HTTPError, URLError) as e:
			print("Error ocurred fetching from nyt api", e)
			return reviews

		url_dict = json.loads(page.read())
		if url_dict["results"] == None or len(url_dict["results"]) == 0:
			return {}
		try:
			reviews["summary"] = url_dict["results"][0]["summary"]
		except Exception as e:
			reviews["summary"] = ""
			reviews["link"] = ""
			print("Error ocurred fetching from SUMMARY nyt api", e)
			return reviews
		try:
			reviews["link"] = url_dict["results"][0]["url"]
		except Exception as e:
			reviews["link"] = ""
			print("Error ocurred fetching from LINK nyt api", e)
			return reviews
	else:
		try:
			page = request.urlopen(f"https://api.nytimes.com/svc/movies/v2/reviews/search.json?query={title}&api-key={keys['nyt']}")
		except (HTTPError, URLError) as e:
			print("Error ocurred fetching from nyt api", e)
			return reviews

		url_dict = json.loads(page.read())
		if url_dict["results"] == None or len(url_dict["results"]) == 0: #if there are not nyt search results
			return {}
		try:
			reviews["summary"] = url_dict["results"][0]["summary_short"]
		except Exception as e:
			reviews["summary"] = ""
			reviews["link"] = ""
			print("Error ocurred fetching from SUMMARY nyt api", e)
			return reviews
		try:
			reviews["link"] = url_dict["results"][0]["link"]["url"]
		except Exception as e:
			reviews["link"] = ""
			print("Error ocurred fetching from LINK nyt api", e)
			return reviews
	return reviews
#print(nyt_search("pale fire", "book"))


def google_search(expression):
	"""
	Searches for books using Google Books API.
	Returns a dictionary with the summary and pages of a book.
	"""
	title = encode_query(expression)

	try:
		page = request.urlopen(f"https://www.googleapis.com/books/v1/volumes?q={title}&key={keys['google']}") #f string to add key to the url
	except (HTTPError, URLError) as e:
		print("Error ocurred fetching from google api", e)
		return None

	url_dict = json.loads(page.read())
	info = {}
	try:
		info["summary"] = url_dict["items"][0]["volumeInfo"]["description"]
	except Exception as e:
		info["summary"] = ""
		info["pages"] = ""
		print("Error ocurred fetching SUMMARY from google json", e)
		return info
	try:
		info["pages"] = str(url_dict["items"][0]["volumeInfo"]["pageCount"]) + " pages"
	except Exception as e:
		info["pages"] = ""
		print("Error ocurred fetching PAGES from google json", e)
		return info
	return info
#print(google_search("it ends with us"))
