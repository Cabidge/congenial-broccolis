from urllib.request import Request, urlopen
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
