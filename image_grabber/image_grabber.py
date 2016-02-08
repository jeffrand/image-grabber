import os
from time import time

from lxml import html
import requests

BASE_URL = 'http://www.bing.com/images/search'
BASE_PAYLOAD = {
    'qft': '+filterui:imagesize-large',
}


def make_request(search_for):
    payload = BASE_PAYLOAD.copy()
    payload['q'] = search_for
    r = requests.get(BASE_URL, params=payload)
    r.raise_for_status()
    return r.text


def parse_response(response_text):
    tree = html.fromstring(response_text)
    for el in tree.xpath('//a[@class="thumb"]'):
        href = el.get('href')
        if href:
            yield href


def mkdir(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError as e:
        if not e.errno == 17:
            raise


def store_image_href(href, dir_name):
    file_name = href.split('/')[-1]
    path = os.path.join(dir_name, file_name)
    if os.path.exists(path):
        file_parts = file_name.split('.')
        file_parts.insert(1, str(time()))
        file_name = '.'.join(file_parts)
        path = os.path.join(dir_name, file_name)

    print 'getting file {}'.format(href)
    r = requests.get(href, stream=True)
    r.raise_for_status()
    with open(path, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
