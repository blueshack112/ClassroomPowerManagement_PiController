"""
This section will contain all the query templates and
important variables needed during the running of this file.
"""
THIS_ROOM = 1001
# For debugging, get date and time
QUERY_GET_DATE_TIME = "SELECT debug_id, system_date_time_to_set FROM tbl_debug "

# for the contents of current week's table
QUERY_GET_WEEK_SCHEDULE = "SELECT week_schedule_id, schedule_id, extra_schedule_id FROM tbl_week_schedule"
QUERY_INSERT_WEEK_SCHEDULE_NORMAL_FORMAT_VALUES = "INSERT INTO tbl_week_schedule (schedule_id) VALUES {};"
QUERY_INSERT_WEEK_SCHEDULE_EXTRA_FORMAT_VALUES = "INSERT INTO tbl_week_schedule (extra_schedule_id) VALUES {};"
QUERY_TRUNCATE_WEEK_SCHEDULE = "TRUNCATE TABLE tbl_week_schedule"

# for the contents of schedule table
QUERY_GET_NORMAL_SCHEDULE_ID = "SELECT schedule_id FROM tbl_schedule"
QUERY_GET_EXTRA_SCHEDULE_ID = "SELECT extra_schedule_id FROM tbl_extra_schedule"

# Select query for views needed to alot schedule items
QUERY_GET_NORMAL_SCHEDULE_ROOM_FORMAT_ROOMID_DAYOFWEEK = "SELECT schedule_id, teacher_id, room_id, course_id, day_of_week, slot, class_length FROM view_normal_schedule WHERE room_id = {} and day_of_week = {}"
QUERY_GET_EXTRA_SCHEDULE_ROOM_FORMAT_ROOMID_DAYOFWEEK = "SELECT extra_schedule_id, teacher_id, room_id, course_id, day_of_week, slot, class_length, accept_status FROM view_extra_schedule WHERE room_id = {} and day_of_week = {}"

# for the contents of room status table
QUERY_GET_ROOM_STATUS_ATTENDANCE_FORMAT_COURSEID = "SELECT attendance FROM tbl_room_status WHERE course_id = {}"
QUERY_INSERT_ROOM_STATUS_FORMAT_VALUES = "INSERT INTO tbl_room_status (room_id, course_id, relay_used, class_date, slot) VALUES {};"

# Function solely to run queries and grab exceptions in a clean manner
# Returns an error and boolean false if an error occures
# Returns true and a "Done" string if it was successful
def runQuery (mainCursor, query):
    try:
        mainCursor.execute(query)
    except Exception as e:
        return (False, e)
    return (True, "Done")
