from pprint import pprint


class SqlOrder:
    def __init__(self, json):
        self.json = json

    def insert_all_train_infos(self):
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

inserter = { 'Start_end_stations': {'line_id': 0, 'start_station': 'test_start_station', 'end_station': 'test_end_station'} }
"""