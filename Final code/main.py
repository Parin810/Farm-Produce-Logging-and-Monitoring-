'''
*
* Project: 	   		Farm Produce: Logging and Monitoring
* Author: 			Bhavesh Jadav
* Filename:    		main.py
* Functions: 			init()
*					tare()
*					calculateWeight()
*					displayWeight()
*					acceptCropID()
*					acceptTroughID()
*					acceptLocationID()
*					fetchCropInfo()
*					fetchCropInfoFromServer()
*					fetchTroughInfoFromServer()
*					takePicture()
*					storedata()
* Global Variables:	baseValue
*					taredWeight
*					imgName
*					measuredWeight
*					DOUT
*					toughID
*					cropID
*					cropName
*					locationName
*					troughIDExcepted
*					locationIDExcepted
*					cropIDExcepted
*					pictureTaken
*					active
* 					server
*
'''

import loadcell as lc #import load cell library
import MySQLdb as sqldb #import mysql library
import RPi.GPIO as GPIO
import lcd	#import lcd library
import kpad	#import keypad library
import time
import os
import math
import datetime
import sys

#address constant for lines in lcd display
LINE_1 = 0x80
LINE_2 = 0xC0
LINE_3 = 0x94
LINE_4 = 0xD4

#change below variable with server IP
server = "169.254.48.23"

baseValue = 0  #variable to store the base value of load cell
taredWeight = 0  #variable to store tared weight
imgName = 0  #variable to store image name
measuredWeight = 0.0  #variable to store calculated weight
DOUT = 22  #constant stores gpio pin used by dout pin of hx711. It will be used to check if hx711 is ready to send data or not
troughID = ""  #variable to sotre trough ID
locationID = "" #variable to sotre location ID
cropID = ""  #variable to store crop ID
cropName = ""  #variable to store crop name
locationName = ""  #variable to store location name

#Flag variables
troughIDExcepted = 0  #to check if trough id is accepted or not
locationIDExcepted = 0  #to check if location id is accepted or not
cropIDExcepted = 0	#to check if crop id is accepted or not
pictureTaken = 0	#to check if picture is taken or not
active = 1	#to check if program is active or not

#defining some database variable
host = "localhost"
username = "root"
password = "firebird"

#initialize lcd
lcd.lcd_init()

'''
*
* Function Name: 	calculateWeight
* Input: 				none
* Output: 			returns the calculated weight from the load cell value
* Logic: 				1) take the reading from load cell
*					2) take the difference between current value and base value
*					3) divide the difference with diference got with known weight
*					4) finally multiply the division answer with known weight value to get the weight
* Example Call:		calculateWeight()
*
'''
def caculateWeight():
	"function to calculate weight"
	global taredWeight
	global measuredWeight
	global baseValue
	val = lc.read_cell_value()  #read load cell value
	weight = ((baseValue - val) / 49000.0) * 230.0  #convert them into weight
	weight = weight - taredWeight  #remove tared weight from calculated weight
	if weight < 0:	#if weight becomes negative then set it back to zero
		weight = 0
	weight = int(weight)
	measuredWeight = weight	#sotre weight into measuredWeight variable
	return measuredWeight	#return the calculated weight

'''
*
* Function Name: 	displayWeight
* Input: 				none
* Output: 			none
* Logic: 				it displays weight on the lcd screen by using calculateWeight function
* Example Call:		displayWeight()
*
'''
def displayWeight() :
	"function to display weight on lcd screen"
	#if there is no weight on the platform display simple message
	if measuredWeight < 10:
		lcd.string("Place your object on", LINE_1)
		lcd.string("the platform", LINE_2)
	#else prompt user to continue by pressing * button
	else:
		lcd.string("Press * button to", LINE_1)
		lcd.string("continue.", LINE_2)
	lcd.string("Object weight is:", LINE_3)
	weight = caculateWeight()	#get calculated weight from the calculateWeight function
	lcd.string(str(weight) + " grams", LINE_4)	#display the weight on the lcd

'''
*
* Function Name: 	tare
* Input: 				none
* Output: 			none
* Logic: 				takes the current weight of the object and stores it in variable then it will be subtracted form current weight value
* Example Call:		tare()
*
'''
def tare():
	"function to tare weight"
	global baseValue
	global taredWeight
	lcd.clear()
	lcd.string("Taring weight...", LINE_1)
	lcval = lc.read_average_value(10)
	diff = math.fabs(baseValue- lcval)
	taredWeight = (diff / 49000.0) * 230.0  #store the calculated weight in variable

