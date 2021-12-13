# Congenial Broccolis: Wen Hao Dong (Jal Hordan), Austin Ngan (Gerald), Liesel Wong (King Hagrid), Rachel Xiao (Mooana)
# SoftDev
# P01 -- ArRESTed Development
# 2021-12-10

from flask import Flask
app = Flask(__name__)


@app.route("/")
def home():
    return "home"


@app.route("/login")
def login():
    return "login"


@app.route("/signup")
def signup():
    return "signup"


if __name__ == "__main__":
    app.debug = True
    app.run()