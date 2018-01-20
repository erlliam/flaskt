import sqlite3
from flask import Flask, render_template, g, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = "flaskt.db"

def get_db():
	db = getattr(g, "_database", None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

@app.route("/")
def index():
	return(render_template("index.html"))

@app.route("/signup", methods=["POST", "GET"])
def signup():
	if request.method == "POST":
		db = get_db()
		cursor = db.cursor()
		username = request.form["username"].lower()
		db_search = cursor.execute("SELECT username, password FROM accounts WHERE username=?", (username, )).fetchone()
		if db_search is None:
			cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, generate_password_hash(request.form["password"])))
			db.commit()
		else:
			print("Username taken")
	return(render_template("signup.html"))

@app.route("/login")
def login():
	if request.method == "POST":
		db = get_db()
		cursor = db.cursor()
	return(render_template("login.html"))

@app.route("/post")
def post():
	return(render_template("post.html"))

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, "_database", None)
	if db is not None:
		db.close()