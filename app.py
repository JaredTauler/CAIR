import json
import os

import sqlalchemy
import yaml

from flask import Flask, abort, redirect, request, redirect, url_for, render_template, request, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

# import pusher
import hashlib

# pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
print(os.chdir("C:\\Users\\Student\\PycharmProjects\\CAIR"))
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
	# Serve login page.
	if request.method == "GET":
		return render_template("login.html")

	# Login routine.
	else:
		class BadPassword(Exception): pass
		class BadUsername(Exception): pass
		try:
			# Get data from form
			requestdict = request.form.to_dict()
			# Abort on blank form.
			if requestdict["username"] == "": raise BadUsername()
			if requestdict["password"] == "": raise BadPassword()
			if requestdict == {}: abort(406)

			# Encode password, wont need to look directly at it.
			requestdict['password'] = requestdict['password'].encode('utf-8')

			# Search database for given username.
			query = db.engine.execute(
				f"SELECT salt, password FROM `user` "
				f"WHERE username is '{requestdict['username']}'"
			)

			# 0 index in case more than one result. Out of scope to worry about more than one user with same ID.
			fetch = query.fetchall() # Running fetchall() once clears query for some reason.
			if fetch == []:
				raise BadUsername()
			else:
				result = fetch[0]

			fromDB = {}
			fromDB["salt"] = bytes.fromhex(result[0]) # Go ahead and convert salt to bytes.
			fromDB["password"] = result[1]

			# Hash password given from form using salt from database.
			hashed = hashlib.pbkdf2_hmac(
				'sha256',
				requestdict['password'],
				fromDB["salt"],
				100000
			)

			hashed = hashed.hex() # To hex.

			# If password from form == password in DB login user.
			if hashed == fromDB["password"]:
				session["logged_in"] = True
				return jsonify("Logged in"), 200

			else:
				raise BadPassword()

		except Exception as e:
			if type(e) == BadPassword: info = jsonify({"bad": "password"})
			elif type(e) == BadUsername: info = jsonify({"bad": "username"})
			else: info = jsonify({"bad": "unknown"})

			return info, 200


@app.route("/newuser", methods = ["GET", "POST"])
def Usermake():
	print(request.form.getlist('username[]'))
	# password hashing
	username = "hi"
	email = "bruh"
	salt = os.urandom(32)
	print(salt.hex())
	password = "a"
	hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

	db.engine.execute(
		"INSERT INTO `user` (`username`, `email`, `password`, `salt`)"
		f"VALUES ('{username}', '{email}', '{hashed.hex()}', '{salt.hex()}')"
	)
	return "made dummy"



# @app.route("/push")
# def push():
# 	pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

# @pusher_client.trigger()

# Start
if __name__ == '__main__':
	# TODO certificates.
	app.run(debug=True)
