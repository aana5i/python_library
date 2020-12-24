# -*- coding: utf-8 -*-

from pprint import pprint
import sys
sys.path.append("../..")
from  add_on.tools.crawler import WebCrawler
# from page_list import PageList as PL


class Builder:
    def __init__(self):
        pass

        # urlをパラメータにしてclawlar実行。
    def get_crawler(self, url):
        self.crawler = WebCrawler(url)

    def get_data(self, url):
        self.get_crawler(url)

        # 全てのaタグ(リンクがある項目)を取ってprint
        titles = self.crawler.get_soup().find_all("a", {'class': 'recipe-title'}, href=True)
        title_dic = {}
        for title in titles:
            # print(title.getText(), title['href'])
            title_dic[title.getText()] = title['href']
        return title_dic


if __name__ == '__main__':
    bu = Builder()
    url = 'https://cookpad.com/search/パスタ'

    print(url)
    print(bu.get_data(url))

# 来週
# titleからcssクラスとリンクとタイトルのテキストを取得。
# クラスによってグループ化。
# ページの同じ順番をキープする。
