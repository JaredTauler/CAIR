from app import DBstr
import mysql.connector

# FIXME return ISO8601 from DB rather than a date object, i feel this would be more efficient.
def Execute(query, auto_index=False, saving = False):
	with Conn() as cnx:
		cur = cnx.cursor()
		cur.execute(query)

		if saving:
			cnx.commit()
			return
		else:
			result = cur.fetchall()

	if result is []:
		return True # if no result (e.g. INSERT)
	json_data = {}

	def func(i, row):
		json_data[i] = row
	# possible to do this without a loop?
	if auto_index:
		for i, row in enumerate(result):
			func(i, row)
	else:
		for row in result:
			# "row[1:]" is targeting between 2nd and last item.
			func(row[0], row[1:])

	return json_data

def Conn():
	return mysql.connector.connect(
		**{k: str(DBstr[k]) for k in DBstr.keys()}
	)

# def Cur():
#
#
# print(Execute(
# 	f"SELECT * FROM `ticket`", False
# ))
