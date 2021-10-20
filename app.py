import os

import sqlalchemy
import yaml

from flask import Flask, abort, redirect, request, redirect, url_for, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

import pusher
import hashlib

# pusher_client = pusher.Pusher(
#   app_id='1278094',
#   key='61e4aab53292a02cf890',
#   secret='ad98e29be2d755447478',
#   cluster='us2',
#   ssl=True
# )

# pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

with open("config.yaml", "r") as f:
	cfg = yaml.safe_load(f)
DBstr = cfg["DBstr"]
#
# try:
# 	c = create_engine(DBstr)
# raise:
# Error

app = Flask(__name__)
app.secret_key = os.urandom(16)
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SQLALCHEMY_DATABASE_URI'] = DBstr
app.config["SESSION_SQLALCHEMY"] = db

sess = Session(app)
db.create_all()


# Main Program
@app.route('/', methods = ["GET", "POST"])
@app.route('/login', methods = ["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else:
		return ('', 204)

@app.route("/newuser", methods = ["GET", "POST"])
def Usermake():
	print(request.data)
	# password hashing
	username = "hi"
	email = "bruh"
	salt = os.urandom(32)
	password = "a"
	hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

	db.engine.execute(
		"INSERT INTO `user` (`username`, `email`, `password`, `salt`)"
		f"VALUES ('{username}', '{email}', '{hashed.hex()}', '{salt.hex()}')"
	)
	return "made dummy"

	# # Store hashed and salt as hex in the database.
	# ExecuteDB(
	# 	f"INSERT INTO `ticketsystem`.`user` (`username`, `email`, `password`, `salt`) VALUES \
	#     ('{form['username']}', '{form['email']}', '{hashed.hex()}', '{salt.hex()}')"
	# 	, engine)



# @app.route("/push")
# def push():
# 	pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

# @pusher_client.trigger()

# Start
if __name__ == '__main__':
	# TODO certificates.
	app.run(debug=True)
