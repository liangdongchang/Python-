# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: yield_test.py
@time: 2020/3/5 15:39
@author:LDC
'''


def foo(end_count):
    print('yield生成器')
    count = 0
    while count < end_count:
        res = yield count
        print('接收到的参数', res)
        if res is not None:
            count = res
        else:
            count += 1


if __name__ == '__main__':
    f = foo(7)
    # 第一次调用yield函数是预激活，
    # 即调用函数foo时，只执行yield前面的语句，
    # 遇到yield就把foo函数挂起来，
    # 并返回yield后面附带的值
    print(next(f))  # 使用next()调用yield函数
    for i in range(3):
        # 第二次调用就开始执行yield后面的语句
        print(next(f))  # 使用next()调用yield函数
    print('*' * 20)
    # s使用send给foo函数传值，yield会接收到并赋给res，
    print(f.send(5))  # send函数中会执行一次next函数
    print(next(f))

    # 生成不占空间的列表[0,1,2,3,4,5,6,7,8,9]
    # for i in foo(10):
    #     print(i)
