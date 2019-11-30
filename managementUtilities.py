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
    mainCursor = connection.cursor()
    print("Connected to the server...")
except Exception as e:
    print("Could not connect to the server, exiting...")
    print (e)
    exit()
"""

"""
This section will contain all the query templates and
important variables needed during the running of this file.
"""
THIS_ROOM = 1001
# For debugging, get date and time
QUERY_GET_DATE_TIME = "SELECT debug_id, system_date_time_to_set FROM tbl_debug "

# for the contents of current week's table
QUERY_GET_WEEK_SCHEDULE = "SELECT week_schedule_id, schedule_id, extra_schedule_id FROM tbl_week_schedule"
QUERY_INSERT_WEEK_SCHEDULE_NORMAL_FORMAT = "INSERT INTO tbl_week_schedule (schedule_id) VALUES {};"
QUERY_INSERT_WEEK_SCHEDULE_EXTRA_FORMAT = "INSERT INTO tbl_week_schedule (extra_schedule_id) VALUES {};"
QUERY_TRUNCATE_WEEK_SCHEDULE = "TRUNCATE TABLE tbl_week_schedule"

# for the contents of schedule table
QUERY_GET_NORMAL_SCHEDULE_ID = "SELECT schedule_id FROM tbl_schedule"
QUERY_GET_EXTRA_SCHEDULE_ID = "SELECT extra_schedule_id FROM tbl_extra_schedule"

# Select query for views needed to a lot schedule items
QUERY_GET_NORMAL_SCHEDULE_ROOM_FORMAT = "SELECT schedule_id, teacher_id, room_id, course_id, day_of_week, slot, class_length FROM view_normal_schedule WHERE room_id = {} and day_of_week = {}"
QUERY_GET_EXTRA_SCHEDULE_ROOM_FORMAT = "SELECT extra_schedule_id, teacher_id, room_id, course_id, day_of_week, slot, class_length, accept_status FROM view_extra_schedule WHERE room_id = {} and day_of_week = {}"
"""
This section will contain all the classes used to store data in a structured format.
"""
class NormalScheduleItem:
    def __init__(self, scheduleID, teacherID, roomID, courseID, dayOfWeek, slot, classLength):
        self.scheduleID = scheduleID
        self.teacherID = teacherID
        self.roomID = roomID
        self.courseID = courseID
        self.dayOfWeek = dayOfWeek
        self.slot = slot
        self.classLength = classLength

class ExtraScheduleItem:
    def __init__(self, extraScheduleID, teacherID, roomID, courseID, dayOfWeek, slot, classLength, acceptStatus):
        self.extra_schedule_id = extraScheduleID
        self.teacherID = teacherID
        self.roomID = roomID
        self.courseID = courseID
        self.dayOfWeek = dayOfWeek
        self.slot = slot
        self.classLength = classLength
        self.acceptStatus = acceptStatus

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

# Function that checks it right now is the start of the week
# Returns true or false
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

# Function that checks it right now is the start of the week
# Returns true or false
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
# Returns true or false as success signal
def truncateWeekSchedule(mainCursor):
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
            truncateResult = truncateResult # Just to remove "Unused variable" warnings
        else:
            print (ifTruncateError)
            return False
    else: 
        print ("Table already empty.")
        return True
    print ("Week schedule truncated!")
    return True

# Fcuntion that will get all entries from schedule and put them in current week's table
# Returns true or false as success signal
def createWeekSchedule(mainCursor):    
    # Get all data from schedule and extra schedule table and assign it to current week's schedule table
    (normalSelectRan, ifNormalSelectError) = runQuery(mainCursor, QUERY_GET_NORMAL_SCHEDULE_ID)
    if normalSelectRan:
        normalSelectResult = mainCursor.fetchall()
    else:
        print (ifNormalSelectError)
        return False
    (extraSelectRan, ifExtraSelectError) = runQuery(mainCursor, QUERY_GET_EXTRA_SCHEDULE_ID)
    if extraSelectRan:
        extraSelectResult = mainCursor.fetchall()
    else:
        print (ifExtraSelectError)
        return False

    # Generate insert queries
    insertQueries = []
    for i in normalSelectResult:
        tempquery = QUERY_INSERT_WEEK_SCHEDULE_NORMAL_FORMAT.format("(" + str(i[0]) + ")")
        insertQueries.append(tempquery)
    for i in extraSelectResult:
        tempquery = QUERY_INSERT_WEEK_SCHEDULE_EXTRA_FORMAT.format("(" + str(i[0]) + ")")
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

# This function will check if the weekly schedule table is not empty
# Returns True if data is present and False if table is empty
def isWeekScheduleCreated(mainCursor):
    (selectRan, ifSelectError) = runQuery(mainCursor, QUERY_GET_WEEK_SCHEDULE)
    if selectRan:
        entriesInTable = len(mainCursor.fetchall())
    else:
        print (ifSelectError)
        return False
    
    if entriesInTable > 0:
        return True
    else:
        return False

# This function will calculate the current slot based on current time
# Returns 0 if not a slot and 1-7 if it is a slot
def getCurrentSlot(DEBUG_TIME_DIFFERENCE):
    rightnow = dt.datetime.now() - DEBUG_TIME_DIFFERENCE
    
    # Starting and ending time ranges of each time slot
    slot1RangeStart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 8, 29, 0, 0)
    slot1RangeEnd = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 9, 25, 0, 0)
    slot2RangeStart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 9, 29, 0, 0)
    slot2RangeEnd = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 10, 25, 0, 0)
    slot3RangeStart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 10, 29, 0, 0)
    slot3RangeEnd = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 11, 25, 0, 0)
    slot4RangeStart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 11, 29, 0, 0)
    slot4RangeEnd = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 12, 25, 0, 0)
    slot5RangeStart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 13, 9, 0, 0)
    slot5RangeEnd = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 14, 5, 0, 0)
    slot6RangeStart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 14, 9, 0, 0)
    slot6RangeEnd = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 15, 5, 0, 0)
    slot7RangeStart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 15, 9, 0, 0)
    slot7RangeEnd = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 16, 5, 0, 0)

    if rightnow > slot1RangeStart and rightnow < slot1RangeEnd:
        return 1
    elif rightnow > slot2RangeStart and rightnow < slot2RangeEnd:
        return 2
    elif rightnow > slot3RangeStart and rightnow < slot3RangeEnd:
        return 3
    elif rightnow > slot4RangeStart and rightnow < slot4RangeEnd:
        return 4
    elif rightnow > slot5RangeStart and rightnow < slot5RangeEnd:
        return 5
    elif rightnow > slot6RangeStart and rightnow < slot6RangeEnd:
        return 6
    elif rightnow > slot7RangeStart and rightnow < slot7RangeEnd:
        return 7
    elif (rightnow > slot1RangeEnd and rightnow < slot2RangeStart) or (rightnow > slot2RangeEnd and rightnow < slot3RangeStart) or (rightnow > slot3RangeEnd and rightnow < slot4RangeStart) or (rightnow > slot5RangeEnd and rightnow < slot6RangeStart) or (rightnow > slot6RangeEnd and rightnow < slot7RangeStart):
        return 0 # 0 Means its the break session
    elif rightnow > slot4RangeEnd and rightnow < slot5RangeStart:
        return -1
    else:
        return -1 # -1 Means that its the end of day right now

# This gets the schedule items from view_normal_schedule and view_extra_schedule based on room id
# Returns a list of normal and extra schedule items for the main controller to use
def getScheduleItems(mainCursor, dayOfWeek):
    normalSelectResult = None
    normalSelectResult = None
    (normalSelectRan, ifNormalSelectError) = runQuery(mainCursor, QUERY_GET_NORMAL_SCHEDULE_ROOM_FORMAT.format(str(THIS_ROOM), str(dayOfWeek)))
    if normalSelectRan:
        normalSelectResult = mainCursor.fetchall()
    else:
        print (ifNormalSelectError)
    
    (extraSelectRan, ifExtraSelectError) = runQuery(mainCursor, QUERY_GET_EXTRA_SCHEDULE_ROOM_FORMAT.format(str(THIS_ROOM), str(dayOfWeek)))
    if extraSelectRan:
        extraSelectResult = mainCursor.fetchall()
    else:
        print (ifExtraSelectError)
    scheduleItems = []
    for i in normalSelectResult:
        temp = NormalScheduleItem(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
        scheduleItems.append(temp)
    for i in extraSelectResult:
        temp = ExtraScheduleItem(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        scheduleItems.append(temp)
    
    return scheduleItems
    

# This section is also for debugging purposes only.
# getScheduleItems(mainCursor, 1)
# connection.commit()
# connection.close()
