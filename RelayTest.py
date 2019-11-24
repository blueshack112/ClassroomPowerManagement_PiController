import RPi.GPIO as GPIO
from time import sleep

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

GPIO.output(3, GPIO.HIGH)
GPIO.output(5, GPIO.HIGH)
GPIO.output(7, GPIO.HIGH)
GPIO.output(11, GPIO.HIGH)

GPIO.output(3, GPIO.LOW)
GPIO.output(5, GPIO.LOW)
GPIO.output(7, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
print('done')

sleep(1)

GPIO.cleanup()
