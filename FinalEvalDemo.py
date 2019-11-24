import RPi.GPIO as GPIO
import requests
from time import sleep

startUrl = 'http://192.168.8.102:80/AreebaFYP/relayDemoStart.php/'
stopUrl = 'http://192.168.8.102:80/AreebaFYP/relayDemoStop.php/'
#Starting demo by opening relays
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
print ('All relays are ON...')

#Sending data to server to update room status
payload = {'roomID': 1001,'courseID': 1001,'relayUsed': 101102103,'slot': 1,'attendance': -1,}
r = requests.post(startUrl, data=payload)
if (r.ok == True):
    print('\nSent data to server.')
    print('\nResponse was '+str(r.ok))
else:
    print('\nData not sent, exiting.')
    print('\nResponse was '+str(r.ok))
    GPIO.cleanup()

#Wait for 60 seconds to check database and app
print('\n\nGoing to sleep for 60 seconds. Check if server has been updated.')
sleep(30)

#After 60 seconds pass, stop the demo and cleanup GPIO
r = requests.post(stopUrl)
if (r.ok == True):
    print('\nData deleted from server.')
    print('\nResponse was '+str(r.ok))
else:
    print('\n\nData not deleted, exiting.')
    print('\nResponse was '+str(r.ok))
    GPIO.cleanup()

GPIO.cleanup()
