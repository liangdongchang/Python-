# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: async_await.py
@time: 2020/3/5 23:15
@author:LDC
'''
from gevent import monkey;

monkey.patch_all()
import gevent

import asyncio
from functools import wraps, partial
import time

import requests


# 定义一个查看函数执行时间的装饰器
def func_use_time(func):
    @wraps(func)
    def inside(*arg, **kwargs):
        start = time.clock()
        res = func(*arg, **kwargs)
        print('***************执行时间*****************', time.clock() - start)
        return res

    return inside


def get_page_text(url):
    # 爬取网站
    print(url)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        }
        resp = requests.get(url, headers=headers)  # 发起网络请求，返回需要时间——阻塞IO

        html = resp.text
        return html
    except Exception as e:
        print('{}发生错误，{}'.format(url, e))
        return ''


class Narmal():
    # 正常爬取
    def __init__(self, urls):
        self.urls = urls
        self.res_dict = {}

    @func_use_time
    def run(self):
        for url in self.urls:
            res = get_page_text(url)
            self.res_dict[url] = len(res)
        print('串行获取结果', self.res_dict)


class UseAsyncio():
    # 使用async实现协程并发
    def __init__(self, urls):
        self.urls = urls
        self.res_dict = {}

    # 定义一个异步函数，，执行爬取任务
    async def task(self, url):
        print(url)
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
            }
            # 利用BaseEventLoop.run_in_executor()可以在coroutine中执行第三方的命令，例如requests.get()
            # 第三方命令的参数与关键字利用functools.partial传入
            future = asyncio.get_event_loop().run_in_executor(None, partial(requests.get, url, headers=headers))
            resp = await future
            html = resp.text
            self.res_dict[url] = len(html)
            return html
        except Exception as e:
            print('{}发生错误，{}'.format(url, e))
            return ''

    @func_use_time
    def run(self):
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(self.task(url)) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        # 获取async结果
        # for task in tasks:
        #     print(task.result())
        print('async获取结果', self.res_dict)


class UseGevent():
    # 使用Gevent实现协程并发
    def __init__(self, urls):
        self.urls = urls
        self.res_dict = {}

    def task(self, url):
        res = get_page_text(url)
        self.res_dict[url] = len(res)

    @func_use_time
    def run(self):
        gevent.joinall([gevent.spawn(self.task, url) for url in self.urls])
        print(self.res_dict)


if __name__ == '__main__':
    urls = ["http://www.sina.com", "http://www.qq.com", "http://www.baidu.com",
            "http://www.163.com", "http://www.4399.com", "http://www.sohu.com",
            "http://www.youku.com",
            ]
    print("使用正常爬取方式，即串行")
    Narmal(urls).run()
    print("使用Asyncio爬取方式，async实现协程并发")
    UseAsyncio(urls).run()
    print("使用Gevent爬取方式，实现协程并发")
    UseGevent(urls).run()