'''
*
* Function Name: 	takePicture
* Input: 				none
* Output: 			none
* Logic: 				takes picture using USB camera using fscam program
* Example Call:		takePicture()
*
'''
def takePicture():
	"fucntion to take picture using USB camera"
	global imgName
	global pictureTaken
	lcd.string("Taking picture...", LINE_2)
	if os.path.exists('/dev/video0'):
		#create image file name with current date
		imgName = "image-" + datetime.datetime.now().isoformat() + ".jpg"
		#capture image and save in images directory. if image file does not exists in folder then retake the image
		while os.path.isfile("/var/www/data/images/%s" %imgName) == False:
			os.system("fswebcam -r 640x480 -S 10 --no-banner /var/www/data/images/%s" %imgName)
		pictureTaken = 1  #if picture is successfully taken then set pictureTaken flag to 1
	else:	#if camera is not attached display error message
		lcd.clear()
		lcd.string("      FAILED", LINE_1)
		lcd.string("No camera attached", LINE_2)
		time.sleep(3)

'''
*
* Function Name: 	storeData
* Input: 				none
* Output: 			none
* Logic: 				stores the data into local database
* Example Call:		storeData()
*
'''
def storeData():
	"fuction to store data in database"
	global imgName
	lcd.string("Storing data...", LINE_3)
	try:
		#create instance of a database with host, username, password and database name
		db = sqldb.connect(host, username, password, 'maindb')
		#create cursor object
		cursor = db.cursor()
		img_path = "./images/" + imgName
		#insert values in database. isoformat() will give mysql compatible datetime object
		cursor.execute("INSERT INTO data (troughid, cropid, name, date, weight, imagepath, location) VALUES (%s, %s, %s, %s, %s, %s, %s)", (troughID, cropID, cropName, datetime.datetime.now().isoformat(), measuredWeight, img_path, locationName))
		db.commit()  #commit the changes
		lcd.clear()
		#lcd.string("Successfully stored", LINE_1)
		#lcd.string("in local database", LINE_2)
		lcd.string("      Success", LINE_2)
		time.sleep(1)
	except:
		lcd.clear()
		#lcd.string("Failed to store", LINE_1)
		#lcd.string("in local database", LINE_2)
		lcd.string("      FAILED", LINE_1)
		time.sleep(3)
	db.close()

'''
*
* Function Name: 	fetchCropInfo
* Input: 				none
* Output: 			none
* Logic: 				fetches the crop name and id from local database
* Example Call:		fetchCropInfo()
*
'''
def fetchCropInfo():
	"retrieves crop info through cropid info"
	global cropID
	global cropName
	global cropIDExcepted
	try:
		lcd.clear()
		lcd.string("Fetching crop info...", LINE_1)
		#create instance of a database with host, username, password and database name
		db = sqldb.connect("localhost", "root", "firebird", "maindb")
		#create cursor object
		cursor = db.cursor()
		cid = int(cropID)  #convert accepted crop id into integer
		sql = "SELECT name FROM cropinfo WHERE id = %d" % (cid)
		cursor.execute(sql)
		data = cursor.fetchone()
		#if there some crop exists with this id
		if data > 0:
			cropName = data[0]  #then assigh cropname to variable
			cropIDExcepted = 1	#set cropIDExcepted flag to one
			#lcd.clear()
			#lcd.string("Successfully fetched", LINE_1)
			#lcd.string("crop information", LINE_2)
			#time.sleep(0.5)
		else:  #if no crop exists with entered ID
			lcd.clear()
			lcd.string("Crop ID does not", LINE_1)
			lcd.string("exists!", LINE_2)
			lcd.string("Enter valid crop ID", LINE_3)
			time.sleep(3)
	except:  #if database connection Fails
		lcd.clear()
		lcd.string("      FAILED", LINE_1)
		lcd.string("Unable to connect to", LINE_2)
		lcd.string("local database", LINE_3)
		lcd.string("Try again later", LINE_4)
		time.sleep(3)
	db.close()

