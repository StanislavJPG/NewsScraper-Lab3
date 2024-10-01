import requests
from bs4 import BeautifulSoup
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


class MathNewsSearcher:
    _HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    def __init__(self):
        self.start = 0
        self.limit = 10
        self.news_titles = []
        # Run fetching news on initialization level to add fetching complicity
        self._fetch_news()

    def _fetch_news(self):
        # google url search
        url = 'https://www.google.com/search'
        # query params. Let's find all mathmatics news
        query = {'q': 'математика+україна', 'tbm': 'nws', 'start': self.start}
        # make GET request with params and headers to get access
        response = requests.get(url, headers=self._HEADERS, params=query)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')  # creating bs instance to parse text into html
            # let's find all div with specific unique class
            search_results = soup.find_all('div', class_='SoaBEf', limit=self.limit)  # NOTE: important to have limit here!

            for result in search_results:
                # Now from div let's get specific news text data
                titles = {
                    'title': result.find("div", class_="n0jPhd ynAwRc MBeuO nDgy9d").text,
                    'new_url': result.find("a", class_="WlydOe").get('href'),
                    'posted': result.find('div', class_='OSrXXb rbYSKb LfVVr').text,
                    'add_info': result.find('div', class_='GI74Re nDgy9d').text
                }
                self.news_titles.append(titles)
        else:
            return HTTP_500_INTERNAL_SERVER_ERROR

    def __iter__(self):
        # return object itself
        return self

    def __next__(self) -> dict:
        """Simple iterator to get single news dict object on every iteration"""

        if self.start < len(self.news_titles):  # iteration will proceed {self.limit} times
            news_item = self.news_titles[self.start]
            self.start += 1
            return news_item
        else:
            raise StopIteration