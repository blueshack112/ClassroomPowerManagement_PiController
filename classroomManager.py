import mysql.connector as cn
import datetime as dt
import managementUtilities as utilities

# database connection variables
dbHost = "192.168.18.4"
dbPort = "3306"
dbUsername = "areeba"
dbPassword = "areebafyp"
dbDatabase = "db_classroom_management"

#Query templates
QUERY_GET_DATE_TIME = "SELECT * FROM tbl_debug"

#connection and getting cursor
try:
    connection = cn.connect(host=dbHost, user=dbUsername, passwd=dbPassword, database=dbDatabase)
    mainCursor = connection.cursor()
    print("Connected to the server...")
except Exception as e:
    print (e)
    exit()

# Get starting system date and time
START_DATE_TIME = dt.datetime.now()


"""
# Change current date and time to server's defined date ad time.
# Done by getting the difference between asked date adn current date.
# Each time the system uses date, it will calculate the difference first.
# Check its working by:
while True:
    CURRENT_DATE_TIME = dt.datetime.now() - (dt.datetime.now()-SERVER_DATE_TIME)
    print (CURRENT_DATE_TIME) #this line will give server time but updated. Time difference must be updated everytime server time changes
"""
#get database's date and time mainly for debug purposes
mainCursor.execute(QUERY_GET_DATE_TIME)
SERVER_DATE_TIME = mainCursor.fetchone()[1]
DEBUG_TIME_DIFFERENCE = dt.datetime.now() - SERVER_DATE_TIME
CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE
"""
- This is the main loop.
- It will be running every second the whole day and all major function will be performed here.
"""
while True:
    # Update local clock to sync with server clock
    mainCursor.execute(QUERY_GET_DATE_TIME)
    newdate = mainCursor.fetchone()[1]
    if str(SERVER_DATE_TIME) != str(newdate):
        SERVER_DATE_TIME = newdate
        DEBUG_TIME_DIFFERENCE = dt.datetime.now() - SERVER_DATE_TIME
        CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE
    else:
        CURRENT_DATE_TIME = dt.datetime.now() - DEBUG_TIME_DIFFERENCE
    utilities.printtest()
    """
    # If it is the start of the week, add schedule from schedule table to this week's schedule table
    if startOfWeek(DEBUG_TIME_DIFFERENCE):
        createWeekSchedule()
    
    # At the end fo the week, remove everything from the weekly schedule table and get it prepared for next week's schedule
    if endOfWeek(DEBUG_TIME_DIFFERENCE):
        truncateWeekSchedule()
    """

    # Commit whatever changes were made during the loop
    connection.commit()

if connection.is_connected():
    connection.close()
    print("Disconnected from the server...")
