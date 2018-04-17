#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Morrow
import json
import requests
import random
import hashlib
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

class TranslateGui(object):

    def __init__(self):
        self.url = ' http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.appid = '-----'  # 你申请的appid
        self.secretKey = '------'  # 百度api发给你的密钥

    def connect_baiduapi(self):
        q = str(self.from_text.get('1.0', END)).strip()
        fromlang = self.lang_from.get().split('-')[1]
        tolang = self.lang_to.get().split('-')[1]
        salt = random.randint(32768, 65536)
        sign = self.appid + q + str(salt) + self.secretKey
        m1 = hashlib.md5()
        m1.update(sign)
        sign = m1.hexdigest()
        params = {
                  'appid': self.appid,
                  'q': q,
                  'from': fromlang,
                  'to': tolang,
                  'salt': str(salt),
                  'sign': sign}
        try:
            r = requests.get(self.url, params)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            content = json.loads(r.text)
            if content['trans_result'][0]['dst']:
                dst = content['trans_result'][0]['dst']
                self.to_text.delete('1.0', END)
                self.to_text.insert(END, dst)
        except Exception as e:
            self.to_text.insert(END, e)


    def translate_GUI(self):
        root = Tk()
        root.title('Easy_translate   Author:Morrow')
        root.geometry('480x245+800+320')

        self.lang_from = StringVar()
        Label(root, font=('微软雅黑', 11), text='选择语言:').grid(row=0, column=0,sticky=N)
        self.lang_from_list = ttk.Combobox(root, width=5, textvariable=self.lang_from)
        self.lang_from_list['values'] = ('自动检测-auto', '中文-zh', '英语-en', '粤语-yue',
                                    '文言文-wyw', '日语-jp','韩语-kor','法语-fra',
                                    '西班牙语-spa','泰语-th','阿拉伯语-ara','俄语-ru',
                                    '葡萄牙语-pt','德语-de','意大利语-it','希腊语-el',
                                    '荷兰语-nl','波兰语-pl','保加利亚语-bul','爱沙尼亚语-est',
                                    '丹麦语-dan','芬兰语-fin','捷克语-cs','罗马尼亚语-rom',
                                    '斯洛文尼亚语-slo','瑞典语-swe','匈牙利语-hu','繁体中文-cht',
                                    '越南语-vie')
        self.lang_from_list.grid(row=0, column=1, sticky=N, ipadx=20)
        self.lang_from_list.set('自动检测-auto')

        self.lang_to = StringVar()
        Label(root,font=('微软雅黑', 11),text='译后语言:').grid(row=0,column=3,sticky=N)
        self.lang_to_list = ttk.Combobox(root, width=5, textvariable=self.lang_to)
        self.lang_to_list['values'] = self.lang_from_list['values'][1:]
        self.lang_to_list.grid(row=0, column=4, sticky=N, ipadx=20)
        self.lang_to_list.set('中文-zh')

        self.from_text = ScrolledText(root, font=('微软雅黑', 11), width=27, height=7, wrap=WORD)
        self.from_text.grid(row=1, column=0, columnspan=3, rowspan=3, sticky=E)
        self.from_text.focus()
        
        self.to_text = ScrolledText(root, font=('微软雅黑', 11), width=27, height=7, wrap=WORD)
        self.to_text.grid(row=1, column=3, columnspan=3, rowspan=3, sticky=E)

        button = Button(root, font=('微软雅黑', 11), width=2, text='查询', command=lambda: self.start())
        button.grid(row=5, column=4, ipadx=5)
        clear_button = Button(root, font=('微软雅黑', 11), width=2, text='清屏', command=lambda: self.clear())
        clear_button.grid(row=5, column=3, ipadx=5)

        en_to_zh = Button(root, font=('微软雅黑', 11), width=4, text='英译汉', command=lambda: self.en2zh())
        en_to_zh.grid(row=5, column=0, ipadx=5)

        zh_to_en = Button(root, font=('微软雅黑', 11), width=4, text='汉译英', command=lambda: self.zh2en())
        zh_to_en.grid(row=5, column=1, ipadx=5)
        root.mainloop()


    def en2zh(self):
        self.lang_from.set('英语-en')
        self.lang_to.set('中文-zh')
        th = threading.Thread(target=self.connect_baiduapi)
        th.start()


    def zh2en(self):
        lang_guess = str(self.from_text.get('1.0', END)).strip()
        if lang_guess >= u'\u4e00' and lang_guess <= u'\u9fa5':
            self.lang_from.set('中文-zh')
            self.lang_to.set('英语-en')
        else:
            self.lang_from.set('自动检测-auto')
            self.lang_to.set('英语-en')
        th = threading.Thread(target=self.connect_baiduapi)
        th.start()


    def clear(self):
        self.from_text.delete('1.0', END)
        self.to_text.delete('1.0', END)
        self.lang_from.set('自动检测-auto')


    def start(self):
        th = threading.Thread(target=self.connect_baiduapi)
        th.start()


if __name__ == '__main__':
    f = TranslateGui()
    f.translate_GUI()
