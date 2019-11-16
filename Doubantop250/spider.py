#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<li>.*?class="">(.*?)</em>.*?<img.*?src="(.*?)".*?'
                         +'title">(.*?)</span>.*?主演:(.*?)/.*?'
                         +'(\d+).*?average">(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'img': item[1],
            'title': item[2],
            'actor': item[3],
            'time': item[4],
            'score': item[5]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://movie.douban.com/top250?start=%s&filter=' % offset
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    # for i in range(10):
    #     main(i*25)
    pool = Pool()
    pool.map(main, [i*25 for i in range(10)])