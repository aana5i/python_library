# -*- coding: utf-8 -*-
from pprint import pprint


class SqlOrder:
    def __init__(self, json):
        self.json = json

    def insert_all_train_infos(self):
        """

        :return: json
        """
        lines = self.json
        result = {}

        for counter, line in enumerate(lines):
            train = {
                counter: {'lines': {'line_name': line['line']},
                          'Start_end_stations': {'start_station': line['start_station'], 'end_station': line['end_station'],
                                                 'line_id': 'id'},
                          'trains': {'line_id': 'id', 'start_end_station_id': 'id', 'delay': line['delay'],
                                     'detail': line['details'] if 'details' in line else '', 'status': line['status'], 'start_time': line['start_time'],
                                     'now_time': 'get_now_time'}}
                      }

            result.update(train)

        return result


"""
USAGE

json = 
    {
        'delay': '止まっている',
        'details': '迷惑行為',
        'end_station': '池袋',
        'line': '山手線',
        'section': '山手線[新宿→池袋]',
        'start_station': '新宿',
        'start_time': '13:12',
        'status': 'ゆったり立てる',
        'timesOfDay': '2020/10/27 13:12'
    }
      
sql_order = SqlOrder(json)

result =
    {
        'lines': {'line_name':  '山手線'},
        'Start_end_stations': {'start_station': '新宿', 'end_station': '池袋', 'line_id': 'id'},  
        'trains': {'line_id': 'id', 'start_end_station_id': 'id',
                            'delay': '止まっている',
                            'detail': '迷惑行為',
                            'status': 'ゆったり立てる',
                            'start_time': '13:12',
                            'now_time': 'get_now_time'}
    }
"""