#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pandas as pd

client = MongoClient('localhost')
db = client['lol_discount']

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

browser = webdriver.Chrome(options=option)
browser.maximize_window()
wait = WebDriverWait(browser, 3)


def first_page():
    try:
        browser.get('https://daoju.qq.com/mall/tao.shtml')
        lol_button = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '#biz_wrapper a[biz="lol"]'
        )))
        lol_button.click()
        time.sleep(2)
        get_product()
    except TimeoutException:
        first_page()


def next_page():
    try:
        next_p = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '#page_wrapper > span.p_next > a'
        )))
        next_p.click()
        time.sleep(2)
        get_product()
    except TimeoutException:
        next_page()


def get_product():
    wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, '#tao_wrapper > dl'
    )))
    html = browser.page_source
    doc = pq(html)
    items = doc('#tao_wrapper dl').items()
    for item in items:
        discount = item.find('dd.bg_sp.zj').text()
        if discount:
            url = item.find('a.click_stream').attr('href')
            name = item.find('a.click_stream').text().replace('立即抢购', '')
            price = item.find('p.red b').text()
            used_price = item.find('.red span > s').text()
            lol_item = {
                'url': url,
                'name': name,
                'price': price,
                'used_price': used_price,
                'discount': discount
            }
            save_to_mongo(lol_item)


def save_to_mongo(item):
    try:
        db['lol_discount'].insert(item)
        print('保存到MongoDB成功', item)
    except:
        print('保存到MongoDB失败', item)


def to_csv():
    lis = []
    for item in db['lol_discount'].find():
        lis.append(item)
    df = pd.DataFrame(lis)
    df.pop('_id')
    df.name = df.name.apply(lambda x: x.strip())
    df.url = df.url.apply(lambda x: 'https://daoju.qq.com' + x)
    df.to_csv(r'c:/Users/79266/Desktop/lol_discount.csv', index=0, encoding='utf_8_sig')


def main(toCsv=False):
    first_page()
    for i in range(68):
        next_page()
    if toCsv:
        to_csv()


if __name__ == '__main__':
    main()