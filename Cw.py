# *************************************************************************************
# Copyright 2022, Racer Designs. 
# This design is confidential and proprietary of Racer Designs. All Rights Reserved.
# **************************************************************************************
# File Name: Cw.py
# Date Last Modified:
#			08/25/2022 simpliy the CW.py to write/read serial no
			09/27/2022 check for write and read permisson on git hub
# Date Created: 08/26/2022 apei
#
# ff042Ecf # bytearray(b'\xff\x04.\xcf')
# **************************************************************************************/
# firmware send back serial number example
# g_u1Tx_buf[0] = ff 
# g_u1Tx_buf[1] = e 
# g_u1Tx_buf[2] = 0 
# g_u1Tx_buf[3] = 1 
# g_u1Tx_buf[4] = 2 
# g_u1Tx_buf[5] = 3 
# g_u1Tx_buf[6] = 4 
# g_u1Tx_buf[7] = 5 
# g_u1Tx_buf[8] = 6 
# g_u1Tx_buf[9] = 7 
# g_u1Tx_buf[10] = 8
# g_u1Tx_buf[11] = 9
# g_u1Tx_buf[12] = 4
# ttt1-- = 14 
# checksum = c2 
# for write check for "Write Finish"
# for read check for "Read Finish"

import tkinter as tk
# from tkinter import Button,Label,Frame,IntVar,Entry,Message,Text,END,Menu,Scrollbar,\
# W,RIGHT,X,Y,WORD,Menubutton,RAISED,font,LEFT,Listbox

from tkinter import Button,filedialog,Label,Radiobutton,Checkbutton,Frame,IntVar,StringVar,Entry,Message,Text,END,Menu,Scrollbar,\
W,RIGHT,X,Y,WORD,Menubutton,RAISED,Entry,font,LEFT,Listbox,SINGLE


from tkinter.ttk import Combobox
import tkinter.messagebox
from time import sleep
import threading
from serial.serialutil import SerialException
import serial
import serial.tools.list_ports as list_ports

