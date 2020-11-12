# -*- coding: utf-8 -*-

import os
import argparse
import logging
import datetime
import pytz
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
        path = os.path.join(os.getcwd(), f'logs/{file}.log')
        logging.basicConfig(filename=path, level=logging.WARNING)

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

        ''' Insert data in Db by train '''
        for train in result:
            for table_name, arg in result[train].items():
                if table_name == 'lines':
                    line_id = db.insert_in_db(table_name, arg)

                elif table_name == 'Start_end_stations':
                    if not line_id:
                        logging.warning(f'Start_end_stations =>     line_id: {line_id}')
                    arg['line_id'] = line_id
                    station_id = db.insert_in_db(table_name, arg)

                elif table_name == 'trains':
                    if not line_id:
                            logging.warning(f'trains =>     line_id: {line_id}')
                    if not station_id:
                        logging.warning(f'trains =>     station_id: {station_id}')
                    arg['line_id'] = line_id
                    arg['start_end_station_id'] = station_id
                    arg['now_time'] = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")
                    trains_id = db.insert_in_db(table_name, arg)
                    logging.info(f'trains =>     station_id: {trains_id}')
        logging.info('train_infos: Finished')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Service chooser.')
    parser.add_argument('--train', '-tr', type=str, help='Train')

    args = parser.parse_args()

    se = ServiceChooser()
    if args.train:
        if args.train == 'infos':
            se.get_train_infos()
