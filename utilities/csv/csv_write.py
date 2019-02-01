import csv
import sys
sys.path.insert(0, "/root/Oauthkeeper/src")

from SqlConnections import connection

def get_all_contacts( username=None, status=None, number=None, company=None ):
	
	sql_query = " SELECT USERID, NAME, COMPANY, MOBILE, EMAIL, ADDRESS, STATUS, PERMISSIONS, HRCOUNT FROM CONTACTS "
	is_none = 0

	# When there are username filters
	if username != None and username!= "Username":

		is_none += 1
		sql_query += "WHERE PERMISSIONS LIKE '%{USERNAME}%' ".format(USERNAME=username)

	# When there are status filters
	if status != None and status!= "All":

		is_none += 1
		if is_none == 1:
			sql_query += "WHERE "
		else:
			sql_query += " AND "

		sql_query += "STATUS LIKE '{STATUS}' ".format(STATUS=status)
	
	# When there are mobile number filters.
	if number != None:
		
		is_none += 1
		if is_none == 1:
			sql_query += "WHERE "
		else:
			sql_query += " AND "

		sql_query += "MOBILE LIKE '%{MOBILE}%' ".format(MOBILE=number)
	
	# When there are company name filters.
	if company != None:
		
		is_none += 1
		if is_none == 1:
			sql_query += "WHERE "
		else:
			sql_query += " AND "

		sql_query += "COMPANY LIKE \"%{COMPANY}%\" ".format(COMPANY=company)

	# We add the final semicolon.
	sql_query += ";"
	conn = connection()
	cursor = conn.cursor()

	try:
		cursor.execute(sql_query)
		conn.close()
	
	except Exception as e:
		conn.close()
		print(e)

	#We write to the CSV file here.
	f = open("demofile.txt", "w")

	for USERID, NAME, COMPANY, MOBILE, EMAIL, ADDRESS, STATUS, PERMISSIONS, HRCOUNT in cursor.fetchall():
		str = "{NAME},{COMPANY},{MOBILE},{EMAIL},{HRCOUNT}\n".format(NAME=NAME.strip(), COMPANY=COMPANY.strip(), MOBILE=MOBILE.strip(), EMAIL=EMAIL.strip(), HRCOUNT=HRCOUNT)
		f.write(str)

get_all_contacts(status="Emailed/Confirmed")
