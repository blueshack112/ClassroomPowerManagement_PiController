import mysql.connector as cn
import datetime as dt
import managementUtilities as utilities

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
CURRENT_SLOT = 0 # 0 Means not a slot. 1-7 are usable values.

#get database's date and time mainly for debug purposes
(debugDateRan, ifDebugDateError) = utilities.runQuery(mainCursor, utilities.QUERY_GET_DATE_TIME)
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
    mainCursor.execute(utilities.QUERY_GET_DATE_TIME)
    newdate = mainCursor.fetchone()[1]
    if SERVER_DATE_TIME != newdate:
        SERVER_DATE_TIME = newdate
        DEBUG_TIME_DIFFERENCE = dt.datetime.now() - SERVER_DATE_TIME
        CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE
    else:
        CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE

    # If it is the start of the week and weekly schedule table is not updated, add schedule from schedule table to this week's schedule table
    if utilities.isStartOfWeek(DEBUG_TIME_DIFFERENCE) and not WEEK_SCHEDULE_CREATED:
        WEEK_SCHEDULE_CREATED = utilities.createWeekSchedule(mainCursor)
        print (WEEK_SCHEDULE_CREATED)
    elif not utilities.isEndOfWeek(DEBUG_TIME_DIFFERENCE) and not WEEK_SCHEDULE_CREATED:
        WEEK_SCHEDULE_CREATED = utilities.createWeekSchedule(mainCursor)
        print (WEEK_SCHEDULE_CREATED)

    # At the end fo the week, remove everything from the weekly schedule table and get it prepared for next week's schedule
    if utilities.isEndOfWeek(DEBUG_TIME_DIFFERENCE) and WEEK_SCHEDULE_CREATED:
        WEEK_SCHEDULE_CREATED = not utilities.truncateWeekSchedule(mainCursor)
        print (WEEK_SCHEDULE_CREATED)
    elif utilities.isEndOfWeek(DEBUG_TIME_DIFFERENCE):
        WEEK_SCHEDULE_CREATED = utilities.isWeekScheduleCreated(mainCursor)
    
    CURRENT_DAY_OF_WEEK = CURRENT_DATE_TIME.weekday() + 1
    print (CURRENT_DAY_OF_WEEK)
    # Commit whatever changes were made during the loop
    connection.commit()

#Close everything (probably not going to occur)
debug = open("debug.log", 'w')
if connection.is_connected():
    connection.close()
    print("Disconnected from the server...")
