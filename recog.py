import speech_recognition as sr
import os
from gtts import gTTS
from pygame import mixer
from time import time, sleep

mixer.init()
Recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text, lang="ko", speed=False):
    tts = gTTS(text=text, lang=lang, slow=speed)
    tts.save("./tts.mp3")
    sleep(1)
    mixer.Channel(0).play(mixer.Sound('tts.mp3'))

while True:
    with mic as source:
        audio = Recognizer.listen(source)
    try:
        data = Recognizer.recognize_google(audio, language="ko")
    except:
        data = ''
    if '더블비' in data:
        mixer.Channel(0).play(mixer.Sound('response.mp3'))
        with mic as source:
            audio = Recognizer.listen(source)
        try:
            data = Recognizer.recognize_google(audio, language="ko")
            speak(data)
        except:
            mixer.Channel(0).play(mixer.Sound('fail.mp3'))
    while mixer.Channel(0).get_busy():
        sleep(.1)
    print(data)
    

