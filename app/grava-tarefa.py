from __future__ import print_function
import smtplib
from apiclient.discovery import build
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
    'summary': 'Teste NIPON1',
    'start': {'dateTime': '2023-02-26T13:00:00%s' % GMT_OFF},
    'end': {'dateTime': '2023-02-26T14:00:00%s' % GMT_OFF},
}
EVENT2 = {
    'summary': 'Teste NIPON2',
    'start': {'dateTime': '2023-02-26T15:00:00%s' % GMT_OFF},
    'end': {'dateTime': '2023-02-26T16:00:00%s' % GMT_OFF},
}
EVENT3 = {
    'summary': 'Teste NIPON3',
    'start': {'dateTime': '2023-02-26T17:00:00%s' % GMT_OFF},
    'end': {'dateTime': '2023-02-26T18:00:00%s' % GMT_OFF},
}

e = CAL.events().insert(calendarId='primary',
                        sendNotifications=True, body=EVENT1).execute()
e = CAL.events().insert(calendarId='primary',
                        sendNotifications=True, body=EVENT2).execute()
e = CAL.events().insert(calendarId='primary',
                        sendNotifications=True, body=EVENT3).execute()

# Enviar e-mail
EVENT4 = {
    'summary': 'Teste NIPON1',
    'start': {'dateTime': '2023-02-10T19:00:00%s' % GMT_OFF},
    'end': {'dateTime': '2023-02-10T19:00:00%s' % GMT_OFF},
    'attendees': [
        {'email': 'amantino@yahoo.com'},

    ],
}


smtp_server = "smtp.gmail.com"
port = 587
sender_email = "claudio.vieiraamantino@gmail.com"
password = "pdrzpituclaxvnag"
recipient_emails = [attendee['email']
                    for attendee in EVENT4['attendees']]
message = "Subject: NIP\n\n" + EVENT4['summary']

with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, recipient_emails, message)
