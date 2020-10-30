# -*- coding: utf-8 -*-

from pprint import pprint
from crawler import WebCrawler
from train.page import TrafficInfos as TF
from train.regions import ListRegions as LR


class Builder:
    def __init__(self):
        pass

    def get_crawler(self, url):
        self.crawler = WebCrawler(url).get_soup()

    def get_train_line_data(self, url, line):
        self.get_crawler(url)

        traffic_infos = TF(self.crawler, line)
        json_result = traffic_infos.get_infos()
        pprint(json_result)

    def get_regions_lines(self):
        self.get_crawler('https://www.tetsudo.com/traffic/')

        list_regions = LR(self.crawler)
        json_region_pages = list_regions.get_regions_pages()

        json_result = {}

        for region_name, region_url in json_region_pages.items():
            self.get_crawler(region_url)

            traffic_infos = TF(self.crawler, line)
            json_company = traffic_infos.get_infos(1)
            json_result[region_name] = json_company
        pprint(json_result)  # region; lines list
        # TODO
        # pour ce faire, le profil de lutilisateur doit etre rensigner
        # en prennant les informations depuis le profil de lutilisateur nous sauront quel train, ligne, heure doit etre utilise chaqu jours


bu = Builder()
url = 'https://www.tetsudo.com/traffic/category/新幹線/'
line = '山陽新幹線'
# bu.get_train_line_data(url, line)
bu.get_regions_lines()
