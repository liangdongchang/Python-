# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 递归锁.py
@time: 2020/3/3 22:16
@author:LDC
'''

import threading
import time

count_list = [0, 0]
lock = threading.RLock()


def change_0():
    global count_list
    with lock:
        tmp = count_list[0]
        time.sleep(0.001)
        count_list[0] = tmp + 1
        time.sleep(2)
        print("Done. count_list[0]:%s" % count_list[0])


def change_1():
    global count_list
    with lock:
        tmp = count_list[1]
        time.sleep(0.001)
        count_list[1] = tmp + 1
        time.sleep(2)
        print("Done. count_list[1]:%s" % count_list[1])


def change():
    with lock:
        change_0()
        time.sleep(0.001)
        change_1()


def verify(sub):
    global count_list
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=sub, args=())
        t.start()
        thread_list.append(t)
    for j in thread_list:
        j.join()
    print(count_list)


if __name__ == "__main__":
    verify(change)
