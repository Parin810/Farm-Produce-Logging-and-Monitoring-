import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


def get_key ():
	MATRIX=[ [1,2,3,'A'],
	 [4,5,6,'B'],
	 [7,8,9,'C'],
	 ['*',0,'#','D']
	]
	MATRIX2=[ [1,1,1,1],
	 [1,1,1,1],
	 [1,1,1,1],
	 [1,1,1,1]
	]

	ROW=[29,31,33,35]
	COL=[18,40, 38, 36]

	for j in range(4):
		GPIO.setup(COL[j],GPIO.OUT)
		GPIO.output(COL[j],1)

	for i in range(4):
		GPIO.setup(ROW[i],GPIO.IN,pull_up_down=GPIO.PUD_UP)
	k=0
	n=0
	m=0
	x=1
	result='E'


	for j in range(4):

		GPIO.output(COL[j],0)
	        for i in range(4):
		      cstate=1
		      if m==i and n==j and x!=1:
		        cstate=MATRIX2[m][n]

		      count=0
		      k=0
		      x=0

		      while k<14:

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
					MATRIX2=[[1,1,1,1], [1,1,1,1],[1,1,1,1],[1,1,1,1]]
					MATRIX2[m][n]=cstate
					if cstate==0:
						#print MATRIX[i][j]
						result= MATRIX[i][j]
		       		k=k+1

		GPIO.output(COL[j],1)
	return str(result)
