import mysql.connector as cn
import datetime as dt
import managementUtilities as utilities
import globalVariablesandFunctions as gvs
import time
import os

# database connection variables
dbHost = "192.168.18.4"
offsiteDbHost = "localhost"
dbPort = "3306"
dbUsername = "areeba"
dbPassword = "areebafyp"
dbDatabase = "db_classroom_management"

#connection and getting cursor
try:
    connection = cn.connect(host=offsiteDbHost, user=dbUsername, passwd=dbPassword, database=dbDatabase)
    mainCursor = connection.cursor()
    print("Connected to the server...")
except Exception as e:
    print("Could not connect to the server, exiting...")
    print (e)
    exit()

# Get starting system date and time
START_DATE_TIME = dt.datetime.now()
SERVER_DATE_TIME = START_DATE_TIME

"""
# Change current date and time to server's defined date ad time.
# Done by getting the difference between asked date adn current date.
# Each time the system uses date, it will calculate the difference first.
# Check its working by:
while True:
    CURRENT_DATE_TIME = dt.datetime.now() - (dt.datetime.now()-SERVER_DATE_TIME)
    print (CURRENT_DATE_TIME) #this line will give server time but updated. Time difference must be updated everytime server time changes
"""

# Global variables to keep track of everything
WEEK_SCHEDULE_CREATED = False
CURRENT_DAY_OF_WEEK = 0 # 1 is monday and 7 is sunday. We need to perform actions 1 through 5 (Monday to Saturday)
CURRENT_SLOT = -1 # -1 Means not a slot. 0 means between two sessions(break). 1-7 are usable values.
CURRENT_DAY_SCHEDULE_ITEMS = [] # Will contain a list of today's schedule items
CURRENT_ACTIVE_COURSE = None # Will specify which course is currently active

#get database's date and time mainly for debug purposes
(debugDateRan, ifDebugDateError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_DATE_TIME)
if debugDateRan:
    SERVER_DATE_TIME = mainCursor.fetchone()[1]
else:
    print(ifDebugDateError)

DEBUG_TIME_DIFFERENCE = dt.datetime.now() - SERVER_DATE_TIME
CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE
"""
- This is the main loop.
- It will be running every second the whole day and all major function will be performed here.
"""
debug = open("debug.log", 'w')
while True:
    # Update local clock to sync with server clock
    (debugDateRan, ifDebugDateError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_DATE_TIME)
    if debugDateRan:
        newdate = mainCursor.fetchone()[1]
        if SERVER_DATE_TIME != newdate:
            SERVER_DATE_TIME = newdate
            DEBUG_TIME_DIFFERENCE = dt.datetime.now() - SERVER_DATE_TIME
            CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE
        else:
            CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE
    else:
        print(ifDebugDateError)
    

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
    
    # Calculate current day of week and slot
    CURRENT_DAY_OF_WEEK = CURRENT_DATE_TIME.weekday() + 1
    tempSlot = utilities.getCurrentSlot(DEBUG_TIME_DIFFERENCE)
    # If the function says its break time (by returning 0) keep the same slot
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
            else:
                if i == len(CURRENT_DAY_SCHEDULE_ITEMS)-1:
                    CURRENT_ACTIVE_COURSE = None

    # if there is an active course, turn on the applicances
    if CURRENT_ACTIVE_COURSE:
        #TODO: write function to adjust slot differences
        if not CURRENT_ACTIVE_COURSE.slot == CURRENT_ACTIVE_COURSE.activeSlot:
            utilities.adjustForSlotChanges(mainCursor, CURRENT_ACTIVE_COURSE, CURRENT_SLOT)
        #TODO: write function to turn on the appliances
        print ("Turn it on!")

    # if there is no course active, turn off the applicances
    # if not CURRENT_ACTIVE_COURSE:
    #     utilities.switchEverythingOff()
    
    time.sleep(1)
    os.system("cls")
    print ("SUMMARY")
    print ("=========")
    print ("Datetime: " + str(CURRENT_DATE_TIME)[:-7])
    print ("Week schedule created: " + str(WEEK_SCHEDULE_CREATED))
    print ("Day: " + str(CURRENT_DAY_OF_WEEK))
    print ("Slot: " + str(CURRENT_SLOT))
    if CURRENT_ACTIVE_COURSE:
        print ("Current active course: " + str(CURRENT_ACTIVE_COURSE.courseID))
    else:
        print ("Current active course: None")
    print ("Today's schedule: ")
    for i in CURRENT_DAY_SCHEDULE_ITEMS:
        print (vars(i))
    

    # Commit whatever changes were made during the loop
    connection.commit()

#Close everything (probably not going to occur)
debug = open("debug.log", 'w')
debug.close()
if connection.is_connected():
    connection.close()
    print("Disconnected from the server...")
