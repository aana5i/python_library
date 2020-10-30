# -*- coding: utf-8 -*-


class ListRegions:
    def __init__(self, crawler):
        self.crawler = crawler

    def get_regions_pages(self):
        json_result = {}

        div = self.crawler.find("div", {'class': 'main-box traffic-category-listbox'})

        ul = div.find('ul')
        lis = ul.find_all('li')

        # get regions
        for li in lis:
            titles = li.find_all("a", href=True)
            for title in titles:
                json_result[title.getText()] = f"https://www.tetsudo.com{title['href']}"

        return json_result
