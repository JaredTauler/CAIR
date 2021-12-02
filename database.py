from app import db
engine = db.engine

# FIXME return ISO8601 from DB rather than a date object, i feel this would be more efficient.
def Execute(query, auto_index=False):
	with engine.connect() as connection:
		result = connection.execute(query).cursor
		if result is None:
			return True # if no result (e.g. INSERT)
		fetch = result.fetchall()

	json_data = {}

	def func(i, row):
		json_data[i] = row

	# TODO possible to do this without a loop?
	if auto_index:
		for i, row in enumerate(fetch):
			func(i, row)
	else:
		for row in fetch:
			# "row[1:]" is targeting between 2nd and last item.
			func(row[0], row[1:])

	return json_data
