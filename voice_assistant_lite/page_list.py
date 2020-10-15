# -*- coding: utf-8 -*-
import re


class PageList:
    def __init__(self, url, soup):
        self.url = url
        self.soup = soup

    def get_data(self):
        clean_url = self.url.replace('?p=mangas', '')

        result = {}
        res = {}
        block = self.soup.find_all('div', {'class': "wa-sub-block wa-post-detail-item"})
        for counter, b in enumerate(block):
            title = b.find('div', {'class': 'wa-sub-block-title'})
            link = title.find_all("a", href=True)

            res['title'] = re.sub(r'\d+\svote\(s\)', '', title.getText()).strip()
            for i in link:
                res['link'] = clean_url + i['href']

            res['img'] = clean_url + re.sub("/", "", b.find('div', {'class': 'cover col-md-2'}).find('img').attrs['src'], count=1)

            res['date'] = b.find('span', {'class': 'date-text text-muted'}).getText().strip()

            res['short_desc'] = b.find('p').getText().strip()

            result[counter] = {k: v for k, v in res.items()}

        return result
