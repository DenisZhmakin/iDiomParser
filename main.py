import json
import string
from pathlib import Path

import grequests
import requests

from bs4 import BeautifulSoup

from entities.idiom import Idiom

SITE_URL = "https://www.phrases.com"


def parse_idioms(idioms_list: list):
    count = 0
    request = (grequests.get(url) for url in idioms_list)
    responses = grequests.map(request)

    for response in responses:
        if response is not None:
            soup = BeautifulSoup(response.text, 'lxml')

            etym_tag = soup.select_one('div.etym')

            idiom = Idiom(
                phrase=soup.select_one('span.disp-phrase-body').text,
                explanation=soup.select_one('div.disp-phrase-exp').text,
                etymology=etym_tag.text if etym_tag is not None else None
            )

            idiom.write()
            count += 1

    print(count)


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.select_one("div.tdata-ext").table.tbody

    idioms_url_list = list()
    for elem in tbody.select("td.tal.fx"):
        if elem.a is not None:
            idioms_url_list.append(
                f"{SITE_URL}{elem.a['href']}"
            )

    parse_idioms(idioms_url_list)


def _main():
    letters = string.ascii_uppercase
    letters_json = Path('.') / 'letters.json'

    if not letters_json.exists():
        letters_json.write_text(json.dumps({}))

    for letter in letters:
        print(f"Обрабатывается литера {letter}")
        letter_dict = json.loads(letters_json.read_text())
        if letter in letter_dict:
            continue

        parse_page(f"{SITE_URL}/letter/{letter}/99999")
        letter_dict[letter] = 1
        letters_json.write_text(json.dumps(letter_dict))


if __name__ == '__main__':
    _main()
