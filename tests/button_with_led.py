#contol led with button press and count how many time button is pressed

#importing gpio library
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)  #to use physical pin numbers on board
gpio.setup(11, gpio.OUT)  #set pin 11 as output
gpio.setup(12, gpio.IN, pull_up_down = gpio.PUD_DOWN)  #set pin 12 as input with pull down resistor enabled

counter = 0  #variable to keep track of button pressed

#call back function when button is pressed
def incrementcounter(channel):
	"keep track of how many time button is pressed"
	global counter
	counter += 1
	print (counter)
	return

#event handler setup to count number of button pressed
gpio.add_event_detect(12, gpio.RISING, callback = incrementcounter)

while 1:
	input = gpio.input(12)
	if input == 1 :
		gpio.output(11, 1)  #led will glow until the button is pressed
	else :
		gpio.output(11, 0)  #otherwise it will be off

GPIO.cleanup()
