import requests


def connection_test():
    try :
        requests.get('https://www.googleapis.com/auth/calendar', timeout=5)
        # requests.get('https://www.googleapis.com/auth/calendar', timeout=.1)
        # print("\nYou have a connection to the calendar API\n")
        return True
    except :
        # print("\nYou dont have a connection to the calendar API.\n")
        return False