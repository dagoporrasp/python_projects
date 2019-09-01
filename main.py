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

speak("hola Dago")
