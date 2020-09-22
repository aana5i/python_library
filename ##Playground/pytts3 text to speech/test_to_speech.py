import pyttsx3


engine = pyttsx3.init()
voices = engine.getProperty('voices')


def get_voice_list():
    for voice in voices:
        print("Voice: %s" % voice.name)
        print(" - ID: %s" % voice.id)
        print(" - Languages: %s" % voice.languages)
        print("\n")


engine.setProperty("voice", voices[2].id)
engine.setProperty('rate', 115)
engine.setProperty('volume', 0.9)
engine.say(f'の天気は。最高温度は24と最低温度は23です。')
engine.runAndWait()
