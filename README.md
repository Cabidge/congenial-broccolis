# Personal Library by Congenial Broccolis

## Roster
- Wen Hao Dong (PM) - Flask app
- Rachel Xiao - SQLite Database
- Austin Ngan - Flask app
- Liesel Wong - Bootstrap/Jinja

## Description
An online library containing a user selected list of books and movies. Each user has their own personal library, which has only the books and movies they themselves selected. The user can mark a book/movie as finished or not finished, and can choose to add more books/movies via a search.

## Launch Codes:

1. Activate virtual environment: `source <name>/bin/activate` or `source <name>/Scripts/activate` for Windows
   - If you don't have a virtual environment, create one: `python3 -m venv <name>`
2. Clone this repository: `git clone https://github.com/Cabidge/congenial-broccolis.git`
3. Cd into the repo directory: `cd congenial-broccolis`
4. Install the required modules: `pip install -r requirements.txt`
5. Cd into app directory: `cd app`
6. Start the Flask server: `python3 __init__.py`
7. In a browser, paste in `https://127.0.0.1:5000/`

## Demo Set-up:

1. Cd into app directory if not already in: `cd app`
2. Copy demo database file: `cp demo_database.db database.db`

This database file contains two premade accounts with a prefilled library of entries.
The account details are (username;password):
- demo;a
- demo2;a