import datetime as dt
import os
import time
import mysql.connector as cn
from operator import itemgetter
import globalVariablesandFunctions as gvs
from utilityClasses import NormalScheduleItem
from utilityClasses import ExtraScheduleItem
import relayController


"""# This section is only for debugging purposes
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

SERVER_DATE_TIME = dt.datetime.now()
(debugDateRan, ifDebugDateError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_DATE_TIME)
if debugDateRan:
    SERVER_DATE_TIME = mainCursor.fetchone()[1]
else:
    print(ifDebugDateError)
DEBUG_TIME_DIFFERENCE = dt.datetime.now() - SERVER_DATE_TIME
"""


"""
This section will contain all the function used by the main file.
"""
# Database connection variables
dbHost = "192.168.18.4"
offsiteDbHost = "localhost"
dbPort = "3306"
dbUsername = "areeba"
dbPassword = "areebafyp"
dbDatabase = "db_classroom_management"

# Funtion that connects to the server and returns the connection and mainCursor object
# Returns a tuple of True or False as success signals and a connection variable
def connectToDatabase():
    connection = None
    isConnected = False
    # Database connection and getting cursor
    while not isConnected:
        try:
            connection = cn.connect(host=dbHost, user=dbUsername, passwd=dbPassword, database=dbDatabase)
            mainCursor = connection.cursor()
            print("Connected to the server...")
            isConnected = True
            return isConnected, connection, mainCursor
        except Exception as e:
            print (e)
            print("Could not connect to the server, retrying in 5 seconds...")
            time.sleep(5)

# Funtion that connects to the server and returns the server's date time and time difference
# Returns a tuple of timedifference and the server's date time
def getDebugTimeDifference(previousServerDateTime, previousTimeDifference, mainCursor):
    timeDifference = None
    serverDateTime = None
    # If we are debugging
    if gvs.DEBUG:
        # Update local clock to sync with server clock
        (debugDateRan, ifDebugDateError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_DATE_TIME)
        if debugDateRan:
            newdate = mainCursor.fetchone()[1]
            if previousServerDateTime != newdate:
                serverDateTime = newdate
            else:
                return previousTimeDifference, previousServerDateTime
        else:
            print ("getDebugTimeDifference: ")
            print(ifDebugDateError)
            serverDateTime = previousServerDateTime
    else:
        serverDateTime = dt.datetime.now()
    
    timeDifference = dt.datetime.now() - serverDateTime
    return timeDifference, serverDateTime

# Function that checks it right now is the start of the week
# Returns true or false
def isStartOfWeek(DEBUG_TIME_DIFFERENCE):
    rightnow = dt.datetime.now()-DEBUG_TIME_DIFFERENCE

    # Ranges just to be safe
    rangestart = dt.datetime(rightnow.year, rightnow.month, rightnow.day, 8, 29, 0, 0)
    
    # Monday 8:30 is start of the week
    if not rightnow.weekday() == 5 or rightnow.weekday() == 6:
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

# Fcuntion that will delete all entries from current week's table and extra schedule table
# Returns true or false as success signal
def truncateWeekSchedule(mainCursor):
    # Run select normal query and get result if there was no error
    (normalQueryRan, ifNormalError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_WEEK_SCHEDULE)
    if normalQueryRan:
        normalResult = mainCursor.fetchall()
    else:
        print ("truncateWeekSchedule-1: ")
        print (ifNormalError)
        return False

    # Run select normal query and get result if there was no error
    (extraQueryRan, ifError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_EXTRA_WEEK_SCHEDULE)
    if extraQueryRan:
        extraResult = mainCursor.fetchall()
    else:
        print ("truncateWeekSchedule-2: ")
        print (ifError)
        return False
    
    # Truncate normal table if their are entries present else return True
    entriesInNormalTable = len(normalResult)    
    if entriesInNormalTable > 0:
        (truncateQueryRan, ifTruncateError) = gvs.runQuery(mainCursor, gvs.QUERY_TRUNCATE_WEEK_SCHEDULE)
        if not truncateQueryRan:
            print ("truncateWeekSchedule-3: ")
            print (ifTruncateError)
            return False
    else: 
        print ("Normal table already empty.")
        return True

    # Truncate extra table if their are entries present else return True
    entriesInExtraTable = len(extraResult)
    if entriesInExtraTable > 0:
        (truncateQueryRan, ifTruncateError) = gvs.runQuery(mainCursor, gvs.QUERY_TRUNCATE_EXTRA_WEEK_SCHEDULE)
        if not truncateQueryRan:
            print ("truncateWeekSchedule-3: ")
            print (ifTruncateError)
            return False
    else: 
        print ("Extra table already empty.")
        return True
    
    print ("Normal and extra week schedule truncated!")
    return True

