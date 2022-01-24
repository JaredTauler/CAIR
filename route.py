from app import app
from flask import Flask, abort, redirect, url_for, render_template, request, session, jsonify, Blueprint
from datetime import date, datetime

import os

import json

import database
import function

import hashlib



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

def OptionsIter(options, rd):
	str = ""
	for i, j in enumerate(options):
		if rd.get(j[0]) is None: continue  # Skip if blank
		if j[1] == 0:
			str += (f" `{j[0]}` = '{rd[j[0]]}',")  # str
		elif j[1] == 1:
			str += (f" `{j[0]}` = {rd[j[0]]},")  # int
	str = str[:-1]  # Remove last comma
	return str


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
			options = [
				("fname", 0),
				("lname", 0),
				("id", 1),
				("email", 0),
				("username", 0)
			]

			str = OptionsIter(options, rd)

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
		data["man"] = {}
		data["drop"] = {}

		q = f"SELECT id, fname, lname FROM `student` WHERE `active` = 1"
		r = database.Execute(q, True)
		data["man"]["student"] = r

		q = f"SELECT id, fname, lname FROM `user`"
		r = database.Execute(q)
		data["man"]["user"] = r

		data["drop"]["action"] = function.GetAction()

		return render_template("report.html", values=json.dumps(data))

	else: # POST
		rd = request.form.to_dict()

		intent = rd.get("ReportDropdown")

		if rd["isMobile"] == "true":
			isMobile = True
		else:
			isMobile = False

		res = {}
		table = {}

		# Return all of a user's tickets.
		if intent == "user":
			# Add where clause
			entry = rd.get("EntryBox")
			if entry is None or entry == "":
				# FIXME user's cookie need to be same as one in db. they will be different if worker master is used on user.
				where = f" WHERE user_id = '{session['id']}' "
			else:
				where = f" WHERE user_id = '{entry}' "

			# Get tickets.
			res["table"] = function.Tickets(
				where,
				(rd.get("DateStart"), rd.get("DateEnd"))
			)

		# Just return student's names + school
		elif intent == "name":
			q = (
				" SELECT id, fname, lname, school "
				" FROM student "
			)
			table["main"] = database.Execute(q, True)
			table["join"] = {}
			table["join"]["schools"] = function.Schools(False)

			res["table"] = table

		# Return a student's tickets.
		elif intent == "student":
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


		# Intervention Statistics
		elif intent == "action_average":
			action = rd.get("EntryDrop")
			# Find average number of days it take for a ticket to be closed.
			q = (
				" SELECT timestamp, closed FROM ticket_old "
			)
			if rd.get("DateStart"):
				q += function.ByDate(
					(rd.get("DateStart"), rd.get("DateEnd")),  # le dates
					False  # has no where!
				)
			r = database.Execute(q, True)

			def seconds(date):
				x = date - datetime(1900, 1, 1)
				return x.total_seconds()

			# create list of seconds, being difference between timestamp and closed date
			SecondsList = [
				seconds(i[1]) - seconds(i[0])
				for i in r.values()
			]

			# find median
			x = 0.0
			for i in SecondsList:
				x += i
			x = x / len(SecondsList)

			x = x // 86400  # floor divide magic number to turn seconds into days

			# prep for client.
			table["main"] = {0: x}
			res["table"] = table


		elif intent == "action":
			action = rd.get("EntryDrop")
			q = (
				" SELECT action_id, COUNT(action_id) FROM ticket "
			)
			HasWhere = False
			if action != "all":
				q += f" WHERE `action_id` = {action} "
				HasWhere = True
			if rd.get("DateStart"):
				q += function.ByDate(
					(rd.get("DateStart"), rd.get("DateEnd")),  # le dates
					HasWhere
				)
			q += " GROUP BY action_id "
			res = {}

			res["table"] = {}
			res["table"]["main"] = database.Execute(q, auto_index=True)
			print(res)

		return json.dumps(res, default=json_serial), 200

@app.route('/entry', methods = ["GET", "POST"])
def entry():
	DEBUG = False
	if request.method == "GET":
		data = {}
		data["list"] = {}

		query = database.Execute(
			f"SELECT id, fname, lname, school FROM `student`", True
		)
		data["list"]["studentlist"] = query

		data["list"]["action"] = function.GetAction()

		return render_template("entry.html", values=data)

	else: # POST
		rd = request.form.to_dict()

		# Make sure student's ID is in DB. TODO There is probably a fancy SQL query that could check if the
		# student's id is in the DB and then insert if it is.
		query = database.Execute(
			f"SELECT id FROM `student` WHERE id = '{rd['student_id']}'"
		)
		if len(query) == 0:
			return "", 400

		# Add ticket to database
		query = (
			"INSERT INTO `ticket` "
				"(`student_id`, `action_id`, `comment`, `info`, `date`, `timestamp`, `user_id`) "
			"VALUES "
				f"('{rd.get('student_id')}', '{rd.get('action')}', '{rd.get('comment')}', '{rd.get('info')}', '{rd.get('date')}', CURRENT_TIMESTAMP, '{session['id']}')"
			)

		val = database.Execute(query, auto_index=True)
		return "", 200 # Return OK


@app.route('/login', methods = ["GET", "POST"])
def login():
	DEBUG = True
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
			query = (
				f"SELECT `salt`, `password`, `id` FROM `user` "
				f"WHERE `username` = '{requestdict['username']}'"
			)
			res = database.Execute(
				query, auto_index=True
			)
			print(query)

			if res == {}:
				raise BadUsername()
			else:
				result = res[0]

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

	database.Execute(
		"INSERT INTO `user` (`username`, `email`, `password`, `salt`)"
		f"VALUES ('{username}', '{email}', '{hashed.hex()}', '{salt.hex()}')"
	)
	return "made dummy"
