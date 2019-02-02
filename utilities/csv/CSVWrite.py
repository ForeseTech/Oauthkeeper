import csv
import sys
sys.path.insert(0, "/root/Oauthkeeper/src")

from SqlConnections import connection

# Generates a CSV file of all contacts.
def generate_contacts( username=None, status=None, number=None, company=None ):
	
	sql_query = " SELECT * FROM CONTACTS "
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

	# We add the final ordering and semicolon.
	sql_query += "ORDER BY PERMISSIONS;"

	#We now execute the query in thr SQL server.
	conn = connection()
	cursor = conn.cursor()

	try:
		cursor.execute(sql_query)
		conn.close()
	
	except Exception as e:
		conn.close()
		print(e)

	#We write to the CSV file here.
	f = open("/root/Oauthkeeper/static/csv/database-contacts.csv", "w")
	f.write("HR Name,Company,Mobile,Email,Address,Status,HR Count, Second-Year\n");

	#All the results are written to the file here.
	for USERID, NAME, COMPANY, MOBILE, EMAIL, ADDRESS, STATUS, PERMISSIONS, HRCOUNT in cursor.fetchall():
		
		str = "\"{NAME}\",\"{COMPANY}\",{MOBILE},{EMAIL},\"{ADDRESS}\",{STATUS},\"{PERMISSIONS}\",{HRCOUNT}\n".format( NAME=NAME, COMPANY=COMPANY, MOBILE=MOBILE, EMAIL=EMAIL, ADDRESS=ADDRESS, STATUS=STATUS, PERMISSIONS=PERMISSIONS, HRCOUNT=HRCOUNT )

		f.write(str)
