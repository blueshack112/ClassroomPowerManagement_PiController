import mysql.connector as cn
import datetime as dt
import managementUtilities as utilities
import globalVariablesandFunctions as gvs
import relayController
import time
import os

# Database connection variables
dbConnected = False
mainCursor = None
connection = None

# Connect to database
(dbConnected, connection, mainCursor) = utilities.connectToDatabase()

# Get starting system date and time
START_DATE_TIME = dt.datetime.now()
SERVER_DATE_TIME = START_DATE_TIME
DEBUG_TIME_DIFFERENCE = START_DATE_TIME - SERVER_DATE_TIME

"""
# Change current date and time to server's defined date ad time.
# Done by getting the difference between asked date adn current date.
# Each time the system uses date, it will calculate the difference first.
# Check its working by:
while True:
    CURRENT_DATE_TIME = dt.datetime.now() - (dt.datetime.now()-SERVER_DATE_TIME)
    print (CURRENT_DATE_TIME) #this line will give server time but updated. Time difference must be updated everytime server time changes
"""

# Vital variables to keep track of everything
WEEK_SCHEDULE_CREATED = False
CURRENT_DAY_OF_WEEK = 0             # 1 is monday and 7 is sunday. We need to perform actions 1 through 5 (Monday to Saturday)
CURRENT_SLOT = -1                   # -1 Means not a slot. 0 means between two sessions(break). 1-7 are usable values.
CURRENT_DAY_SCHEDULE_ITEMS = []     # Will contain a list of today's schedule items
CURRENT_ACTIVE_COURSE = None        # Will specify which course is currently active

# Get server's date time
(DEBUG_TIME_DIFFERENCE, SERVER_DATE_TIME) = utilities.getDebugTimeDifference(SERVER_DATE_TIME, DEBUG_TIME_DIFFERENCE, mainCursor)
CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE

