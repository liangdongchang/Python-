# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 进程间的通讯.py
@time: 2020/3/3 15:13
@author:LDC
'''

from multiprocessing import Process, Queue, current_process

def start(q):
    pname = current_process().name
    pid = current_process().pid
    print('当前进程是{}_{}'.format(pid, pname))
    # 从队列中取出数据,先判断队列 是否为空
    if not q.empty():
        print(q.get())
    # 存数据进队列
    q.put('hello from {}_{}'.format(pid, pname))


if __name__ == '__main__':
    q = Queue()
    p_list = []
    for i in range(0, 2):
        p = Process(target=start, args=(q,))
        p.start()
        p_list.append(p)
    # 确保所有进程执行完
    for p in p_list:
        p.join()
