# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: greenlet创建协程.py
@time: 2020/3/4 23:08
@author:LDC
'''

'''
使用greenlet + switch实现协程调度
'''
from greenlet import greenlet
import time


def func1():
    print("开门走进卫生间")
    time.sleep(3)
    gr2.switch()  # 把CPU执行权交给gr2

    print("飞流直下三千尺")
    time.sleep(3)
    gr2.switch()
    pass


def func2():
    print("一看拖把放旁边")
    time.sleep(3)
    gr1.switch()

    print("疑是银河落九天")
    pass


if __name__ == '__main__':
    gr1 = greenlet(func1)
    gr2 = greenlet(func2)
    gr1.switch()  # 把CPU执行权先给gr1
    pass
