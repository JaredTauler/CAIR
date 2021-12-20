from app import app
from flask import Flask, abort, redirect, url_for, render_template, request, session, jsonify, Blueprint
from datetime import date, datetime

import json

import database
import function



# Flask's "jsonify" serializes datetime objects into a stupid looking string. Using JSON library, I can
# tell the serializer what to do when there's a datetime object, in this case it returns as string in
# ISO 8601 format.

def Error400(comment):
	d = {}
	d["comment"] = comment
	return json.dumps(d), 400

def json_serial(obj):
	if isinstance(obj, (datetime, date)):
		return obj.isoformat()
	raise TypeError("Type %s not serializable" % type(obj))

@app.route('/worker_master', methods = ["GET", "POST"])
def worker_master():
	if request.method == "GET":
		data = {}
		q = f"SELECT id, fname, lname FROM `user`"
		r = database.Execute(q, True)
		data["user"] = r
		return render_template("worker_master.html", values=json.dumps(data))


	elif request.method == "POST":
		rd = request.form.to_dict()

		if rd["intent"] == "query":
			# EDITORS BEWARE:
			# The order in which columns are in queries is crucial to how the client loads the data.

			query = {} # data to give back to client.

			# TODO figure out how to combine DB queries.
			# Get data about the particular student
			id = rd["EntryBox"]
			rq = (
				' SELECT '
				' id, fname, lname, username, email'
				' FROM `user` '
				f' WHERE id = \'{id}\' '
			)
			query["man"] = database.Execute(rq, auto_index=True)

			if len(query["man"]) == 0:
				return Error400("Worker is not in database.")

			# Get related tickets
			table = function.Tickets(
				where=f" WHERE user_id = '{id}' "
			)

			if table:
				query["table"] = table

			return json.dumps(query, default=json_serial), 200


		elif rd["intent"] == "save":
			# with this setup, not every column has to be updated. TODO add on client
			str = ""
			options = [
				("fname", 0),
				("lname", 0),
				("id", 1),
				("email", 0),
				("username", 0)
			]

			for i, j in enumerate(options):
				if rd.get(j[0]) is None: continue # Skip if blank
				if j[1] == 0: str += (f" `{j[0]}` = '{rd[j[0]]}',") # str
				elif j[1] == 1: str += (f" `{j[0]}` = {rd[j[0]]},") # int
			str = str[:-1] # Remove last comma

			rq = (
				 " UPDATE `user` SET "
				 f"{str}"
				f" WHERE `id` = {rd['EntryBox']}"
			)
			val = database.Execute(rq, auto_index=True)

			return "", 200

@app.route('/student_master', methods = ["GET", "POST"])
def student_master():
	if request.method == "GET":
		data = {}
		q = f"SELECT id, fname, lname FROM `student` WHERE `active` = 1"
		r = database.Execute(q, True)
		data["student"] = r
		data["school"] = function.Schools() # Return schools
		return render_template("student_master.html", values=json.dumps(data))


	elif request.method == "POST":
		rd = request.form.to_dict()

		if rd["intent"] == "query":
			# EDITORS BEWARE:
			# The order in which columns are in queries is crucial to how the client loads the data.

			query = {} # data to give back to client.

			# TODO figure out how to combine DB queries.
			# Get data about the particular student
			id = rd["EntryBox"]
			rq = (
				' SELECT '
				' id, fname, lname, school, active'
				' FROM `student` '
				f' WHERE id = \'{id}\' '
			)
			query["man"] = database.Execute(rq, auto_index=True)

			if len(query["man"]) == 0:
				return Error400("Student is not in database.")

			if id:
				where = f" WHERE student_id = '{id}' "
			else:
				where = False

			# Get student tickets
			table = function.Tickets(where)

			# add table if its not empty
			if table:
				query["table"] = table

			# Return all this crap to client.
			return json.dumps(query, default=json_serial), 200


		elif rd["intent"] == "save":
			if rd.get("active") == "on": rd["active"] = 1
			else: rd["active"] = 0

			# with this setup, not every column has to be updated. TODO add on client
			str = ""
			options = [
				("fname", 0),
				("lname", 0),
				("id", 1),
				("school", 1),
				("active", 1)
			]

			for i, j in enumerate(options):
				print(rd[j[0]])
				if j[1] == 0: str += (f" `{j[0]}` = '{rd[j[0]]}',") # str
				elif j[1] == 1: str += (f" `{j[0]}` = {rd[j[0]]},") # int
				if i == len(options) - 1: str = str[:-1] # Remove last char , if the last object in loop

			rq = (
				 " UPDATE `student` SET "
				 f"{str}"
				f" WHERE `id` = {rd['EntryBox']}"
			)
			val = database.Execute(rq, auto_index=True)

			return "", 200


