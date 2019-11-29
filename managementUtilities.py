import datetime as dt
import mysql.connector as cn

"""
# This section is only for debugging purposes
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
    print("Connected to the server...")
except Exception as e:
    print("Could not connect to the server, exiting...")
    print (e)
    exit()
"""

"""
This section will contain all the query templates
needed during the running of this file.
"""
# For debugging, get date and time
QUERY_GET_DATE_TIME = "SELECT debug_id, system_date_time_to_set FROM tbl_debug "

# for the contents of current week's table
QUERY_GET_WEEK_SCHEDULE = "SELECT week_schedule_id, schedule_id, extra_schedule_id FROM tbl_week_schedule"
QUERY_INSERT_WEEK_SCHEDULE_NORMAL_FORMAT = "INSERT INTO tbl_week_schedule (schedule_id) VALUES {};"
QUERY_TRUNCATE_WEEK_SCHEDULE = "TRUNCATE TABLE tbl_week_schedule"

# for the contents of schedule table
QUERY_GET_SCHEDULE_SCHED_ID = "SELECT schedule_id FROM tbl_schedule"

"""
This section will contain all the function used by the main file.
"""
# Function solely to run queries and grab exceptions in a clean manner
# Returns an error and boolean false if an error occures
# Returns true and a "Done" string if it was successful
def runQuery (mainCursor, query):
    try:
        mainCursor.execute(query)
    except Exception as e:
        return (False, e)
    return (True, "Done")

# Function that checks it right now is the start of the week.
# Returns true or false.
def isStartOfWeek(DEBUG_TIME_DIFFERENCE):
    rightnow = dt.datetime.now()-DEBUG_TIME_DIFFERENCE

    # Ranges just to be safe
    rangestart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 8, 29, 0, 0)
    rangeend = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 8, 31, 0, 0)
    
    # Monday 8:30 is start of the week
    if rightnow > rangestart and rightnow < rangeend and rightnow.weekday() == 0:
        return True
    else:
        return False

# Function that checks it right now is the start of the week.
# Returns true or false.
def isEndOfWeek(DEBUG_TIME_DIFFERENCE):
    rightnow = dt.datetime.now()-DEBUG_TIME_DIFFERENCE

    # Ranges just to be safe
    rangestart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 16, 15, 0, 0)
    
    # Friday after 16:30, saturday and sunday are end of week
    if (rightnow > rangestart and rightnow.weekday() == 4) or rightnow.weekday() == 5 or rightnow.weekday() == 6:
        return True
    else:
        return False

# Fcuntion that will delete all entries from current week's table
# Returns true or false as success signal.
def truncateWeekSchedule(connection):
    mainCursor = connection.cursor()
    #Run select query and get result if there was no error    
    (queryRan, ifError) = runQuery(mainCursor, QUERY_GET_WEEK_SCHEDULE)
    if queryRan:
        result = mainCursor.fetchall()
    else:
        print (ifError + " here.")
        return False
    
    # Truncate Table if their are entries present else return True
    entriesInTable = len(result)
    if entriesInTable > 0:
        (truncateQueryRan, ifTruncateError) = runQuery(mainCursor, QUERY_TRUNCATE_WEEK_SCHEDULE)
        if truncateQueryRan:
            truncateResult = mainCursor._rowcount
        else:
            print (ifTruncateError)
            return False
    else: 
        print ("Table already empty.")
        return True
    print ("Week schedule truncated!")
    return True

# Fcuntion that will get all entries from schedule and put them in current week's table
# Returns true or false as success signal.
def createWeekSchedule(connection):
    mainCursor = connection.cursor()
    
    # Get all data from schedule table and assign it to current week's schedule table
    (selectRan, ifSelectError) = runQuery(mainCursor, QUERY_GET_SCHEDULE_SCHED_ID)
    if selectRan:
        selectResult = mainCursor.fetchall()
    else:
        print (ifSelectError)
        return False

    # Generate insert queries
    insertQueries = []
    for i in selectResult:
        tempquery = QUERY_INSERT_WEEK_SCHEDULE_NORMAL_FORMAT.format("(" + str(i[0]) + ")")
        insertQueries.append(tempquery)
    
    # Execute insert queries
    counter = 0 # Will keep count of successful insertions
    for i in insertQueries:
        (insertRan, ifInsertError) = runQuery(mainCursor, i)
        if not insertRan:
            print (ifInsertError)
        else:
            counter = counter + 1
    print ("Week schedule created!\nInserted: " + str(counter) + " entries.")
    return True

"""
# This section is also for debuggin purposes only.
#truncateWeekSchedule(connection)
createWeekSchedule(connection)
connection.commit()
connection.close()
"""