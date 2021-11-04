import json
import os
import re

import datetime
import yaml
from sqlalchemy import create_engine

from flask import Flask, abort, redirect, request, redirect, url_for, render_template, request, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

# import pusher
import hashlib

# pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
os.chdir("C:\\Users\\Student\\PycharmProjects\\CAIR")
# os.chdir("C:\\Users\\Jared\\PycharmProjects\\CAIR")
with open("config.yaml", "r") as f:
	cfg = yaml.safe_load(f)

DBstr = cfg["DBstr"]
DEBUG = cfg["DEBUG"]

class Database():
	def __init__(self, engine):
		self.engine = engine

	def execute(self, query, ForJSON=False, NoResult=False, Columns=None):
		with self.engine.connect() as connection:
			result = connection.execute(query).cursor
			if NoResult:
				return True
			fetch = result.fetchall()

		if not ForJSON:
			return fetch

		# Prepare the data for JSON serialization
		else:
			if Columns is None:
				description = result.description
				row_headers = [x[0] for x in description]
			else:
				row_headers = Columns
			json_data = []
			for result in fetch:
				json_data.append(dict(zip(row_headers, result)))
		return json_data


def IsDate(item):
	if type(item) is list:
		iter = item
	else:
		iter = []
		iter.append(item)

	for i in iter:
		i = i.replace("-", "")  # remove dashes
		if not i.isnumeric:  # Not a number
			return False

	return True


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
@app.template_global()
def static_include(filename):
	fullpath = os.path.join(app.static_folder, filename)
	with open(fullpath, 'r') as f:
		return f.read()


@app.route("/", methods = ["GET"])
def guide():
	if not session.get("id"):
		return redirect(url_for("login"))
	else:
		return redirect(url_for("report"))


@app.route('/report', methods = ["GET", "POST"])
def report():
	if request.method == "GET":
		data = {}
		data["list"] = {}

		query = database.execute(
			f"SELECT id, fname, lname FROM `student`", True
		)
		data["list"]["studentlist"] = query
		return render_template("report.html", values=data)

	else: # POST
		rd = request.form.to_dict()

		if rd.get("ByDate") == "on":
			# SQL Injection Prevention
			if not IsDate(
				[rd.get("DateStart"), rd.get("DateEnd")]
			):
				return "", 400
			else:
				ByDate = True
		else:
			ByDate = False

		# Return all of a user's tickets.
		if rd.get("ReportDropdown") == "user":

			id = session['id']

			col = ["user_fname", "user_lname", "date", "student_fname", "student_lname", "type"]
			rq = \
				"SELECT c.fname, c.lname, date, a.fname, a.lname, b.type FROM ticket " \
				"INNER JOIN student a on ticket.student_id = a.id " \
				"INNER JOIN action b on ticket.action_id = b.id " \
				"INNER JOIN user c on ticket.user_id = c.id " \
				f"WHERE user_id = '{id}' "

			if ByDate:
				rq += \
					" AND date BETWEEN " \
					f" '{rd['DateStart']}' " \
					" AND " \
					f" '{rd['DateEnd']}' "


			query = database.execute(rq, True, Columns=col)
			from datetime import date, datetime

			# TODO do this in other places?
			def json_serial(obj):
				if isinstance(obj, (datetime, date)):
					print(obj.isoformat())

					return obj.isoformat()
				raise TypeError("Type %s not serializable" % type(obj))

			# Flask's "jsonify" serializes datetime objects into a stupid looking string. Using JSON library, I can
			# tell the serializer what to do when there's a datetime object, in this case it returns as string in
			# ISO format.
			return json.dumps(query, default=json_serial), 200

		# Just return student's names
		elif rd.get("ReportDropdown") == "name":
			query = database.execute(
				"SELECT fname, lname, t.shortname "
				"FROM student "
				"INNER JOIN school t on student.id = t.id",
				True
			)
			print(query)

		# Return a student's tickets.
		elif rd.get("ReportDropdown") == "student":
			# Check here because only need it here.
			if not rd.get("student_id").isnumeric():
				return "", 400

			id = rd["student_id"]
			col = ["fname", "lname", "type", "date"]
			rq = \
				"SELECT student.fname, student.lname, action.type, date FROM `ticket` " \
				"INNER JOIN `student` on ticket.student_id = student.id " \
				f"INNER JOIN `action` on ticket.action_id = action.id WHERE student_id = '{id}' "

			if ByDate:
				rq += \
					" AND date BETWEEN " \
					f" '{rd['DateStart']}' " \
					" AND " \
					f" '{rd['DateEnd']}' "

			query = database.execute(rq, True, Columns= col)

		# Impossible
		else:
			return "", 400

		return jsonify(query), 200



@app.route('/entry', methods = ["GET", "POST"])
def entry():
	if not session.get("id"):
		return redirect(url_for("login"))

	if request.method == "GET":
		data = {}
		data["list"] = {}

		query = database.execute(
			f"SELECT id, fname, lname, school FROM `student`", True
		)
		data["list"]["studentlist"] = query

		query = database.execute(
			f"SELECT id, type FROM `action`", True
		)
		data["list"]["action"] = query

		return render_template("entry.html", values=data)

	else: # POST
		try:
			class DBerror(Exception): pass

			rd = request.form.to_dict()

			# Prevent SQL injection.
			if not rd['student_id'].isnumeric(): return "", 400
			# TODO secure other stuff

			# Make sure student's ID is in DB. TODO There is probably a fancy SQL query that could check if the
			# student's id is in the DB and then insert if it is.
			query = database.execute(
				f"SELECT id FROM `student` WHERE id = '{rd['student_id']}'"
			)
			if len(query) == 0:
				return "", 400

			# Add ticket to database
			# try:
			query = database.execute(
				"INSERT INTO `ticket` "
					"(`student_id`, `action_id`, `comment`, `info`, `date`, `timestamp`, `user_id`) "
				"VALUES "
					f"('{rd.get('student_id')}', '{rd.get('action')}', '{rd.get('comment')}', '{rd.get('info')}', '{rd.get('date')}', CURRENT_TIMESTAMP, '{session['id']}')",
				NoResult=True
			)
			# except:
			# 	raise DBerror()

			# No need to check query. If there was an error inserting then there will be an exception.


			return "", 200 # Return OK

		except Exception as e:
			if DEBUG:  # Dont handle excepection if debugging
				raise e
			info = "unknown"

			return jsonify(["bad", info]), 200


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
				f"SELECT `salt`, `password`, `id` FROM `user` "
				f"WHERE `username` = '{requestdict['username']}'"
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
			fromDB["id"] = result[2]

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
				session["id"] = fromDB["id"]
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
