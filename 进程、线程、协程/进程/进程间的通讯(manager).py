# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 进程间的通讯(manager).py
@time: 2020/3/3 15:54
@author:LDC
'''

from multiprocessing import Process, Manager, current_process


def start(m_dict, m_list):
    pname = current_process().name
    pid = current_process().pid
    print('当前进程是{}_{}'.format(pid, pname))
    print(m_dict)
    m_dict[pid] = pname
    m_list.append(pid)



if __name__ == '__main__':
    manager = Manager()
    m_dict = manager.dict()  # 通过manager生成一个字典
    m_list = manager.list()  # 通过manager生成一个列表
    p_list = []
    for i in range(10):
        p = Process(target=start, args=(m_dict, m_list))
        p.start()
        p_list.append(p)
    for res in p_list:
        res.join()

    print(m_dict)
    print(m_list)
