# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 信号量实现线程同步.py
@time: 2020/3/4 22:30
@author:LDC
'''
# python 多线程同步   semaphore
import threading
import time

# 初始化信号量数量...当调用acquire 将数量置为 0, 将阻塞线程等待其他线程调用release() 函数
semaphore = threading.Semaphore(2)


def func():
    if semaphore.acquire():
        for i in range(2):
            print(threading.currentThread().getName() + ' get semaphore')
            time.sleep(1)
        semaphore.release()
        print(threading.currentThread().getName() + ' release semaphore')


if __name__ == '__main__':
    for i in range(4):
        t1 = threading.Thread(target=func)
        t1.start()
