import RPi.GPIO as GPIO

"""
This code is used to switch relays on and off.
Raspberry Pi Pinout diagram is present in the root directory. Please take a look.
Always Connect 5 Volt to JDVCC on the relay board
Always Connect 3.3 Volt to VCC on the relay board

Pins that we will use are:
Pin 1: 3.3v
Pin 2: 5v
Pin 6: Ground

Pin  3: GPIO-02 | RelayChannel-1 | RelayID-101 | Row 1
Pin  5: GPIO-03 | RelayChannel-2 | RelayID-102 | Row 2
Pin  7: GPIO-04 | RelayChannel-3 | RelayID-103 | Row 3
Pin 11: GPIO-17 | RelayChannel-4 | RelayID-104 | Row 4
Pin 13: GPIO-27 | RelayChannel-5 | RelayID-105 | Row 5
Pin 15: GPIO-22 | RelayChannel-6 | RelayID-106 | Row 6
Pin 19: GPIO-10 | RelayChannel-7 | RelayID-107 | AC Front
Pin 21: GPIO-09 | RelayChannel-8 | RelayID-108 | AC Back

-In the above configuration, the actual addressable pin number is written after "Pin " (3, 5, 6, etc)
-In the above configuration, the relay id corresponding to the database's relay id is written after "RelayID-" (101, 102, 103, etc)
-This is how we will configure global variables for relay pins. (Done right after this long comment)
-Relay switches on when pin has LOW signal and switches off when pin has HIGH signal

-Considering that we have 8 relays to choose from, the spreadout is as follows:
    *.RelayID-101: Fans and Lights - Row 1
    *.RelayID-102: Fans and Lights - Row 2
    *.RelayID-103: Fans and Lights - Row 3
    *.RelayID-104: Fans and Lights - Row 4
    *.RelayID-105: Fans and Lights - Row 5
    *.RelayID-106: Fans and Lights - Row 6
    *.RelayID-107: Air conditioner - Front
    *.RelayID-108: Air conditioner - Back

-Considering that a class can have a maximum of 60 students, Every 10 students should activate a row:
    *. Attendance: 10       -> Row 1
    *. Attendance: 20       -> Row 2
    *. Attendance: 30       -> Row 3
    *. Attendance: 40       -> Row 4
    *. Attendance: 50       -> Row 5
    *. Attendance: 60       -> Row 6
    *. Attendance: 0-25     -> AC Front
    *. Attendance: 26-60    -> AC Back
-Taking all this into account, there will be two ways to address relay pins.    
"""

# Global variables for relay pins raspberry pi's perspective
RELAY_101 = 3
RELAY_102 = 5
RELAY_103 = 7
RELAY_104 = 11
RELAY_105 = 13
RELAY_106 = 15
RELAY_107 = 19
RELAY_108 = 21

# Global variables for relay pins system's perspective
RELAY_ROW_1 = 101
RELAY_ROW_2 = 102
RELAY_ROW_3 = 103
RELAY_ROW_4 = 104
RELAY_ROW_5 = 105
RELAY_ROW_6 = 106
RELAY_AC_FRONT = 107
RELAY_AC_BACK = 108

# Setup relay pints for output mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
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

# Function to switch off all relays
def switchOffAll ():
    if GPIO.input(RELAY_101) == 0: # If Pin is on
        switchOff(RELAY_101)
    if GPIO.input(RELAY_102) == 0:
        switchOff(RELAY_102)
    if GPIO.input(RELAY_103) == 0:
        switchOff(RELAY_103)
    if GPIO.input(RELAY_104) == 0:
        switchOff(RELAY_104)
    if GPIO.input(RELAY_105) == 0:
        switchOff(RELAY_105)
    if GPIO.input(RELAY_106) == 0:
        switchOff(RELAY_106)
    if GPIO.input(RELAY_107) == 0:
        switchOff(RELAY_107)
    if GPIO.input(RELAY_108) == 0:
        switchOff(RELAY_108)

# Function to switch on all relays
def switchOnAll ():
    if GPIO.input(RELAY_101) == 1: # If Pin is off
        switchOn(RELAY_101)
    if GPIO.input(RELAY_102) == 1:
        switchOn(RELAY_102)
    if GPIO.input(RELAY_103) == 1:
        switchOn(RELAY_103)
    if GPIO.input(RELAY_104) == 1:
        switchOn(RELAY_104)
    if GPIO.input(RELAY_105) == 1:
        switchOn(RELAY_105)
    if GPIO.input(RELAY_106) == 1:
        switchOn(RELAY_106)
    if GPIO.input(RELAY_107) == 1:
        switchOn(RELAY_107)
    if GPIO.input(RELAY_108) == 1:
        switchOn(RELAY_108)

# Fucntion which returns a string of all the relays that are switched on at the moment of calling the function
def whichRelaysAreOn():
    onRelays = "|"
    if GPIO.input(RELAY_101) == 0: # If Pin is off
        onRelays += "101|"
    if GPIO.input(RELAY_102) == 0:
        onRelays += "102|"
    if GPIO.input(RELAY_103) == 0:
        onRelays += "103|"
    if GPIO.input(RELAY_104) == 0:
        onRelays += "104|"
    if GPIO.input(RELAY_105) == 0:
        onRelays += "105|"
    if GPIO.input(RELAY_106) == 0:
        onRelays += "106|"
    if GPIO.input(RELAY_107) == 0:
        onRelays += "107|"
    if GPIO.input(RELAY_108) == 0:
        onRelays += "108|"
    
    if len(onRelays) == 1:
        onRelays = "None"
    return onRelays

"""
# Dummy function to switch on a relay
# Returns true and false as success signals
def switchOn (relayPin):
    print (str(relayPin) + " switched on!")

# Dummy function to switch on a relay
# Returns true and false as success signals
def switchOff (relayPin):
    print (str(relayPin) + " switched of!")

# Dummy function to switch off all relays
# Returns true and false as success signals
def switchOffAll ():
    print ("Switch all off.")
"""

# Set all pins to high so the relay switches can be off
switchOffAll()