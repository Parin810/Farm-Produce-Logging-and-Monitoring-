'''
*
* Project: 	   		Farm Produce: Logging and Monitoring
* Author: 			Bhavesh Jadav
* Filename:    		send.py
* Functions: 			None
* Global Variables:	None
*
'''

#Thsi python script is used for sending data back to server

import MySQLdb as sqldb #import mysql library

try:
	#connect to server database. Change host according to the server IP and smae for the user, password and database
	serverdb = sqldb.connect(host = "169.254.48.23", user = "bhavesh", passwd = "123456789", db = "opencart", connect_timeout = 5)
	#connect to local database
	localdb = sqldb.connect("localhost", "root", "firebird", "maindb")

	#create cursor object for both server and local database
	serverc = serverdb.cursor()
	localc = localdb.cursor()

	#fetch all the data from local database which is not sent to server database
	localc.execute("SELECT * FROM data WHERE sent = 0")
	result = localc.fetchall()
	
	#go through each row which is not sent to server and perform the following steps
	#1) update e-commerce website by updating its quantity
	#2) send all data
	#3) set sent = 1 after data has succesfullly transfered 
	for row in result:
		serverc.execute("UPDATE opencart.oc_product SET quantity = quantity + %s WHERE product_id = %s", (row[4], row[1]))
		serverc.execute("INSERT INTO data (troughid, cropid, name, date, weight, imagepath, location) VALUES (%s, %s, %s, %s, %s, %s, %s)", (row[0], row[1], row[2], row[3], row[4], row[5], row[7]))
		localsql = "UPDATE data SET sent = 1 WHERE cropid = %s" % (row[1])
		localc.execute(localsql)
	
	serverdb.commit()
	localdb.commit()
	
except:
	print "failed"
	serverdb.rollback()
	localdb.rollback()
	serverdb.close()
	localdb.close()


