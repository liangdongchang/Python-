# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 多进程.py
@time: 2020/3/3 16:19
@author:LDC
'''
import time
from concurrent import futures
from multiprocessing import current_process


def foo(i):
    pid = current_process().pid
    pname = current_process().name
    time.sleep(3)
    print('hello', '{},{}_{}'.format(i, pid, pname))
    return '{},{}_{}'.format(i, pid, pname)


if __name__ == '__main__':
    i_list = [1, 2, 3, 4, 5]
    with futures.ProcessPoolExecutor(5) as executor:

        res = executor.map(foo, i_list)
        # to_do = [executor.submit(foo, item) for item in i_list]
        # ret = [future.result() for future in futures.as_completed(to_do)]