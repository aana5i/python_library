# coding: utf-8 
import re
from pprint import pprint
import sys
sys.path.append("../..")
from crawler import WebCrawler


class Jourudan:
    def __init__(self):
        self.url = 'https://mb.jorudan.co.jp/os/live.cgi?aid=全国&offset='

    def routine(self):
        self.get_all_pages()
        return self.get_line_infos()

    def get_all_pages(self):
        self.page_soup = []
        regex = {
            '遅れ(10分未満)':'遅れ\(\S+分\S+\)',
            '遅れ(30分以上)':'遅れ\(\S+分\S+\)',
            '遅れ(10〜30分)': '遅れ\(\S+分\)',
            '止まっている': '止まっている',
            '順調': '順調',
            'その他': 'その他',
            '運転再開': '運転再開'
        }

        for page_number in range(0, 900, 30):  # 581
            list_page = WebCrawler(self.url + str(page_number))
            list_page_soup = list_page.get_soup()
            tables = list_page_soup.find_all('div', {'class': 'div_table'})

            for table in tables:
                spans = table.find_all('span')
                train = {}

                for span_counter, span in enumerate(spans):
                    span = span.getText()
                    if span_counter == 0:
                        for key, reg in regex.items():
                            if key in span:
                                train['line'] = re.sub(reg, '', span).replace(' ', '')
                                train['delay'] = re.findall(reg, span)[0]

                    elif span_counter == 1:
                        train['start_time'] = span.split(' ')[0]

                        tmp = re.findall(r'(\S+) → (\S+)', span)

                        if not tmp:
                            tmp = [(re.findall(r'(\S+) →', span)[0], '')]

                        train['start_station'], train['end_station'] = tmp[0]

                    elif span_counter == 2:
                        train['status'] = span

                    elif span_counter == 3:
                        a = table.parent.parent.find("a", href=True)
                        a = re.findall(r'id=\d+', a['href'])[0]

                        detail_page_soup = WebCrawler('https://mb.jorudan.co.jp/os/live.cgi?' + a).get_soup()
                        detail_table = detail_page_soup.find('table', {'class': 'detail_table'})
                        trs = detail_table.find_all('tr')

                        english_trad = {
                            '時刻': 'timesOfDay',
                            '区間': 'section',
                            '詳細': 'details'
                        }

                        for tr in trs:
                            tds = tr.find_all('td')
                            train[english_trad[tds[0].getText()]] = tds[1].getText().strip()

                self.page_soup.append(train)

    def get_line_infos(self):
        return self.page_soup


if __name__ == '__main__':
    J = Jourudan()
    J.routine()

"""
USAGE
a faire toutes les X minutes
mettre a jours la db, chaque maj ajoute des infos sans supprimer, pour avoir un historique.

creer une requete de recherche dans le db pour que l'utilisateur puisse rechercher sa ligne uniquement, ou une autre ligne
creer une tache qui va questionner la db sur le trajet ( une ou plusieurs lignes ) toutes les X 

DB
Table: Lines  ()  ID, line_name
insert line if not exist, id incremental 

Table: Start_end_station  ()  ID, lines_id, start_station, end_station
insert start_station, end_station, (select lines_id from lines where line_name == line) if not exist, id incremental

Table: Trains  ()  ID, Lines_id, Start_end_station_id, delay, details, status, start_time, now_time
insert lines_id, Start_end_station_id, delay, details, status, start_time, now_time, id incremental
"""
