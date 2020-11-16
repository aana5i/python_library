from crawler import WebCrawler


class Voice:
    def __init__(self):
        pass

    def youtube_search(self, query):
        url = f'https://www.youtube.com/results?search_query={query}'
        list_page = WebCrawler(url)
        list_page_soup = list_page.get_soup()

        tables = list_page_soup.find_all('a')
        for title in tables:
            print(title)


v = Voice()
v.youtube_search('猫')
