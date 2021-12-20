import re
from database import Execute

### DB operations

# TODO do
# Goal of this function is to take input and find students.
# def StudentSearch(engine):

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
	s += (
		" date BETWEEN " 
		f" '{dater[0]}' " 
		" AND " 
		f" '{dater[1]}' "
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
def Tickets(where, dater=()):
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

	# FIXME date dont work
	# if dater != ():
	# 	rq += ByDate(dater, where)

	table["ticket"] = Execute(rq)

	if len(table["ticket"]) == 0:  # No tickets
		return False

	String = Find_ID(
		table["ticket"], (1, 3, 4)
	)
	# Get users related to query.
	rq = (
		" SELECT DISTINCT id, fname, lname FROM `user` "
		f" WHERE id IN ({String[3]}) "
	)
	table["user"] = Execute(rq)

	# Get students related to the query.
	rq = (
		" SELECT DISTINCT id, fname, lname FROM `student` "
		f" WHERE id IN ({String[4]}) "
	)
	table["student"] = Execute(rq)

	# Get actions related to the query.
	rq = (
		" SELECT DISTINCT id, type FROM `action` "
		f" WHERE id IN ({String[1]}) "
	)
	table["action"] = Execute(rq)

	return table
