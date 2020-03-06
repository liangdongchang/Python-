# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 创建线程(常用).py
@time: 2020/3/3 16:49
@author:LDC
'''

import threading
import time

'''直接调用'''


def foo(name):
    time.sleep(name)
    # 获取当前线程名称与标志号
    print(threading.currentThread().name, threading.currentThread().ident)
    print("Hello %s" % name)



if __name__ == "__main__":
    t_list = []
    for i in range(2):
        t = threading.Thread(target=foo, args=(i+2,), name='t_{}'.format(i))  # 生成线程实例
        # t.setDaemon(True)  # True表示子线程设置为守护线程,主线程死去，子线程也跟着死去，不管是否执行完
        # t.setDaemon(False)  # False表示子线程设置为非守护线程,主线程死去，子线程依然在执行
        t_list.append(t)
        t.start()

    # for t in t_list:
    #     t.join()  # 等待子线程执行完，
    #     print(t.getName())  # 获取线程名

