import sys
import re
sys.path.append("../../..")
from tools.word_extractor import get_words_list
from db.tools.db_sqlite import DB
from db.tools.create_table import DbBuilder

import speech_recognition as sr
import pyttsx3


class MasterVoice:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.set_engine()

    def set_engine(self):
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty("voice", self.voices[0].id)
        self.engine.setProperty('rate', 115)
        self.engine.setProperty('volume', 0.9)

    def myCommand(self):
        # "listens for commands"
        r = sr.Recognizer()# Recognizerはライブラリ
        # engine.runAndWait()

        with sr.Microphone() as source:# 音(source)はマイクロフォンから取ってくる。
            r.pause_threshold = 0.5# 音を取った後、カットする。
            r.adjust_for_ambient_noise(source, duration=1)# ノイズを取り除く。
            audio = r.listen(source)# 綺麗になった音がaudioになる。

        try:
            self.command = r.recognize_google(audio, language='ja-JP')# このaudioはどんな言語か。

        except sr.UnknownValueError:# 音を拾ったけど言語ではないとき。
            print('....')
            self.myCommand()

    def read_text(self, text):
        self.engine.say(text)

    def assistant(self):
        #TODO retirer tout les cases d'ici pour les mettre dans des fichiers seprarer
        if 'そこまで' in self.command:
            # self.engine.say(f'さようなら、{self.name[0][0]}ちゃん')
            self.engine.say(f'さようなら')
            self.engine.runAndWait()
            exit()

        elif re.match(r'\S+の\S+方', self.command.replace(' ', '')):
            print(get_words_list(self.command))
            site_name, subsearch, order = get_words_list(self.command)
            site_dic = {'クックパッド': 'https://cookpad.com/search/', 'youtube': 'https://www.youtube.com/results?search_query='}# key:サイト名 value:サイトURL
            url = 'https://www.google.co.jp/'
            for kwords, urls in site_dic.items():# site_dicのkey, valueをペアで取得。
                if site_name in kwords:# reg_ex[0]の含まれるkeyから命令を出す。
                    url = urls# kwordsのurlsが代入される。
            if site_name:
                if 'https://www.google.co.jp/' in url:
                    url += f'search?sxsrf=ALeKk01uAOvlPejHN4lH97ttu805Q_WuLw%3A1603514862906&ei=7rGTX6DxNsz7-QbG_4Bo&q=site%3A+{site_name}+{subsearch}&oq=site%3A+{site_name}+{subsearch}'
                else:
                    url += f'{subsearch}'

                self.engine.say(f'{subsearch}の{order}を探しました。')

            else:
                self.read_text('命令をわかりませんでした。')

        elif 'クックパッド' in self.command:


        self.engine.runAndWait()
