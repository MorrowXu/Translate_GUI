#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Morrow
import json
import requests
import random
import md5
import threading
from Tkinter import *
from ScrolledText import ScrolledText
try:
    from tkinter import ttk
except ImportError:
    import ttk
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
   appid和secretkey得在百度翻译api平台申请
   Appid and secretkey have to apply in the Baidu translation API platform
'''


def connect_baiduapi():
    url = ' http://api.fanyi.baidu.com/api/trans/vip/translate'
    appid = 'your appid'  # 你申请的appid
    secretKey = 'your secretKey'  # 百度api发给你的密钥
    q = str(from_text.get('1.0', END)).strip()
    fromlang = lang_from.get().split('-')[1]
    tolang = lang_to.get().split('-')[1]
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    params = {'appid': appid, 'q': q, 'from': fromlang, 'to': tolang,
                              'salt': str(salt), 'sign': sign}
    try:
        r = requests.get(url, params)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        content = json.loads(r.text)
        if content['trans_result'][0]['dst']:
            dst = content['trans_result'][0]['dst']
            to_text.delete('1.0', END)
            to_text.insert(END, dst)
    except Exception as e:
        to_text.insert(END, e)


def translate_GUI():
    root = Tk()
    root.title('Easy_translate   Author:Morrow')
    root.geometry('480x245+800+320')
    global lang_from
    lang_from = StringVar()
    Label(
        root,
        font=(
            '微软雅黑',
            11),
        text='选择语言:').grid(
            row=0,
            column=0,
        sticky=N)
    lang_from_list = ttk.Combobox(root, width=5, textvariable=lang_from)
    lang_from_list['values'] = ('自动检测-auto', '中文-zh', '英语-en', '粤语-yue',
                                '文言文-wyw', '日语-jp','韩语-kor','法语-fra',
                                '西班牙语-spa','泰语-th','阿拉伯语-ara','俄语-ru',
                                '葡萄牙语-pt','德语-de','意大利语-it','希腊语-el',
                                '荷兰语-nl','波兰语-pl','保加利亚语-bul','爱沙尼亚语-est',
                                '丹麦语-dan','芬兰语-fin','捷克语-cs','罗马尼亚语-rom',
                                '斯洛文尼亚语-slo','瑞典语-swe','匈牙利语-hu','繁体中文-cht',
                                '越南语-vie')
    lang_from_list.grid(row=0, column=1, sticky=N, ipadx=20)
    lang_from_list.set('自动检测-auto')
    global lang_to
    lang_to = StringVar()
    Label(
        root,
        font=(
            '微软雅黑',
            11),
        text='译后语言:').grid(
            row=0,
            column=3,
        sticky=N)
    lang_to_list = ttk.Combobox(root, width=5, textvariable=lang_to)
    lang_to_list['values'] = lang_from_list['values'][1:]
    lang_to_list.grid(row=0, column=4, sticky=N, ipadx=20)
    lang_to_list.set('中文-zh')
    global from_text
    from_text = ScrolledText(
        root,
        font=(
            '微软雅黑',
            11),
        width=27,
        height=7,
        wrap=WORD)
    from_text.grid(row=1, column=0, columnspan=3, rowspan=3, sticky=E)
    from_text.focus()
    global to_text
    to_text = ScrolledText(
        root,
        font=(
            '微软雅黑',
            11),
        width=27,
        height=7,
        wrap=WORD)
    to_text.grid(row=1, column=3, columnspan=3, rowspan=3, sticky=E)

    button = Button(
        root,
        font=(
            '微软雅黑',
            11),
        width=2,
        text='查询',
        command=lambda: start())
    button.grid(row=5, column=4, ipadx=5)
    clear_button = Button(
        root,
        font=(
            '微软雅黑',
            11),
        width=2,
        text='清屏',
        command=lambda: clear())
    clear_button.grid(row=5, column=3, ipadx=5)

    en_to_zh = Button(
        root,
        font=(
            '微软雅黑',
            11),
        width=2,
        text='英译汉',
        command=lambda: en2zh())
    en_to_zh.grid(row=5, column=0, ipadx=5)

    zh_to_en = Button(
        root,
        font=(
            '微软雅黑',
            11),
        width=2,
        text='汉译英',
        command=lambda: zh2en())
    zh_to_en.grid(row=5, column=1, ipadx=5)
    root.mainloop()


def en2zh():
    lang_from.set('英语-en')
    lang_to.set('中文-zh')
    th = threading.Thread(target=connect_baiduapi)
    th.start()


def zh2en():
    lang_guess = str(from_text.get('1.0', END)).strip()
    if lang_guess >= u'\u4e00' and lang_guess <= u'\u9fa5':
        lang_from.set('中文-zh')
        lang_to.set('英语-en')
    else:
        lang_from.set('自动检测-auto')
        lang_to.set('英语-en')
    th = threading.Thread(target=connect_baiduapi)
    th.start()


def clear():
    from_text.delete('1.0', END)
    to_text.delete('1.0', END)
    lang_from.set('自动检测-auto')


def start():
    th = threading.Thread(target=connect_baiduapi)
    th.start()


if __name__ == '__main__':
    translate_GUI()
