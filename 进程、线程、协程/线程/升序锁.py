# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 升序锁.py
@time: 2020/3/3 22:39
@author:LDC
'''

import threading
import time
from contextlib import contextmanager

thread_local = threading.local()


@contextmanager
def acquire(*locks):
    # sort locks by object identifier
    # 根据对象标识符对锁进行排序
    locks = sorted(locks, key=lambda x: id(x))

    # make sure lock order of previously acquired locks is not violated
    # 确保没有违反先前获取的锁的顺序
    acquired = getattr(thread_local, 'acquired', [])
    if acquired and (max(id(lock) for lock in acquired) >= id(locks[0])):
        raise RuntimeError('Lock Order Violation')

    # Acquire all the locks
    # 获取所有锁
    acquired.extend(locks)
    thread_local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]


class Account(object):
    def __init__(self, name, balance, lock):
        self.name = name
        self.balance = balance
        self.lock = lock

    def withdraw(self, amount):
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount


def transfer(from_account, to_account, amount):
    print("%s transfer..." % amount)
    with acquire(from_account.lock, to_account.lock):
        from_account.withdraw(amount)
        time.sleep(1)
        to_account.deposit(amount)
    print("%s transfer... %s:%s ,%s: %s" % (
    amount, from_account.name, from_account.balance, to_account.name, to_account.balance))
    print("transfer finish")


if __name__ == "__main__":
    a = Account('a', 1000, threading.Lock())
    b = Account('b', 1000, threading.Lock())

    thread_list = []
    thread_list.append(threading.Thread(target=transfer, args=(a, b, 100)))
    thread_list.append(threading.Thread(target=transfer, args=(b, a, 500)))
    for i in thread_list:
        i.start()
    for j in thread_list:
        j.join()


