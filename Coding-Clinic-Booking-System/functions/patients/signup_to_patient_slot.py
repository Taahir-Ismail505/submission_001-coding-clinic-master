import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import connection_test as ct
import calender_api
import get_events
import date_format as df
import auth_interface
from pprint import pprint
import json
import re
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
            # pprint(event)
            # print(start1)
            if df.calculate_time_difference_personal_calendar(start, start1, end1, 'patient') == True:
                # pprint(event)
                return True
    return False


def update_slot_with_patient(uid, username, event, service):
    descr = argv[1]
    if len(event['attendees']) == 2:
        print(f"\nThe slot you tried signing up for is already taken. Please choose another slot.")
        return
    response = {'displayName': username,
    'email': f'{username}@student.wethinkcode.co.za',
    'optional': True,
    'responseStatus': 'accepted',
    }
    event['attendees'].append(response)
    event['description'] = descr
    service.events().update(calendarId=get_events.calendar_id, eventId=uid, body=event, sendUpdates='all').execute()
    print(f"\nYou have successfully signed up for {event['summary']}...")


def add_patient_slot_to_calender(service, username):
    events, count = get_events.get_all_code_clinic_slots_to_signup_without_printing_anything(service, username)
    while True:
        uid = argv[2]
        for event in events:
            event_id = event['id']
            if event_id == uid:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                overlaps = check_if_slots_overlap_on_personal_calender(start, end, service, username)
                # print(overlaps)
                # return
                if overlaps:
                    print("\nYou already have an event scheduled for this time. Please choose another slot...\n")
                    return
                
                event2 = service.events().get(calendarId=get_events.calendar_id, eventId=uid).execute()
                update_slot_with_patient(uid, username, event2, service)
                get_events.get_all_code_clinic_slots_to_delete(service, username)
                return
            if events[-1] == event:
                print("\nPlease enter a valid ID.\n")
                return


def main_function():
    if ct.connection_test() == False:
        print("\nPlease check your internet connection.\n")
        return
    if len(argv) != 3:
        print("\nPlease enter valid input. e.g: wtc-clinic patient signup <description> <ID>\n")
        return
    service = calender_api.create_auth_service()
    if auth_interface.check_if_credentials_have_expired():
        return
    username = get_events.get_username()
    add_patient_slot_to_calender(service, username)


if __name__ == '__main__':
    main_function()