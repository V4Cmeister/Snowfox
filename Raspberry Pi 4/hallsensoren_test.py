import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BOARD) #set the GPIO Board mode to Board (1,2,3,4,5,6,7,8,9,...)
GPIO.setwarnings(False) #disables GPIO warnings
GPIO.setup(12, GPIO.IN)

start = 0
stopp = 0
delta = 0
flanke = 0

def RPM(channel):
    global stopp
    global start
    global delta
    global flanke

    if flanke == 0: #first falling flanke starts the timer
        start = time.time()
        flanke = flanke + 1
    elif flanke == 1: #second falling flanke ends the timer, calculates the differenz between first and secons and prints
        stopp = time.time()
        delta = stopp - start
        RPM = (1 / delta) * 60
        print("%1.2f" % RPM)
        flanke = 0

GPIO.add_event_detect(12, GPIO.FALLING, callback = RPM) #defines pin 12 as an intrupt

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
	print("Programm 'serial_text_to_pwm.py' wurde beendet")
finally:	
	GPIO.cleanup()
