from flask import Flask, request
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

app = Flask(__name__)

# Define as credenciais e autoriza a API do Google Calendar
SCOPES = "https://www.googleapis.com/auth/calendar"
store = file.Storage("storage.json")
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(
        "C:/workspace/nipon1/app/dist/client_secret.json", SCOPES
    )
    creds = tools.run_flow(flow, store)

CAL = build("calendar", "v3", http=creds.authorize(Http()))


@app.route("/")
def main():
    # Obter duas datas como parâmetros na URL
    primeira = request.args.get("primeira")
    segunda = request.args.get("segunda")

    # Montar as strings de data/hora de início e fim do evento
    primeira = f"'{primeira}T13:00:00%s % GMT_OFF'"
    segunda = f"'{segunda}T13:00:00%s % GMT_OFF'"

    GMT_OFF = "-04:00"
    EVENT1 = {
        "summary": "Buy apples",
        "start": {"dateTime": primeira},
        "end": {"dateTime": segunda},
    }

    # Criar um evento no Google Calendar e retorna "Hello, World" como resposta
    e = (
        CAL.events()
        .insert(calendarId="primary", sendNotifications=True, body=EVENT1)
        .execute()
    )

    return "Hello, World"


if __name__ == "__main__":
    app.config["ENV"] = "development"
    app.run(debug=True, port=5000)
