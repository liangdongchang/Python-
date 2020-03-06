# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 互斥锁.py
@time: 2020/3/3 21:08
@author:LDC
'''

import threading

lock = threading.Lock()
money = 0

def add_money():
    global money
    with lock:
        for i in range(10000000):
            money += 1

if __name__ == '__main__':
    add_money()
    add_money()
    print('调用两次函数money实际值为：', money)
    money = 0
    t_list = []
    for i in range(2):
        t = threading.Thread(target=add_money)
        t.start()
        t_list.append(t)
    for t in t_list:
        t.join()
    print('使用线程后money实际值为：', money)