# Fcuntion that will get all entries from schedule and put them in current week's table
# Returns true or false as success signal
def createWeekSchedule(mainCursor):    
    # Get all data from normal schedule and assign it to current week's schedule table
    (normalSelectRan, ifNormalSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_NORMAL_SCHEDULE_ID)
    if normalSelectRan:
        normalSelectResult = mainCursor.fetchall()
    else:
        print ("createWeekSchedule-1: ")
        print (ifNormalSelectError)
        return False

    # Generate insert queries
    insertQueries = []
    for i in normalSelectResult:
        tempquery = gvs.QUERY_INSERT_WEEK_SCHEDULE_NORMAL_FORMAT_VALUES.format("(" + str(i[0]) + ")")
        insertQueries.append(tempquery)
    
    # Execute insert queries
    counter = 0 # Will keep count of successful insertions
    for i in insertQueries:
        (insertRan, ifInsertError) = gvs.runQuery(mainCursor, i)
        if not insertRan:
            print ("createWeekSchedule-2: ")
            print (ifInsertError)
        else:
            counter = counter + 1
    print ("Week schedule created!\nInserted: " + str(counter) + " entries.")
    return True

# This function will check if the weekly schedule table is not empty
# Returns True if data is present and False if table is empty
def isWeekScheduleCreated(mainCursor):
    (selectRan, ifSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_WEEK_SCHEDULE)
    if selectRan:
        entriesInTable = len(mainCursor.fetchall())
    else:
        print ("isWeekScheduleCreated: ")
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
    normalSelectResult = []
    extraSelectResult = []
    (normalSelectRan, ifNormalSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_NORMAL_SCHEDULE_ROOM_FORMAT_ROOMID_DAYOFWEEK.format(str(gvs.THIS_ROOM), str(dayOfWeek)))
    if normalSelectRan:
        normalSelectResult = mainCursor.fetchall()
    else:
        print ("getScheduleItems-1: ")
        print (ifNormalSelectError)
    
    (extraSelectRan, ifExtraSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_EXTRA_SCHEDULE_ROOM_FORMAT_ROOMID_DAYOFWEEK.format(str(gvs.THIS_ROOM), str(dayOfWeek)))
    if extraSelectRan:
        extraSelectResult = mainCursor.fetchall()
    else:
        print ("getScheduleItems-2: ")
        print (ifExtraSelectError)
    
    scheduleItems = []
    for i in normalSelectResult:
        temp = NormalScheduleItem(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
        scheduleItems.append(temp)
    for i in extraSelectResult:
        temp = ExtraScheduleItem(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9])
        scheduleItems.append(temp)
    
    # Sort the elements inside the list in ascending order
    if len(scheduleItems) > 0:
        scheduleItems = sorted(scheduleItems, key=lambda k: k.slot) 
    return scheduleItems

