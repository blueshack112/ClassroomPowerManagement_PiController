import globalVariablesandFunctions as gvs
"""
This section will contain all the classes used to store data in a structured format.
"""

# Class description for normal schedule item
class NormalScheduleItem:
    isActive = False
    relaysToTurnOn = ["None"]
    relaysOn = ["None"]
    roomStatusUpdated = False
    attendance = -1 # -1 means that attendance has not yet arrived
    def __init__(self, scheduleID, teacherID, roomID, courseID, dayOfWeek, slot, classLength):
        self.scheduleID = scheduleID
        self.teacherID = teacherID
        self.roomID = roomID
        self.courseID = courseID
        self.dayOfWeek = dayOfWeek
        self.slot = slot
        self.classLength = classLength
        self.isActive = False
        self.roomStatusUpdated = False
        self.attendance = -1
        self.relaysToTurnOn = ["None"]
        self.relaysOn = ["None"]
    
    # To insert in room status table
    def relaysOnToString(self):
        relaysOn = self.relaysOn
        if relaysOn[0] == "None":
            return "None"
        else:
            relaysList = ""
            for i in relaysOn:
                relaysList += str(i) + ","
            relaysList = relaysList[:-1]
            return relaysList
    
    # Calculate which relays to switch on based on attendance information
    # TODO: massive changes needed here! (decide which relay does what)
    def calculateRelaysToTurnOn(self):
        relaysToTurnOn = []
        attendance = self.attendance
        
        # if attendance has not arrived, turn on only eesentials (first row of lights and fans and 1 AC)
        if attendance == -1:
            relaysToTurnOn = [101,102]
        self.relaysToTurnOn = relaysToTurnOn
    
    # This function will tell if the room status table contains the entry of the active course
    # Returns true if table is updated and false if not
    def isRoomStatusTableUpdated(self, mainCursor):
        tableUpdated = False
        (selectRan, ifSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_ATTENDANCE_FORMAT_COURSEID.format(str(self.courseID)))
        if selectRan:
            if len(mainCursor.fetchall()) > 0:
                tableUpdated = True
        else:
            print (ifSelectError)
        self.roomStatusUpdated = tableUpdated
    
    # This function will check if the attendance of a course has been updated
    # Returns -1 if attendance is not updated and a number if it is updated
    def checkAttendanceStatus (self, mainCursor):
        tempAttendance = -1
        (attendanceRan, ifAttendanceError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_ATTENDANCE_FORMAT_COURSEID.format(str(self.courseID)))
        if attendanceRan:
            tempAttendance = mainCursor.fetchone()[0]
        else:
            print (ifAttendanceError)
        self.attendance = tempAttendance

# Class description for extra schedule item
class ExtraScheduleItem:
    isActive = False
    relaysToTurnOn = ["None"]
    relaysOn = ["None"]
    roomStatusUpdated = False
    attendance = -1 # -1 means that attendance has not yet arrived
    def __init__(self, extraScheduleID, teacherID, roomID, courseID, dayOfWeek, slot, classLength, acceptStatus):
        self.extra_schedule_id = extraScheduleID
        self.teacherID = teacherID
        self.roomID = roomID
        self.courseID = courseID
        self.dayOfWeek = dayOfWeek
        self.slot = slot
        self.classLength = classLength
        self.acceptStatus = acceptStatus
        self.isActive = False
        self.roomStatusUpdated = False
        self.attendance = -1
        self.relaysToTurnOn = ["None"]
        self.relaysOn = ["None"]
    
    # To insert in room status table
    def relaysOnToString(self):
        relaysOn = self.relaysOn
        if relaysOn[0] == "None":
            return "None"
        else:
            relaysList = ""
            for i in relaysOn:
                relaysList += str(i) + ","
            relaysList = relaysList[:-1]
            return relaysList

    # Calculate which relays to switch on based on attendance information
    # TODO: massive changes needed here! (decide which relay does what)
    def calculateRelaysToTurnOn(self):
        relaysToTurnOn = []
        attendance = self.attendance
        
        # if attendance has not arrived, turn on only eesentials (first row of lights and fans and 1 AC)
        if attendance == -1:
            relaysToTurnOn = [101,102]
        self.relaysToTurnOn = relaysToTurnOn
    
    # This function will tell if the room status table contains the entry of the active course
    # Returns true if table is updated and false if not
    def isRoomStatusTableUpdated(self, mainCursor):
        tableUpdated = False
        (selectRan, ifSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_ATTENDANCE_FORMAT_COURSEID.format(str(self.courseID)))
        if selectRan:
            if len(mainCursor.fetchall()) > 0:
                tableUpdated = True
        else:
            print (ifSelectError)
        self.roomStatusUpdated = tableUpdated
    
    # This function will check if the attendance of a course has been updated
    # Returns -1 if attendance is not updated and a number if it is updated
    def checkAttendanceStatus (self, mainCursor):
        tempAttendance = -1
        (attendanceRan, ifAttendanceError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_ATTENDANCE_FORMAT_COURSEID.format(str(self.courseID)))
        if attendanceRan:
            tempAttendance = mainCursor.fetchone()[0]
        else:
            print (ifAttendanceError)
        self.attendance = tempAttendance
    
