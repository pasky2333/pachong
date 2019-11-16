#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests


def get_proxy():
    r = requests.get('http://127.0.0.1:5556/random')
    return 'http://' + r.text


def crawl(url, proxy):
    proxies = {'http:': proxy}
    r = requests.get(url, proxies=proxies)
    return r.text


def main():
    proxy = get_proxy()
    html = crawl('http://python.org/', proxy)
    print(html)


if __name__ == '__main__':
    main()