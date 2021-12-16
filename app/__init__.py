# Congenial Broccolis: Wen Hao Dong (Jal Hordan), Austin Ngan (Gerald), Liesel Wong (King Hagrid), Rachel Xiao (Mooana)
# SoftDev
# P01 -- ArRESTed Development
# 2021-12-10

from flask import Flask, request, redirect, render_template, session
import database
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(32)

def logged_in():
	return "user" in session


@app.route("/")
def home():
	if logged_in():
		return render_template("home.html", user=session["user"], library="")
	return render_template("login.html") #render login template because can't access home page without logging in


@app.route("/login", methods=['GET', 'POST'])
def login():
	if logged_in():
		return redirect("/")

	if request.method == 'GET':
		return render_template("login.html")

	username = request.form["username"]
	password = request.form["password"]

	if username.strip() == "" or password.strip() == "":
		return "render login template with error about not having blank fields"

	# Verify this user and password exists
	user_id = database.fetch_user_id(username, password)
	if user_id is None:
		return "render login template with error about the user not existing or the info is wrong"

	# Adds user and user id to session if all is well
	session["user"] = database.fetch_username(user_id)
	session["user_id"] = user_id
	return redirect("/")


@app.route("/logout")
def logout():
	if logged_in():
		session.pop("user")
		session.pop("user_id")
	return redirect("/")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
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


@app.route("/searchMovie")
def search_movie():
	searchQ = request.form["search"]
	movie_dict = api.imdb_search(searchQ)
	return "returns template with every entry from api"
	#WIP	

@app.route("/searchBook")
def search_book():
	searchQ = request.form["search"]
	book_dict = api.nyt_search(searchQ)
	return "returns template with every entry from api"
	#WIP

if __name__ == "__main__":
	app.debug = True
	app.run()
