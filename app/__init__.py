# Congenial Broccolis: Wen Hao Dong (Jal Hordan), Austin Ngan (Gerald), Liesel Wong (King Hagrid), Rachel Xiao (Mooana)
# SoftDev
# P01 -- ArRESTed Development
# 2021-12-10

from flask import Flask, request, redirect, render_template, session
import database
from os import urandom

app = Flask(__name__)
app.secret_key = "hello"

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
		return render_template("login.html", explain = "Username/Password cannot be blank")

	# Verify this user and password exists
	user_id = database.fetch_user_id(username, password)
	if user_id is None:
		return render_template("login.html", explain = "Password/Username is incorrect.")

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


@app.route("/movie", methods=['GET', 'POST'])
def search_movie():
	if not logged_in():
		return redirect("/login")
	searchM = request.form["searchM"]
	movie_dict = database.search_for_movies(searchM)
	return render_template("results.html", title=searchM, json=movie_dict)
	#WIP


@app.route("/book", methods=['GET', 'POST'])
def search_book():
	if not logged_in():
		return redirect("/login")
	searchB = ""
	book_dict = []
	if "searchB" in request.form:
		searchB = request.form["searchB"]
		book_dict = database.search_for_books(searchB)
	if "add" in request.form:
		print("yas")

	return render_template("results.html", title=searchB, json=book_dict)
	#WIP


if __name__ == "__main__":
	app.debug = True
	app.run()
