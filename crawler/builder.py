# -*- coding: utf-8 -*-

from crawler import WebCrawler


class Builder:
    def __init__(self):
        pass

    def get_crawler(self, url):
        self.crawler = WebCrawler(url)

    def get_data(self, url):
        self.get_crawler(url)
        return self.crawler.get_soup()

"""
USAGE

bu = Builder()
url = 'https://cookpad.com/search/パスタ'

bu.get_data(url)
"""