'''
*
* Function Name: 	acceptCropID
* Input: 				none
* Output: 			none
* Logic: 				accepts crop ID from user using keypad
* Example Call:		acceptCropID()
*
'''
def acceptCropID():
	"function to accept crop through keypad"
	global cropID
	lcd.clear()
	cropID = ""
	key = ""
	time.sleep(0.1)

	lcd.string("Enter Crop ID", LINE_1)
	lcd.string("Press * to continue", LINE_2)
	lcd.string("and # for backspace", LINE_3)
	#loop until some crop id is entered and * key is pressed. Following loop will run until valid crop id entered
	while  key != "*":
		lcd.string(cropID, LINE_4)
		key = kpad.get_key()
		if key == '*':
			if len(cropID) <= 0:
				lcd.clear()
				lcd.string("Crop ID cant", LINE_1)
				lcd.string("be null", LINE_2)
				time.sleep(3)
				lcd.clear()
				lcd.string("Enter Crop ID", LINE_1)
				lcd.string("Press * to continue", LINE_2)
				lcd.string("and # for backspace", LINE_3)
			else:
				break
		elif key == '#':  #for backspacing
			if len(cropID) > 0:
				cropID = cropID[:-1]
		elif key.isdigit():
			cropID += key
			time.sleep(0.2)
		key = ""
	#after accepting crop ID fetch crop information from local database
	fetchCropInfo()
	
'''
*
* Function Name: 	fetchLocationInfo
* Input: 				none
* Output: 			none
* Logic: 				fetches the location name and id from local database
* Example Call:		fetchLocationInfo()
*
'''
def fetchLocationInfo():
	"retrieves location info through locationid info"
	global locationID
	global locationName
	global locationIDExcepted
	try:
		lcd.clear()
		lcd.string("Fetching location...", LINE_1)
		#create instance of a database with host, username, password and database name
		db = sqldb.connect("localhost", "root", "firebird", "maindb")
		#create cursor object
		cursor = db.cursor()
		lid = int(locationID)  #convert accepted location id into integer
		sql = "SELECT locationname FROM locationinfo WHERE locationid = %d" % (lid)
		cursor.execute(sql)
		data = cursor.fetchone()
		#if there some location exists with this id
		if data > 0:
			locationName = data[0]  #then assigh locationname to variable
			locationIDExcepted = 1	#set locationIDExcepted flag to one
			#lcd.clear()
			#lcd.string("Successfully fetched", LINE_1)
			#lcd.string("location information", LINE_2)
			#time.sleep(0.5)
		else:  #if no location exists with entered ID
			lcd.clear()
			lcd.string("location ID does not", LINE_1)
			lcd.string("exists!", LINE_2)
			lcd.string("Enter valid location", LINE_3)
			lcd.string("ID", LINE_4)
			time.sleep(3)
	except:  #if database connection Fails
		lcd.clear()
		lcd.string("      FAILED", LINE_1)
		lcd.string("Unable to connect to", LINE_2)
		lcd.string("local database", LINE_3)
		lcd.string("Try again later", LINE_4)
		time.sleep(3)
	db.close()


'''
*
* Function Name: 	acceptLocationID
* Input: 				none
* Output: 			none
* Logic: 				accepts location ID from user using keypad
* Example Call:		acceptLocationID()
*
'''
def acceptLocationID():
	"function to accept locationid through keypad"
	global locationID
	global locationIDExcepted
	lcd.clear()
	locationID = ""
	key = ""
	time.sleep(0.1)
	lcd.string("Enter Location ID", LINE_1)
	lcd.string("Press * to continue", LINE_2)
	lcd.string("and # for backspace", LINE_3)
	#loop until some location id is entered and * key is pressed. Following loop will only break when valid location ID is entered
	while  key != "*":
		lcd.string(locationID, LINE_4)
		key = kpad.get_key()
		if key == '*':
			if len(locationID) <= 0:
				lcd.clear()
				lcd.string("Location ID can't", LINE_1)
				lcd.string("be null", LINE_2)
				time.sleep(3)
				lcd.clear()
				lcd.string("Enter Location ID", LINE_1)
				lcd.string("Press * to continue", LINE_2)
				lcd.string("and # for backspace", LINE_3)
			else:
				break
		elif key == '#':  #for backspacing
			if len(locationID) > 0:
				locationID = locationID[:-1]
		elif key.isdigit():
			locationID += key
			time.sleep(0.1)
		key = ""
	#after accepting locationID fetch location info from local database
	fetchLocationInfo()

