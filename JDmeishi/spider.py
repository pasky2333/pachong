#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import requests
from requests import RequestException
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from pymongo import MongoClient
from .config import *


client = MongoClient(MONGO_URL)
db = client[MONGO_DB]


# 令window.navigator.webdriver = undefined
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])


browser = webdriver.Chrome(options=option)
browser.maximize_window()
wait = WebDriverWait(browser, 3)


def search():
    try:
        browser.get('https://www.jd.com')
        input = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, '#key'
            )))
        submit = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, '#search > div > div.form > button'
            )))
        input.send_keys(KEYWORD)
        submit.click()
        time.sleep(2)
        slide_down()
        total = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b'
        )))
        count = get_products(1)
        print('已爬取第1页,总计：%s 条' % count)
        return total.text
    except TimeoutException:
        return search()


def next_page(page):
    try:
        global current_url
        current_url = browser.current_url
        input = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input'
        )))
        submit = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a'
            )))
        input.clear()
        input.send_keys(page)
        # element = browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > a')
        # browser.execute_script('arguments[0].click();', element)
        submit.click()
        time.sleep(2)
        slide_down()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page)))
        print('跳转到第%s页' % page)
        count = get_products(page)
        print('已爬取第%s页,总计：%s 条' % (page, count))
    except TimeoutException:
        if browser.current_url == 'https://www.jd.com/':
            browser.get(current_url)
        next_page(page)


def get_products(page, download=False):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList ul li')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_goodsList ul li.gl-item').items()
    count = 0
    for index, item in enumerate(items):
        img = item.find('.p-img img').attr('src')
        if not img:
            img = item.find('.p-img img').attr('data-lazy-img')
        idx = '%s_%s' % (page, index+1)
        product = {
            'index': idx,
            'img': img,
            'price': item.find('.p-price i').text(),
            'title': item.find('.p-name em').text().replace('\n', ''),
            'commit': item.find('.p-commit a').text(),
            'shop': item.find('.p-shop a').text()
        }
        if download:
            download_img(img, idx)
        count += 1
        print(product)
        save_to_mongo(product)
    return count


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功', result)
    except Exception:
        print('存储到MONGODB失败', result)


def slide_down():
    js_down = 'window.scrollTo(0, 5000)'
    browser.execute_script(js_down)
    time.sleep(2)


def download_img(url, index):
    url = 'http:' + url
    print('正在下载图片：', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            save_img(content, index)
    except RequestException:
        print('下载图片失败', url)


def save_img(content, index):
    file_path = '%s/tmp/%s.jpg' % (os.getcwd(), index)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
        print('下载图片成功')


def main():
    try:
        total = int(search())
        for i in range(2, total+1):
            next_page(i)
    except Exception:
        print('出错啦')
    finally:
        browser.close()


if __name__ == '__main__':
    main()