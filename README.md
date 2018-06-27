# QProxy 代理池

QProxy 数据主要来自于互联网中的免费代理网站，目前收集了九个站点

运行之后的代理池数量大概在 2000+

### 使用说明

一句话启动
```
QProxyServer().run()
```

修改配置（请参阅配置说明）
```
config = {
    'redis': {'port': 6379, 'password': 'xxx'},
}
server = QProxyServer(config=config)
server.run()
```

### 配置说明

```
BASE_CONFIG = {
    # 是否启用 API 服务器，False 为关闭
    'enable_api_server': True,
    # 爬虫执行周期，单位为秒
    'crawl_cycle': 3600,
    # 校验器执行周期，单位为秒
    'checker_cycle': 10,
    # 爬虫相关配置
    'crawl': {
        # 代理所在国家, 不限制写 None, 限制填入国家名称(如'中国')
        'proxy_country': None,
    },
    # 存储配置
    'redis': {
        # Redis 服务器地址
        'host': '127.0.0.1',
        # Redis 服务器端口
        'port': 6379,
        # Redis 服务器密码
        'password': None,
        # Redis 存储使用的键名
        'redis_key_name': 'proxies',
    },
    # 校验器配置
    'checker': {
        # 校验目标地址, 最好填写爬虫要爬的网址
        'check_url': 'http://www.baidu.com',
        # 代理响应码正确值, 不在该 list 中的响应码不会添加该代理
        'valid_status_code': [200, 302],
        # 批量校验的线程数量
        'batch_check_thread': 10,
        # 代理最大分值，100为最优
        'score_max': 100,
        # 代理最小分值，每校验一次如果没有成功会将该值减1，为 0 时移除该代理
        'score_min': 0,
        # 代理初始化分值
        'score_init': 10,
    },
    'api': {
        # API 服务器地址
        'host': '0.0.0.0',
        # API 服务器端口
        'port': 2589,
        # API 接口访问密码
        'password': 'qproxy'
    }

}
```

上述所有配置需按结构传入构造器函数中

如想关闭 API 服务器

```
config = {
    'enable_api_server': False,
}
server = QProxyServer(config=config)
server.run()
```

如想修改 API 服务器端口

```
config = {
    'api': {'port': 8888},
}
server = QProxyServer(config=config)
server.run()
```
