#!/usr/bin/env python
# encoding: utf-8

"""
@file: QProxyAPI.py
@time: 2018/6/26 15:08
@desc: 代理数据接口服务器
@author: hongquanpro@126.com
"""

from QProxy.QProxyCenter import QProxyCenter
from flask import Flask, g, request

CONFIG = {}


class QProxyAPI:

    def __init__(self, config=None):
        if config is None:
            raise ValueError('Config param is None in the QProxyAPI.')
            exit()
        self.host = config['api']['host']
        self.port = config['api']['port']
        self.password = config['api']['password']
        global CONFIG
        CONFIG = config

    def run(self):
        print('API: http://%s:%d/proxy?p=%s' % (self.host, self.port, self.password))
        print('API: http://%s:%d/count?p=%s' % (self.host, self.port, self.password))
        app.run(host=self.host, port=self.port)


__all__ = ['app']
app = Flask(import_name=__name__)


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = QProxyCenter(config=CONFIG)
        print('init db property')
    return db


@app.route('/proxy')
def get_proxy():
    if request.args.get('p') == CONFIG['api']['password']:
        return get_db().get_best()
    else:
        return 'localhost:2589'


@app.route('/count')
def get_count():
    if request.args.get('p') == CONFIG['api']['password']:
        return str(get_db().get_count())
    else:
        return '0'
