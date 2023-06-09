from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
     
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
          if flags else tools.run(flow, store)
CAL = build('calendar', 'v3', http=creds.authorize(Http()))

GMT_OFF = '-04:00'          # ET/MST/GMT-4
EVENT1 = {
    'summary': 'Buy apples',
    'start': {'dateTime': '2023-07-06T13:00:00%s' % GMT_OFF},
    'end': {'dateTime': '2023-07-06T14:00:00%s' % GMT_OFF},
}
EVENT2 = {
    'summary': 'Buy Bannanas',
    'start': {'dateTime': '2023-07-07T13:00:00%s' % GMT_OFF},
    'end': {'dateTime': '2023-07-07T14:00:00%s' % GMT_OFF},
}
EVENT3 = {
    'summary': 'Buy candy',
    'start': {'dateTime': '2023-07-08T13:00:00%s' % GMT_OFF},
    'end': {'dateTime': '2023-07-08T14:00:00%s' % GMT_OFF},
}

e = CAL.events().insert(calendarId='primary',
                sendNotifications=True, body=EVENT1).execute()
e = CAL.events().insert(calendarId='primary',
                sendNotifications=True, body=EVENT2).execute()
e = CAL.events().insert(calendarId='primary',
                sendNotifications=True, body=EVENT3).execute()