from app import app
from flask import Flask, abort, redirect, url_for, render_template, request, session, jsonify, Blueprint
from datetime import date, datetime

import json

import database
import function

# Flask's "jsonify" serializes datetime objects into a stupid looking string. Using JSON library, I can
# tell the serializer what to do when there's a datetime object, in this case it returns as string in
# ISO 8601 format.

def json_serial(obj):
	if isinstance(obj, (datetime, date)):
		# print(obj.isoformat())

		return obj.isoformat()
	raise TypeError("Type %s not serializable" % type(obj))

@app.route('/master', methods = ["GET", "POST"])
def master():
	if request.method == "GET":
		data = {}
		data["school"] = function.Schools() # Return schools
		return render_template("master.html", values=json.dumps(data))


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
				" SELECT " 
				" id, fname, lname, school, active" 
				" FROM `student` " 
				f" WHERE id = '{id}' "
			)
			val = database.Execute(rq, auto_index=True)
			if len(val) == 0:
				pass # TODO no student
			query["man"] = val

			table = {} # easier to read.

			# Get student's tickets.
			rq = (
				" SELECT " 
				" id, date, action_id, info, user_id " 
				" FROM `ticket` " 
			   f" WHERE student_id = '{id}' "
			)
			table["ticket"] = database.Execute(rq)

			# Dirty. Do not try at home. FIXME finish
			seen = []
			user = "("
			iter = table["ticket"].values()
			for i, row in enumerate(iter):
				if row[3] not in seen:
					seen.append(row[3])
					user += f" {row[3]},"
				if i == len(iter) -1:
					user = user[:-1]

			user += ")"

			print(user)
			# Get users related to query.
			rq = (
				" SELECT DISTINCT id, fname, lname FROM `user` " 			
			   f" WHERE id IN ({user}) "
			)
			table["user"] = database.Execute(rq)
			print(table["user"])
			# Get actions related to the query.
			rq = (
				" SELECT DISTINCT action_id, action.type FROM `ticket` " 
				" INNER JOIN `action` on ticket.action_id = action.id " 
				f" WHERE student_id = '{id}' "
			)
			table["action"] = database.Execute(rq)

			query["table"] = table

			# Return all this crap to client.
			return json.dumps(query, default=json_serial), 200

		elif rd["intent"] == "save":
			if rd.get("active") == "on": rd["active"] = 1
			else: rd["active"] = 0

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
		#FIXME this explodes sometimes?
		if not session.get("id"):
			return "", 400

		rd = request.form.to_dict()

		if rd["isMobile"] == "true":
			isMobile = True
		else:
			isMobile = False

		def ByDate(start, end, HadWhere):
			# if were getting by date...
			if rd.get("DateStartCheckbox") == "on":
				if not IsDate(start):
					return "", 400 #Ignore if doesnt look like a date.

				# End date?
				if rd.get("DateEndCheckbox") == "on":
					if not IsDate(end):
						return "", 400

				# only doing one date, end should be start
				else:
					end = start

				s = ""
				if not HadWhere:
					s+= " WHERE "
				elif HadWhere:
					s += " AND "
				s += \
					" date BETWEEN " \
					f" '{start}' " \
					" AND " \
					f" '{end}' "
				return s

			# Add nothing to string if not checkbox was false.
			else:
				return ""

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

		# Return all of a user's tickets.
		if rd.get("ReportDropdown") == "user":
			# Get tickets
			import time
			q = (
				"SELECT id, date, action_id, info, user_id FROM ticket "
			)

			entry = rd.get("EntryBox")
			if entry is None or entry == "":
				HadWhere = True
				q += f" WHERE user_id = '{session['id']}' "
			else:
				HadWhere = False
				q += f" WHERE user_id = '{entry}' "

			q += ByDate(
				rd.get("DateStart"), rd.get("DateEnd"), HadWhere
			)

			query = database.Execute(q)
			toc = time.perf_counter()
			return json.dumps(query, default=json_serial), 200

		# Just return student's names + school
		elif rd.get("ReportDropdown") == "name":
			query = database.execute(
				"SELECT fname, lname, t.shortname "
				"FROM student "
				"INNER JOIN school t on student.id = t.id",
				True
			)

		# Return a student's tickets.
		elif rd.get("ReportDropdown") == "student":
			if isMobile: # Mobile data
				col = ["fname", "lname", "type", "date"]
				HadWhere = False
				rq = \
					"SELECT student.fname, student.lname, action.type, date FROM `ticket` " \
					"INNER JOIN `student` on ticket.student_id = student.id " \
					f"INNER JOIN `action` on ticket.action_id = action.id "
			else: # 'Puter data
				col = ["fname", "lname", "type", "date", "info", "comment"]
				HadWhere = False
				rq = \
					"SELECT student.fname, student.lname, action.type, date, info, comment FROM `ticket` " \
					"INNER JOIN `student` on ticket.student_id = student.id " \
					f"INNER JOIN `action` on ticket.action_id = action.id "

			entry = rd.get('EntryBox')
			if entry is None or entry == "":
				pass

			# If not none and not numeric, 400
			elif not entry.isnumeric():
				return "", 400
			else:
				HadWhere = True
				rq += f" WHERE student_id = '{entry}' "

			rq += ByDate(
				rd.get("DateStart"), rd.get("DateEnd"), HadWhere
			)

			query = database.execute(rq, True, Columns= col)

		else:
			return "", 400

		return jsonify(query), 200


@app.route('/entry', methods = ["GET", "POST"])
def entry():
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
			print(rd)
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
