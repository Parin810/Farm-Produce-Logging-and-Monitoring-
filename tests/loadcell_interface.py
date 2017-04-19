"""
This program is use to interface loadcell with raspberry pi using HX711
read HX711 data sheet for more information
"""

#importing gpio library
import RPi.GPIO as GPIO

#import math library for power function
import math

#to use physical pin numbers on board
GPIO.setmode(GPIO.BOARD)

SCK = 15   #define pin for serial clock input of HX711 
DOUT = 16  #define pin for serial data output of HX711

GPIO.setup(SCK, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)

#define array of size 24 for storing 24 bit data sent by HX711
bits = [0 for i in range(24)]

#infinite while loop for receiving data from HX711 
while 1 :
	#if DOUT pin is low means HX711 is ready to sent data
	if GPIO.input(DOUT) == 0 :
		val = 0
		
		#loop 24 times to get 24 bits
		for i in range(24) :
			GPIO.output(SCK, GPIO.HIGH)  #set SCK high
			bits[i] = GPIO.input(DOUT)   #store bit in bits array
			GPIO.output(SCK, GPIO.LOW)   #set sck low

		#sending 25th pulse to set gain 128 and to complete the transfer
		GPIO.output(SCK, GPIO.HIGH)
		GPIO.output(SCK, GPIO.LOW)

		power = 23  #for conversion for binary to decimal
		for i in range(24) :	#print the bits and equivalent decimal value
			print(bits[i], end = "")
			val += bits[i] * math.pow(2, power)  #binary to decimal conversion
			power -= 1
		print("")
		print(val)
	#when HX711 is not ready to sent data set sck low
	else :
		GPIO.output(SCK, GPIO.LOW)

GPIO.cleanup()
