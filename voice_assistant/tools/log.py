
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
    logging.basicConfig(filename=path, level=log_level, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %p %I:%M:%S')
