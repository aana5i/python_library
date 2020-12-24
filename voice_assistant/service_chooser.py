#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import argparse
import logging
import datetime
import pytz
import webbrowser

from tools.log import log

from add_on.train.jourudan import Jourudan
from add_on.meteo.meteo import Meteo
from add_on.case_cookpad.builder import Builder
from add_on.youtube.api_youtube import Youtube
from db.populate_db.train.train import SqlOrder
from db.tools.create_table import DbBuilder
from db.tools.db_sqlite import DB
from engine.vocal.voice import assistant


class ServiceChooser:
    def __init__(self):
        self.db_path = os.path.join('/'.join(os.getcwd().split('/')[:-1]), 'html/database.db')

    def create_base_db(self):
        database = DbBuilder(DB(self.db_path))

    def get_current_weather(self, city):
        weather = Meteo(city)
        print(weather.current_weather())
        print(weather.forecast_weather())

    def get_youtube_infos(self):
        youtube = Youtube()
        query = input('検索ワード')
        youtube.routine(query)

    def get_train_infos(self):
        """
        Get all trains infos
        :return:
        """
        print('service: train')
        file = 'train_infos'
        log(file=file, log_level=logging.INFO)

        logging.info('train_infos: Started')

        ''' Connect to the DB '''
        database = DB(self.db_path)
        db = DbBuilder(database)

        ''' Retrieve train add_on page crawled data '''
        J = Jourudan()
        json = J.routine()

        ''' Retrieve train add_on Sql  '''
        train = SqlOrder(json)
        result = train.insert_all_train_infos()

        ''' Pre-set var '''
        line_id = None
        station_id = None

        ''' Info logger '''
        max_line_id = 0
        max_start_end_stations_id = 0
        max_station_id = 0

        ''' Insert data in Db by train '''
        for train in result:
            for table_name, arg in result[train].items():
                if table_name == 'Train_lines':
                    line_id = db.insert_in_db(table_name, arg)
                    logging.info(f'trains =>     lines: {line_id}')

                    max_line_id = self.get_max_id(line_id, max_line_id)

                elif table_name == 'Train_Start_end_stations':
                    if not line_id:
                        logging.debug(f'Start_end_stations =>     line_id: {line_id}')
                    arg['line_id'] = line_id
                    station_id = db.insert_in_db(table_name, arg)
                    logging.info(f'trains =>     Start_end_stations: {station_id}')

                    max_start_end_stations_id = self.get_max_id(station_id, max_start_end_stations_id)

                elif table_name == 'Train_trains':
                    if not line_id:
                        logging.debug(f'trains =>     line_id: {line_id}')
                    if not station_id:
                        logging.debug(f'trains =>     station_id: {station_id}')
                    arg['line_id'] = line_id
                    arg['start_end_station_id'] = station_id
                    arg['now_time'] = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")
                    trains_id = db.insert_in_db(table_name, arg)
                    logging.info(f'trains =>     station_id: {trains_id}')

                    max_station_id = self.get_max_id(trains_id, max_station_id)
        logging.info(f'Lines: {max_line_id},  Start_end_stations: {max_start_end_stations_id},  Stations: {max_station_id}')
        logging.info('train_infos: Finished')

    @staticmethod
    def get_max_id(source, to_compare):
        """
        dave max id
        :param source: str
        :param to_compare: str
        :return:
        """
        if to_compare > source:
            source = to_compare
        return source

    def get_page(self, target):
        bu = Builder()
        #TODO separer les ordre de voice et creer une master qui ne fait que lancer la voix
        #TODO utiliser une fonction qui ne fasse que lire e qu'on lui envoit
        #TODO varier la vitesse et la frequense
        user = input('何を作りたいですか？\n')
        urls = {'cookpad': f'https://cookpad.com/search/{user}', 'youtube': f'https://cookpad.com/search/{user}'}
        url = urls[target]

        self.data = bu.get_data(url)# ディクショナリ型で返ってくる。

        self.lst = [key for key in self.data.keys()]

    def get_cookpad(self):
        self.get_page('cookpad')# レシピの表示
        assistant(read(self.lst))
        self.get_user_input()

    def get_user_input(self):
        user = input('どんなレシピが見たいですか？\n')
        try:
            user = int(user)
            if user > len(self.lst):
                self.get_user_input()
                return
            else:
                url = 'https://cookpad.com' + self.data[self.lst[user-1]]# 選んだ料理名のクックパッドのページのURLを作成。self.data[料理名] = recipeのID

        except ValueError:
            url = 'https://cookpad.com' + self.data[user]# 選んだ料理名のクックパッドのページのURLを作成。self.data[料理名] = recipeのID
        webbrowser.open(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Service chooser.')
    parser.add_argument('--train', '-tr', type=str, help='Train')
    parser.add_argument('--meteo', '-me', type=str, help='Meteo')
    # parser.add_argument('--time', '-ti', help='Time', action='store_true')
    parser.add_argument('--youtube', '-yo', help='Youtube', action='store_true')
    parser.add_argument('--cookpad', '-co', help='Cookpad', action='store_true')

    args = parser.parse_args()

    se = ServiceChooser()
    if args.train:
        if args.train == 'infos':
            se.get_train_infos()
    if args.meteo:
        se.get_current_weather(args.meteo)
    if args.youtube:
        se.get_youtube_infos()
    if args.cookpad:
        se.get_cookpad()

''' USAGE '''
"""
python service_chooser.py -tr infos
"""
