from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None

    # 🔍 Check if token already exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 🔁 Refresh or Get New Token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # 💾 Save token to file manually
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service
import datetime

def check_availability(service, date, start_time, end_time):
    start = datetime.datetime.combine(date, start_time).isoformat() + 'Z'
    end = datetime.datetime.combine(date, end_time).isoformat() + 'Z'

    events = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return not events.get('items')

def book_slot(service, summary, date, start_time, end_time):
    start = datetime.datetime.combine(date, start_time).isoformat()
    end = datetime.datetime.combine(date, end_time).isoformat()

    event = {
        'summary': summary,
        'start': {'dateTime': start, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end, 'timeZone': 'Asia/Kolkata'},
    }

    return service.events().insert(calendarId='primary', body=event).execute()

if __name__ == "__main__":
    get_calendar_service()
    print("token.json saved successfully ")
