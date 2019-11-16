#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import time
from proxypool.utils import get_page, get_random_page
from pyquery import PyQuery as pq
from proxypool.settings import PAGE_COUNT


class ProxyMetaClass(type):

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for key, value in attrs.items():
            if 'crawl_' in key:
                attrs['__CrawlFunc__'].append(key)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):

    def get_proxies(self, callback):
        proxies = []
        # eval()函数用来执行一个字符串表达式，并返回表达式的值
        # >>> eval('3 * 7')
        # 21
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=PAGE_COUNT):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in get_random_page(page_count)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_ip3366(self, page_count=PAGE_COUNT):
        """
        抓取ip3366
        :param page_count:
        :return:
        """
        start_url = 'http://www.ip3366.net/free/?stype=1&page={}'
        urls = [start_url.format(page) for page in get_random_page(page_count)]
        for url in urls:
            html = get_page(url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格， 起到执行作用
            re_ip_address = ip_address.findall(html)
            for ip, port in re_ip_address:
                yield ':'.join([ip, port])

    def crawl_kuaidaili(self, page_count=PAGE_COUNT):
        """
        抓取kuaidaili
        :param page_count:
        :return:
        """
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in get_random_page(page_count)]
        for url in urls:
            html = get_page(url)
            time.sleep(1)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>.*?"PORT">(.*?)</td>', re.S)
                re_ip_address = ip_address.findall(html)
                for ip, port in re_ip_address:
                    yield ':'.join([ip, port])

    def crawl_xicidaili(self, page_count=PAGE_COUNT):
        """
        抓取xicidaili
        :param page_count:
        :return:
        """
        start_url = 'https://www.xicidaili.com/nn/{}'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
            'Host': 'www.xicidaili.com',
            'Referer': 'http://www.xicidaili.com/nn/3',
            'Upgrade-Insecure-Requests': '1',
        }
        urls = [start_url.format(page) for page in get_random_page(page_count)]
        for url in urls:
            html = get_page(url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    ip_address = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    port_address = re.compile('<td>(\d+)</td>')
                    re_ip = ip_address.findall(tr)
                    re_port = port_address.findall(tr)
                    for ip, port in zip(re_ip, re_port):
                        yield ':'.join([ip, port])

    def crawl_iphai(self):
        start_url = 'http://www.iphai.com'
        html = get_page(start_url)
        if html:
            find_trs = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_trs.findall(html)
            for tr in trs:
                ip_address = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                port_address = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_ip = ip_address.findall(tr)
                re_port = port_address.findall(tr)
                for ip, port in zip(re_ip, re_port):
                    yield ':'.join([ip, port])


if __name__ == '__main__':
    crawler = Crawler()
    for ip in crawler.crawl_iphai():
        print(ip)