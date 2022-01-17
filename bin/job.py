from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

invite_base = {
  'location': 'Google Building TC5, 811 11th Ave, Sunnyvale, CA 94089, USA',
  'attendees': [
    {'email': 'jgray8@ymail.com'},
    {'email': 'jagray@zuora.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'popup', 'minutes': 30},
      {'method': 'popup', 'minutes': 60},
    ],
  },
  'guestsCanInviteOthers': True,
  'guestsCanSeeOtherGuests': True,
  "organizer": {
    "email": 'jlgray024@gmail.com',
    "displayName": 'Jacob Gray',
    "self": True,
  },
}

timezone = 'America/Los_Angeles'


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now()
        print(f'{now}: Creating basketball invite...')
        tommorow = f'{now.year}-{now.month}-{now.day + 1}'

        invite = invite_base
        invite['summary'] = f'{now.month}/{now.day + 1} Basketball'
        # 2022-01-23T13:00:00
        invite['start'] = {
            'dateTime': f'{tommorow}T13:00:00',
            'timeZone': timezone,
        }
        invite['end'] = {
            'dateTime': f'{tommorow}T16:00:00',
            'timeZone': timezone,
        }

        event = service.events().insert(calendarId='basketball', body=invite, sendNotifications=True).execute()

        print (f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()