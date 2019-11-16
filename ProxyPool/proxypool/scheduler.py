#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.settings import *


class Schedualer():

    def scheduale_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle:
        :return:
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def scheduale_getter(self, cycle=GETTER_CYCLE):
        """
        定是获取代理
        :param cycle:
        :return:
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def scheduale_api(self):
        """
        开始api
        :return:
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运作')
        if TESTER_ENABLED:
            tester_process = Process(target=self.scheduale_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.scheduale_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheduale_api)
            api_process.start()