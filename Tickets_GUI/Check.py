#!/usr/bin/python
# -*- coding: utf-8 -*-
# -- Author: Morrow --
import sys
import ssl
import json
import time
import urllib
import datetime
import threading
from Tkinter import *
from ScrolledText import ScrolledText  # 滚动条
from station_name import get_citycode
# import ttk #--> Ubuntu16.04
# from tkinter import ttk #--> windows
try:
    from tkinter import ttk
except ImportError:
    import ttk

reload(sys)
sys.setdefaultencoding('utf-8')
station = get_citycode()
ssl._create_default_https_context = ssl._create_unverified_context # 关闭12306SSL认证


def get_jsonlist(from_name, to_name, date_num):
    content = []
    if not str(from_name) in station:
        content.append('--------------起始站台名不正确,或注意书写格式--------------')
        return content
    _from = station[str(from_name)]
    print _from
    if not str(to_name) in station:
        content.append('--------------终点站台名不正确,或注意书写格式--------------')
        return content
    _to = station[str(to_name)]
    print _to
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (
        date_num, _from, _to)

    html = urllib.urlopen(url).read().decode('utf-8')
    dict_html = json.loads(html)
    if 'data' in dict_html:
        print '数据已拿到 来源:12306JSON'
        if dict_html['data'] == []:
            content.append('--------------很抱歉，按您的查询条件未找到列车--------------')
            return content
        for i in dict_html['data']:
            bw = i['buttonTextInfo']  # 预定/未出售?
            wz = i['queryLeftNewDTO']['wz_num']  # 无座位
            ydz = i['queryLeftNewDTO']['zy_num']  # 一等座
            edz = i['queryLeftNewDTO']['ze_num']  # 二等座
            rw = i['queryLeftNewDTO']['rw_num']  # 软卧
            rz = i['queryLeftNewDTO']['rz_num']  # 软座
            yw = i['queryLeftNewDTO']['yw_num']  # 硬卧
            yz = i['queryLeftNewDTO']['yz_num']  # 硬座

            ls = i['queryLeftNewDTO']['lishi']  # 历时
            qd = i['queryLeftNewDTO']['from_station_name']  # 始
            zd = i['queryLeftNewDTO']['end_station_name']  # 终
            cc = i['queryLeftNewDTO']['station_train_code']  # 车次
            start_time = i['queryLeftNewDTO']['start_time']  # 发车时间
            arrive_time = i['queryLeftNewDTO']['arrive_time']  # 到达时间

            all_str = '日期:'+date_num+' 车次:'+cc+' 发车时间>'+start_time+' 到达时间>' +\
                arrive_time+'\n'+'历时>'+ls+' 起始站:'+qd + ' 终点站:'+zd+'\n'+'无座:'+wz +\
                ' 一等座:'+ydz+' 二等座:'+edz+' 硬座:' + yz+' 硬卧:'+yw+' 软座:'+rz+' 软卧:' +\
                rw+'\n'+'可购票状态:'+bw+'\n'
            content.append(all_str)
            # time.sleep(0.5)
        return content
    else:
        content.append('输入格式错误 或 暂无信息...')
        return content


def write_data():
    t1 = time.time()
    Lower_left_word.set('请等待,搜索中..')
    content = get_jsonlist(Starting_station.get(), Terminus.get(), date.get())
    time.sleep(1)
    text.delete('1.0', END)
    for icontent in content:
        text.insert(END, icontent)
    t2 = time.time()
    cost = t2 - t1
    time_cost.set('用时%.2f秒' % cost)
    Lower_left_word.set('数据来自:12306..')


def start():
    # 添加一个搜索的进程
    th = threading.Thread(target=write_data)
    th.start()


def main():
    root = Tk()
    root.title('Check-Check V_1.8.1    Author:莫罗')  # 标题
    # root.iconbitmap('ICON\\tubiao.ico')  # logo
    root.geometry('435x580+400+120')  # 窗口坐标 大小用x,坐标用+

    scrolW = 50
    scrolH = 20
    global text
    text = ScrolledText(
        root, font=('微软雅黑', 10), width=scrolW, height=scrolH)  # 设置文本滚动条
    text.grid(row=5, column=0, columnspan=3, rowspan=3, sticky=E)  # 滚动条布局

    global Lower_left_word
    Lower_left_word = StringVar()  # 设置变量字
    Label(root,  font=('微软雅黑', 10), fg='blue', textvariable=Lower_left_word).grid(
        row=15, column=0)  # row=15, column=0,sticky=W
    Lower_left_word.set('引擎准备完毕....')

    global time_cost
    time_cost = StringVar()  # 设置变量字
    Label(root,  font=('微软雅黑', 10), fg='red', textvariable=time_cost).grid(
        row=15, column=1)  # row=15, column=0,sticky=W
    # time_cost.set('耗时0.0S')

    global Starting_station
    Starting_station = StringVar()
    Label(root, font=('微软雅黑', 10), text='起始站:').grid(row=0, column=0, sticky=N)
    _from_entry = Entry(root, width=5, textvariable=Starting_station)
    _from_entry.grid(row=0, column=1, sticky=W, ipadx=7)
    _from_entry.focus()  # 设置光标起点

    global Terminus
    Terminus = StringVar()
    Label(root, font=('微软雅黑', 10), text='目的站:').grid(row=1, column=0, sticky=N)
    Entry(root, width=5, textvariable=Terminus).grid(
        row=1, column=1, sticky=W, ipadx=7)

    global date
    date = StringVar()
    localdate = datetime.date.today()  # 当天时间
    tomorrow = localdate + datetime.timedelta(days=1)
    Label(root, font=('微软雅黑', 10), text='出发日期:').grid(
        row=2, column=0, sticky=N)
    calendar = ttk.Combobox(root, width=5, textvariable=date)
    calendar['values'] = (localdate, tomorrow, localdate + datetime.timedelta(days=2), localdate + datetime.timedelta(days=3), localdate + datetime.timedelta(days=4),
                          localdate + datetime.timedelta(days=5), localdate + datetime.timedelta(
        days=6), localdate + datetime.timedelta(days=7), localdate + datetime.timedelta(days=8),
        localdate + datetime.timedelta(days=9), localdate + datetime.timedelta(
        days=10), localdate + datetime.timedelta(days=11), localdate + datetime.timedelta(days=12),
        localdate + datetime.timedelta(days=13), localdate + datetime.timedelta(
        days=14), localdate + datetime.timedelta(days=15), localdate + datetime.timedelta(days=16),
        localdate + datetime.timedelta(days=17), localdate + datetime.timedelta(
        days=18), localdate + datetime.timedelta(days=19), localdate + datetime.timedelta(days=20))
    # 读取本地时间设置下拉列表时间参数
    calendar.grid(row=2, column=1, sticky=W, ipadx=18)
    calendar.set(localdate)  # 默认日期当日本地时间

    button = ttk.Button(root, text='开始查票', command=lambda: start())
    button.grid(row=3, column=1, sticky=W)  # 按键布局
    Label(root, font=('微软雅黑', 10), text='查询格式:').grid(
        row=4, column=0, sticky=N)
    Label(root, font=('微软雅黑', 10), text='起始站:北京 到达站:重庆').grid(
        row=4, column=1, sticky=N)

    root.mainloop()

if __name__ == '__main__':
    main()
