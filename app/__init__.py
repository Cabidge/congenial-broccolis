# Congenial Broccolis: Wen Hao Dong (Jal Hordan), Austin Ngan (Gerald), Liesel Wong (King Hagrid), Rachel Xiao (Mooana)
# SoftDev
# P01 -- ArRESTed Development
# 2021-12-10

from flask import Flask, request, redirect, render_template, session
import database
#from os import urandom

app = Flask(__name__)
app.secret_key = "foo"

def logged_in():
	"""
	Returns True if the user is in session.
	"""
	return "user" in session


@app.route("/")
def home():
	"""
	Displays user's library if they're logged in.
	"""
	if logged_in():
		entries = database.fetch_entries(session["user_id"]) #users' library
		return render_template("home.html", user=session["user"], library=entries)
	return render_template("login.html") #render login template because can't access home page without logging in


@app.route("/login", methods=['GET', 'POST'])
def login():
	"""
	Retrieves user login inputs and checks it against the "users" database table.
	Brings user to home page after successful login.
	"""
	if logged_in():
		return redirect("/")

	if request.method == 'GET':
		return render_template("login.html")

	username = request.form["username"]
	password = request.form["password"]

	#this may not be needed because bootstrap checks it for us
	if username.strip() == "" or password.strip() == "":
		return render_template("login.html", explain = "Username/Password cannot be blank")

	# Verify this user and password exists
	user_id = database.fetch_user_id(username, password)
	if user_id is None:
		return render_template("login.html", explain = "Username or Password is incorrect")

	# Adds user and user id to session if all is well
	session["user"] = database.fetch_username(user_id)
	session["user_id"] = user_id
	return redirect("/")


@app.route("/logout")
def logout():
	"""
	Removes user from session.
	"""
	if logged_in():
		session.pop("user")
		session.pop("user_id")
	return redirect("/")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	"""
	Retrieves user inputs from signup page.
	Checks it against the database to make sure the information is unique.
	Adds information to the "users" database table.
	"""
	if logged_in():
		return redirect("/")

	# Default page
	if request.method == "GET":
		return render_template("register.html")

	# Check sign up
	user = request.form["newusername"]
	pwd = request.form["newpassword"]
	if user.strip() == "" or pwd.strip == "":
		return render_template("register.html", explain="Please enter characters and/or numbers")

	# Add user information if passwords match
	if (request.form["newpassword"] != request.form["newpassword1"]):
		return render_template("register.html", explain="The passwords do not match")
	else:
		register_success = database.register_user(user, pwd) # checks if not successful in the database file

	if not register_success:
		return render_template("register.html", explain="Username already exists")
	else:
		return render_template("login.html")


@app.route("/search", methods=["POST"])
def search():
	"""
	Checks if user wants to search for a book or movie from Modal form.
	Retrieves title from user input and stores the results of the API search into the database.
	Returns the results of the search.
	"""
	if not logged_in():
		return redirect("/login")

	query = request.form["search-query"]
	media_type = request.form["media-type"]

	if query == "": #if title is blank
		return redirect("/")

	if media_type == "book":
		json = database.search_for_books(query)
	elif media_type == "movie":
		json = database.search_for_movies(query)

	return render_template("results.html", title=query, json=json, type=media_type)


@app.route("/book/<media_id>", methods=["GET", "POST"])
def display_book(media_id):
	"""
	Creates route to a specific book based its unique ID.
	Returns a specific page about the book.
	"""
	if not logged_in():
		return redirect("/login")
	if request.method == "GET":
		book = database.fetch_media(media_id, "book")
		return render_template("media.html", entry=book)
	elif request.method == "POST":
		print(database.add_to_library("book", session["user_id"], media_id))
		return redirect("/")


@app.route("/movie/<media_id>", methods=["GET", "POST"])
def display_movie(media_id):
	"""
	Creates route to a specific movie based its unique ID.
	Returns a specific page about the movie.
	"""
	if not logged_in():
		return redirect("/login")
	if request.method == "GET":
		movie = database.fetch_media(media_id, "movie")
		return render_template("media.html", entry=movie)
	elif request.method == "POST":
		print(database.add_to_library("movie", session["user_id"], media_id))
		return redirect("/")


@app.route("/update", methods=["POST"])
def update_library():
	table = {}
	for key, value in request.form.items():
		media_type, media_id = key.split("-")
		media_id = int(media_id)

		complete = value == "on"
		table[(media_type, media_id)] = complete

	completion_statuses = []
	for (media_type, media_id), complete in table.items():
		completion_statuses.append((media_type, media_id, complete))

	database.update_completion(session["user_id"], completion_statuses)
	return redirect("/")


if __name__ == "__main__":
	app.debug = True
	app.run()