"""
- This is the main loop.
- It will be running every second the whole day and all major function will be performed here.
"""
while True:
    # Check if connection is still open or not
    if not connection.is_connected():
        dbConnected = False
        (dbConnected, connection) = utilities.connectToDatabase()

    os.system("clear")
    print ("SUMMARY")
    print ("=========")

    # Update date time if it was changed
    (DEBUG_TIME_DIFFERENCE, SERVER_DATE_TIME) = utilities.getDebugTimeDifference(SERVER_DATE_TIME, DEBUG_TIME_DIFFERENCE, mainCursor)
    CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE

    # If it is the start of the week and weekly schedule table is not updated, add schedule from schedule table to this week's schedule table
    if utilities.isStartOfWeek(DEBUG_TIME_DIFFERENCE) and not WEEK_SCHEDULE_CREATED:
        WEEK_SCHEDULE_CREATED = utilities.createWeekSchedule(mainCursor)
    elif not utilities.isEndOfWeek(DEBUG_TIME_DIFFERENCE) and not WEEK_SCHEDULE_CREATED:
        WEEK_SCHEDULE_CREATED = utilities.createWeekSchedule(mainCursor)

    # At the end fo the week, remove everything from the weekly schedule table and get it prepared for next week's schedule
    if utilities.isEndOfWeek(DEBUG_TIME_DIFFERENCE) and WEEK_SCHEDULE_CREATED:
        WEEK_SCHEDULE_CREATED = not utilities.truncateWeekSchedule(mainCursor)
    elif utilities.isEndOfWeek(DEBUG_TIME_DIFFERENCE):
        WEEK_SCHEDULE_CREATED = utilities.isWeekScheduleCreated(mainCursor)
    
    # Calculate current day of week
    CURRENT_DAY_OF_WEEK = CURRENT_DATE_TIME.weekday() + 1

    # Calculate current slot
    # If the function says its break time (by returning 0) keep the same slot
    tempSlot = utilities.getCurrentSlot(DEBUG_TIME_DIFFERENCE)
    if not tempSlot == 0:
        CURRENT_SLOT = tempSlot
    
    # Get today's schedule items from the database
    CURRENT_DAY_SCHEDULE_ITEMS = utilities.getScheduleItems(mainCursor, CURRENT_DAY_OF_WEEK)

    # Determine which course is currently active
    for i in range(0, len(CURRENT_DAY_SCHEDULE_ITEMS)):
        if CURRENT_DAY_SCHEDULE_ITEMS[i].dayOfWeek == CURRENT_DAY_OF_WEEK:
            if CURRENT_DAY_SCHEDULE_ITEMS[i].slot == CURRENT_SLOT:
                CURRENT_ACTIVE_COURSE = CURRENT_DAY_SCHEDULE_ITEMS[i]
                CURRENT_ACTIVE_COURSE.isACtive = True
                break
            elif CURRENT_DAY_SCHEDULE_ITEMS[i].classLength == 2 and CURRENT_DAY_SCHEDULE_ITEMS[i].slot+1 == CURRENT_SLOT:
                CURRENT_ACTIVE_COURSE = CURRENT_DAY_SCHEDULE_ITEMS[i]
                CURRENT_ACTIVE_COURSE.activeSlot = CURRENT_SLOT
                CURRENT_ACTIVE_COURSE.isACtive = True
                break
            elif CURRENT_DAY_SCHEDULE_ITEMS[i].classLength == 3 and (CURRENT_DAY_SCHEDULE_ITEMS[i].slot+1 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+2 == CURRENT_SLOT):
                CURRENT_ACTIVE_COURSE = CURRENT_DAY_SCHEDULE_ITEMS[i]
                CURRENT_ACTIVE_COURSE.activeSlot = CURRENT_SLOT
                CURRENT_ACTIVE_COURSE.isACtive = True
                break
            elif CURRENT_DAY_SCHEDULE_ITEMS[i].classLength == 4 and (CURRENT_DAY_SCHEDULE_ITEMS[i].slot+1 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+2 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+3 == CURRENT_SLOT):
                CURRENT_ACTIVE_COURSE = CURRENT_DAY_SCHEDULE_ITEMS[i]
                CURRENT_ACTIVE_COURSE.activeSlot = CURRENT_SLOT
                CURRENT_ACTIVE_COURSE.isACtive = True
                break
            elif CURRENT_DAY_SCHEDULE_ITEMS[i].classLength == 5 and (CURRENT_DAY_SCHEDULE_ITEMS[i].slot+1 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+2 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+3 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+4 == CURRENT_SLOT):
                CURRENT_ACTIVE_COURSE = CURRENT_DAY_SCHEDULE_ITEMS[i]
                CURRENT_ACTIVE_COURSE.activeSlot = CURRENT_SLOT
                CURRENT_ACTIVE_COURSE.isACtive = True
                break
            elif CURRENT_DAY_SCHEDULE_ITEMS[i].classLength == 6 and (CURRENT_DAY_SCHEDULE_ITEMS[i].slot+1 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+2 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+3 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+4 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+5 == CURRENT_SLOT):
                CURRENT_ACTIVE_COURSE = CURRENT_DAY_SCHEDULE_ITEMS[i]
                CURRENT_ACTIVE_COURSE.activeSlot = CURRENT_SLOT
                CURRENT_ACTIVE_COURSE.isACtive = True
                break
            elif CURRENT_DAY_SCHEDULE_ITEMS[i].classLength == 7 and (CURRENT_DAY_SCHEDULE_ITEMS[i].slot+1 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+2 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+3 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+4 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+5 == CURRENT_SLOT or CURRENT_DAY_SCHEDULE_ITEMS[i].slot+6 == CURRENT_SLOT):
                CURRENT_ACTIVE_COURSE = CURRENT_DAY_SCHEDULE_ITEMS[i]
                CURRENT_ACTIVE_COURSE.activeSlot = CURRENT_SLOT
                CURRENT_ACTIVE_COURSE.isACtive = True
                break            
            else:
                if i == len(CURRENT_DAY_SCHEDULE_ITEMS)-1:
                    CURRENT_ACTIVE_COURSE = None
    
    # if no scedule today
    if len(CURRENT_DAY_SCHEDULE_ITEMS) == 0:
        CURRENT_ACTIVE_COURSE = None

    # if there is an active course...
    if CURRENT_ACTIVE_COURSE:
        CURRENT_ACTIVE_COURSE.isActive = True
        # Adjusting slot differences if applicable
        if not CURRENT_ACTIVE_COURSE.slot == CURRENT_ACTIVE_COURSE.activeSlot:
            utilities.adjustForSlotChanges(mainCursor, CURRENT_ACTIVE_COURSE, CURRENT_SLOT)
        # Turn on the appliances
        utilities.turnOnAppliances(mainCursor, CURRENT_ACTIVE_COURSE, DEBUG_TIME_DIFFERENCE)

    # If there is no course active...
    if not CURRENT_ACTIVE_COURSE:
        # Switch everything off
        utilities.switchEverythingOff(mainCursor)
    
    # Reporting at the end of the loop
    print ("Datetime: " + str(CURRENT_DATE_TIME)[:-7])
    print ("Week schedule created: " + str(WEEK_SCHEDULE_CREATED))
    print ("Day: " + str(CURRENT_DAY_OF_WEEK))
    print ("Slot: " + str(CURRENT_SLOT))
    print ("Relays on right now: " + relayController.whichRelaysAreOn())

    if CURRENT_ACTIVE_COURSE:
        print ("\n\nCurrent active course:")
        print ("\tCourse ID: " + str(CURRENT_ACTIVE_COURSE.courseID) + "   Teacher ID: " + str(CURRENT_ACTIVE_COURSE.teacherID) + "   Room ID: " + str(CURRENT_ACTIVE_COURSE.roomID) + "   Active Status: " + str(CURRENT_ACTIVE_COURSE.isActive) + "   Attendance: " + str(CURRENT_ACTIVE_COURSE.attendance) + "   Relays On: " + CURRENT_ACTIVE_COURSE.relaysOnToString() + "   Slot: " + str(CURRENT_ACTIVE_COURSE.slot) + "   Length: " + str(CURRENT_ACTIVE_COURSE.classLength))
    else:
        print ("\n\nCurrent active course: None")
    

    print ("\nToday's schedule: ")
    for i in CURRENT_DAY_SCHEDULE_ITEMS:
        print ("\tCourse ID: " + str(i.courseID) + "   Teacher ID: " + str(i.teacherID) + "   Room ID: " + str(i.roomID), end = '')
        print ("   Slot: " + str(i.slot) + "   Length: " + str(i.classLength))
    print('\033[0;0H')
    time.sleep(0.5)
    # long sleep
    # TODO: remove it
    time.sleep(3)
    # Commit whatever changes were made during the loop
    connection.commit()

#Close everything (probably not going to occur)
if connection.is_connected():
    connection.close()
    print("Disconnected from the server...")
