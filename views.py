import json

from fastapi import FastAPI
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scraper import MathNewsSearcher

# using FastAPI as framework because of it's simplicity
app = FastAPI(
    title='MathNews'
)


def _save_news_into_txt(dict_: dict):
    # save json news with encoding utf-8 to keep ukrainian language in txt file
    with open('mathNewsDocs.txt', 'a', encoding='utf-8') as file:
        file.write(json.dumps(dict_, ensure_ascii=False) + '\n')
        file.close()


@app.get('/api/news/')
def news_api_view():
    titles = MathNewsSearcher()  # create MathNewsSearcher instance (should remember that is iterator now)
    try:
        lst = []
        for title in titles:  # every iteration add news info dict to list and write it into txt file
            dict_ = {
                'title': title['title'],
                'new_url': title['new_url'],
                'posted': title['posted'],
                'additional_info': title['add_info']
            }
            _save_news_into_txt(dict_)
            lst.append(dict_)
        return lst
    except:
        return HTTP_500_INTERNAL_SERVER_ERROR
