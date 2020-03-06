# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 线程池.py
@time: 2020/3/3 20:36
@author:LDC
'''
import time
from concurrent.futures import ThreadPoolExecutor


# 任务
def doSth(args):

    print("hello", args)
    # time.sleep(2)


if __name__ == '__main__':
    # max_workers 线程数
    argsList = (1, 2, 3, 4, 5, 6)
    # 使用sumbit()函数提交任务
    with ThreadPoolExecutor(5) as exe:
        for a in argsList:
            # fn,
            # *args 不定长位置参数
            #  **kwargs 不定长关键字参数
            exe.submit(doSth, a)
    # 使用map()函数提交任务
    print("使用map()提交任务")
    with ThreadPoolExecutor(5) as exe:
        #  fn, 方法
        # *iterables 可迭代对象 ，如列表
        exe.map(doSth, argsList)
