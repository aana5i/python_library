# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import quote


class WebCrawler:
    def __init__(self, url, agent='Mozilla/5.0', decoder='utf-8', parser='html.parser'):# htmlでparsing
        """
        get soup
        :param url: str
        :param agent: str
        :param decoder: str
        :param parser: str
        """
        self.url = url
        self.request = Request(self.url, headers={'User-Agent': agent})
        try:
            self.response = urlopen(self.request).read()
        except UnicodeEncodeError:
            # tmp_url = url.split('/')  # get url and split
            # begin = tmp_url[0]  # remove the 'https:' to not quote it
            # end = quote('/'.join(tmp_url[1:]))  # quote the rest
            # self.url = begin + '/' + end  # reform url
            self.url = self.the_kanji_problem()

            self.response = urlopen(self.url).read()

        self.soup = BeautifulSoup(self.response.decode(decoder), parser)

    def the_kanji_problem(self):
        url_to_test = [char for char in self.url]
        result = ''
        for letter in url_to_test:
            if len(letter.encode('utf-8')) > 1:# 漢字・ひらがなの時、3になる。
                letter = quote(letter)# quote(日本語の一文字)は、日本語の一文字をASCII化する。
            result += letter
        return result

    def get_soup(self):# soup(HTML)を取得。__init__()では作成しない。
        return self.soup