# This function will request teh realy controller to switch eerything off
# It is called when there is not active course
def switchEverythingOff(mainCursor):
    # Request relayController to switch everything off
    relayController.switchOffAll()

    # Check if there is something on room_status table and move it to history table
    (selectRan, ifSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_FORMAT_ROOMID.format(str(gvs.THIS_ROOM)))
    if selectRan:
        selectResult = mainCursor.fetchall()
        if len(selectResult) == 0:
            return
        selectResult = selectResult[0]
    else:
        print ("switchEverythingOff-1: ")
        print (ifSelectError)
    
    # If there is an entry against this room, send it to history table
    roomStatusDate = str(selectResult[0])
    roomStatusRoomID = str(selectResult[1])
    roomStatusSlot = str(selectResult[2])
    roomStatusRelayUsed = str(selectResult[3])

    insertValues = "("
    insertValues += "'" + roomStatusDate + "',"
    insertValues += "'" + roomStatusRoomID + "',"
    insertValues += "'" + roomStatusSlot + "',"
    insertValues += "'" + roomStatusRelayUsed + "')"
    
    (insertRan, ifInsertError) = gvs.runQuery(mainCursor, gvs.QUERY_INSERT_HISTORY_FORMAT_VALUES.format(insertValues))
    if not insertRan:
        print ("switchEverythingOff-2: ")
        print (ifInsertError)
        return
    
    # Now remove the entry from room_status table
    (deleteRan, ifDeleteError) = gvs.runQuery(mainCursor, gvs.QUERY_DELETE_ROOM_STATUS_FORMAT_ROOMID.format(str(gvs.THIS_ROOM)))
    if not deleteRan:
        print ("switchEverythingOff-3: ")
        print (ifDeleteError)
        return
    print ("-Everything switched off and tables updated.")

# This function checks if slot has moved on but the room_status table is still active on the old one
# Check if slot on room status is different than activeCourse's active slot
# If there is a difference, shift the entry to history table and create new entry for new slot
def adjustForSlotChanges(mainCursor, activeCourse, currentSlot):
    if activeCourse.slot == activeCourse.activeSlot:
        print ("-No slot changes necessary.")
        return

    if str(activeCourse.courseID):
        (selectRan, ifSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_FORMAT_COURSEID.format(str(-1)))
    else:
        (selectRan, ifSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_FORMAT_COURSEID.format(str(activeCourse.courseID)))
    if selectRan:
        selectResult =  mainCursor.fetchall()
        if len(selectResult) == 0:
            print ("-No slot changes necessary.")
            return
        else:
            selectResult = selectResult[0]

    else:
        print ("adjustForSlotChanges-1: ")
        print (ifSelectError)
    
    roomStatusDate = str(selectResult[0])
    roomStatusRoomID = selectResult[1]
    roomStatusSlot = selectResult[2]
    roomStatusRelayUsed = selectResult[3]
    
    if roomStatusSlot == activeCourse.activeSlot:
        print ("Slot changes already done.")
        return

    insertValues = "("
    insertValues += "'" + roomStatusDate + "',"
    insertValues += "'" + str(roomStatusRoomID) + "',"
    insertValues += "'" + str(roomStatusSlot) + "',"
    insertValues += "'" + roomStatusRelayUsed + "')"

    # Insert current room_status entry to history
    (insertRan, ifInsertError) = gvs.runQuery(mainCursor, gvs.QUERY_INSERT_HISTORY_FORMAT_VALUES.format(insertValues))
    if not insertRan:
        print ("adjustForSlotChanges-2: ")
        print (ifInsertError)
        return
    
    # Update current room_status entry to next slot
    if str(activeCourse.courseID):
        (updateRan, ifUpdateError) = gvs.runQuery(mainCursor, gvs.QUERY_UPDATE_ROOM_STATUS_FORMAT_SLOT_COURSEID.format(str(activeCourse.activeSlot), str(-1)))
    else:
        (updateRan, ifUpdateError) = gvs.runQuery(mainCursor, gvs.QUERY_UPDATE_ROOM_STATUS_FORMAT_SLOT_COURSEID.format(str(activeCourse.activeSlot), str(activeCourse.courseID)))
    if not updateRan:
        print ("adjustForSlotChanges-3: ")
        print (ifUpdateError)
        return
    print ("-Slot changes made.")


