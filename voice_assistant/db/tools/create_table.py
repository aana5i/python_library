import os
import sys
sys.path.append("../..")
from tools.importer_saver import from_json
from db.tools.db_sqlite import DB


class DbBuilder:
    def __init__(self, db):
        # self.sql_db = DB('../database.db')
        self.sql_db = db
        self.create_base_tables()

    def create_base_tables(self):
        """
        Set the base tables sql syntax
        :return:
        """
        PATH = 'db/base_tables'
        f = []
        for (dirpath, dirnames, filenames) in os.walk(PATH):
            f.extend(filenames)
            break

        for files in f:
            if '.json' in files:
                base_tables = from_json(PATH, files)
                self.set_table(base_tables)

    def set_table(self, args):
        """
        create the sql order to create table
        :param table_name:
        :param args:
        :return:
        """
        for table_name, args in args.items():
            sql = f'CREATE TABLE IF NOT EXISTS {table_name} ('
            for counter, arg in enumerate(args):
                sql += arg
                if counter < len(args) - 1:
                    sql += ', '
            sql += ');'
            self.create_tables(sql)

    def create_tables(self, sql):
        """
        Create the table using the sql order
        :param sql:
        :return:
        """
        # constuire les relations entre les tables
        self.sql_db.create_table(sql)

    def select_in_db(self, table_name, column, conditions=None):
        sql = f'SELECT id, '
        for counter, arg in enumerate(column):
            sql += arg
            if counter < len(column) - 1:
                sql += ', '
        sql += f' FROM {table_name}'
        if conditions:
            for counter, condition in enumerate(conditions):
                sql += ' WHERE' if counter == 0 else ' AND'
                sql += f' {condition[0]} = '
                sql += f'{condition[1]}' if isinstance(condition[1], int) else f'"{condition[1]}"'
        sql += ';'

        return self.sql_db.task_select(sql)[0]

    def insert_in_db(self, table_name, arg):
        sql = 'INSERT INTO ' + table_name
        col = []
        param = []
        for column, value in arg.items():
            col.append(column)
            param.append(value)

        for counter, column in enumerate(col):
            if counter == 0:
                sql += ' ('
            sql += f'{column}'
            if counter < len(col) - 1:
                sql += ', '

        sql += ')'

        for counter, value in enumerate(param):
            if counter == 0:
                sql += ' VALUES ('
            sql += f'{value}' if isinstance(value, int) else f'"{value}"'
            if counter < len(col) - 1:
                sql += ', '

        sql += ');'

        # check_select = []
        # if table_name != 'trains':
        check_select = self.select_in_db(table_name, col, arg.items())
        if not check_select:
            return self.sql_db.task_insert(sql)
        return check_select[0][0]


if __name__ == '__main__':
    # TODO Add argparse and logging
    database = DB('../database.db')
    db = DbBuilder(database)

    ''' Populate base table '''
    db.create_base_tables()

"""
USAGE
db = DbBuilder('db')
''' Populate base table '''
# db.create_base_tables()
builder = {
    'lines': {'column': ['id'], 'condition': ['WHERE line_name = test_name_line', 'and', 'id = 1']}
}
inserter = { 'Start_end_stations': {'line_id': 0, 'start_station': 'test_start_station', 'end_station': 'test_end_station'}}
# db.select_in_db()

for table_name, arg in args.items():
    db.insert_in_db(inserter)
"""
