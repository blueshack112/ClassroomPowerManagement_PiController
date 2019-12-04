import globalVariablesandFunctions as gvs
import relayController
"""
This section will contain all the classes used to store data in a structured format.
"""

# Class description for normal schedule item
class NormalScheduleItem:
    def __init__(self, scheduleID, teacherID, roomID, courseID, dayOfWeek, slot, classLength):
        self.scheduleID = scheduleID
        self.teacherID = teacherID
        self.roomID = roomID
        self.courseID = courseID
        self.dayOfWeek = dayOfWeek
        self.slot = slot
        self.activeSlot = slot
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


    # Calculate which relays to switch on based on attendance information
    def calculateRelaysToTurnOn(self):
        relaysToTurnOn = []
        attendance = self.attendance

        # if attendance has not arrived, turn on only eesentials (first row of lights and fans and Front AC)
        if attendance <= 10:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
        elif attendance <= 20:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
        elif attendance <= 30:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_ROW_3)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
            if attendance > 25:
                relaysToTurnOn.append(relayController.RELAY_AC_BACK)
        elif attendance <= 40:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_ROW_3)
            relaysToTurnOn.append(relayController.RELAY_ROW_4)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
            relaysToTurnOn.append(relayController.RELAY_AC_BACK)
        elif attendance <= 50:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_ROW_3)
            relaysToTurnOn.append(relayController.RELAY_ROW_4)
            relaysToTurnOn.append(relayController.RELAY_ROW_5)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
            relaysToTurnOn.append(relayController.RELAY_AC_BACK)
        elif attendance <= 60:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_ROW_3)
            relaysToTurnOn.append(relayController.RELAY_ROW_4)
            relaysToTurnOn.append(relayController.RELAY_ROW_5)
            relaysToTurnOn.append(relayController.RELAY_ROW_6)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
            relaysToTurnOn.append(relayController.RELAY_AC_BACK)
        
        relaysToTurnOn.sort()
        self.relaysToTurnOn = relaysToTurnOn

    # This function will switch relay pins on based on the relays that need to turn on
    # Doesn't return anything, just asks raspberry pi to turn switches on and updates the relaysOn variables
    def switchRelays(self):
        relaysToTurnOn = self.relaysToTurnOn
        relaysOn = []
        
        # If no relays need to turn on
        if relaysToTurnOn[0] == "None":
            relaysOn = relaysToTurnOn
            self.relaysOn = relaysOn
            return
        
        for i in relaysToTurnOn:
            if i == relayController.RELAY_ROW_1:
                relayController.switchOn(relayController.RELAY_101)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_2:
                relayController.switchOn(relayController.RELAY_102)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_3:
                relayController.switchOn(relayController.RELAY_103)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_4:
                relayController.switchOn(relayController.RELAY_104)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_5:
                relayController.switchOn(relayController.RELAY_105)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_6:
                relayController.switchOn(relayController.RELAY_106)
                relaysOn.append(i)
            elif i == relayController.RELAY_AC_FRONT:
                relayController.switchOn(relayController.RELAY_107)
                relaysOn.append(i)
            elif i == relayController.RELAY_AC_BACK:
                relayController.switchOn(relayController.RELAY_108)
                relaysOn.append(i)
        relaysOn.sort()
        self.relaysOn = relaysOn
            

# Class description for extra schedule item
class ExtraScheduleItem:
    def __init__(self, extraScheduleID, teacherID, roomID, courseID, dayOfWeek, slot, classLength, acceptStatus):
        self.extra_schedule_id = extraScheduleID
        self.teacherID = teacherID
        self.roomID = roomID
        self.courseID = courseID
        self.dayOfWeek = dayOfWeek
        self.slot = slot
        self.activeSlot = slot
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
    
    
        tempAttendance = -1
        (attendanceRan, ifAttendanceError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_ATTENDANCE_FORMAT_COURSEID.format(str(self.courseID)))
        if attendanceRan:
            tempAttendance = mainCursor.fetchone()[0]
        else:
            print (ifAttendanceError)
        self.attendance = tempAttendance

    
    # Calculate which relays to switch on based on attendance information
    def calculateRelaysToTurnOn(self):
        relaysToTurnOn = []
        attendance = self.attendance

        # if attendance has not arrived, turn on only eesentials (first row of lights and fans and Front AC)
        if attendance <= 10:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
        elif attendance <= 20:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
        elif attendance <= 30:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_ROW_3)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
            if attendance > 25:
                relaysToTurnOn.append(relayController.RELAY_AC_BACK)
        elif attendance <= 40:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_ROW_3)
            relaysToTurnOn.append(relayController.RELAY_ROW_4)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
            relaysToTurnOn.append(relayController.RELAY_AC_BACK)
        elif attendance <= 50:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_ROW_3)
            relaysToTurnOn.append(relayController.RELAY_ROW_4)
            relaysToTurnOn.append(relayController.RELAY_ROW_5)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
            relaysToTurnOn.append(relayController.RELAY_AC_BACK)
        elif attendance <= 60:
            relaysToTurnOn.append(relayController.RELAY_ROW_1)
            relaysToTurnOn.append(relayController.RELAY_ROW_2)
            relaysToTurnOn.append(relayController.RELAY_ROW_3)
            relaysToTurnOn.append(relayController.RELAY_ROW_4)
            relaysToTurnOn.append(relayController.RELAY_ROW_5)
            relaysToTurnOn.append(relayController.RELAY_ROW_6)
            relaysToTurnOn.append(relayController.RELAY_AC_FRONT)
            relaysToTurnOn.append(relayController.RELAY_AC_BACK)
        
        relaysToTurnOn.sort()
        self.relaysToTurnOn = relaysToTurnOn
    
    # This function will switch relay pins on based on the relays that need to turn on
    # Doesn't return anything, just asks raspberry pi to turn switches on and updates the relaysOn variables
    def switchRelays(self):
        relaysToTurnOn = self.relaysToTurnOn
        relaysOn = []
        
        # If no relays need to turn on
        if relaysToTurnOn[0] == "None":
            relaysOn = relaysToTurnOn
            self.relaysOn = relaysOn
            return
        
        for i in relaysToTurnOn:
            if i == relayController.RELAY_ROW_1:
                relayController.switchOn(relayController.RELAY_101)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_2:
                relayController.switchOn(relayController.RELAY_102)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_3:
                relayController.switchOn(relayController.RELAY_103)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_4:
                relayController.switchOn(relayController.RELAY_104)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_5:
                relayController.switchOn(relayController.RELAY_105)
                relaysOn.append(i)
            elif i == relayController.RELAY_ROW_6:
                relayController.switchOn(relayController.RELAY_106)
                relaysOn.append(i)
            elif i == relayController.RELAY_AC_FRONT:
                relayController.switchOn(relayController.RELAY_107)
                relaysOn.append(i)
            elif i == relayController.RELAY_AC_BACK:
                relayController.switchOn(relayController.RELAY_108)
                relaysOn.append(i)
        relaysOn.sort()
        self.relaysOn = relaysOn     
