# Congenial Broccolis: Wen Hao Dong (Jal Hordan), Austin Ngan (Gerald), Liesel Wong (King Hagrid), Rachel Xiao (Mooana)
# SoftDev
# P01 -- ArRESTed Development
# 2021-12-10

from flask import Flask, request, redirect, render_template, session
app = Flask(__name__)


@app.route("/")
def home():
	if loggedIn():
		return 1 #will change



def loggedIn():
	return "user" in session


@app.route("/login")
def login():
	if loggedIn():
		return redirect("/")
		
	if request.method == 'GET':
		return "hello"
        
	username = request.form["username"]
	password = request.form["password"]
    
	if username.strip() == "" or password.strip == "":
		return "" #should return something that tells user they cannot have a blank user/pass
    
	user_id = database.fetch_user_id(username, password)
	if user_id is None:
		return "1" #shold return page telling user that something is incorrect
    	
	return "login"
		

@app.route("/logout")
def logout():
	if loggedIn():
		session.pop("user")
	return redirect("/")


@app.route("/signup")
def signup():
    return "signup"


if __name__ == "__main__":
    app.debug = True
    app.run()
