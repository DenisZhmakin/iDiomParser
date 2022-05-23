import json
import string
import time

import requests
from bs4 import BeautifulSoup
from jsonlines import jsonlines

SITE_URL = "https://www.theidioms.com"


def url_generator(letter: str):
    current_page = 2

    yield f"{SITE_URL}/{letter}/"

    while True:
        yield f"{SITE_URL}/{letter}/page/{current_page}/"
        current_page += 1


def parse_page(response_text: str):
    soap = BeautifulSoup(response_text, 'lxml')
    idiom_list = list(soap.select_one("div.new-list").dl.children)

    for dt, dd in zip(idiom_list[0::2], idiom_list[1::2]):
        idiom = {
            "phrase": dt.p.a.text,
            "meaning": dd.p.text,
        }

        with jsonlines.open('idioms.jsonl', mode='a') as writer:
            writer.write(json.dumps(idiom))


def _main():
    for letter in string.ascii_lowercase:
        for url in url_generator(letter):
            response = requests.get(url)

            soap = BeautifulSoup(response.text, 'lxml')
            next_page = soap.select_one('p.pagination').select_one('span.next').a

            parse_page(response.text)
            print(url)

            if next_page is None:
                break

            time.sleep(1)


if __name__ == '__main__':
    _main()
