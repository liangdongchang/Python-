# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 云短信.py
@time: 2020/2/5 20:19
@author:LDC
'''

# encoding: utf-8
'''
@contact: 1257309054@qq.com
@wechat: 1257309054
@Software: PyCharm
@file: 测试.py
@time: 2020/2/5 20:09
@author:LDC
'''

# 自动抓取云短信网页上的验证码短信并分析来源
# Tsing 2019.03.21
# https://zhuanlan.zhihu.com/tsing

import re
import time
import requests
from bs4 import BeautifulSoup

header = {  # 伪造 headers
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Referer': 'https://www.pdflibr.com',
    'accept': 'text/html, application/xhtml+xml,application/xml;'

}


def get_page_phone(link, f):
    r = requests.get(link, headers=header)
    soup = BeautifulSoup(r.content, "html.parser")
    # print(soup)

    phone_list = soup.select(
        "body>article>section>div>div>div>div>h3")  # 有两个 sms-content-table 的 table，第一个是最新的4条信息，第二个是全部的信息。
    a_list = soup.select('body>article>section>div>div>div>a')
    print(len(phone_list))
    print(len(a_list))
    # print(a_list)
    for i in range(0, len(phone_list)):
        phone = phone_list[i].text
        href = a_list[i].get('href')

        url = 'https://www.materialtools.com{}'.format(href)
        get_page_info(url, f, phone)
        time.sleep(4)


def get_page_info(link, f, phone):
    header = {  # 伪造 headers
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Referer': 'https://www.pdflibr.com',
    }
    r = requests.get(link, headers=header)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find_all("div", class_="sms-content-table")  # 有两个 sms-content-table 的 table，第一个是最新的4条信息，第二个是全部的信息。
    infos = table[1].select('tbody tr')
    for info in infos:
        content = info.find_all("td")[2].text[1:-1]  # 首尾各去掉空格，这就是每一条短信的内容啦，可以写入文件里面哈。

        from_name = re.match(r'【(.*?)】', content)  # 第一个大括号里面一般就是来源名称，采用(.*?)进行最短匹配，不然默认的(.*)是贪婪匹配。
        # print(from_name)
        if not from_name:
            continue
        from_name = from_name.group(0)[1:-1]  # 去掉首尾的大括号【】
        if from_name and '抖音' in from_name:


            # print(from_name)
            save_str = '{}__{}__{}\n'.format(phone, link, from_name)
            print(content)
            print(save_str)
            print("-" * 30)
            f.write(save_str)  # 逐行写入txt文档，其实也可以不用写入文件，这里主要是方便自己查看。


def sort_result(filename):
    result = []  # 逐行读取文本文档中的来源名称，生成list
    with open(filename, 'r') as f:
        for line in f:
            result.append(line.strip('\n').split(',')[0])

    name_count = {}  # 定义一个元组，键名为list中的元素，键值为出现的次数
    for i in set(result):  # set 用于去除重复元素。
        name_count[i] = result.count(i)

    sorted_dict = sorted(name_count.items(), key=lambda d: d[1], reverse=True)  # 按照键值对 Dict 进行从大到小排序。
    for item in sorted_dict:
        print(item[0] + ': ' + str(item[1]))


if __name__ == '__main__':
    filename = "info.txt"  # 指定一个文本文件保存数据
    f = open(filename, 'w')
    for i in range(1, 2000):  # 自动翻页，这里可以设定需要抓取多少页（示例是100页）
        print("\n第%s页\n" % i)
        link = "https://www.materialtools.com/?page=" + str(i)
        get_page_phone(link, f)
        time.sleep(4)  # 不要频率太快，不然容易被封IP

    f.close()
    print('\r\n各个来源出现的频次分别为：\r\n')
    sort_result(filename)
