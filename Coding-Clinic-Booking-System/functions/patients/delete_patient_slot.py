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
from sys import argv


def update_slot_with_deleted_patient(uid, username, event, service):
    for student in event['attendees']:
        if student['displayName'] == username:
            event['attendees'].remove(student)
            event['description'] = 'empty'
    service.events().update(calendarId=get_events.calendar_id, eventId=uid, body=event, sendUpdates='all').execute()
    print(f"\nYou have successfully deleted slot {uid}...")


def delete_patient_slot(service, username):
    events, count = get_events.get_all_code_clinic_slots_to_delete_without_printing(service, username)
    if count == 0:
        print("\nYou currently have no available slots to delete.\n")
        return
    while True:
        uid = argv[1]
        for event in events:
            event_id = event['id']
            if event_id == uid and len(event['attendees']) == 2:
                event2 = service.events().get(calendarId=get_events.calendar_id, eventId=uid).execute()
                update_slot_with_deleted_patient(uid, username, event2, service)
                events, count = get_events.get_all_code_clinic_slots_to_delete(service, username)
                if count == 0:
                    print("You don't have anymore slots.\n")
                    return
                return
            if events[-1] == event:
                print("\nPlease enter a valid ID.\n")
                return


def main_function():
    if ct.connection_test() == False:
        print("\nPlease check your internet connection.\n")
        return
    if len(argv) != 2:
        print("\nPlease enter valid input. e.g: wtc-clinic patient delete <ID>\n")
        return
    service = calender_api.create_auth_service()
    if auth_interface.check_if_credentials_have_expired():
        return
    username = get_events.get_username()
    delete_patient_slot(service, username)


if __name__ == '__main__':
    main_function()