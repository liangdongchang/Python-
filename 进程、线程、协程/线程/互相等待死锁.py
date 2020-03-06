# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 互相等待死锁.py
@time: 2020/3/3 22:29
@author:LDC
'''
import threading
import time


class Account(object):
    def __init__(self, name, balance, lock):
        self.name = name
        self.balance = balance
        self.lock = lock

    def withdraw(self, amount):
        # 转账
        self.balance -= amount

    def deposit(self, amount):
        # 存款
        self.balance += amount


def transfer(from_account, to_account, amount):
    # 转账操作
    with from_account.lock:
        from_account.withdraw(amount)
        time.sleep(1)
        print("trying to get %s's lock..." % to_account.name)
        with to_account.lock:
            to_account.deposit(amount)
    print("transfer finish")


if __name__ == "__main__":
    a = Account('a', 1000, threading.RLock())
    b = Account('b', 1000, threading.RLock())
    thread_list = []
    thread_list.append(threading.Thread(target=transfer, args=(a, b, 100)))
    thread_list.append(threading.Thread(target=transfer, args=(b, a, 500)))
    for i in thread_list:
        i.start()
    for j in thread_list:
        j.join()