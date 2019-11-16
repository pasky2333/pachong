#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import time
from hashlib import md5
from multiprocessing import Pool
from urllib.parse import urlencode
import pymongo
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
from config import *


def get_page_inde(offset, keyword):
    data = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time())
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)
    try:
        response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
        if response.status_code == 200:
            print('请求索引页成功')
            return response.content.decode()
        else:
            print('请求索引页失败')
            return None
    except RequestException:
        print('请求出错')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        if data.get('data'):
            for item in data.get('data'):
                if 'article_url' in item.keys():
                    url = item.get('article_url')
                    yield url
        else:
            print('获取data失败')


def get_page_detail(url):
    try:
        response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
        if response.status_code == 200:
            content = response.content.decode()
            print('请求详情页成功')
            return content
        else:
            print('请求详情页失败')
            return None
    except RequestException:
        print('请求详情页出错')
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    image_pattern = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
    result = re.search(image_pattern, html)
    if result:
        print('解析json成功')
        ret = result.group(1)
        # {\"count\":4,\"sub_images\":[{\"url\":\"http:\\\u002F\\\u002Fp9.pstatp.com\\\u002Fo
        ret = ret.replace('\\', '')  # 把\替换为空字符
        ret = ret.replace('u002F', '/') # 把u002F替换成/
        data = json.loads(ret)
        if data and 'sub_images' in data.keys():
            print('获取图片url成功')
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for img in images:
                download(img)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def download(url):
    print('正在下载图片', url)
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            content = response.content
            save_img(content)
        return None
    except RequestException:
        print('下载失败')
        return None


def save_img(content):
    file_path = '{0}/{1}/{2}.{3}'.format(os.getcwd(), 'tmp', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)


def save(result):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(ret, ensure_ascii=False) + '\n')


client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功')
        return True
    else:
        return False


def main(offset):
    html = get_page_inde(offset, KEYWORD)
    if html:
        for url in parse_page_index(html):
            content = get_page_detail(url)
            if content:
                ret = parse_page_detail(content, url)
                if ret:
                    save_to_mongo(ret)


if __name__ == '__main__':
    pool = Pool()
    groups = [i * 20 for i in range(START_PAGE, END_PAGE+1)]
    pool.map(main, groups)