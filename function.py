import re
from database import Execute
import os
import hashlib

### DB operations

# Goal of this function is to take some input and find students that match said input.
def StudentSearch(phrase, school=False, active=False):
	rq = (
		"SELECT " 
    	"id, fname, lname "
		"FROM "
    	"student "
		"WHERE "
	)
	if active:
		rq += "(active = 1) AND "

	if school:
		rq += f"(school = {school}) AND " # Add school

	rq += (
		f"(fname RLIKE '{phrase}' "
		"OR "
		f"lname RLIKE '{phrase}') "
	)

	return Execute(rq)

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

def GetAction():
	return Execute(
		f"SELECT id, type FROM `action`", False
	)

def Schools(auto_index=True):
	q = (
		"SELECT id, fullname FROM `school`"
	)
	r = Execute(q, auto_index)
	return r

def ByDate(dater, HasWhere):
	s = ""
	if not HasWhere:
		s += " WHERE "
	elif HasWhere:
		s += " AND "
	if dater[1]:
		s += (
			" date BETWEEN " 
			f" '{dater[0]}' " 
			" AND " 
			f" '{dater[1]}' "
		)
	else:
		s += (
			f" date = '{dater[0]}'"
		)
	return s


def Find_ID(res, icol):
	# Determine which ID's need to be looked up in the DB.
	# Shameful to do a loop on this but I dont know SQL well enough to write a slick query that could do this
	# the proper way.
	# I feel like this is better than bothering the database into doing a join on the previous query to get
	# data fom different tables.
	seen = {}
	str = {}
	for c in icol:
		seen[c] = []
		str[c] = ""

	for i, row in enumerate(res.values()):
		for c in icol: # for passed columns
			if row[c] not in seen[c]:
				seen[c].append(row[c])
				str[c] += f" {row[c]},"

	# del last comma from every str
	for i in str:
		str[i] = str[i][:-1]

	return str


# TODO mobile data different: no info or comment.
def Tickets(where, dater=None):
	# Data for on screen table.
	table = {}

	# Get tickets.
	rq = (
		" SELECT "
		" id, date, action_id, info, user_id, student_id "
		" FROM `ticket` "
	)
	# Add where
	if where:
		rq += where

	# date range thingy (i sleepy ok)
	if dater:
		if dater[0]:
			rq += ByDate(dater, where)

	table["main"] = Execute(rq)

	if len(table["main"]) == 0:  # No tickets
		return False

	String = Find_ID(
		table["main"], (1, 3, 4)
	)
	# Get users related to query.
	rq = (
		" SELECT DISTINCT id, fname, lname FROM `user` "
		f" WHERE id IN ({String[3]}) "
	)
	table["join"] = {}
	table["join"]["user"] = Execute(rq)

	# Get students related to the query.
	rq = (
		" SELECT DISTINCT id, fname, lname FROM `student` "
		f" WHERE id IN ({String[4]}) "
	)
	table["join"]["student"] = Execute(rq)

	# Get actions related to the query.
	rq = (
		" SELECT DISTINCT id, type FROM `action` "
		f" WHERE id IN ({String[1]}) "
	)
	table["join"]["action"] = Execute(rq)

	return table

def password(password):
	salt = os.urandom(32)
	hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
	return hashed, salt