class windows:
	def com_list(self):
		dd=[]
		ports=list(list_ports.comports())
		for p in ports:
			dd.append(p.device)
		self.combox['values']=dd
		dd.clear()

	def exit(self):#關閉接口
		if(self.ser!=None):
			self.ser.close()

	def clear(self):#清除    
		self._init_AllThread()
		sleep(0.01)
		self.serialclose()
		self.combox['state']=tk.NORMAL
		self._connect_btn_['state']=tk.NORMAL

	'''
	t1=serprint
	t5=com_list
	# '''

	def serprint(self):#串口PRINT//usb print
		print("serial print process")
		error_counter = 0
		error_counter_max = 2
		while True:
			try:
				data=self.ser.readlline()
				data=data.decode()
				self._debug_txt_.insert("end",str(data)+"\n")
				self._debug_txt_.see(END)
				sleep(0.01)
			except :
				self._debug_txt_.insert("end","comport read error\n")
				self._debug_txt_.see(END)
				error_counter = error_counter + 1
				print("read ERROR")
			if error_counter == error_counter_max:
				self._connect_btn_['state']=tk.NORMAL
				self.combox['state']=tk.NORMAL
				self._init_AllThread()                
				self.t5.setDaemon(True)
				self.t5.start()
				break
		

	def serialclose(self):
		if(self.ser!=None):
			self.ser.close()
			self.ser=None
			self._connect_btn_['state']=tk.NORMAL


	# def connect(self):
		# self.serialclose()
		# try:
			# print 
			# self.ser=serialf(self.combox.get(),115200)
			# # self.t1.start()
			# self._connect_btn_['state']=tk.DISABLED
            
		# except SerialException:
			# tkinter.messagebox.showerror("ERROR","comport not found")
            
	def connect(self):
		self.serialclose()
		if(self.is_connect ==0):
			self.button_text.set("stop")
			self.is_connect =1
			try:
				print 
				self.ser=serialf(self.combox.get(),115200)
				# self._connect_btn_['state']=tk.DISABLED
			except SerialException:
				tkinter.messagebox.showerror("ERROR","comport not found")
		else:
			self.button_text.set("connect")
			self.is_connect =0
            
		sleep(0.3)






	# 0525 add by apei
	def set_serial_num(self):
		self.write_btn['state']=tk.DISABLED #disable     
		print(self.serial_no) # 0828 apei
		self.serial_no =  self.enter_serial_num.get()	
		new_serial_no =self.serial_no[0:11]	# 06/14 serial num is 11bytes
		
		# print(self.serial_no) # 0828 apei
		
		serial_with_zero = ''		
		# for check sum verify
		add = 0
		len = 0
		check_sum =0

		for x in self.serial_no :
			if(x.isdigit()) :
				print("true "+x)	
			else :
				tkinter.messagebox.showerror("ERROR","only 0-9 can accept")
			len += 1
			
		if(len<=11)	:	    # 06/14 serial num is 11bytes
			for x in new_serial_no :
				add += int(x,16)
				serial_with_zero += '0'+ x
				
				
		while len < 11 :   # 06/14 serial num is 11bytes
			serial_with_zero += '00'
			len +=1

		add += int('ff',16)	
		add += int('e',16)	# 06/17 serial num is 11bytes
		add = (add % 256)
		
		add1=hex(~add & 0xFF)		
		add2= int(add1,16) + int('1',16)		
		
		serial_with_zero += hex(add2)[2] 
		serial_with_zero += hex(add2)[3] 
		print(serial_with_zero)
		self.enter_serial_num.delete(0, END)	
		self.enter_serial_num.insert(0,new_serial_no)
		self.serial_no_to_firm = 'ff0e'+serial_with_zero # 06/14 serial num is 11bytes
		msg=self.serial_no_to_firm          
		data=bytearray.fromhex(msg)
		print(msg)
		print(data)
		self.ser.write(data)
			

        # check for "Write finised"     
		error_counter = 0
		error_counter_max = 2       
		len1 = 0          
		while len1 < 4 :   # 09/13
			try:
				data=self.ser.readlline()
				data=data.decode()
				if('Write Finish' in data):
					print('Write Finish')
					break
				print(len1)
				len1 +=1

			except :
				error_counter = error_counter + 1                
				len1 =0                             
				print("read ERROR")
			if error_counter == error_counter_max:
				break  
        ### show to entry box                                

		self.write_btn['state']=tk.NORMAL #normal 



			
	# 0907 add by apei
	def get_serial_num(self):
		self.read_btn['state']=tk.DISABLED #disable 
		error_counter = 0
		error_counter_max = 2    
		get_serial_no = ""         
		len = 0          
		index = 0          
		msg='ff042Ecf'          
		data=bytearray.fromhex(msg)  
		print(msg)
		print(data)
        
		try:
			self.ser.write(data)
		except :
			self.enter_serial_num.delete(0, END)
			self.enter_serial_num.insert(0,"error")                 

		# self.ser.write(data)        
        
		print("get_serial_num")
		sleep(0.5)


		while len < 13 :   # 09/7 "ff,0e" and serial num is 11bytes
			try:
				data=self.ser.readlline()
				data=data.decode()
				if('=' in data):
					# print(data)
					index = (data.find('='))
					# print(data.find('='))
					# print(index)
					if(data[index+2] =='f'):
						print(data[index+2])
					elif(data[index+2] =='e'):
						print(data[index+2])
					else:
						print(data[index+2])
						get_serial_no = get_serial_no + data[index+2]

					len +=1
                
				self._debug_txt_.insert("end",str(data)+"\n")
				self._debug_txt_.see(END)
			except :
				self._debug_txt_.insert("end","comport read error\n")
				self._debug_txt_.see(END)
				error_counter = error_counter + 1                
				len =0                
				get_serial_no =""                
				# self.enter_serial_num.delete(0, END)
				# self.enter_serial_num.insert(0,"error")                
				print("read ERROR")
			if error_counter == error_counter_max:
				self.enter_serial_num.insert(0,"error restart program")                
				self.read_btn['state']=tk.NORMAL #normal                
				break                

        # check for "Read finised"     
		error_counter = 0
		len1 = 0          
		while len1 < 4 :   # 09/13
			try:
				data=self.ser.readlline()
				data=data.decode()
				if('Read Finish' in data):
					print('Read Finish')
					self.read_btn['state']=tk.NORMAL #normal 
					break
				print(len1)
				len1 +=1

			except :
				error_counter = error_counter + 1                
				len1 =0                             
				print("read ERROR")
			if error_counter == error_counter_max:
				self.read_btn['state']=tk.NORMAL #normal  
				break  
			self._debug_txt_.insert("end",str(get_serial_no)+"\n")
			self._debug_txt_.see(END)
        ### show to entry box                                
			self.enter_serial_num.delete(0, END)
			self.enter_serial_num.insert(0,get_serial_no)
			# print(len)
		self.read_btn['state']=tk.NORMAL #normal 



	def _init_AllThread(self):
		print("初始化執行緒")
		# self.t1=threading.Thread(target=self.serprint,name="t1")
		self.t5=threading.Thread(target=self.com_list,name="t5")

	def __init__(self):
