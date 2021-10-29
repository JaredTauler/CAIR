import json
import os
import re

import yaml
from sqlalchemy import create_engine

from flask import Flask, abort, redirect, request, redirect, url_for, render_template, request, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

# import pusher
import hashlib

# pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
# os.chdir("C:\\Users\\Student\\PycharmProjects\\CAIR")
os.chdir("C:\\Users\\Jared\\PycharmProjects\\CAIR")
with open("config.yaml", "r") as f:
	cfg = yaml.safe_load(f)

DBstr = cfg["DBstr"]
DEBUG = cfg["DEBUG"]

class Database():
	def __init__(self, engine):
		self.engine = engine

	def execute(self, query, ForJSON=False):
		with self.engine.connect() as connection:
			result = connection.execute(query).cursor
			description = result.description
			fetch = result.fetchall()

		if not ForJSON:
			return fetch

		# Prepare the data for JSON serialization
		else:
			row_headers = [x[0] for x in description]
			json_data = []
			for result in fetch:
				json_data.append(dict(zip(row_headers, result)))
		return json_data

# Prepare app
app = Flask(__name__)
app.secret_key = os.urandom(16)
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SQLALCHEMY_DATABASE_URI'] = DBstr
app.config["SESSION_SQLALCHEMY"] = db

sess = Session(app)
db.create_all()
database = Database(db.engine)


# Main Program
@app.route("/", methods = ["GET"])
def guide():
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	else:
		return redirect(url_for("entry"))



@app.route('/entry', methods = ["GET", "POST"])
def entry():
	if not session.get("logged_in"):
		return redirect(url_for("login"))

	if request.method == "GET":
		data = {}
		data["list"] = {}

		query = database.execute(
			f"SELECT id, fullname FROM `school` ", True
		)
		data["list"]["school"] = query
		query = database.execute(
			f"SELECT id, fname, lname, school FROM `student`", True
		)
		data["list"]["studentlist"] = query
		print(query)
		query = database.execute(
			f"SELECT id, description FROM `action`", True
		)
		data["list"]["action"] = query



		return render_template("entry.html", values=data)

	else: # POST
		print(request.form.to_dict())
		rd = request.form.to_dict()
		'''
If the student is selected from the dropdown, client will return the student's ID in the database.
If a students name is typed, name will be searched for in database, if that fails will ask user if they want
to create a new entry.

Unfortunately this makes an assumption that the student ID's will never have letters in them.
		'''

		class DBerror(Exception): pass

		# TODO robust?
		name = rd["student_id"]
		if not name.isnumeric(): # If ID is a name rather than an ID number,
			# Split in 2.
			fname, lname = name.split(maxsplit=1)

			# Leave only letters behind.
			fname = re.sub('[^a-zA-Z]+', '', fname)
			lname = re.sub('[^a-zA-Z]+', '', lname)


			query = database.execute(
				f"SELECT id, fname, lname FROM `student` WHERE `fname` REGEXP '{fname}' OR `lname` REGEXP '{lname}'",
				True
			)
			if len(query) == 0:
				raise DBerror()
			else:
				return jsonify({"result": "pick", "query": query}), 200

		else:
			query = database.execute(
				f"SELECT id FROM `student` WHERE id IS '{name}'"
			)
			if len(query) == 0:
				raise DBerror()

		# query = database.execute(
		# 	"INSERT INTO `ticket` "
		# 		"(`student_id`, `action`, `comment`, `info`)"
		# 	"VALUES "
		# 		f"('{rd['student']}', '{email}', '{hashed.hex()}', '{salt.hex()}')"
		# )


		return "", 200


@app.route('/login', methods = ["GET", "POST"])
def login():
	print(request.method)
	# if session.get("logged_in"):
	# 	return redirect(url_for("entry"))

	# Serve login page.
	if request.method == "GET":
		return render_template("login.html")

	# Login routine.
	else: # POST
		class BadPassword(Exception): pass
		class BadUsername(Exception): pass
		try:
			# Get data from form
			requestdict = request.form.to_dict()
			print(requestdict)
			if requestdict == {}: abort(406) # Abort on blank form.
			if requestdict["username"] == "": raise BadUsername()
			if requestdict["password"] == "": raise BadPassword()

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
				print("Logged in")
				return jsonify(["redirect", url_for("guide")]), 200

			else:
				raise BadPassword()

		except Exception as e:
			if type(e) == BadPassword: info = "password"
			elif type(e) == BadUsername: info = "username"
			else: # Unknown error
				if DEBUG == True: # Dont handle excepection if debug mode
					raise e
				info = "unknown"

			return jsonify(["bad", info]), 200


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
	app.run(debug=True)
