# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: monkey_patch.py
@time: 2020/3/4 23:40
@author:LDC
'''

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


def get_page_text(url, order):
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


def gevent_joinall():
    # spawn是异步提交任务
    gevent.joinall([
        gevent.spawn(get_page_text, "http://www.sina.com", order=1),
        gevent.spawn(get_page_text, "http://www.qq.com", order=2),
        gevent.spawn(get_page_text, "http://www.baidu.com", order=3),
        gevent.spawn(get_page_text, "http://www.163.com", order=4),
        gevent.spawn(get_page_text, "http://www.4399.com", order=5),
        gevent.spawn(get_page_text, "http://www.sohu.com", order=6),
        gevent.spawn(get_page_text, "http://www.youku.com", order=7),
    ])
    g_iqiyi = gevent.spawn(get_page_text, "http://www.iqiyi.com", order=8)
    g_iqiyi.join()
    # #拿到任务的返回值
    print('获取返回值', g_iqiyi.value)


if __name__ == '__main__':
    #
    start = time.time()
    time.clock()
    gevent_joinall()
    end = time.time()
    print("over，耗时%d秒" % (end - start))
    print(time.clock())
