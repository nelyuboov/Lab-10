import time
import requests
import pyttsx3
import webbrowser
import speech_recognition as sr
from speech_recognition import UnknownValueError

engine = pyttsx3.init()
newVoiceRate = 130

voices = engine.getProperty('voices')
engine.setProperty('voices', 'en')

for voice in voices:
    if voice.name == 'Shelley (English (UK))':
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', newVoiceRate)

r = sr.Recognizer()


def greetings():
    engine.say('Hello, My name is JARVIS, I am your personal assistant.')
    engine.say('I can find some information about many English words.')
    engine.say('Just tell me: find a word. For example, find a lemonade, find an apple.')
    engine.say('If you wan\'t close the program, you can say EXIT.')
    engine.runAndWait()


def talk(say):
    engine.say(say)
    engine.runAndWait()


def listening():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('Listening...')
        voice = r.listen(source)
        try:
            time.sleep(1.5)
            command = r.recognize_google(voice, language="en-GB")
            return command
        except UnknownValueError:
            talk("Sorry, I could not recognize what you said.")
            return 'Wrong value'


def commands():
    talk('Do you want to open the source webpage,'
         ' listen the pronunciation,  get a meaning, transcription or  an example?')
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('Waiting for the command...')
            voice = r.listen(source)
            try:
                time.sleep(1.5)
                command = r.recognize_google(voice)
                print(command)
            except UnknownValueError:
                command = 'Wrong value'
        if 'webpage' in command:
            return 1
        if 'pronunciation' in command:
            return 2
        if 'example' in command:
            return 4
        if 'transcription' in command:
            return 5
        if 'Wrong enter' in command:
            return 10
    except:
        pass


def JARVIS(rg):
    url = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/' + rg)
    s = url.json()
    iss = commands()
    match iss:
        case 5:
            if s[0].get('phonetic') != "None":
                print('phonetic : %s' % s[0].get('phonetic'))
            else:
                talk('This information not available at this moment.')
        case 2:
            if s[0].get('phonetics')[0].get('audio') != 'None':
                webbrowser.open_new_tab((s[0].get('phonetics')[0]).get('audio'))
            else:
                talk('Sorry, i can\'t find pronunciation recording')
        case 1:
            try:
                webbrowser.open_new_tab(s[0].get('sourceUrls')[0])
            except:
                talk('I  can\'t find source URL')
        case 4:
            if s[0].get('meanings')[0].get('definitions')[0].get('example') != 'None':
                print('example : %s' % s[0].get('meanings')[0].get('definitions')[0].get('example'))
            else:
                talk('I  don\'t have example')
        case _:
            talk('Wrong value, try again')


rg = ''
greetings()

while True:
    speech = listening()
    print(speech)
    if 'find a' in speech:
        rg = speech.split(' ')[-1]
        JARVIS(rg)
    elif 'find an' in speech:
        rg = speech.split(' ')[-1]
        JARVIS(rg)
    elif 'exit' in speech:
        quit()
    if rg == '':
        talk(f'Did not hear the word. Say again.')
        continue