import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import connection_test as ct
import calender_api
import get_events
import auth_interface
import date_format as df
import json
import os
from pprint import pprint
from sys import argv


def main_function():
    if ct.connection_test() == False:
        print("\nPlease check your internet connection.\n")
        return
    if auth_interface.check_if_credentials_have_expired():
        return
    service = calender_api.create_auth_service()
    username = get_events.get_username()
    events, count = get_events.get_events_for_next_7_days_to_delete(username, service)
    if count == 0:
        print("\nYou currently don't have any slots created.\n")


if __name__ == '__main__':
    main_function()
