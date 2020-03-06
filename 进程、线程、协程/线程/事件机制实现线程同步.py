# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 事件机制实现线程同步.py
@time: 2020/3/4 22:46
@author:LDC
'''

import logging
import threading
import time


# 打印线程名以及日志信息
logging.basicConfig(level=logging.DEBUG, format="(%(threadName)-10s : %(message)s", )


def wait_for_event_timeout(e, t):
    """Wait t seconds and then timeout"""
    while not e.isSet():
        logging.debug("wait_for_event_timeout starting")
        event_is_set = e.wait(t)  # 阻塞, 等待设置为true
        logging.debug("event set: %s" % event_is_set)
        if event_is_set:
            logging.debug("processing event")
        else:
            logging.debug("doing other work")


e = threading.Event()  # 初始化为false
t2 = threading.Thread(name="nonblock", target=wait_for_event_timeout, args=(e, 2))
t2.start()
logging.debug("Waiting before calling Event.set()")
# time.sleep(7)
e.set()  # 唤醒线程, 同时将event 设置为true
logging.debug("Event is set")