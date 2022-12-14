import datetime
from datetime import datetime as dT
from datetime import timedelta
from calendar import monthrange
import re

"""
Data formats
"""
def format_time_to_make_readable(event):
    """[Converts time from RFC3339 to a more readable format]

    Args:
        event ([object]): [an event object]

    Returns:
        [string]: [Time in a more readable format]
    """    

    start1 = event['start'].get('dateTime', event['start'].get('date'))
    start = re.split("[-T:+]",start1)
    return f'{start[0]}-{start[1]}-{start[2]} @ {start[3]}:{start[4]}'


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    """
    converting date data into a format used by google calendar api
    """
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


def get_current_and_7_days_date_and_time_in_RFC3339():
    """[Gets current time and return it in RFC3339 time for Google calendar to understand]

    Returns:
        [tuple]: [tuple of strings with the first being the current date and the second element being the the date in 7 days]
    """    
    date = datetime.datetime.utcnow()
    date_in_7_days = date + timedelta(7)
    date_with_timezone = date.isoformat("T") + "Z"
    date_in_7_days_with_timezone = date_in_7_days.isoformat("T") + "Z"

    return (date_with_timezone, date_in_7_days_with_timezone)


def get_add_to_calender_input(dateP, timeP):
    """[Checks whether the date and time the user inputs is valid and displays appropriate responses if it isnt]

    Args:
        dateP ([string]): [date in this format - 2020/12/08]
        timeP ([string]): [time in this format 14:20]

    Returns:
        [tuple]: [tuple with the year, day, start time, end time]
    """ 

    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    now = datetime.datetime.now()
  
    date = re.split("[-/]",dateP)
    if len(date) != 3:
        print('\nPlease enter a valid date.\n')
        return
    while True:
        if int(date[0]) >= now.year and int(date[0]) <= now.year+1:
            year = int(date[0])
            break
        else:
            print('\nPlease enter a valid date.\n')
            return

    while True:
        if int(date[1]) < 1 or int(date[1]) > 12:
            print('\nPlease enter a valid date.\n')
            return
        month = valid_months[int(date[1])-1]
        if month in valid_months and (valid_months.index(month)+1 >= now.month or now.year < year):
            break
        elif valid_months.index(month)+1 < now.month and now.year <= year:
            print('\nThe date you chose has already passed. Please enter another date.\n')
            return
        else:
            print('\nPlease enter a valid date.\n')
            return
        
    while True:
        day = int(date[2])
        if day > 0 and day <= monthrange(now.year, valid_months.index(month)+1)[1]:
            break
        else:
            print('\nPlease enter a valid date.\n')
            return

    while True:
        time = timeP
        t = time.split(':')
        if len(t) == 2 and t[0].isdigit and t[1].isdigit and int(t[0]) > 0 and int(t[0]) < 24 and int(t[1]) > -1 and int(t[1]) < 60:
            start = (int(t[0]), int(t[1]))
            a = datetime.datetime(100,1,1,int(t[0]),int(t[1]))
            b = a + timedelta(minutes=30)
            end = (int(b.time().hour), int(b.time().minute))
            break
        else:
            print('\nPlease enter a valid time.\n')
            return

    return (year, valid_months.index(month)+1, day, start, end)      


def calculate_seconds(time1, time2):
    """[Takes 2 time intervals and calculate the time difference between the 2 in seconds]

    Args:
        time1 ([string]): [time in the following format HH:MM:SS]
        time2 ([string]): [time in the following format HH:MM:SS]

    Returns:
        [int}: [return the difference between the 2 times in seconds]
    """    
    FMT = '%H:%M:%S'
    tdelta = dT.strptime(time1, FMT) - dT.strptime(time2, FMT)
    return tdelta.total_seconds()


def calculate_time_difference_code_clinics_calender(start, start1, user='clinician'):
    """[takes date and time in RFC3339 format and calculate the time difference between the 2 in seconds]

    Args:
        start ([string]): [date and time in RFC3339 format]
        start1 ([string]): [date and time in RFC3339 format]
        user (str, optional): [specifies if we want to calculate the time difference for a clinician of a patient]. Defaults to 'clinician'.

    Returns:
        [int]: [return the difference between the 2 times in seconds]
    """    
    FMT = '%H:%M:%S'
    start_time = re.split("[-T:+]",start)
    start = re.split("[-T:+]",start1)

    if user == 'clinician':
        current_event_time = f'{int(start[3])}:{start[4]}:00'
        new_event_time = f'{int(start_time[3])}:{start_time[4]}:00'
    else:
        current_event_time = f'{int(start[3])-2}:{start[4]}:00'
        new_event_time = f'{int(start_time[3])-2}:{start_time[4]}:00'
    tdelta = dT.strptime(current_event_time, FMT) - dT.strptime(new_event_time, FMT)
    return tdelta.total_seconds()


def calculate_time_difference_personal_calendar(start, start1, end1, user='clinician'):
    """[Checks whether a slot that a patient is trying to create overlaps with any events hes/shes involved in whehter its code clinics related
    of on their personal calender.]

    Args:
        start ([string]): [start of the event that the student is to create (if clinician) or signup to (if patient)]
        start1 ([string]): [start of the event that is on the students calendar]
        end1 ([type]): [end time of the event that is on the students calendar]
        user (str, optional): [specifies if we want to calculate the time difference for a clinician of a patient]. Defaults to 'clinician'.

    Returns:
        [bool]: [Returns True or False. True if event being created or being signed up to overlaps, false if it doesnt]
    """    
    start_of_new = re.split("[-T:+]",start)
    start_of_old = re.split("[-T:+]",start1)
    end_of_old = re.split("[-T:+]",end1) 

    if user == 'clinician':
        new_s = f'{int(start_of_new[3])}:{start_of_new[4]}:00'
        new_e = f'{timedelta(hours=int(start_of_new[3]), minutes=int(start_of_new[4])) + timedelta(minutes=30)}'
    else:
        new_s = f'{int(start_of_new[3])-2}:{start_of_new[4]}:00'
        new_e = f'{timedelta(hours=int(start_of_new[3])-2, minutes=int(start_of_new[4])) + timedelta(minutes=30)}'

    old_s = f'{int(start_of_old[3])}:{start_of_old[4]}:00'
    old_e = f'{int(end_of_old[3])}:{end_of_old[4]}:00'

    if calculate_seconds(old_s, new_e) < 0 and  calculate_seconds(old_e, new_e) > 0:
        return True
    elif calculate_seconds(old_e, new_s) > 0 and calculate_seconds(old_s, new_s) < 0:
        return True
    elif calculate_seconds(old_s, new_s) > 0 and calculate_seconds(old_e, new_e) < 0:
        return True
    elif calculate_seconds(old_s, new_s) <= 0 and calculate_seconds(old_e, new_e) >= 0:
        return True
    else:
        return False


def check_if_events_are_in_same_day(start, start1):
    """[Takes 2 dates in RFC3339 time and checks whether they are in the same day. returns either True or False]

    Args:
        start ([string]): [Date in RFC3339]
        start1 ([string]): [Date in RFC3339]

    Returns:
        [bool]: [True if dates are in the same day. False if they arent]
    """    
    start_t = re.split("[-T:+]",start)
    start = re.split("[-T:+]",start1)
    return start[0] == start_t[0] and start[1] == start_t[1] and start[2] == start_t[2]



