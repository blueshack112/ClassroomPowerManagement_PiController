import mysql.connector as cn
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
            selectResult = mainCursor.fetchall()
            if len(selectResult) > 0:
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
        
        relayController.switchOffAll()
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
    def __init__(self, extraScheduleID, teacherID, roomID, courseID, dayOfWeek, slot, classLength, acceptStatus, requestType, message):
        self.extra_schedule_id = extraScheduleID
        self.teacherID = teacherID
        self.roomID = roomID
        self.courseID = courseID
        self.dayOfWeek = dayOfWeek
        self.slot = slot
        self.activeSlot = slot
        self.classLength = classLength
        self.acceptStatus = acceptStatus
        self.requestType = requestType
        self.message = message
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
        if str(self.courseID) == 'None':
            (selectRan, ifSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_ROOM_STATUS_ATTENDANCE_FORMAT_COURSEID.format(str(-1)))            
        else:
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

        # If this is an HOD override schedule item, then get the relays to turn on form the message
        if self.requestType == 'HOD':
            message = self.message
            
            temprelays = []
            while (',' in message):
                temprelays.append(int(message[:message.index(',')]))
                message = message[message.index(',')+1:]
            temprelays.append(int(message))

            # Assign to the class variable
            self.relaysToTurnOn = temprelays
            return
            


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

# TODO: find the query problem here
"""DEBUG"""
"""
# Database connection variables
dbHost = "192.168.18.4"
offsiteDbHost = "localhost"
dbPort = "3306"
dbUsername = "areeba"
dbPassword = "areebafyp"
dbDatabase = "db_classroom_management"
#connection and getting cursor
try:
    connection = cn.connect(host=dbHost, user=dbUsername, passwd=dbPassword, database=dbDatabase)
    mainCursor = connection.cursor()
    print("Connected to the server...")
except Exception as e:
    print (e)
    exit()

extraSelectResult = []
(extraSelectRan, ifExtraSelectError) = gvs.runQuery(mainCursor, gvs.QUERY_GET_EXTRA_SCHEDULE_ROOM_FORMAT_ROOMID_DAYOFWEEK.format(str(gvs.THIS_ROOM), 5))
if extraSelectRan:
    extraSelectResult = mainCursor.fetchall()
else:
    print (ifExtraSelectError)
scheduleItems = []
for i in extraSelectResult:
    print (i[0])
    temp = ExtraScheduleItem(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9])
    scheduleItems.append(temp)
if len(scheduleItems) > 0:
    scheduleItems = sorted(scheduleItems, key=lambda k: k.slot) 

import os
os.system('clear')
scheduleItems[1].calculateRelaysToTurnOn()
print(scheduleItems[1].relaysToTurnOn)
"""