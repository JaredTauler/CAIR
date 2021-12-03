import re
from database import Execute
### DB operations
# Goal of this function is to take input and find students.
# def StudentSearch(engine):



def Schools():
	q = (
		"SELECT id, fullname FROM `school`"
	)
	r = Execute(q, True)
	return r