'''
*
* Function Name: 	fetchTroughInfo
* Input: 				none
* Output: 			none
* Logic: 				fetches the trough name and id from local database
* Example Call:		fetchTroughInfo()
*
'''
def fetchTroughInfo():
	"checks id entered troughid is valid of not"
	global troughID
	global troughIDExcepted
	try:
		lcd.clear()
		lcd.string("Fetching trough id...", LINE_1)
		#create instance of a database with host, username, password and database name
		db = sqldb.connect("localhost", "root", "firebird", "maindb")
		#create cursor object
		cursor = db.cursor()
		tid = int(troughID)  #convert accepted trough id into integer
		sql = "SELECT troughid FROM troughinfo WHERE troughid = %d" % (tid)
		cursor.execute(sql)
		data = cursor.fetchone()
		#if entered trough ID is valid
		if data > 0:
			troughIDExcepted = 1	#set troughIDExcepted flag to one
		else:  #if no trough id exists with entered ID
			lcd.clear()
			lcd.string("trough ID does not", LINE_1)
			lcd.string("exists!", LINE_2)
			lcd.string("Enter valid trough", LINE_3)
			lcd.string("ID", LINE_4)
			time.sleep(3)
	except:  #if database connection Fails
		lcd.clear()
		lcd.string("      FAILED", LINE_1)
		lcd.string("Unable to connect to", LINE_2)
		lcd.string("local database", LINE_3)
		lcd.string("Try again later", LINE_4)
		time.sleep(3)
	db.close()


'''
*
* Function Name: 	acceptTroughID
* Input: 				none
* Output: 			none
* Logic: 				accepts trough ID from user using keypad
* Example Call:		acceptTroughID()
*
'''
def acceptTroughID():
	"function to accept troughid through keypad"
	global troughID
	global troughIDExcepted
	lcd.clear()
	troughID = ""
	key = ""
	time.sleep(0.1)
	lcd.string("Enter Trough ID", LINE_1)
	lcd.string("Press * to continue", LINE_2)
	lcd.string("and # for backspace", LINE_3)
	#loop until some trough id is entered and * key is pressed. Following loop will only break when valid trough ID is entered
	while  key != "*":
		lcd.string(troughID, LINE_4)
		key = kpad.get_key()
		if key == '*':
			if len(troughID) <= 0:
				lcd.clear()
				lcd.string("Trough ID can't", LINE_1)
				lcd.string("be null", LINE_2)
				time.sleep(3)
				lcd.clear()
				lcd.string("Enter Trough ID", LINE_1)
				lcd.string("Press * to continue", LINE_2)
				lcd.string("and # for backspace", LINE_3)
			else:
				break
		elif key == '#':  #for backspacing
			if len(troughID) > 0:
				troughID = troughID[:-1]
		elif key.isdigit():
			troughID += key
			time.sleep(0.1)
		key = ""
	#check if entered trough ID is valid or not by fetching it from local database
	fetchTroughInfo()

'''
*
* Function Name: 	fetchTroughInfoFromServer
* Input: 				none
* Output: 			none
* Logic: 				fetches newly added or removed trough info from server database
* Example Call:		fetchTroughInfoFromServer()
*
'''
def fetchTroughInfoFromServer():
	"fetch newly added troughinfo such as id from the server"
	updated = 0
	removed = 0
	lcd.clear()
	lcd.string("      Welcome", LINE_1)
	lcd.string("Fetching troughinfo...", LINE_2)
	try:
		lcd.string("Connect to database", LINE_3)
		#connect to server database to fetch information
		serverdb = sqldb.connect(host = server, user = "bhavesh", passwd = "123456789", db = "opencart", connect_timeout = 5)
		#connect to local databse to store fetched information
		localdb = sqldb.connect("localhost", "root", "firebird", "maindb")
		serverc = serverdb.cursor()
		localc = localdb.cursor()
		lcd.string("     Connected", LINE_4)
		serverc.execute("SELECT troughid FROM troughinfo")
		result = serverc.fetchall()  #fetch all trough information form server database
		for row in result:
			localc.execute("SELECT * FROM troughinfo WHERE troughid = %s", (row[0]))  #fetch the trough info from local database with selected server trough id
			count = localc.fetchall()
			if len(count) == 0:  #if trough info does not exists in the server then count will be zero so add it in local database
				localc.execute("INSERT INTO troughinfo(troughid) VALUES (%s)", (row[0]))
				updated += 1

		localc.execute( "SELECT troughid FROM troughinfo")  #fetch all the local trough information
		lresult = localc.fetchall()

		for lrow in lresult:
			count = 0
			for row in result:
				if lrow[0] == row[0]: #if there is trough which is in both server and local database then this condition will be true.
					count += 1
			if count == 0:  #if there is some row in local database wich does not exists in server database then count will be zero then remove the entry from local database
				localc.execute("DELETE FROM troughinfo WHERE troughid = %s", (lrow[0]))
				removed += 1

		localdb.commit()
		lcd.clear()
		lcd.string("      Success", LINE_2)
		if updated > 0:
			msg = str(updated)
			msg += " trough id updated"
			lcd.string(msg, LINE_3)
			time.sleep(3)
		if removed > 0:
			msg = str(removed)
			msg += " trough id removed"
			lcd.string(msg, LINE_3)
			time.sleep(3)
		serverdb.close()
		localdb.close()
	except:
		#localdb.rollback()
		lcd.clear()
		lcd.string("      Failed to", LINE_2)
		lcd.string("   fetch troughinfo", LINE_3)
		time.sleep(3)

