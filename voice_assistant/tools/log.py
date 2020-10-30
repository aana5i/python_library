
# -*- coding: utf-8 -*-

import logging
import os


def log(file, log_level):
    """
    set the basicConfig for logging
    :param file: str PATH
    :param log_level: logging
    :return:
    """
    path = os.path.join(os.getcwd(), f'logs/{file}.log')
    if not os.path.isfile(path):
        f = open(path,  'w+')
        f.close()
    logging.basicConfig(filename=path, level=log_level)


# myapp.py
import logging
import mylib

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Started')
    mylib.do_something()
    logging.info('Finished')

if __name__ == '__main__':
    main()
# mylib.py
import logging

def do_something():
    logging.info('Doing something')