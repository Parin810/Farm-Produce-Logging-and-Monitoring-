import RPi.GPIO as GPIO		#importing libraries
import time
GPIO.setmode(GPIO.BOARD)	#accessing pins using pin numbers
MATRIX=[ [1,2,3],			# 4*3 matrix to store keypad elements
	 [4,5,6],
	 [7,8,9],
	 ['*',0,'#']
	]
MATRIX2=[ [1,1,1],			# 4*3 matrix to store cstate values
	 [1,1,1],
	 [1,1,1],
	 [1,1,1]
	]

ROW=[35,40,38,36]
COL=[29,31,33]	
k=0							
m=0
n=0



for j in range(3):			# coloumn loop
	GPIO.setup(COL[j],GPIO.OUT)	#setting GPIO pins in output mode
	GPIO.output(COL[j],1)		#output GPIO pins set high

for i in range(4):			# rows loop
	GPIO.setup(ROW[i],GPIO.IN,pull_up_down=GPIO.PUD_UP) # set GPIO pin in input mode, connected via pull up resiis 

try:   
	check=1							
	while(True):
	  for j in range(3):			# scannin coloumns
		       
			GPIO.output(COL[j],0)	# set the current coloumn (GPIO pin) to low 
		        for i in range(4):	# scanning rows 
			      cstate=1			# current state of GPIO(input) pins
			      if m==i and n==j and check!=1: #checks for cstate value
			        cstate=MATRIX2[m][n]
			      
			      count=0			# variable to store the bouncing of switch 
			      dloop=0 			
			      check=0			# set check=0 again
				
			      while dloop<14:
										      	
			   		recieve=GPIO.input(ROW[i])
					if recieve == cstate and count>0:
						count = count-1
					if recieve != cstate:
						count = count+1
											
					if count >=10:
						count = 0
						cstate=recieve
						m=i
						n=j
						MATRIX2=[[1,1,1], [1,1,1],[1,1,1],[1,1,1]]
						MATRIX2[m][n]=cstate
						if cstate==0:
							print MATRIX[i][j]	# print the particular key pressed
						
			       		dloop=dloop+1
				

			GPIO.output(COL[j],1)	# restores high value in current coloumn (GPIO pin) 
except KeyboardInterrupt:
	GPIO.cleanup()		