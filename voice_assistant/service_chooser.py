# -*- coding: utf-8 -*-

import os
from add_on.train.jourudan import Jourudan
from db.populate_db.train.train import SqlOrder
from db.tools.create_table import DbBuilder
from db.tools.db_sqlite import DB
from pprint import pprint


class ServiceChooser:
    def __init__(self):
        pass

    def get_train_infos(self):
        J = Jourudan()
        json = J.routine()
        train = SqlOrder(json)
        result = train.insert_all_train_infos()
        db_path = os.path.join(os.getcwd(), 'db/database.db')
        database = DB(db_path)
        db = DbBuilder(database)
        pprint(result)
        # for train in result:
        #     print(train)
        #     for table_name, arg in train.items():
        #         print(table_name, arg)
        #     #     line_id = db.insert_in_db(table_name, arg)
            #     print(line_id)


if __name__ == '__main__':
    se = ServiceChooser()
    se.get_train_infos()
