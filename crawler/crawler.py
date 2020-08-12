# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


class WebCrawler:
    def __init__(self, url, agent='Mozilla/5.0', decoder='utf-8', parser='html.parser'):
        self.url = url
        self.request = Request(self.url, headers={'User-Agent': agent})
        self.response = urlopen(self.request).read()
        self.soup = BeautifulSoup(self.response.decode(decoder), parser)
    
    def get_soup(self):
        return self.soup
