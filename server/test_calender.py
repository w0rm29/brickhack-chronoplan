import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


# add event in the calendar
def add_event(user_event_details):
    service = get_service()
    try:
        event_description = {
        'summary': user_event_details[0],
        'start': {
          'dateTime': user_event_details[1],
          'timeZone': 'America/New_York'},
        'end': {
            'dateTime': user_event_details[2],
            'timeZone': 'America/New_York'},
        'colorId': 6}
        
        CALENDAR_ID = "primary"
        event = service.events().insert(calendarId=CALENDAR_ID, body=event_description).execute()
        return event['id']
    except HttpError as error:
      print("Error1=> ", error)

# update event details
def update_event(updated_details):
    service = get_service()
    event_id = get_event_id(service, "Test from postman")
    try:
        new_event_details = {
        'summary': updated_details[0],
        'start': {
          'dateTime': updated_details[1],
          'timeZone': 'America/New_York'},
        'end': {
            'dateTime': updated_details[2],
            'timeZone': 'America/New_York'},
        'colorId': 6}
        
        CALENDAR_ID = "primary"
        event_to_change = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()
        event_to_change.update(new_event_details)  
        updated_event = service.events().update(calendarId=CALENDAR_ID, eventId=event_id, body=event_to_change).execute()
             
        
    except HttpError as error:
      print("Error1=> ", error)

# get id of the event
def get_event_id(service, event_summary):
    try:
        CALENDAR_ID = "primary"
        events_list = service.events().list(calendarId=CALENDAR_ID).execute()
        events_list = events_list.get('items', [])
        
        for event in events_list:
            if 'summary' in event and event['summary'] == event_summary:
                return event['id']
        return None        
        
    except HttpError as error:
      print("Error1=> ", error)

def get_latest_events():
    service = get_service()
    try:
        CALENDAR_ID = "primary"
        events_list = service.events().list(calendarId=CALENDAR_ID).execute()  
        events_list = events_list.get('items', [])
        final_list = []
        for event in events_list:
            record = {'summary': "",
                      'start': "",
                      'end': ""}
            if 'summary' in event:
                record['summary'] = event['summary']
            if 'start' in event:
                record['start'] = event['start']['dateTime']
            if 'end' in event:
                record['end'] = event['end']['dateTime']
            final_list.append(record)
        return final_list
    except HttpError as error:
      print("Error1=> ", error)

def get_service():
    creds = None
    cred_file_path = "auth2_credentials_desktop.json"

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file_path, SCOPES)
            creds = flow.run_local_server(port=0)
    
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        API_NAME = "calendar"
        API_VERSION = "v3"
        return build(API_NAME, API_VERSION, credentials=creds)          
    except HttpError as error:
      print("Error1=> ", error)