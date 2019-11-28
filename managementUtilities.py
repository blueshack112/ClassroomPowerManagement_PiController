import datetime as dt

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

# Fcuntion that will get all entries from schedule and put them in weekly schedule table
def createWeekSchedule():
    print ("Week schedule created!")
    return True

# Fcuntion that will delete all entries from weekly schedule table
def truncateWeekSchedule():
    print ("Week schedule truncated!")
    return True