# This function will turn on the appliances based on the requirements
# returns a boolean true or false as success signal and an updated object of ScheduleItem (normal or extra)
def turnOnAppliances(mainCursor, activeCourse, DEBUG_TIME_DIFFERENCE):
    rightnow = dt.datetime.now() - DEBUG_TIME_DIFFERENCE
    # Check if room status table is updated
    activeCourse.isRoomStatusTableUpdated(mainCursor)

    # If room status table is not updated, run the insert query. OTherwise get attendance
    if activeCourse.roomStatusUpdated:
        activeCourse.checkAttendanceStatus(mainCursor)
        activeCourse.calculateRelaysToTurnOn()
    else:
        # Check if there is an entry and move it to history table (There will be the entry of older course)
        (selectRan, ifSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_FORMAT_ROOMID.format(str(gvs.THIS_ROOM)))
        if selectRan:
            selectResult = mainCursor.fetchall()
            if not len(selectResult) == 0:
                selectResult = selectResult[0]
                # If there is an entry against this room, send it to history table
                roomStatusDate = str(selectResult[0])
                roomStatusRoomID = str(selectResult[1])
                roomStatusSlot = str(selectResult[2])
                roomStatusRelayUsed = str(selectResult[3])

                insertValues = "("
                insertValues += "'" + roomStatusDate + "',"
                insertValues += "'" + roomStatusRoomID + "',"
                insertValues += "'" + roomStatusSlot + "',"
                insertValues += "'" + roomStatusRelayUsed + "')"

                (insertRan, ifInsertError) = gvs.runQuery(mainCursor, gvs.QUERY_INSERT_HISTORY_FORMAT_VALUES.format(insertValues))
                if not insertRan:
                    print ("turnOnAppliances-1: ")
                    print (ifInsertError)
                    return
    
                # Now remove the entry from room_status table
                (deleteRan, ifDeleteError) = gvs.runQuery(mainCursor, gvs.QUERY_DELETE_ROOM_STATUS_FORMAT_ROOMID.format(str(gvs.THIS_ROOM)))
                if not deleteRan:
                    print ("turnOnAppliances-2: ")
                    print (ifDeleteError)
                    return

        else:
            print ("turnOnAppliances-3: ")
            print (ifSelectError)
            return

        activeCourse.attendance = -1
        activeCourse.calculateRelaysToTurnOn()
        # Generate values to insert in the format: (room_id, course_id, relay_used, class_date, slot)
        values = "("
        values += "'" + str(activeCourse.roomID) + "',"
        if str(activeCourse.courseID) == 'None':
            values += "'" + str(-1) + "',"
        else:
            values += "'" + str(activeCourse.courseID) + "',"
        values += "'" + str(activeCourse.relaysOnToString()) + "',"
        values += "'" + str(rightnow.date()) + "',"
        values += "'" + str(activeCourse.slot) + "')"
        
        # Execute the query
        (insertRan, ifInsertError) = gvs.runQuery(mainCursor, gvs.QUERY_INSERT_ROOM_STATUS_FORMAT_VALUES.format(values))
        if insertRan:
            activeCourse.roomStatusUpdated = True
        else:
            print ("turnOnAppliances-4: ")
            print (ifInsertError)
    
    # This part will switch on relays and update the relaysOn variable
    activeCourse.switchRelays()

    # Executing query to udpate the relays on variable
    if str(activeCourse.courseID) == 'None':
        (updateRan, ifUpdateError) = gvs.runQuery(mainCursor, gvs.QUERY_UPDATE_ROOM_STATUS_FORMAT_RELAYSUSED_COURSEID.format(activeCourse.relaysOnToString(), str(-1)))
    else:
        (updateRan, ifUpdateError) = gvs.runQuery(mainCursor, gvs.QUERY_UPDATE_ROOM_STATUS_FORMAT_RELAYSUSED_COURSEID.format(activeCourse.relaysOnToString(), str(activeCourse.courseID)))
    if not updateRan:
        print ("turnOnAppliances-5: ")
        print (ifUpdateError)
    return activeCourse


# This section is also for debugging purposes only.
#CURRENT_SLOT = 2
#activeCourse = NormalScheduleItem(10, 1002, 1001, 1001, 3, 1, 2)
#activeCourse.activeSlot = activeCourse.activeSlot + 1
#print (vars(turnOnAppliances(mainCursor, activeCourse, DEBUG_TIME_DIFFERENCE)))
#adjustForSlotChanges(mainCursor, activeCourse, CURRENT_SLOT)
#switchEverythingOff()
#connection.commit()
#connection.close()
