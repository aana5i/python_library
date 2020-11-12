# -*- coding: utf-8 -*-

import os
import argparse
import logging
import datetime
import pytz

from tools.log import log

from add_on.train.jourudan import Jourudan
from db.populate_db.train.train import SqlOrder
from db.tools.create_table import DbBuilder
from db.tools.db_sqlite import DB


class ServiceChooser:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), 'db/database.db')

    def get_train_infos(self):
        """
        Get all trains infos
        :return:
        """
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
                if table_name == 'lines':
                    line_id = db.insert_in_db(table_name, arg)
                    logging.info(f'trains =>     lines: {line_id}')

                    max_line_id = self.get_max_id(line_id, max_line_id)

                elif table_name == 'Start_end_stations':
                    if not line_id:
                        logging.debug(f'Start_end_stations =>     line_id: {line_id}')
                    arg['line_id'] = line_id
                    station_id = db.insert_in_db(table_name, arg)
                    logging.info(f'trains =>     Start_end_stations: {station_id}')

                    max_start_end_stations_id = self.get_max_id(station_id, max_start_end_stations_id)

                elif table_name == 'trains':
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Service chooser.')
    parser.add_argument('--train', '-tr', type=str, help='Train')

    args = parser.parse_args()

    se = ServiceChooser()
    if args.train:
        if args.train == 'infos':
            se.get_train_infos()

''' USAGE '''
"""
python service_chooser.py -tr infos
"""
