import RPi.GPIO as GPIO
from time import sleep

RELAY_101 = 3
RELAY_102 = 5
RELAY_103 = 7
RELAY_104 = 11
RELAY_105 = 13
RELAY_106 = 15
RELAY_107 = 19
RELAY_108 = 21

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)


GPIO.output(3, GPIO.HIGH)
GPIO.output(5, GPIO.HIGH)
GPIO.output(7, GPIO.HIGH)
GPIO.output(11, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)
GPIO.output(15, GPIO.HIGH)
GPIO.output(19, GPIO.HIGH)
GPIO.output(21, GPIO.HIGH)

GPIO.output(3, GPIO.LOW)
sleep(1)

GPIO.output(3, GPIO.HIGH)
GPIO.output(5, GPIO.LOW)
sleep(1)

GPIO.output(5, GPIO.HIGH)
GPIO.output(7, GPIO.LOW)
sleep(1)

GPIO.output(7, GPIO.HIGH)
GPIO.output(11, GPIO.LOW)
sleep(1)

GPIO.output(11, GPIO.HIGH)
GPIO.output(13, GPIO.LOW)
sleep(1)

GPIO.output(13, GPIO.HIGH)
GPIO.output(15, GPIO.LOW)
sleep(1)

GPIO.output(15, GPIO.HIGH)
GPIO.output(19, GPIO.LOW)
sleep(1)

GPIO.output(19, GPIO.HIGH)
GPIO.output(21, GPIO.LOW)
sleep(1)

GPIO.output(21, GPIO.HIGH)

GPIO.cleanup()
