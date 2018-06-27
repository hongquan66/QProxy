#!/usr/bin/env python
# encoding: utf-8

"""
@file: QProxyServer.py
@time: 2018/6/26 14:42
@desc: 主程序
@author: hongquanpro@126.com
"""

import time
import collections

from multiprocessing import Process
from QProxy.QProxyCrawler import QProxyCrawler
from QProxy.QProxyChecker import QProxyChecker
from QProxy.QProxyAPI import QProxyAPI

# 默认配置
BASE_CONFIG = {
    'enable_api_server': True,
    'crawl_cycle': 3600,
    'checker_cycle': 10,
    'crawl': {
        'proxy_pool_max_count': 50000,
        'proxy_country': None,
    },
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'password': None,
        'redis_key_name': 'proxies',
    },
    'checker': {
        'check_url': 'http://www.baidu.com',
        'valid_status_code': [200, 302],
        'batch_check_thread': 10,
        'score_max': 100,
        'score_min': 0,
        'score_init': 10,
    },
    'api': {
        'host': '0.0.0.0',
        'port': 2589,
        'password': 'qproxy'
    }

}


class QProxyServer:
    def __init__(self, config={}):
        self.config = self.merge_dict(BASE_CONFIG, config)
        print(self.config)

    def merge_dict(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                r = self.merge_dict(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]
        return d

    def schedule_crawler(self):
        crawler = QProxyCrawler(config=self.config)
        print('QProxyCrawler is running')
        while True:
            crawler.run()
            time.sleep(self.config['crawl_cycle'])

    def schedule_checker(self):
        checker = QProxyChecker(config=self.config)
        print('QProxyChecker is running')
        while True:
            checker.run()
            time.sleep(self.config['checker_cycle'])

    def schedule_api(self):
        api_server = QProxyAPI(config=self.config)
        api_server.run()
        print('QProxyAPI Server is running at http://%s:%s' % (self.config['api']['host'], self.config['api']['port']))

    def run(self):
        print('QProxy is running')

        crawl_pro = Process(target=self.schedule_crawler)
        crawl_pro.start()

        check_pro = Process(target=self.schedule_checker)
        check_pro.start()

        if self.config['enable_api_server']:
            api_pro = Process(target=self.schedule_api)
            api_pro.start()


if __name__ == '__main__':
    config = {
        'redis': {'port': 6379, 'password': 'xxx'},
    }
    server = QProxyServer(config=config)
    server.run()
