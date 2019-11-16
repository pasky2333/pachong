#!/usr/bin/env python
# -*- coding:utf-8 -*-
cookies = {
    'Cookie': 'csrftoken=7ad1bc74712bd2dac3820aa92af472b9; tt_webid=6739706978094614023; tt_webid=6739706978094614023; s_v_web_id=a3b685213fdcd19209b0e4f2b44d061c; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=cb7u7gmjy1573636959780'
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
}
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

START_PAGE = 5
END_PAGE = 10

MONGO_URL = 'localhost'
MONGO_DB = 'toutiao'
MONGO_TABLE = 'toutiao'

KEYWORD = '猫'