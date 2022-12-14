import date_format as df
from rich.console import Console
from rich import print
from rich.table import Table, Column
from pprint import pprint
import json

# global variable calender_id
calendar_id = 'wethinkmock@gmail.com'

def get_slot_attendee_names(event):
    """[Takes in an event and returns whos the patient and whos the clinician]
    Args:
        event ([dictionary]): [dictionary where well check whos the clinician and patient]
    Returns:
        [tuple of strings]: [patient and clinician usernames]
    """  

    events_list = event['attendees']
    if len(events_list) == 1:
        clinician_dict = events_list[0]
        clinician = clinician_dict['displayName']
        patient = ''
    else:
        clinician_dict = events_list[0]
        patient_dict = events_list[1]
        clinician = clinician_dict['displayName']
        patient = patient_dict['displayName']
    return clinician, patient


def print_events(start, event, description):
    """[Prints out the a code clinic slot in table format using rich module (check imports)]
    Args:
        start ([string]): [start time of the event]
        event ([dictionary]): [the event that has to be printed out as a slot]
        description ([type]): [The description of what the event does]
    """ 

    console = Console()
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Date", style="dim", width=18)
    table.add_column("Summary", style="dim", width=25)
    table.add_column("Description", style="dim", width=30)
    table.add_column("ID", style="dim", width=30)
    table.add_column("Attendees", style="dim", width=15)

    clinician, patient = get_slot_attendee_names(event)
    table.add_row(start, event['summary'], description, event['id'], f"{clinician}\n{patient}")
    console.print(table)


def get_events_for_next_7_days_to_delete(username, service):
    """[This function gets all the slots that the particular user has created for the next 7 days ]
    Args:
        username ([string]): [student username]
        service ([object]): [the api object that allows us to connect to google calenders]
    Return:
        events ([list]): list of dictionaries, with each dictionary being a google cal event.
        count ([int]): either 1 or 0, returns 1 if there where events returned and 0 if there arent any events.
    """    
    event_list = {"events" : []}
    print("\nThese are your upcoming slots for the next 7 days: \n")
    time = df.get_current_and_7_days_date_and_time_in_RFC3339()
    events_result = service.events().list(calendarId=calendar_id, timeMin=time[0],
                                        singleEvents=True, timeMax=time[1],
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    count = 0

    for event in events:
        start = df.format_time_to_make_readable(event)
        description = event['description']
        if event['summary'] == f'{username} - Code Clinic':
            count = 1
            print_events(start, event, description)
            event_list['events'].append({event['id'] : event})
    with open('functions/data_files/events.json', 'w+') as outfile:
        json.dump(event_list, outfile, sort_keys=True, indent=4)
    outfile.close()
    return events, count


def simple_get_events_without_printing_anything(username, service):
    time = df.get_current_and_7_days_date_and_time_in_RFC3339()
    events_result = service.events().list(calendarId=calendar_id, timeMin=time[0],
                                        singleEvents=True, timeMax=time[1],
                                        orderBy='startTime').execute()
    return events_result.get('items', [])


def get_all_code_clinic_slots_to_signup(service, username):
    """[This function gets all the slots available to the student to sign up to.
        it checks that the length of the list with all the attendees is 1 and that they are not the
        one that created the slot in the first place.]
    Args:
        username ([string]): [student username]
        service ([object]): [the api object that allows us to connect to google calenders]
    Return:
        events ([list]): list of dictionaries, with each dictionary being a google cal event.
        count ([int]): either 1 or 0, returns 1 if there where events returned and 0 if there arent any events.
    """  

    print("\nThese are all the available slots you can choose from.\n")
    events = get_events_from_service(service)
    count = 0
    for event in events:
        start = df.format_time_to_make_readable(event)
        description = event['description']
        items_list =  event['attendees']
        if len(items_list) == 1 and username not in event['summary']:
            count = 1
            print_events(start, event, description)
    return events, count


def get_all_code_clinic_slots_to_signup_without_printing_anything(service, username):
    """
    [Does everything above function does, without printing anything in the process.]
    Args:
        username ([string]): [student username]
        service ([object]): [the api object that allows us to connect to google calenders]
    Return:
        events ([list]): list of dictionaries, with each dictionary being a google cal event.
        count ([int]): either 1 or 0, returns 1 if there where events returned and 0 if there arent any events.
    """

    events = get_events_from_service(service)
    count = 0
    for event in events:
        items_list =  event['attendees']
        if len(items_list) == 1 and username not in event['summary']:
            count = 1
    return events, count


def get_events_from_service(service):
    """
    [Uses service object to get list of all events found on calender]
    Args:
        service ([object]): [the object that allows us to connect to the google calender api]
    Returns:
        [list]: [list of dictionaries with each dictionary being a calender event]
    """

    time = df.get_current_and_7_days_date_and_time_in_RFC3339()
    events_result = service.events().list(calendarId=calendar_id, timeMin=time[0],
                                        singleEvents=True, timeMax=time[1],
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    return events


def get_all_code_clinic_slots_to_delete(service, username):
    """
    [Gets all slots student has signed up to as a patient.]
    Args:
        username ([string]): [student username]
        service ([object]): [the api object that allows us to connect to google calenders]
    Return:
        events ([list]): list of dictionaries, with each dictionary being a google cal event.
        count ([int]): either 1 or 0, returns 1 if there where events returned and 0 if there arent any events.
    """

    print("\nThese are the clinics you've signed up for: \n")
    time = df.get_current_and_7_days_date_and_time_in_RFC3339()
    events_result = service.events().list(calendarId=calendar_id, timeMin=time[0],
                                        singleEvents=True, timeMax=time[1],
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    count = 0
    for event in events:
        start = df.format_time_to_make_readable(event)
        description = event['description']
        items_list =  event['attendees']
        if len(items_list) == 2:
            items_dict = items_list[0]
            items_dict2 = items_list[1]
        else:    
            items_dict = items_list[0]
            items_dict2 = {'displayName': 'placeholder'}
        if (items_dict['displayName'] == username or items_dict2['displayName'] == username) and username not in event['summary']:
            count = 1
            print_events(start, event, description)
    return events, count


def get_all_code_clinic_slots_to_delete_without_printing(service, username):
    """
    [Does everything above function does, without printing anything in the process.]
    Args:
        username ([string]): [student username]
        service ([object]): [the api object that allows us to connect to google calenders]
    Return:
        events ([list]): list of dictionaries, with each dictionary being a google cal event.
        count ([int]): either 1 or 0, returns 1 if there where events returned and 0 if there arent any events.
    """
    events = get_events_from_service(service)
    count = 0
    for event in events:
        items_list =  event['attendees']
        if len(items_list) == 2:
            items_dict = items_list[0]
            items_dict2 = items_list[1]
        else:    
            items_dict = items_list[0]
            items_dict2 = {'displayName': 'placeholder'}
        if (items_dict['displayName'] == username or items_dict2['displayName'] == username) and username not in event['summary']:
            count = 1
    return events, count


def get_username():
    f = open("username_file", "r")
    username_list = (f.readlines())
    f.close()
    username = username_list[1]
    return username