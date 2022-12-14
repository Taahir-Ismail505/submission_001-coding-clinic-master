from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
API_NAME = 'calender'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


creds = ''


def cred_gen():
    global creds
    if os.path.exists('tokens/token.pickle'):
        with open('tokens/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokens/token.pickle', 'wb') as token:
            pickle.dump(creds, token)


def service_gen():
    service = ''
    service = build('calendar', 'v3', credentials=creds)
    return service