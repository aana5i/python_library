# -*- coding: utf-8 -*-

from pprint import pprint
from crawler import WebCrawler
from page_list import PageList as PL


class Builder:
    def __init__(self):
        pass

    def get_crawler(self, url):
        self.crawler = WebCrawler(url)

    def get_data(self, url):
        self.get_crawler(url)

        # manga_list = PL(url, self.crawler.get_soup())
        # result = manga_list.get_data()
        #
        # # _url = 'https://www.wawacity.vip/?p=manga&id=1872-the-millionaire-detective-balance-unlimited-saison1'
        # # _url = 'https://www.wawacity.vip/?p=manga&id=1874-food-wars-saison5'
        # for k, v in result.items():
        #     result[k]['page'] = self.get_page_data(result[k]['link'])

        titles = self.crawler.get_soup().find_all("a", href=True)
        for title in titles:
            print(title)

        #TODO, enregister les differents lien + text
#       les séparer par class de css


bu = Builder()
url = 'https://www.cookpad.com/search/パスタ'

bu.get_data(url)
