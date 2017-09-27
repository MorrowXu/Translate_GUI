#!/usr/bin/python
# -*- coding: utf-8 -*-
# -- Author: Morrow --


def get_citycode():
	file = open('./files/station_name.txt','r')
	station_name = file.read()
	name = station_name.split('@')
	station_dict = {'':''}
	for i in name:
	    if i:
	    # 防止为空
	        list_i = i.split('|')
	        station_name_ = list_i[1] # 地点名
	        station_code_ = list_i[2] # 地点代码
	        station_dict[station_name_] = station_code_ # 字典加入对应地点的代码
	file.close()
	return station_dict
