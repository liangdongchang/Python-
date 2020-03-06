# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 创建进程.py
@time: 2020/3/3 12:22
@author:LDC
'''

import multiprocessing
import time


def func(arg):
    pname = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    print("当前进程ID=%d,name=%s" % (pid, pname))

    for i in range(5):
        print(pname, pid, arg)
        time.sleep(1)

    pass


if __name__ == "__main__":
    pname = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    print("当前进程ID=%d,name=%s" % (pid, pname))

    p = multiprocessing.Process(target=func, name='我是子进程', args=("hello",))
    p.daemon = True  # 设为【守护进程】（随主进程的结束而结束）
    p.start()

    while True:
        print("子进程是否活着？", p.is_alive())
        if not p.is_alive():
            break
        time.sleep(1)
        pass

    print("main over")