# YUTA do homepage
@app.route('/home', methods = ["GET", "POST"])
def home():
	return render_template("home.html")


@app.route('/logout', methods = ["POST"])
def logout():
	# No need to check if given session has id. guide() should take care of that.
	session.pop("id")
	return "", 200


@app.route('/report', methods = ["GET", "POST"])
def report():
	if request.method == "GET":
		data = {}

		q = f"SELECT id, fname, lname FROM `student` WHERE `active` = 1"
		r = database.Execute(q, True)
		data["student"] = r

		q = f"SELECT id, fname, lname FROM `user`"
		r = database.Execute(q, True)
		data["user"] = r

		return render_template("report.html", values=json.dumps(data))

	else: # POST
		rd = request.form.to_dict()

		if rd["isMobile"] == "true":
			isMobile = True
		else:
			isMobile = False

		res = {}
		table = {}

		# Return all of a user's tickets.
		if rd.get("ReportDropdown") == "user":
			# Add where clause
			entry = rd.get("EntryBox")
			if entry is None or entry == "":
				where = f" WHERE user_id = '{session['id']}' "
			else:
				where = f" WHERE user_id = '{entry}' "

			# Get tickets.
			res["table"] = function.Tickets(
				where,
				(rd.get("DateStart"), rd.get("DateEnd"))
			)

		# Just return student's names + school
		elif rd.get("ReportDropdown") == "name":
			q = (
				" SELECT id, fname, lname, school "
				" FROM student "
			)
			table["man"] = database.Execute(q, True)

			table["school"] = function.Schools(False)

			res["table"] = table

		# Return a student's tickets.
		elif rd.get("ReportDropdown") == "student":
			entry = rd.get('EntryBox')
			if entry:
				where = f" WHERE student_id = '{entry}' "
			else:
				where = False

			# Get tickets.
			res["table"] = function.Tickets(
				where,
				(rd.get("DateStart"), rd.get("DateEnd"))
			)

		return json.dumps(res, default=json_serial), 200

# FIXME refactor this page
@app.route('/entry', methods = ["GET", "POST"])
def entry():
	if request.method == "GET":
		data = {}
		data["list"] = {}

		query = database.Execute(
			f"SELECT id, fname, lname, school FROM `student`", True
		)
		data["list"]["studentlist"] = query

		query = database.Execute(
			f"SELECT id, type FROM `action`", True
		)
		data["list"]["action"] = query

		return render_template("entry.html", values=data)

	else: # POST
		try:
			class DBerror(Exception): pass

			rd = request.form.to_dict()
			print(rd)
			# Prevent SQL injection.
			if not rd['student_id'].isnumeric(): return "", 400
			# TODO secure other stuff

			# Make sure student's ID is in DB. TODO There is probably a fancy SQL query that could check if the
			# student's id is in the DB and then insert if it is.
			query = database.Execute(
				f"SELECT id FROM `student` WHERE id = '{rd['student_id']}'"
			)
			if len(query) == 0:
				return "", 400

			# Add ticket to database
			# try:
			query = database.Execute(
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
				return jsonify(["redirect", url_for("home")]), 200

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


# TODO temporary
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
