#! /usr/bin/env python

import os
from time import time

from lxml import html
import requests
import argparse

parser = argparse.ArgumentParser(description='Download images from Bing Search')
parser.add_argument('search_for', help='search for these terms', nargs='+')
parser.add_argument('-d', '--dir_name', help='Target director name')

args = parser.parse_args()

BASE_URL = 'http://www.bing.com/images/search'
BASE_PAYLOAD = {
    'qft': '+filterui:imagesize-large',
}


def main(search_for, dir_name=None):
    if not dir_name:
        dir_name = search_for

    mkdir(dir_name)
    response_text = make_request(search_for)
    for href in parse_response(response_text):
        store_image_href(href, dir_name)


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

if __name__ == '__main__':
    main(' '.join(args.search_for), args.dir_name)
