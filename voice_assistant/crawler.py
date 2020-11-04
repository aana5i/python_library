# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import quote


class WebCrawler:
    def __init__(self, url, agent='Mozilla/5.0', decoder='utf-8', parser='html.parser'):
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
            self.url = self.the_kanji_problem()

            self.response = urlopen(self.url).read()

        self.soup = BeautifulSoup(self.response.decode(decoder), parser)

    def the_kanji_problem(self):
        url_to_test = [char for char in self.url]
        result = ''
        for letter in url_to_test:
            if len(letter.encode('utf-8')) > 1:
                letter = quote(letter)
            result += letter
        return result

    def get_soup(self):
        return self.soup
