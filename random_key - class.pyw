# -*- coding: utf-8 -*-
#!/bin/usr/env python
# author: Morrow
import time
import random
import threading
import win32clipboard
from Tkinter import *
from ScrolledText import ScrolledText  # 滚动条
try:
    from tkinter import ttk	  
except ImportError:
    import ttk

class Gui(object):

	def __init__(self):
		root = Tk()
		root.title('随机秘钥生成器 v1.6 Author：Morrow')
		root.geometry('480x245+600+320')
		# root.iconbitmap('')
	
		Label(root, font=('微软雅黑',11),text='请输入位数:',fg='blue').place(relx=0.1,rely=0.09)
		num_text = StringVar()
		self.num_text = num_text
		num_select = ttk.Entry(root,textvariable=num_text,width=8)
		num_select.place(relx=0.3,rely=0.1)
		num_select.focus()
	
		Label(root, font=('微软雅黑',11),text='请选择复杂度:',fg='purple').place(relx=0.069,rely=0.29)
		var1 = IntVar()
		numbers = Checkbutton(root,text='[0-9]',fg='purple',variable=var1)
		self.numbers = numbers
		numbers.select()
		numbers.var = var1
		numbers.place(relx=0.3,rely=0.3)
		# 该复选框是否勾选,select为勾选, deselect为不勾选
	
		var2 = IntVar()
		letter = Checkbutton(root,text='[A-Za-z]',fg='purple',variable=var2)
		self.letter = letter
		letter.var = var2
		letter.place(relx=0.45,rely=0.3)
	
		var3 = IntVar()
		symbol = Checkbutton(root,text='[@#$%^!&*]',fg='purple',variable=var3)
		self.symbol = symbol
		symbol.var = var3
		symbol.place(relx=0.65,rely=0.3)
	
		scrolW = 20
		scrolH = 2
		text = ScrolledText(root, font=('微软雅黑', 11), width=scrolW, height=scrolH)
		self.text = text
		text.place(relx=0.3,rely=0.49)
		Label(root, font=('微软雅黑',11),text='随机后的秘钥:',fg='green').place(relx=0.069,rely=0.49)
	
		button = ttk.Button(root, text='生成', command= lambda: self.start())
		button.place(relx=0.65,rely=0.79)
		
		copy_button = ttk.Button(root, text='复制', command= lambda: self.func())
		copy_button.place(relx=0.3,rely=0.79)

		mainloop()
	
	
	def output(self):
		string = self.main()
		self.string = string
		self.text.delete('1.0',END) # 从起始清除到结束
		self.text.insert(END,string)
		time.sleep(1)
	
	
	def start(self):
		# 生成一个线程来执行main
		th = threading.Thread(target=self.output)
		th.start()


	def main(self):
		# 创造随机数的主函数
		length = self.num_text.get()
		num_choice = self.numbers.var.get()
		letter_choice = self.letter.var.get()
		symbol_choice = self.symbol.var.get()
	
		try:
			length = int(length)
		except Exception as e:
			return '输入不符合规范请重新输入！错误代码：%s' % e
	
		if int(length) >= 1001:return '数字过大,请重新输入';
		num = [str(x) for x in range(10)] * 3 # 生成数字列表
		en = [chr(i) for i in range(97,123)] # 生成字母列表
		EN = [chr(i).upper() for i in range(97,123)] # 生成大写字母表
		symbol_list = ['@','#','$','%','^','!','&','*'] * 3# 生成符号表
	
		if num_choice == 0: # 如果没有勾选就置空
			num = []
		if letter_choice == 0:
			en,EN = [],[]
		if symbol_choice == 0:
			symbol_list = []
	
		code_list = num + en + symbol_list +EN
		if symbol_choice ==0 and letter_choice ==0 and num_choice == 0:
			code_list = ['']
		random.shuffle(code_list) # 每次原表随机排序
		code = ''
	
		for i in range(length):
			code += random.choice(code_list)
		return code
	

	def func(self):
		# 定义复制按钮功能
		if not self.string:self.string == '';
		content = self.string
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(win32clipboard.CF_TEXT, content)
		win32clipboard.CloseClipboard()
		if content: # conteng不为空就弹出复制成功
			import tkMessageBox # 导入tk消息盒子
			tkMessageBox.showinfo( "", "已复制到剪贴板")


if __name__ == '__main__':
	Gui()
