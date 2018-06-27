#!/usr/bin/env python
# encoding: utf-8

"""
@file: QProxyCrawler.py
@time: 2018/6/26 15:07
@desc: 获取代理数据的爬虫
@author: hongquanpro@126.com
"""

import requests
import time

from collections import Generator, Iterator
from pyquery import PyQuery
from QProxy.QProxyCenter import QProxyCenter


class CrawlerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # 使用元类获取代理爬虫中所有的爬虫函数, 然后批量自动调用
        attrs['__crawlers__'] = []
        for k, v in attrs.items():
            if callable(v) and 'crawl_' in k:
                attrs['__crawlers__'].append(k)
        return type.__new__(cls, name, bases, attrs)


class QProxyCrawler(object, metaclass=CrawlerMetaclass):
    def __init__(self, config=None):
        if config is None:
            raise ValueError('Config param is None in the QProxyCrawler.')
            exit()
        self.config = config
        self.db = QProxyCenter(config=config)
        pass

    def crawl_goubanjia(self):
        url = 'http://www.goubanjia.com'
        print('crawl %s' % url)
        html = self.get_page_source(url)
        if html:
            doc = PyQuery(html)
            data = doc('td.ip').items()
            for td in data:
                td.find('p').remove()
                yield td.text().replace(' ', '').replace('\n', '')

    def crawl_66ip(self):
        base = 'http://www.66ip.cn/{}.html'
        urls = [base.format(x + 1) for x in range(10)]
        for url in urls:
            print('crawl %s' % url)
            html = self.get_page_source(url)
            if html:
                doc = PyQuery(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    yield '%s:%s' % (tr.find('td:nth-child(1)').text(), tr.find('td:nth-child(2)').text())

    def crawl_ip3366(self):
        base = 'http://www.ip3366.net/free/?page={}'
        urls = [base.format(x + 1) for x in range(10)]
        for url in urls:
            print('crawl %s' % url)
            html = self.get_page_source(url)
            if html:
                doc = PyQuery(html)
                trs = doc('.table tr:gt(0)').items()
                for tr in trs:
                    yield '%s:%s' % (tr.find('td:nth-child(1)').text(), tr.find('td:nth-child(2)').text())

    def crawl_kuaidaili(self):
        base = 'http://www.kuaidaili.com/free/inha/{}'
        urls = [base.format(x + 1) for x in range(10)]
        for url in urls:
            print('crawl %s' % url)
            html = self.get_page_source(url)
            # 如果不加延时容易返回错误
            # time.sleep(1)
            if html:
                doc = PyQuery(html)
                trs = doc('.table tbody tr').items()
                for tr in trs:
                    yield '%s:%s' % (tr.find('td[data-title="IP"]').text(), tr.find('td[data-title="PORT"]').text())

    def crawl_xicidaili(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': ('_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTVmNGNkODFlN2Y5NWQ0Y2VjZjBjMDY2MT'
                       'U1NzZmZjk4BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUNVaDZISEpyUFk2SjNXMDNFbkdaZXJOZ3R0ZFl2T1VI'
                       'aUZLeEdkT2VqVUk9BjsARg%3D%3D--7b4f92a270609a3fe2220604179b774a0884418f; Hm_lvt_0cf76c7'
                       '7469e965d2957f0553e6ecf59=1530017168; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1530017699'),
            'Host': 'www.xicidaili.com',
            'Referer': 'http://www.xicidaili.com/nn/',
            'Upgrade-Insecure-Requests': '1',
        }
        base = 'http://www.xicidaili.com/nn/{}'
        urls = [base.format(x + 1) for x in range(10)]
        for url in urls:
            print('crawl %s' % url)
            html = self.get_page_source(url, options=headers)
            if html:
                doc = PyQuery(html)
                trs = doc('#ip_list tr:gt(0)').items()
                for tr in trs:
                    yield '%s:%s' % (tr.find('td:nth-child(2)').text(), tr.find('td:nth-child(3)').text())

    def crawl_iphai(self):
        base = 'http://www.iphai.com/free/ng'
        print('crawl %s' % base)
        html = self.get_page_source(base)
        if html:
            doc = PyQuery(html)
            trs = doc('.table tr:gt(0)').items()
            for tr in trs:
                yield '%s:%s' % (tr.find('td:nth-child(1)').text(), tr.find('td:nth-child(2)').text())

    def crawl_89ip(self):
        base = 'http://www.89ip.cn/index_{}.html'
        urls = [base.format(x + 1) for x in range(10)]
        for url in urls:
            print('crawl %s' % url)
            html = self.get_page_source(url)
            if html:
                doc = PyQuery(html)
                trs = doc('.layui-table tr:gt(0)').items()
                for tr in trs:
                    yield '%s:%s' % (tr.find('td:nth-child(1)').text(), tr.find('td:nth-child(2)').text())

    def crawl_data5u(self):
        base = 'http://www.data5u.com/free/gngn/index.shtml'
        print('crawl %s' % base)
        html = self.get_page_source(base)
        if html:
            doc = PyQuery(html)
            uls = doc('.wlist ul:gt(0)').items()
            for ul in uls:
                yield '%s:%s' % (ul.find('span:nth-child(1)').text(), ul.find('span:nth-child(2)').text())

    def crawl_ihuan(self):
        base = 'https://ip.ihuan.me/address/5Lit5Zu9.html'
        print('crawl %s' % base)
        html = self.get_page_source(base)
        if html:
            doc = PyQuery(html)
            trs = doc('.table tr:gt(0)').items()
            for tr in trs:
                yield '%s:%s' % (tr.find('td:nth-child(1)').text(), tr.find('td:nth-child(2)').text())

    def get_page_source(self, url, options={}):
        base_headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'),
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }
        try:
            response = requests.get(url=url, headers=dict(base_headers, **options))
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                return response.text
        except requests.ConnectionError as e:
            print('Fetch %s error' % url, e.args)
            return None

    def run(self):
        print('total crawl method %s' % len(self.__crawlers__))
        for func in self.__crawlers__:
            method = eval('self.%s()' % func)
            if isinstance(method, (Generator, Iterator)):
                for proxy in method:
                    try:
                        country = self.config['crawl']['proxy_country']
                        if country is not None:
                            url = ('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % (proxy.split(':')[0]))
                            response = requests.get(url=url)
                            if response.status_code == 200:
                                obj = response.json()
                                if obj.get('data').get('country', None) == country:
                                    self.db.add(proxy)
                        else:
                            self.db.add(proxy)
                    except requests.ConnectionError as e:
                        pass
            else:
                print('%s not generator. It is %s' % (func, type(method)))
