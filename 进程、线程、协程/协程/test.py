# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: monkey_patch.py
@time: 2020/3/4 23:40
@author:LDC
'''
import asyncio

'''
使用gevent +　monkey.patch_all()自动调度网络IO协程
'''
from gevent import monkey;

monkey.patch_all()  # 将【标准库-阻塞IO实现】替换为【gevent-非阻塞IO实现，即遇到需要等待的IO会自动切换到其它协程
import sys
import gevent
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
        resp = requests.get(url, headers=headers)  # 发起网络请求，返回需要时间——阻塞IO

        html = resp.text
        html_len = len(html)
        print("%s成功返回：长度为%d" % (url, html_len))
        return html_len
    except Exception as e:
        print('{}发生错误，{}'.format(url, e))
        return 0


async def task(url, order):
    # 创建一个异步任务，遇到IO阻塞就把任务函数挂起
    return await get_page_text(url, order)

def callback(future):
    print(future)
def async_run():
    # 使用async创建协程
    urls = ["http://www.sina.com", "http://www.qq.com", "http://www.baidu.com",
            "http://www.163.com", "http://www.4399.com", "http://www.sohu.com",
            "http://www.youku.com",
            ]
    loop_task = []
    loop = asyncio.get_event_loop()
    for i in range(len(urls)):
        t = loop.create_task(task(urls[i], i + 1))
        t.add_done_callback(callback)
        loop_task.append(t)

    loop.run_until_complete(asyncio.wait(loop_task))
    loop.close()


if __name__ == '__main__':
    start = time.time()
    time.clock()
    async_run()
    end = time.time()
    print("over，耗时%d秒" % (end - start))
    print(time.clock())
