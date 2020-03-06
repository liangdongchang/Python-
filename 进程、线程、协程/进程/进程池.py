# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 进程池.py
@time: 2020/3/3 16:05
@author:LDC
'''

from multiprocessing import Pool, current_process
import time


def Foo(i):
    pid = current_process().pid
    pname = current_process().name
    time.sleep(1)
    print('hello','{},{}_{}'.format(i, pid, pname))
    return '{},{}_{}'.format(i, pid, pname)


def Bar(arg):
    print('number::', arg)


if __name__ == "__main__":
    pool = Pool(3)  # 定义一个进程池，里面有3个进程
    for i in range(10):
        pool.apply_async(func=Foo, args=(i,), callback=Bar)
        # pool.apply(func=Foo, args=(i,))

    pool.close()  # 关闭进程池
    pool.join()  # 进程池中进程执行完毕后再关闭,(必须先close在join)
