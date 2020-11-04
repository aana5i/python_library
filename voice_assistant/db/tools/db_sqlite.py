# -*- coding: utf-8 -*-

import sqlite3 as sql


class DB:
    def __init__(self, db):
        self.get_connection(db)

    def create_connection(self, db_file):
        """
        create or connect to the DB
        :param db_file: str
        :return:
        """
        """ create a database connection to a SQLite database """
        self.con = None
        try:
            self.con = sql.connect(db_file)
        except Error as e:
            print(e)

    def get_connection(self, db):
        """
        un-used
        :param db: str
        :return:
        """
        self.create_connection(db)

    def create_table(self, create_table_sql):
        """
        create table
        :param create_table_sql: str SQL
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


"""
USAGE 

database = DB('../database.db')

CREATE TABLE:
create_table_sql = 
    "CREATE TABLE IF NOT EXIST groups (
        group_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );"
database.create_table(create_table_sql)
create_table_sql = 
    "CREATE TABLE IF NOT EXIST groups (
        group_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );"
database.create_table(create_table_sql)
create_table_sql = 
    "CREATE TABLE IF NOT EXIST groups (
        group_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );"
database.create_table(create_table_sql)
create_table_sql = 
    "CREATE TABLE IF NOT EXIST groups (
        group_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );"
database.create_table(create_table_sql)

SELECT:
select = "SELECT column_list FROM table;"
database.task_select(select)

INSERT:
insert = "INSERT INTO table (column1,column2 ,..) VALUES (value1, value2 , ...);"
database.task_insert(insert)

UPDATE:
task = 
    "UPDATE table
    SET column_1 = new_value_1,
        column_2 = new_value_2
    WHERE
        search_condition 
    ORDER column_or_expression
    LIMIT row_count OFFSET offset;"
database.task_update(task)
"""