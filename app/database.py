import sqlite3
import api

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
cur = db.cursor()

cur.execute("""
	CREATE TABLE IF NOT EXISTS users(
	  id INTEGER PRIMARY KEY,
	  username TEXT,
	  password TEXT)""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS movies(
	  id INTEGER PRIMARY KEY,
	  title TEXT,
	  cover_url TEXT)""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS books(
	  id INTEGER PRIMARY KEY,
	  title TEXT,
	  cover_url TEXT,
	  author TEXT)""")

cur.execute("""
	CREATE TABLE IF NOT EXISTS entries(
	  id INTEGER PRIMARY KEY,
	  type TEXT,
	  user_id INTEGER,
	  media_id INTEGER,
	  complete BOOLEAN)""")

db.commit()
db.close()

#####################
#                   #
# Utility Functions #
#                   #
#####################


def fetch_user_id(username, password):
	"""
	Gets the id of the user with the given username/password combination from the database.
	Returns None if the combination is incorrect.
	"""
	db = sqlite3.connect(DB_FILE)

	# The following line turns the tuple into a single value (sqlite3 commands always return a tuple, even when it is one value)
	# You can read more about row_factory in the official docs:
	# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
	db.row_factory = lambda curr, row: row[0]
	c = db.cursor()

	c.execute("""
		SELECT id
		FROM   users
		WHERE  LOWER(username) = LOWER(?)
		AND    password = ?
	""", (username, password))

	# user_id is None if no matches were found
	user_id = c.fetchone()

	db.close()

	return user_id


def register_user(username, password):
	"""
	Tries to add the given username and password into the database.
	Returns False if the user already exists, True if it successfully added the user.
	"""
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	c.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,))
	row = c.fetchone()

	if row is not None:
		return False

	c.execute("""INSERT INTO users(username,password) VALUES(?, ?)""",(username,password))
	db.commit()
	db.close()
	return True


def fetch_username(user_id):
	"""
	Returns the username of the user with the given id.
	"""
	db = sqlite3.connect(DB_FILE)
	db.row_factory = lambda curr, row: row[0]
	c = db.cursor()

	c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
	username = c.fetchone()

	db.close()
	return username


def fetch_media(media_id, media_type):
	"""
	Returns a dictionary containing the information of the media.
	It should also have a key "type" with the value of what media type it is.
	"""
	db = sqlite3.connect(DB_FILE)
	db.row_factory = sqlite3.Row
	c = db.cursor()

	table = ""
	if media_type == "book":
		table = "books"
	elif media_type == "movie":
		table = "movies"
	else:
		return None

	c.execute("""
		SELECT *
		FROM   ?
		WHERE  id = ?""", (table, media_id))

	media = c.fetchone()

	db.close()

	if media is None:
		return

	media = dict(media)
	media["type"] = media_type

	return media


def search_for_movies(title):
	"""
	Searches for movies with the matching title using the imdb api.
	The movie information is then stored in the movies table.
	Returns a list of dictionaries with the title, id, and cover_url.
	"""
	json = api.imdb_search(title)
	if json is None:
		return []

	res = json["results"]
	movies = []
	for result in res:
		movie = {}
		movie["id"] = int(result["id"][2:])
		movie["title"] = f"{result['title']} {result['description']}"
		movie["cover_url"] = result["image"]
		movies.append(movie)

	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	for movie in movies:
		c.execute("""
			INSERT OR REPLACE INTO movies(id, title, cover_url)
				VALUES(:id, :title, :cover_url)""", movie)

	db.commit()
	db.close()

	return movies


def join_nouns(nouns):
	"""
	Joins a list of strings into a single string with commas and an 'and'.
	eg. ["Hamzah", "Bethaney", "Elliot"] -> "Hamzah, Bethaney and Elliot"
	Used for joining author names.
	"""
	if len(nouns) == 0:
		return ""

	if len(nouns) == 1:
		return nouns[0]

	s = nouns[0]
	for noun in nouns[1:-1]:
		s += ", " + noun
	s += " and " + nouns[-1]

	return s


def search_for_books(title):
	"""
	Searches for books with the matching title using the openlibrary api.
	The book information is then stored in the books table.
	Returns a list of dictionaries with the title, id, cover_url, and author.
	"""
	json = api.ol_search(title)
	if json is None:
		return []

	res = json["docs"]

	books = []
	for result in res:
		book = {}
		work_id = result["key"].split("/")[-1]
		book["id"] = int(work_id[2:-1])
		book["title"] = result["title"]
		if "cover_i" in result:
			book["cover_url"] = f"https://covers.openlibrary.org/b/id/{result['cover_i']}-L.jpg"
		else:
			book["cover_url"] = "https://islandpress.org/sites/default/files/default_book_cover_2015.jpg"
		if "author_name" in result:
			book["author"] = join_nouns(result["author_name"])
		else:
			book["author"] = "No Author"

		books.append(book)

	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	for book in books:
		c.execute("""
			INSERT OR REPLACE INTO books(id, title, cover_url, author)
				VALUES(:id, :title, :cover_url, :author)""", book)

	db.commit()
	db.close()

	return books


def fetch_entries(user_id):
	"""
	Returns a list of dictionaries in the same format as fetch_media,
	all of which come from entries made by the user with the given user_id.
	"""

	db = sqlite3.connect(DB_FILE)
	c = db.cursor()

	c.execute("""
		SELECT media_id
		     , media_type
		FROM   entries
		WHERE  user_id = ? """, (user_id,))

	entries_data = c.fetchall()

	entries = []
	for media_id, media_type in entries_data:
		media = fetch_media(media_id, media_type)
		if media is not None:
			entries.append(media)

	db.commit()
	db.close()

	return entries


def add_to_library(type, user_id, media_id):
    """
    Adds entry to entries table with its corresponding information refering to a specific user.
    This adds a book or movie to a user's library
    """
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    complete = False # media shouldn't be completed by default
    c.execute("INSERT INTO entries(type, user_id, media_id, complete) VALUES (?,?,?,?)", (type, user_id, media_id, complete))


    db.commit()
    db.close()

    return True
