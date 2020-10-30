# -*- coding: utf-8 -*-

import sqlite3 as sql


class DB:
    def __init__(self, db):
        self.get_connection(db)

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        self.con = None
        try:
            self.con = sql.connect(db_file)
        except Error as e:
            print(e)

    def get_connection(self, db):
        self.create_connection(db)

    def create_table(self, create_table_sql):
        """
        create table
        :param create_table_sql:
        """
        c = self.con.cursor()
        c.execute(create_table_sql)

    def task_select(self, select):
        """
        Executes a select statement and return results and column/field names.
        :param select:
        :return: column/field names
        """
        with self.con as conn:
            c = conn.cursor()
            c.execute(select)
            col_names = [str(name[0]).lower() for name in c.description]
            return c.fetchall(), col_names

    def task_insert(self, insert):
        """
        Executes a insert statement and return the last inserted id.
        :param insert:
        :return: last id
        """
        c = self.con.cursor()
        c.execute(insert)

        self.con.commit()

        return c.lastrowid

    def task_update(self, task):
        """
        Executes a update statement and return the last inserted id.
        :param task:
        :return: last id
        """
        c = self.con.cursor()
        c.execute(task)

        self.con.commit()

        return c.lastrowid

    def close_db(self):
        self.con.close()