'''
*
* Function Name: 	fetchLocationInfoFromServer
* Input: 				none
* Output: 			none
* Logic: 				fetches the newly added or removed location from server database
* Example Call:		fetchLocationInfoFromServer()
*
'''
def fetchLocationInfoFromServer():
	"fetch newly added locationinfo such as id and locationname from the server"
	updated = 0
	removed = 0
	lcd.clear()
	lcd.string("      Welcome", LINE_1)
	lcd.string("Fetching locationinfo...", LINE_2)
	try:
		lcd.string("Connect to database", LINE_3)
		#connect to server database to fetch information
		serverdb = sqldb.connect(host = server, user = "bhavesh", passwd = "123456789", db = "opencart", connect_timeout = 5)
		#connect to local databse to store fetched information
		localdb = sqldb.connect("localhost", "root", "firebird", "maindb")
		serverc = serverdb.cursor()
		localc = localdb.cursor()
		lcd.string("     Connected", LINE_4)
		serverc.execute("SELECT * FROM locationinfo")
		result = serverc.fetchall()  #fetch all location information form server database
		for row in result:
			localc.execute("SELECT * FROM locationinfo WHERE locationid = %s", (row[0]))  #fetch the location info from local database with selected server location id
			count = localc.fetchall()
			if len(count) == 0:  #if location does not exists in the server then count will be zero so add it in local database
				localc.execute("INSERT INTO locationinfo(locationid, locationname) VALUES (%s, %s)", (row[0], row[1]))
				updated += 1

		localc.execute( "SELECT locationid FROM locationinfo")  #fetch all the local location information
		lresult = localc.fetchall()

		for lrow in lresult:
			count = 0
			for row in result:
				if lrow[0] == row[0]: #if there is location which is in both server and local database then this condition will be true.
					count += 1
			if count == 0:  #if there is some row in local database wich does not exists in server database then count will be zero then remove the entry from local database
				localc.execute("DELETE FROM locationinfo WHERE locationid = %s", (lrow[0]))
				removed += 1

		localdb.commit()
		lcd.clear()
		lcd.string("      Success", LINE_2)
		if updated > 0:
			msg = str(updated)
			msg += " location updated"
			lcd.string(msg, LINE_3)
			time.sleep(3)
		if removed > 0:
			msg = str(removed)
			msg += " location removed"
			lcd.string(msg, LINE_3)
			time.sleep(3)
		serverdb.close()
		localdb.close()
	except:
		#localdb.rollback()
		lcd.clear()
		lcd.string("      Failed to", LINE_2)
		lcd.string("   fetch locationinfo", LINE_3)
		time.sleep(3)