#init
	#member
		self.is_connect=0
		self.ser=None
		self.serial_no = "01234567890"  # 06/14 serial num is 11bytes
		self.serial_no_to_firm = ""		

	#thread
		self._init_AllThread()
#windows
		self.window=tk.Tk()
		self.window.resizable(0,0)
		# self.window.geometry('600x300') # for debug use
		self.window.geometry('615x73') # for release use
		self.window.configure(background='white')


		self.button_text = tk.StringVar()
		self.button_text.set("connect")

		frame0_0=Frame(self.window)
		frame0_0.grid(column=0, row=0)		

		frame1_0=Frame(self.window)
		frame1_0.grid(column=1, row=0)
		
		frame0_1=Frame(self.window)
		frame0_1.grid(column=0, row=1)

		
		frame0=Frame(frame0_0)
		frame0.pack()

		frame1=Frame(frame1_0)
		frame1.pack()
		
		self.combox=Combobox(frame0,width=11,font=("Arial", 16))
		self.combox.configure(state='readonly')#normal#readonly#disableed//baudrate
		self.combox.grid(column=0, row=0)
		
		# self._connect_btn_=Button(frame0,text="connect",command=self.connect,height=1,width=11,font=('Arial',16,'bold'), bg='#F0F8FF',fg ='#2E8B57')
		self._connect_btn_=Button(frame0,textvariable=self.button_text,command=self.connect,height=1,width=11,font=('Arial',16,'bold'), bg='#F0F8FF',fg ='#2E8B57')
		self._connect_btn_.grid(column=0, row=1)
		
		# self.enter_serial_num=Entry(frame1, width=11,font=('Arial',17,'bold'), bg='#F0F8FF',fg ='#CC853F')
		self.enter_serial_num=Entry(frame1, width=11,font=('Arial',17,'bold'), bg='#F0F8FF',fg ='#8B0000')
		self.enter_serial_num.insert(0,self.serial_no)
		self.enter_serial_num.pack(side=LEFT)	
		
		# self.read_btn=Button(frame1,text="read",command=self.get_serial_num,width=11,font=('Arial',16,'bold'), bg='#F0F8FF',fg ='#CD853F')
		self.read_btn=Button(frame1,text="read",command=self.get_serial_num,width=11,font=('Arial',16,'bold'), bg='#F0F8FF',fg ='#C71585')
		self.read_btn.pack(side=LEFT,fill = 'y')
		# self.write_btn=Button(frame1,text="write",command=self.set_serial_num,height=2,width=11,font=('Arial',16,'bold'), bg='#F0F8FF',fg ='#CD853F')
		self.write_btn=Button(frame1,text="write",command=self.set_serial_num,height=2,width=11,font=('Arial',16,'bold'), bg='#F0F8FF',fg ='#4169E1')
		self.write_btn.pack(side=LEFT, fill = 'y')





		#Textbox & scrollbar set
		scrollbar_1=Scrollbar(frame0_1)
		scrollbar_1.pack(side=RIGHT,fill=Y)
		self._debug_txt_=Text(frame0_1,wrap=WORD,width=20,height=10,yscrollcommand=scrollbar_1.set)
		self._debug_txt_.pack()
		scrollbar_1.config(command=self._debug_txt_.yview)

		self._debug_txt_.insert(END," ")
		
		
	
        ## apei t5 comport list       
		self.t5.start()
        
        
        
	#mochon mode set
		self._connect_btn_['state']=tk.NORMAL
		self.combox['state']=tk.NORMAL
		self.window.title('SERIAL NO TOOL')

	#run mainloop
		self.window.mainloop()


class serialf:
	def __init__(self,USER_PORT,USER_BAUDRATE,USER_FILE=None):
		self.ser=serial.Serial(USER_PORT,USER_BAUDRATE)
		self.data=""

	def close(self):
		self.ser.close()

	def readlline(self):
		return self.ser.readline()

	def write(self,data):
		self.ser.write(data)

if __name__=="__main__":
	windows()






