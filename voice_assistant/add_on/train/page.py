# -*- coding: utf-8 -*-


class TrafficInfos:
    def __init__(self, crawler, line):
        self.crawler = crawler
        self.line = line
        # self.get_infos()

    def get_infos(self, full_flag=0):
        json_result = {}

        table = self.crawler.find("table", {'class': 'main-table'})
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        list_name = []
        for tr in trs:
            company = tr.find('th', {'class': 'company'}).getText()
            if full_flag:
                list_name.append(company)
            else:
                if self.line in company:
                    json_result['company'] = company
                    json_result['status'] = tr.find('td', {'class': 'pictgram-official'}).find('a').get('title')
                    json_result['predict'] = tr.find('td', {'class': 'predict'}).getText() \
                        .replace('きょう1%', '') \
                        .replace('あす1%', '') \
                        .replace('あす', 'jklあす') \
                        .split('jkl')
        if full_flag:
            json_result = list_name
        return json_result
