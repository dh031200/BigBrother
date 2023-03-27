from time import time, sleep

# import os
import openai
from gtts import gTTS
from pygame import mixer
import speech_recognition as sr
# from pydub import AudioSegment

mixer.init()
Recognizer = sr.Recognizer()
mic = sr.Microphone()
with open('.KEY', 'r') as f:
    openai.api_key = f.read()


def speak(text, lang="ko", speed=False):
    tts = gTTS(text=text, lang=lang, slow=speed)
    tts.save("./tts.mp3")
    sleep(0.1)
    # sound = AudioSegment.from_file("tts.mp3")
    # speed_sound = speed_swifter(sound, 1.1)
    # speed_sound.export(os.path.join("fast.mp3"), format="mp3")
    # sleep(0.1)
    # mixer.Channel(0).play(mixer.Sound('fast.mp3'))
    mixer.Channel(0).play(mixer.Sound('tts.mp3'))


def speed_swifter(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data,
                                                 overrides={"frame_rate": int(sound.frame_rate * speed)})
    return sound_with_altered_frame_rate


def listen(call=False):
    while mixer.Channel(0).get_busy():
        sleep(.1)
    if not call:
        mixer.Channel(0).play(mixer.Sound('beep.mp3'))
    with mic as source:
        audio = Recognizer.listen(source)
    try:
        data = Recognizer.recognize_google(audio, language="ko")
    except Exception as e:
        print(e)
        data = ''
    return data


def main():
    while True:
        data = listen(call=True)
        if '조수' in data:
            mixer.Channel(0).play(mixer.Sound('response.mp3'))
            data = listen()
            print(data)
            if data:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": data}]
                )
                speak(completion['choices'][0].message.content)
            else:
                mixer.Channel(0).play(mixer.Sound('fail.mp3'))


if __name__ == '__main__':
    main()
