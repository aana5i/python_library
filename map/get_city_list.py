import sys
from pprint import pprint
sys.path.append("..\Crawler")
from builder import Builder


def to_text(path, data, mode='a', encoding='utf-8'):
    """
    write one line in a text file
    :param path: str
    :param data: str
    :param mode: str
    :param encoding: str
    """
    _encoding = ['utf-8', 'shift_jis']
    with open(path, mode, encoding=[_encoding[encoding] if isinstance(encoding, int) else encoding][0]) as f:
        f.write(f'{data}\r')
        f.close()


bu = Builder()


for i in range(1, 700):
    url = f'http://www.journaldunet.com/management/ville/index/villes?page={i}'

    soup = bu.get_data(url)
    get_lists = soup.find_all('ul', {'class': 'bloc size1of2 odSquareList'})

    for lists in get_lists:
        for city in lists.find_all("a", href=True):
            latitude = ''
            longitude = ''
            value = city.getText().split(' ')

            url2 = f'http://www.journaldunet.com/{city["href"]}'

            soup2 = bu.get_data(url2)
            get_lists2 = soup2.find_all('table', {'class': 'odTable odTableAuto'})
            for table in get_lists2:
                trs = table.find_all('tr')
                for tr in trs:
                    if 'Latitude' in tr.getText():
                        latitude = tr.getText().replace('Latitude', '').replace('-', '')
                    if 'Longitude' in tr.getText():
                        longitude = tr.getText().replace('Longitude', '').replace('-', '')

            to_save = f"{value[1].replace('(', '').replace(')', '')}, {value[0]}, {latitude}, {longitude}"

            to_text('cities.txt', to_save)
    print(f'page: {i}')

print('done')
