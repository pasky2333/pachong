#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from random import choice
import redis
from proxypool.error import ProxyEmptyError
from proxypool.settings import *


class RedisClient(object):

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        """
        self.db = redis.Redis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为初始化分数
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        # 代理不符合规范则丢弃
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
        # 如果REDIS_KEY表中不存在当前proxy，就存储
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        # zrangebyscore(key, min_score, max_score)通过分数排名
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            # zrevrange(key, start, end)从大到小排名
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise ProxyEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，小于最小值删除
        :param proxy:
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            # zincrby(key, amount, value) 修改分数
            # key: redis_key
            # amount: 修改的分数
            # value: 键名
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return self.db.zscore(REDIS_KEY, proxy)

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, end):
        """
        批量获取
        :param start: 开始索引
        :param end: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, end - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(0, 10)
    print(result)