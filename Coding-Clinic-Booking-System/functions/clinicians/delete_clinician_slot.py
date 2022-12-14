import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import connection_test as ct
import calender_api
import get_events
import date_format as df
import auth_interface
import json
import os
from sys import argv

def delete_clinician_slot(service, username):
    events = get_events.simple_get_events_without_printing_anything(username, service)
    while True:
        user_input = argv[1]
        for event in events:
            event_id = event['id']
            if event_id == user_input:
                events1, count1 = actual_delete_events(user_input, username, service)
                if count1 == 0:
                    print("\nYou currently don't have any slots created.\n")
                return
            if events[-1] == event:
                print("\nPlease enter a valid ID.\n")
                return


def actual_delete_events(user_input, username, service):
    event = service.events().get(calendarId=get_events.calendar_id, eventId=user_input).execute()
    if len(event['attendees']) == 2:
        print("\nThe slot you tried deleting already has a patient signed up. Please choose another slot to delete.")
    elif username not in event['summary']:
        print("\nSorry you cant delete other student's slots. Please choose your OWN slot.")
    else:    
        service.events().delete(calendarId=get_events.calendar_id, eventId=user_input, sendUpdates='all').execute()
        print(f"\nSlot {user_input} was deleted...")
    events, count = get_events.get_events_for_next_7_days_to_delete(username, service)
    return events, count


def main_function():
    if ct.connection_test() == False:
        print("\nPlease check your internet connection.\n")
        return
    if len(argv) != 2:
        print("\nPlease enter valid input. e.g: wtc-clinic clinician delete <ID>\n")
        return
    service = calender_api.create_auth_service()
    if auth_interface.check_if_credentials_have_expired():
        return
    username = get_events.get_username()
    delete_clinician_slot(service, username)


if __name__ == '__main__':
    main_function()