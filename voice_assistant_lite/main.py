# -*- coding: utf-8 -*-

import random
import datetime
import time
import re
import os
import webbrowser
import subprocess
from time import strftime
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

import speech_recognition as sr
import pyttsx3
from word_extractor import get_words_list


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[2].id)
engine.setProperty('rate', 115)
engine.setProperty('volume', 0.9)
webbrowser_is_open = 0

def get_name():
    _name = ""
    if os.path.exists('name.txt'):
        file = open("name.txt","r")
        _name = file.read()
        file.close()

    return _name


def myCommand():
    "listens for commands"
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language='ja-JP')

    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command


def ok_cmd():
    response_file = ["かしこまりました", '了解です']
    engine.say(response_file)


def assistant(command):
    # play un fichier audio                       **play me a song
    # play une video mp.4
    # creer une list de lecture
    # creer un fichier texte et ecrire de dans
    # lancer une application                      **launch
    # creer / envoyer un mail                     **email + thundermail
    # recherche wikipedia                         **tell me about + wikipediaapi
    # recherche youtube                           **play me a song
    # faire correspondre les news avec le wiki ?  ??resuse tell me about ???
    # ouvrir google                               **open
    # help me                                     **help me
    # change wallpaper                            **change wallpaper

    # meteo                                       **current weather

    if 'そこまで' in command:
        # aana.get_single_audio('さようなら')  # a faire
        engine.say(f'さようなら、{name}')
        exit()

    elif 'パソコン様' in command:
        response_file = ["かしこまりました", '了解です']
        # aana.get_single_audio(random.choice(response_file))
        engine.say(random.choice(response_file))

    elif 'おはよう' in command or 'こんにちは' in command or 'こんばんは' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            # aana.get_single_audio('おはようございます')
            engine.say(f'おはようございます、{name}')
        elif 12 <= day_time < 18:
            # aana.get_single_audio('こんにちは')
            engine.say(f'こんにちは、{name}')
        else:
            # aana.get_single_audio('こんばんは')
            engine.say(f'こんばんは、{name}')

    elif 'ニュース' in command:
        try:
            news_url = "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, "lxml")
            news_list = soup_page.findAll("item")
            for counter, news in enumerate(news_list[:3]):
                # aana.get_audio(counter, news.title.text)
                print(counter, news.title.text)
                engine.say(news.title.text)
                # aana.get_response(file)  # stoquer les files dans une list est les lancer quand le reader est pres.
        except Exception as e:
            print(e)

    elif 'の作り方' in command:
        reg_ex = get_words_list(command)

        site_urls = {
            'youtube': 'https://www.youtube.com/results?search_query=',
            'クックパッド': 'https://cookpad.com/search/'
        }
        for keywords, urls in site_urls.items():
            if reg_ex[0] in keywords:
                url = urls
            # TODO add the "not in dict" case

        if reg_ex:
            subsearch = reg_ex[1]
            # TODO add the 'special search url' and google case
            url += f'{subsearch}'
            webbrowser.open(url)
            engine.say(f'{subsearch}の作り方を探しました。')
            # aana.get_single_audio(f'{subsearch}を探しました。')

    elif 'を探す' in command:
        reg_ex = re.search('(.*)を探す', command)
        url = 'https://www.google.co.jp/'
        if reg_ex:
            subsearch = reg_ex.group(1)
            url += f'search?source=hp&ei=yW9cXqOsBeytmAWK06PgBg&q={subsearch}&oq={subsearch}'
            webbrowser.open(url)
            print(webbrowser)
            engine.say(f'{subsearch}を探しました。')
            # aana.get_single_audio(f'{subsearch}を探しました。')

    elif 'の画像' in command:
        reg_ex = re.search('(.*)の画像', command)
        url = 'https://www.google.co.jp/'
        if reg_ex:
            subsearch = reg_ex.group(1)
            url += f'search?tbm=isch&source=hp&ei=yW9cXqOsBeytmAWK06PgBg&q={subsearch}&oq={subsearch}'
            webbrowser.open(url)
            # aana.get_single_audio(f'{subsearch}画像を探しました。')
            engine.say(f'{subsearch}画像を探しました。')

    elif 'を実行する' in command:
        reg_ex = re.search('(.*)を実行する', command)
        print(reg_ex)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = f"{appname[:-1]}.app"
            print(os.path.join("/Applications/", appname1))
            subprocess.Popen(["open", "-n", os.path.join("/Applications/", appname1)], stdout=subprocess.PIPE)
            # aana.get_single_audio(f'{appname}を実行する。')
            engine.say(f'{appname}を実行する。')

    elif "私の名前は" in command:
        reg_ex = re.search("私の名前は(.+)", command)
        if reg_ex:
            callname = reg_ex.group(1)
            file = open("name.txt","w+")
            file.write(callname)
            file.close()
            engine.say(f"{callname}で呼びます。")
            print(f"{callname}で呼びます。")

    elif '時間' in command:
        now = datetime.datetime.now()
        # aana.get_single_audio(f'現在の時間は{now.hour}時{now.minute}分です。')
        engine.say(f'現在の時間は{now.hour}時{now.minute}分です。')

    # execute engine then wait next
    engine.runAndWait()

while True:
    name = get_name()
    if name == '':
        engine.say('お名前はなんですか？')
    # else:
    #     engine.say(f'おはよう、{name}たん')

    print(f'話してください...')
    assistant(myCommand())

#TODO
# voice assistant ouvrir un fichier video ou audio sur commande
# user : douga
# assistant: quel film voulez vous voir ? ( list all files from the folder video )
# user: title
