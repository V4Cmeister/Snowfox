import serial
import time
import sys
from datetime import datetime
import RPi.GPIO as GPIO
from numpy import interp

#setup GPIO
GPIO.setmode(GPIO.BOARD) #set the GPIO Board mode to Board (1,2,3,4,5,6,7,8,9,...)
GPIO.setwarnings(False) #disables GPIO warnings
GPIO.setup(12, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
pwm_vor = GPIO.PWM(12, 10000)
pwm_back = GPIO.PWM(33, 10000)

#prepears the array
serial_data = []
for x in range(15):
	serial_data.append(x) #creats space for serial data
usb_port = serial.Serial('/dev/ttyUSB0',115200)	#defined the Path of the USB device

def getValue(channel):
	position = 0
	while position < 14: #loops trough the 14 positions
		read_serial=usb_port.readline()	#reads in serial_data over the USB port
		values = read_serial.decode('cp1250').strip() #converts the receaved value to processable value
		serial_data[position] = values #writes the value to the array with the current position
		position=position+1 #jumps to the next positon
	return serial_data[channel]

def map(input, in_min, in_max, out_min, out_max): #maps a range of values to a wanted range of values
	output = (input - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	if output > out_max:
		return out_max
	elif output < out_min:
		return out_min
	else:
		return output

try:
	while True:
		pwm_value = (map(int(getValue(3)), 946, 2040, 0, 100))
		if (pwm_value > 52):
			pwm_back.stop()
			pwm_vor.start(0)
			vor = map(pwm_value, 52, 100, 0, 100)
			#print(vor)
			pwm_vor.ChangeDutyCycle(vor)
		elif (pwm_value < 48):
			pwm_back.start(0)
			pwm_vor.stop()
			back = map(pwm_value, 48, 0, 0, 100)
			#print(back)
			pwm_back.ChangeDutyCycle(back)
		else:
			pwm_back.stop()
			pwm_vor.stop()
except KeyboardInterrupt:
	print("Programm 'serial_data_transmission.py' wurde beendet")
finally:	
	GPIO.cleanup()
