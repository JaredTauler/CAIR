from app import app, DEBUG
from flask import Flask, abort, redirect, url_for, render_template, request, session, jsonify, Blueprint
from datetime import date, datetime

import os
import hashlib
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
		try:
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

			elif rd["intent"] in ["save", "new"]:
				options = [
					("fname", 0),
					("lname", 0),
					("email", 0),
					("username", 0),
					("password", 0),
					("salt", 0)
				]

				pw, salt = function.password(rd["newpassword"])
				rd["password"] = pw.hex()
				rd["salt"] = salt.hex()

				if rd["intent"] == "save":
					s = ""
					for i in options:
						if i[1] == 0:
							s += (f" `{i[0]}` = '{rd[i[0]]}',")  # str
						elif i[1] == 1:
							s += (f" `{i[0]}` = {rd[i[0]]},")  # int
					s = s[:-1]  # Remove last char

					rq = (
						" UPDATE `user` SET "
						f"{s}"
						f" WHERE `id` = {rd['EntryBox']}"
					)

				else:
					colstr = ""
					valstr = ""
					for i in options:
						colstr += " " + i[0] + ","

						if i[1] == 0:
							valstr += (f" '{rd[i[0]]}',")  # str
						elif i[1] == 1:
							valstr += (f" {rd[i[0]]},")  # int
					valstr = valstr[:-1]  # Remove last char
					colstr = colstr[:-1]
					rq = (
						" INSERT INTO `user` "
						f" ({colstr}) "
						" VALUES "
						f" ({valstr}) "
					)
				database.Execute(rq, saving=True)

				return "", 200
		except Exception as e:
			print(e)
			return json.dumps({"error": str(e)}), 500

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
		try:
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


			elif rd["intent"] in ["save", "new"]:
				if rd.get("active") == "on": rd["active"] = 1
				else: rd["active"] = 0

				# with this setup, not every column has to be updated. TODO add on client

				options = [
					("fname", 0),
					("lname", 0),
					("id", 1),
					("school", 1),
					("active", 1)
				]

				if rd["intent"] == "save":
					s = ""
					for i in options:
						if i[1] == 0:
							s += (f" `{i[0]}` = '{rd[i[0]]}',")  # str
						elif i[1] == 1:
							s += (f" `{i[0]}` = {rd[i[0]]},")  # int
					s = s[:-1]  # Remove last char

					rq = (
						 " UPDATE `student` SET "
						 f"{s}"
						f" WHERE `id` = {rd['EntryBox']}"
					)
				else:
					colstr = ""
					valstr = ""
					for i in options:
						colstr += " " + i[0] + ","

						if i[1] == 0:
							valstr += (f" '{rd[i[0]]}',")  # str
						elif i[1] == 1:
							valstr += (f" {rd[i[0]]},")  # int
					valstr = valstr[:-1]  # Remove last char
					colstr = colstr[:-1]

					rq = (
						" INSERT INTO `student` "
						f" ({colstr}) "
						" VALUES "
						f" ({valstr}) "
					)
				print(rq)
				database.Execute(rq, saving=True)

				return "", 200
		except Exception as e:
			return json.dumps({"error": str(e)}), 500

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

		data["man"]["school"] = function.Schools(False)

		q = f"SELECT id, fname, lname FROM `student` WHERE `active` = 1"
		r = database.Execute(q, True)
		data["man"]["student"] = r

		q = f"SELECT id, fname, lname FROM `user`"
		r = database.Execute(q, True)
		data["man"]["user"] = r

		data["drop"]["action_type"] = function.GetAction()

		return render_template("report.html", values=json.dumps(data))

	else: # POST
		try:
			rd = request.form.to_dict()

			intent = rd.get("ReportDropdown")

			if rd["isMobile"] == "true":
				isMobile = True
			else:
				isMobile = False

			res = {}
			res["table"] = {}

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
				res["table"]["main"] = database.Execute(q, True)

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
				if r != {}:
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
					res["table"]["main"] = {0: [x]}

			elif intent == "action_type":
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
				res["table"]["main"] = database.Execute(q, auto_index=True)

			# School Statistics
			elif intent == "school_percent":
				action = rd.get("EntryDrop")

				school = rd["EntryDrop"]
				if school != "all":
					q = (
						" SELECT DISTINCT action_id, COUNT(action_id) "
						" FROM ticket "
						" JOIN student S on S.id = ticket.student_id "
						f" WHERE S.school = {school} "
					)

					if rd.get("DateStart"):
						q += function.ByDate(
							(rd.get("DateStart"), rd.get("DateEnd")),  # le dates
							True
						)

					q += (
						" GROUP BY action_id "
					)
					r = database.Execute(q, True)
					print(r)

				else:
					q = (
						" SELECT DISTINCT S.school, COUNT(S.school) "
						" FROM ticket JOIN student S on S.id = ticket.student_id "
					)

					if rd.get("DateStart"):
						q += function.ByDate(
							(rd.get("DateStart"), rd.get("DateEnd")),  # le dates
							False
						)

					q += " GROUP BY S.school "

				r = database.Execute(q, True)
				if r != {}:
					res["table"]["main"] = r

			print(json.dumps(res, default=json_serial))
			return json.dumps(res, default=json_serial), 200
		except Exception as e:
			return json.dumps({"error": str(e)}), 500

@app.route('/entry', methods = ["GET", "POST"])
def entry():
	if request.method == "GET":
		data = {}
		data["list"] = {}

		query = database.Execute(
			f"SELECT id, fname, lname, school FROM `student` WHERE `active` = 1", True
		)
		data["list"]["studentlist"] = query

		data["list"]["action"] = function.GetAction()

		return render_template("entry.html", values=json.dumps(data))

	else: # POST
		rd = request.form.to_dict()

		# Make sure student's ID is in DB. TODO There is probably a fancy SQL query that could check if the
		# student's id is in the DB and then insert if it is.
		query = database.Execute(
			f"SELECT id FROM `student` WHERE id = '{rd['student_id']}'"
		)
		if len(query) == 0:
			return "", 400


		print(session['id'])
		# Add ticket to database
		query = (
			"INSERT INTO `ticket` "
				"(`student_id`, `action_id`, `comment`, `info`, `date`, `timestamp`, `user_id`) "
			"VALUES "
				f"('{rd.get('student_id')}', '{rd.get('action')}', '{rd.get('comment')}', '{rd.get('info')}', '{rd.get('date')}', CURRENT_TIMESTAMP, '{session['id']}')"
			)

		val = database.Execute(query, saving=True)
		return "", 200 # Return OK


@app.route('/login', methods = ["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")

	# Login routine.
	else: # POST
		bad = {}
		bad["username"] = jsonify(["bad", "username"]), 200
		bad["password"] = jsonify(["bad", "password"]), 200
		# Get data from form
		requestdict = request.form.to_dict()
		if requestdict == {}: abort(406) # Abort on blank form.
		if requestdict["username"] == "": return bad["username"]
		if requestdict["password"] == "": return bad["password"]

		# Encode password
		requestdict['password'] = requestdict['password'].encode('utf-8')

		# Search database for given username.
		query = (
			f"SELECT `salt`, `password`, `id` FROM `user` "
			f"WHERE `username` = '{requestdict['username']}'"
		)
		res = database.Execute(
			query, auto_index=True
		)

		if res == {}:
			print("bad user")
			return jsonify(["bad", "username"]), 200
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
			print("bad password")
			return bad["password"]
