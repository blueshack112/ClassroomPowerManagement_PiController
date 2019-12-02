import RPi.GPIO as GPIO
from time import sleep

"""
This code is used to switch relays on and off.
Raspberry Pi Pinout diagram is present in the root directory. Please take a look.
Always Connect 5 Volt to JDVCC on the relay board
Always Connect 3.3 Volt to VCC on the relay board

Pins that we will use are:
Pin 1: 3.3v
Pin 2: 5v
Pin 6: Ground

Pin  3: GPIO-02 | RelayChannel-1 | RelayID-101
Pin  5: GPIO-03 | RelayChannel-2 | RelayID-102
Pin  6: GPIO-04 | RelayChannel-3 | RelayID-103
Pin 11: GPIO-17 | RelayChannel-4 | RelayID-104
Pin 13: GPIO-27 | RelayChannel-5 | RelayID-105
Pin 15: GPIO-22 | RelayChannel-6 | RelayID-106
Pin 19: GPIO-10 | RelayChannel-7 | RelayID-107
Pin 21: GPIO-09 | RelayChannel-8 | RelayID-108

-In the above configuration, the actual addressable pin number is written after "Pin " (3, 5, 6, etc)
-In the above configuration, the relay id corresponding to the database's relay id is written after "RelayID-" (101, 102, 103, etc)
-This is how we will configure global variables for relay pins. (Done right after this long comment)
-Relay switches on when pin has LOW signal and switches off when pin has HIGH signal
"""

# Global variables for relay pins
RELAY_101 = 3
RELAY_102 = 5
RELAY_103 = 6
RELAY_104 = 11
RELAY_105 = 13
RELAY_106 = 15
RELAY_107 = 19
RELAY_108 = 21

# Setup relay pints for output mode
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
GPIO.setup(RELAY_101, GPIO.OUT)
GPIO.setup(RELAY_102, GPIO.OUT)
GPIO.setup(RELAY_103, GPIO.OUT)
GPIO.setup(RELAY_104, GPIO.OUT)
GPIO.setup(RELAY_105, GPIO.OUT)
GPIO.setup(RELAY_106, GPIO.OUT)
GPIO.setup(RELAY_107, GPIO.OUT)
GPIO.setup(RELAY_108, GPIO.OUT)

# Function to switch on a relay
# Returns true and false as success signals
def switchOn (relayPin):
    if GPIO.input(relayPin) == 0: # Pin is already on
        return True
    else:
        GPIO.output(relayPin, GPIO.LOW)
        if GPIO.input(relayPin) == 0:
            return True
        else:
            return False

# Function to switch on a relay
# Returns true and false as success signals
def switchOff (relayPin):
    if GPIO.input(relayPin) == 1: # Pin is already off
        return True
    else:
        GPIO.output(relayPin, GPIO.HIGH)
        if GPIO.input(relayPin) == 1:
            return True
        else:
            return False

# Set all pins to high so the relay switches can be off
switchOff(RELAY_101)
switchOff(RELAY_102)
switchOff(RELAY_103)
switchOff(RELAY_104)
switchOff(RELAY_105)
switchOff(RELAY_106)
switchOff(RELAY_107)
switchOff(RELAY_108)