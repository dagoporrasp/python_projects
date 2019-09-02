import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

def speak(text):
	# RFC5646 language tag 
	tts = gTTS(text=text, lang="es")
	filename = "voice.mp3"
	tts.save(filename)
	playsound.playsound(filename)

def get_audio():
	# obtain audio from the microphone
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Di algo!")
		audio = r.listen(source)
		said = ""
		try:
			said = r.recognize_google(audio, language = "es")
			print(said)
		except Exception as e:
			print("Exception: "+ str(e))
	return said

def main():
	print(".....")
	text = get_audio()

	if "Hola" in text:
		speak("¡Hola Dago!, ¿Cómo estás?")

	if "Cómo te llamas" in text:
		speak("Mi nombre es D.A.I")

	# speak("hola Dago")
	
	# said = get_audio()

if __name__ == '__main__':
	main()
