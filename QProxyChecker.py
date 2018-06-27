#!/usr/bin/env python
# encoding: utf-8

"""
@file: QProxyChecker.py
@time: 2018/6/26 15:08
@desc: 代理校验器
@author: hongquanpro@126.com
"""

import aiohttp
import asyncio
import sys
import time

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from QProxy.QProxyCenter import QProxyCenter


class QProxyChecker:
    def __init__(self, config=None):
        if config is None:
            raise ValueError('Config param is None in the QProxyChecker.')
            exit()
        self.db = QProxyCenter(config=config)
        self.target = config['checker']['check_url']
        self.status = config['checker']['valid_status_code']
        self.thread_count = config['checker']['batch_check_thread']

    async def check_proxy(self, proxy):
        """
        测试代理
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                print('check proxy %s' % proxy)
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                async with session.get(url=self.target, proxy=('http://' + proxy),
                                       timeout=10, allow_redirects=False) as response:
                    if response.status in self.status:
                        self.db.reset(proxy)
                        print('The proxy %s is valid' % proxy)
                    else:
                        self.db.reduce(proxy)
                        print('The response code(%s) is invalid. Proxy = %s' % (response.status, proxy))
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.db.reduce(proxy)
                # print('Connect %s failed' % proxy)

    def run(self):
        try:
            count = self.db.get_count()
            print('There are %d proxy in the pool' % count)
            for i in range(0, count, self.thread_count):
                start = i
                stop = min(i + self.thread_count, count)
                test_proxies = self.db.get_batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.check_proxy(proxy=proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('QProxyChecker running error', e.args)
