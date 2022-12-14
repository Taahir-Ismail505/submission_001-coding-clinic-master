import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import connection_test as ct
import calender_api
import get_events
import date_format as df
import json
from pprint import pprint
import auth_interface
import datetime
import re
import os
from sys import argv


def check_if_slots_overlap_on_personal_calender(start2, end, service, username):
    events_result = service.events().list(calendarId='primary',
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        st = re.split("[-T:+]",start2)
        start1 = event['start'].get('dateTime', event['start'].get('date'))
        end1 = event['end'].get('dateTime', event['end'].get('date'))
        start = df.convert_to_RFC_datetime(int(st[0]), int(st[1]), int(st[2]), int(st[3])+2, int(st[4]))
    
        if df.check_if_events_are_in_same_day(start, start1):
            if df.calculate_time_difference_personal_calendar(start, start1, end1) == True:
                return True
    return False



def check_if_slots_overlap(start2, end, service, username):
    events_result = service.events().list(calendarId=get_events.calendar_id,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    my_bool = check_if_slots_overlap_on_personal_calender(start2, end, service, username)
    if my_bool == True:
        return True

    for event in events:
        start1 = event['start'].get('dateTime', event['start'].get('date'))
        st = re.split("[-T:+]",start2)
        start = df.convert_to_RFC_datetime(int(st[0]), int(st[1]), int(st[2]), int(st[3])+2, int(st[4]))
        if df.check_if_events_are_in_same_day(start, start1):
            time_diff = df.calculate_time_difference_code_clinics_calender(start, start1)
            if time_diff > -1800.0 and time_diff < 1800.0 and username in event['summary']:
                return True
    return False



def add_to_calender(service, username):
    """[Adding an event to Google Calendar by saving all the info for that event to an event request body ]

    Args:
        service ([object]): [the service object that will allow us to add events to the calender]
        username ([string]): [students username]
    """    
    colors = service.colors().get().execute()
    d_and_t = df.get_add_to_calender_input(argv[1], argv[2])
    now = datetime.datetime.now()
    if d_and_t == None:
        return
    event_request_body = {
        'start': {
            'dateTime': df.convert_to_RFC_datetime(d_and_t[0], d_and_t[1], d_and_t[2], d_and_t[3][0]-2, d_and_t[3][1]),
            'timeZone': 'Africa/Johannesburg'
        },
        'end': {
            'dateTime': df.convert_to_RFC_datetime(d_and_t[0], d_and_t[1], d_and_t[2], d_and_t[4][0]-2, d_and_t[4][1]),
            'timeZone': 'Africa/Johannesburg'
        },
        'summary': f"{username} - Code Clinic",
        'description': 'empty',
        'status': 'confirmed',
        'transparency': 'opaque',
        'visibility': 'public',
        'location': 'WTC',
        'guestsCanModify': True,
        'attendees': [
            {  
            'displayName': username,
            'organizer': True,
            'email': f'{username}@student.wethinkcode.co.za',
            'optional': True,
            'responseStatus': 'accepted'
            }
        ]
    }
    start = event_request_body['start']['dateTime']
    end = event_request_body['end']['dateTime']

    overlaps = check_if_slots_overlap(start, end, service, username)
    if overlaps == False:
        response = service.events().insert(calendarId=get_events.calendar_id, sendUpdates='all', body=event_request_body).execute()
        print("\nYour slot has been created...")
    else:
        print("\nYou already have an event scheduled for this time. Please choose another time...")
    events, count = get_events.get_events_for_next_7_days_to_delete(username, service)
    if count == 0:
        print("\nYou currently don't have any slots created.")
        return


def main_function():
    if ct.connection_test() == False:
        print("\nPlease check your internet connection.\n")
        return
    if len(argv) != 3:
        print("\nPlease enter valid input. e.g: wtc-clinic clinician create <date> <time>\n")
        return
    service = calender_api.create_auth_service()
    if auth_interface.check_if_credentials_have_expired():
        return
    username = get_events.get_username()
    add_to_calender(service, username)


if __name__ == '__main__':
    main_function()