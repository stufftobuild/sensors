###
# Measuring distance with the HC-SR04 ultrasonic range sensor
# Code example from www.stufftobuild.co.uk
###

import RPi.GPIO as GPIO
import time

#Note using BCM numbering, not BOARD
#If you change to BOARD mode, remember to update the pin numbers
GPIO.setmode(GPIO.BCM)

#Use variables to store the pin numbers so they
#are easy to change later if needed
TRIGGER_PIN = 18
ECHO_PIN = 25

#The TRIGGER is an output (sends signal to the sensor)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
#The ECHO is an input (recieves signal from the sensor)
GPIO.setup(ECHO_PIN, GPIO.IN)


def measure_distance():
	#trigger measurement with a 10us HIGH signal to the sensor
	GPIO.output(TRIGGER_PIN, True)
	time.sleep(0.00001)
	GPIO.output(TRIGGER_PIN, False)

	#get ready to time the output
	output_high_start = time.time()
	output_high_stop = time.time()

	#keep updating output_high_start while we wait for the echo signal
	#to start (when it becomes HIGH)
	while GPIO.input(ECHO_PIN) == 0:
		output_high_start = time.time()

	#now the output is HIGH, and will be high for as long as the
	#ping took to return to the sensor. We want to know what time
	#the output signal returns to LOW
	while GPIO.input(ECHO_PIN) == 1:
		output_high_stop = time.time()

	#now we know what time the echo signal started and ended, we can 
	#calculate the duration of the signal (time elapsed between start and end)
	output_high_duration = output_high_stop - output_high_start

	#total distance = time * speed
	#distance to object = (total distance)/2
	#speed of sound at sea level = 343 m/s = 34300 cm/s
	distance = (output_high_duration * 34300) / 2

	return distance

#Test the sensor
#use a try/except block so we can stop measurement with ctrl+c and 
#then call GPIO.cleanup() rather than just killing an infinite loop
try:
	while True:
		distance = measure_distance()
		print "Distance to object = %0.1f cm" % distance
except KeyboardInterrupt:
	print "Stopping measurement"
	GPIO.cleanup()

