# Congenial Broccolis: Wen Hao Dong (Jal Hordan), Austin Ngan (Gerald), Liesel Wong (King Hagrid), Rachel Xiao (Mooana)
# SoftDev
# P01 -- ArRESTed Development
# 2021-12-10

from flask import Flask, request, redirect, render_template, session
import database

app = Flask(__name__)


def logged_in():
	return "user" in session


@app.route("/")
def home():
	if logged_in():
		return render_template("home.html", user=session["user"], library="")
	return redirect("/login")


@app.route("/login")
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


@app.route("/signup")
def signup():
	if request.method == "GET":
		return render_template("register.html")
	#nUser = request.form[]
    #nPass = request.form[]
    #if nUser.strip() == "" or nPass.srip() == "":
	return "signup"


if __name__ == "__main__":
    app.debug = True
    app.run()
