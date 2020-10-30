from pprint import pprint
import requests
import json


def to_json(path, data, mode='a', encoding='utf-8'):
    """
    write one line in a text file
    :param path: str
    :param data: str
    :param mode: str
    :param encoding: str
    """
    _encoding = ['utf-8', 'shift_jis']
    with open(path, mode, encoding=[_encoding[encoding] if isinstance(encoding, int) else encoding][0]) as f:
        json.dump(data, f, sort_keys=True, ensure_ascii=False, indent=4)
        f.close()


def from_json(path, mode='r', encoding='utf-8'):
    """
    get all line from a text file
    :param path: str
    :param mode: str
    :param encoding: str
    :return: list
    """
    _encoding = ['utf-8', 'shift_jis']
    with open(path, mode=mode, encoding=[_encoding[encoding] if isinstance(encoding, int) else encoding][0]) as f:
        result = json.load(f)
        f.close()
    return result


BASE_URL = 'https://www.train-guide.westjr.co.jp'
master_links = ['https://www.train-guide.westjr.co.jp/api/v3/area_kinki_master.json',
                'https://www.train-guide.westjr.co.jp/api/v3/area_hokuriku_master.json',
                'https://www.train-guide.westjr.co.jp/api/v3/area_okayama_master.json',
                'https://www.train-guide.westjr.co.jp/api/v3/area_hiroshima_master.json',
                'https://www.train-guide.westjr.co.jp/api/v3/area_sanin_master.json']

# lines
data = requests.get(master_links[0])
line = {}  # to do to get all lines
for lines in data.json()['lines']:
    current_line = data.json()['lines'][lines]
    line['name'] = current_line['name']
    line['destination'] = current_line['dest']['lower'], current_line['dest']['upper'],
    line['pos'] = BASE_URL + current_line['pos']
    line['st'] = BASE_URL + current_line['st']
    if 'relatelines' in current_line:
        line['relatelines'] = current_line['relatelines']

    pprint(line)

    # trains
    data_pos = requests.get(BASE_URL + current_line['pos'])
    current_trains = data_pos.json()['trains']
    trains = {}  # to use
    for current_train in current_trains:
        train = {
            'line': current_train['dest']['line'],
            'text': current_train['dest']['text'],
            'displayType': current_train['displayType'],
            'numberOfCars': current_train['numberOfCars'],
            'direction': line['destination'][current_train['direction']],
            'pos': current_train['pos'],
            'delayMinutes': current_train['delayMinutes']
        }

        pprint(train)

    # station
    data_st = requests.get(BASE_URL + current_line['st'])
    # pprint(data_st.json())
    break

for link in master_links:
    filename = ''.join(link.split('/')[-1])
    # to_json(filename, data.json(), 'w')
    # pprint(from_json(filename))
    break


'''
USAGE

l'utilisateur cherche une ligne par son nom
l'app retourne des informations si le train est en retard
    le delay, le nombre de voiture du prochain train en gare, le displaytype
l'app retourne des informations si tout va bien
    le nombre de voitures si celui-ci est different des autres jours, le displaytype si different des autres jours. 
'''
