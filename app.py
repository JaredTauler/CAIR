# Jared Tauler 10/20/21

import os
import yaml

# flask
from flask import Flask, abort, redirect, url_for, request, session
from flask_session import Session

os.chdir("C:\\Users\\Teacher\\PycharmProjects\\CAIR")

# Load config
with open("config.yaml", "r") as f:
	cfg = yaml.safe_load(f)

DBstr = cfg["DBstr"]
DEBUG = cfg["DEBUG"]

# Prepare app
app = Flask(__name__)

app.secret_key = os.urandom(16)
# db = SQLAlchemy(app)

app.config['SESSION_TYPE'] = "filesystem"

sess = Session(app)
import route

# Routes not logged in users can access.
# remember to keep this updated
NoLoginWhitelist = [
	"/login", "/home",
	"/static/login/login.css", "/static/base/base.css", "/static/common.css", "/static/header/header.css",
	"/static/login/login.js", "/static/base/base.js", "/static/header/header.js",
	"/static/berklogo.png", "/static/favicon.ico",
	"/static/popup/style.css", "/static/popup/main.js"

]

@app.before_request
def guide():
	if not session.get("id"): # If not logged in,
		if request.path == "/":  # If at root, redirect
			return redirect(url_for("login"))
		if not request.path in NoLoginWhitelist: # If accessing a whitelisted route,
			abort(401)
	else:
		if request.path == "/":
			return redirect(url_for("home"))

# For jinja
@app.template_global()
def static_include(filename):
	fullpath = os.path.join(app.static_folder, filename)
	with open(fullpath, 'r') as f:
		return f.read()

# Start
if __name__ == '__main__':
	app.run(debug=True)
