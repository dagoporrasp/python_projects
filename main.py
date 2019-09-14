from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os
import time
import playsound
import speech_recognition as sr
#from gtts import gTTS #slow
import pyttsx3
import pytz


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
            'septiembre', 'octubre', 'noviembre', 'diciembre']
DAYS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
DAY_EXTENTIONS = ['primero']

def speak(text):
	# RFC5646 language tag 
	# tts = gTTS(text=text, lang="es")
	# filename = "voice.mp3"
	# tts.save(filename)
	# playsound.playsound(filename)
    es_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0"
    engine = pyttsx3.init()
    engine.setProperty('voice', es_voice_id)
    engine.say(text)
    engine.runAndWait()


def get_audio():
	# obtain audio from the microphone
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Di algo!")
		audio = r.listen(source)
		said = ""
		try:
			said = r.recognize_google(audio, language = "es")
			# print(said)
		except Exception as e:
			print("Exception: "+ str(e))
	return said

# def main():
	# print(".....")
	# text = get_audio()

	# if "Hola" in text:
	# 	speak("¡Hola Dago!, ¿Cómo estás?")

	# if "Cómo te llamas" in text:
	# 	speak("Mi nombre es D.A.I")

	# speak("hola Dago")
	# said = get_audio()

# if __name__ == '__main__':
# 	main()


def authenticate_google():

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(day,service):
    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print(f'Getting the upcoming {n} events')
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)



    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                        timeMax=end_date.isoformat(), singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No tienes ningún evento.')
    else:
        if len(events) ==1:
            speak(f'Tienes {len(events)} evento este día')
        else:
            speak(f'Tienes {len(events)} eventos este día')

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split('T')[1].split('-')[0])
            if int(start_time.split(':')[0])<12:
                start_time = start_time + 'am'
            else:
                start_time = str(int(start_time.split(':')[0]) - 12)
                start_time = start_time + 'pm'
            speak(event['summary'] + ' desde las ' + start_time)

def get_date(text):
    text = text.lower()
    today = datetime.date.today()
    # print(today)

    if text.count('hoy') > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year


    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        elif word in 'mañana':
            day = today.day + 1
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                # print('Aún no funcionan las extensiones')
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year+1

    if month == -1 and day != -1:
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()

    if day == -1 and month == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        # print(current_day_of_week)
        dif = day_of_week - current_day_of_week

        if dif <0:
            dif += 7
            if text.count('siguiente') >= 1:
                dif += 7

        return today + datetime.timedelta(dif)
    # print(str(day) + '-'+ str(month) +'-'+ str(year))
    if day != -1:
        return datetime.date(month=month, day=day, year=year) 

if __name__ == '__main__':
    service = authenticate_google()
	# get_events(2, service)
    # main()
    print("B I E N V E N I D O  A L  A S I S T E N T E  D E  V O Z")
    text = get_audio()

    CALENDAR_STRS = ['que tengo','tengo planes', 'tengo algo para']
    for phrase in CALENDAR_STRS:
        if phrase in text:
            date = get_date(text)
            if date:
                print('')
                print(date)
                get_events(get_date(text), service)
            else:
                speak('Por favor, intenta de nuevo')


        # print(text)
