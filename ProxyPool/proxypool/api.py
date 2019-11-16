#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, g
from proxypool.db import RedisClient
from proxypool.settings import *


__all__ = ['app']

app = Flask(__name__)


# g对象用于存储
def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    随机返回一个proxy
    :return: 随机proxy
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_count():
    """
    返回代理池中代理数量
    :return: 代理数量
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run(API_HOST, API_PORT)