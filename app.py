from time import sleep
from random import randint
from threading import Thread

import openai
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from loguru import logger

mixer.init()
Recognizer = sr.Recognizer()
mic = sr.Microphone()
with open('.KEY', 'r') as f:
    openai.api_key = f.read()


class Speaker(Thread):
    def __init__(self, txt):
        super().__init__()
        self.daemon = True
        self.txt = txt
        self.lang = 'ko'
        self.slow = False

    def run(self):
        speak(self.txt, self.lang, self.slow)


class Listener(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.flag = False
        self.data = None

    def run(self):
        while True:
            if self.flag:
                data = self.listen(call=True, delay=False, phrase_time_limit=2)
                logger.info(f'User: {data}')
                if '그만' in data or '조용' in data:
                    if mixer.Channel(0).get_busy():
                        mixer.Channel(0).stop()
                        self.flag = False
            sleep(0.1)

    def listen(self, call=False, delay=True, phrase_time_limit=0):
        if delay:
            while self.flag or mixer.Channel(0).get_busy():
                sleep(.1)
            sleep(0.5)
        if not call:
            mixer.Channel(0).play(mixer.Sound('beep.mp3'))
        data = ''
        try:
            with mic as source:
                if phrase_time_limit:
                    audio = Recognizer.listen(source, phrase_time_limit=phrase_time_limit)
                else:
                    audio = Recognizer.listen(source)
            data = Recognizer.recognize_google(audio, language="ko")
        except:
            pass
        return data


def speak(text, lang="ko", speed=False):
    logger.info(f'Brother: {text}')
    tts = gTTS(text=text, lang=lang, slow=speed)
    tts.save("./tts.mp3")
    sleep(0.1)
    mixer.Channel(0).play(mixer.Sound('tts.mp3'))
    while mixer.Channel(0).get_busy():sleep(0.1)


def main():
    listener = Listener()
    listener.start()
    while True:
        txt = listener.listen(call=True)
        if txt:logger.info(f'User: {txt}')
        if '조수' in txt:
            speak(['말씀하세요.', '부르셨나요?', '왜요?', '저요?'][randint(0, 3)])
            # sleep(0.2)
            # mixer.Channel(0).play(mixer.Sound('response.mp3'))
            speech = listener.listen()
            logger.info(f'User: {speech}')
            if speech:
                listener.flag = True
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": speech}]
                )
                speak(completion['choices'][0].message.content)
                listener.flag = False
                # s = Speaker(completion['choices'][0].message.content)
                # s.start()

            else:
                mixer.Channel(0).play(mixer.Sound('fail.mp3'))


if __name__ == '__main__':
    main()
