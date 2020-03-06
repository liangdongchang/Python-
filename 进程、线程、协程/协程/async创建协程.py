# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: async创建协程.py
@time: 2020/3/6 12:03
@author:LDC
'''

import asyncio
from functools import partial

'''
使用gevent +　monkey.patch_all()自动调度网络IO协程
'''
import sys
import requests
import time

sys.setrecursionlimit(1000000)  # 增加递归深度


async def get_page_text(url, order):
    # 使用async创建一个可中断的异步函数
    print('No{}请求'.format(order))
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        }
        # 利用BaseEventLoop.run_in_executor()可以在coroutine中执行第三方的命令，例如requests.get()
        # 第三方命令的参数与关键字利用functools.partial传入
        future = asyncio.get_event_loop().run_in_executor(None, partial(requests.get, url, headers=headers))
        resp = await future

        html = resp.text
        html_len = len(html)
        print("%s成功返回：长度为%d" % (url, html_len))
        return html_len
    except Exception as e:
        print('{}发生错误，{}'.format(url, e))
        return 0


# 异步函数执行完后回调函数
def callback(future):  # 这里默认传入一个future对象
    print(future.result())


# 异步函数执行完后回调函数,可接收多个参数
def callback_2(url, future):  # 传入值的时候，future必须在最后一个
    print(url, future.result())


def async_run():
    # 使用async创建协程
    urls = ["http://www.youku.com", "http://www.sina.com", "http://www.qq.com", "http://www.baidu.com",
            "http://www.163.com", "http://www.4399.com", "http://www.sohu.com",

            ]
    loop_task = []
    loop = asyncio.get_event_loop()
    for i in range(len(urls)):
        t = asyncio.ensure_future(get_page_text(urls[i], i + 1))
        # t = loop.create_task(task(urls[i], i + 1))
        t.add_done_callback(callback)
        # t.add_done_callback(partial(callback_2, urls[i]))
        loop_task.append(t)
    print('等待所有async函数执行完成')
    start = time.time()
    loop.run_until_complete(asyncio.wait(loop_task))
    loop.close()
    end = time.time()
    print("over，耗时%d秒" % (end - start))


if __name__ == '__main__':
    async_run()
