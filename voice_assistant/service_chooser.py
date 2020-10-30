# -*- coding: utf-8 -*-

import os
from add_on.train.jourudan import Jourudan
from db.populate_db.train.train import SqlOrder
from db.tools.create_table import DbBuilder
from db.tools.db_sqlite import DB
import datetime
import pytz
from pprint import pprint


class ServiceChooser:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), 'db/database.db')

    def get_train_infos(self):
        database = DB(self.db_path)
        db = DbBuilder(database)

        J = Jourudan()
        json = J.routine()

        train = SqlOrder(json)
        result = train.insert_all_train_infos()
        counter_ = 0
        for train in result:
            for table_name, arg in result[train].items():
                if table_name == 'lines':
                    line_id = db.insert_in_db(table_name, arg)
                    counter_ += 1
                elif table_name == 'Start_end_stations':
                    arg['line_id'] = line_id
                    station_id = db.insert_in_db(table_name, arg)

                elif table_name == 'trains':
                    arg['line_id'] = line_id
                    arg['start_end_station_id'] = station_id
                    arg['now_time'] = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")
                    trains_id = db.insert_in_db(table_name, arg)
        print(counter_)


if __name__ == '__main__':
    se = ServiceChooser()
    se.get_train_infos()
