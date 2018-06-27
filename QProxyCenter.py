#!/usr/bin/env python
# encoding: utf-8

"""
@file: QProxyCenter.py
@time: 2018/6/26 15:06
@desc: 代理池的数据中心
@author: hongquanpro@126.com
"""

import redis
import re
from random import choice

PROXY_KEY = 'proxies'


def check_proxy_format(proxy):
    # 数据格式校验
    if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
        print('代理格式错误 [%s]' % proxy)
        return


class QProxyCenter:
    def __init__(self, config=None):
        if config is None:
            raise ValueError('Config param is None in the QProxyCenter.')
            exit()
        self.db = redis.StrictRedis(host=config['redis']['host'], port=config['redis']['port'],
                                    password=config['redis']['password'], decode_responses=True)
        self.init_score = config['checker']['score_init']
        self.max_score = config['checker']['score_max']
        self.min_score = config['checker']['score_min']

        global PROXY_KEY
        PROXY_KEY = config['redis']['redis_key_name']
        print('PROXY_KEY = %s' % PROXY_KEY)

    def add(self, proxy):
        """
        添加新的代理到池中， 初始化分值为最高分
        :param proxy: 代理，格式如 IP:PORT
        :return:
        """
        check_proxy_format(proxy)
        if not self.db.zscore(PROXY_KEY, proxy):
            return self.db.zadd(PROXY_KEY, self.init_score, proxy)

    def reduce(self, proxy):
        """
        如果发现代理出错，降低一次权重，一旦发现权重小于最低分时，则将代理从池中移除
        :param proxy:
        :return:
        """
        check_proxy_format(proxy)
        score = self.db.zscore(PROXY_KEY, proxy)
        if score and score > self.min_score:
            return self.db.zincrby(PROXY_KEY, proxy, -1)
        else:
            print('Proxy %s score is %d, removed!' % (proxy, score))
            return self.db.zrem(PROXY_KEY, proxy)

    def reset(self, proxy):
        """
        如果发现代理可用，则重置代理分数为最高分
        :param proxy:
        :return:
        """
        return self.db.zadd(PROXY_KEY, self.max_score, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy:
        :return:
        """
        return not self.db.zscore(PROXY_KEY, proxy) is None

    def get_best(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(PROXY_KEY, self.max_score, self.max_score)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(PROXY_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                return None

    def get_count(self):
        return self.db.zcard(PROXY_KEY)

    def get_all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(PROXY_KEY, self.min_score, self.max_score)

    def get_batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(PROXY_KEY, start, stop - 1)