'''
*
* Function Name: 	fetchCropInfoFromServer
* Input: 				none
* Output: 			none
* Logic: 				fetches the newly added or removed crop from server database
* Example Call:		fetchCropInfoFromServer()
*
'''
def fetchCropInfoFromServer():
	"fetch newly added cropinfo such as id and name from the server"
	updated = 0
	removed = 0
	lcd.clear()
	lcd.string("      Welcome", LINE_1)
	lcd.string("Fetching cropinfo...", LINE_2)
	try:
		lcd.string("Connect to database", LINE_3)
		#connect to server database to fetch information
		serverdb = sqldb.connect(host = server, user = "bhavesh", passwd = "123456789", db = "opencart", connect_timeout = 5)
		#connect to local databse to store fetched information
		localdb = sqldb.connect("localhost", "root", "firebird", "maindb")
		serverc = serverdb.cursor()
		localc = localdb.cursor()
		lcd.string("     Connected", LINE_4)
		serverc.execute("SELECT product_id, name FROM oc_product_description")
		result = serverc.fetchall()  #fetch all crop information form server database
		for row in result:
			localc.execute("SELECT * FROM cropinfo WHERE id = %s", (row[0]))  #fetch the crop info from local database with selected server crop id
			count = localc.fetchall()
			if len(count) == 0:  #if crop does not exists in the server then count will be zero so add it in local database
				localc.execute("INSERT INTO cropinfo(id, name) VALUES (%s, %s)", (row[0], row[1]))
				updated += 1

		localc.execute( "SELECT id FROM cropinfo")  #fetch all the local crop information
		lresult = localc.fetchall()

		for lrow in lresult:
			count = 0
			for row in result:
				if lrow[0] == row[0]: #if there is crop which is in both server and local database then this condition will be true.
					count += 1
			if count == 0:  #if there is some row in local database wich does not exists in server database then count will be zero then remove the entry from local database
				localc.execute("DELETE FROM cropinfo WHERE id = %s", (lrow[0]))
				removed += 1

		localdb.commit()
		lcd.clear()
		lcd.string("      Success", LINE_2)
		if updated > 0:
			msg = "   "
			msg += str(updated)
			msg += " crop updated"
			lcd.string(msg, LINE_3)
			time.sleep(3)
		if removed > 0:
			msg = "   "
			msg += str(removed)
			msg += " crop removed"
			lcd.string(msg, LINE_3)
			time.sleep(3)
		serverdb.close()
		localdb.close()
	except:
		#localdb.rollback()
		lcd.clear()
		lcd.string("      Failed to", LINE_2)
		lcd.string("   fetch cropinfo", LINE_3)
		time.sleep(3)

'''
*
* Function Name: 	init
* Input: 				none
* Output: 			none
* Logic: 				calculates the baseValue of load cell and fetches the crop info from the server database
* Example Call:		init()
*
'''
def init():
	"initialization function"
	global baseValue
	lcd.string("      Welcome", LINE_1)
	lcd.string(" Remove any object", LINE_2)
	lcd.string(" from the platform.", LINE_3)
	time.sleep(5)
	lcd.clear()
	lcd.string("      Welcome", LINE_1)
	lcd.string("   Please wait...", LINE_2)
	baseValue = lc.base_value()
	fetchCropInfoFromServer()
	fetchTroughInfoFromServer()
	fetchLocationInfoFromServer()

try :
	init()
	#while the program is active
	while active :
		#reset the flags
		troughIDExcepted = cropIDExcepted = pictureTaken = 0
		key = kpad.get_key()  #read the keypad value

		#while key pressed is not the * key
		while key is not '*' :
			displayWeight()
			key = kpad.get_key()
			if key == 'D' :
				tare()
			elif key == 'A':
				lcd.clear()
				lcd.string("       System", LINE_2)
				lcd.string("  Shutting down...", LINE_3)
				active = 0
				os.system("sudo poweroff")
				lcd.clear()
				break
			elif key == 'B':
				lcd.clear()
				lcd.string("       Script", LINE_2)
				lcd.string("     Restarting", LINE_3)
				lcd.string("   Please wait...", LINE_4)
				active = 0
				GPIO.cleanup()
				sys.stdout.flush()
				os.execl('/home/pi/Desktop/Final/startup.sh', '')
				break
			elif key == 'C':
				lcd.clear()
				lcd.string("       System", LINE_2)
				lcd.string("     Restarting", LINE_3)
				lcd.string("   Please wait...", LINE_4)
				active = 0
				os.system("sudo reboot")
				break
		if active:
			acceptCropID()
			if cropIDExcepted:
				acceptTroughID()
			if troughIDExcepted:
				acceptLocationID()
			if locationIDExcepted:
				takePicture()
			if pictureTaken:
				storeData()
	GPIO.cleanup()
except KeyboardInterrupt:
	lcd.clear()
	time.sleep(1)
	GPIO.cleanup()
