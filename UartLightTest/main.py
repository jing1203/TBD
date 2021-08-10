#coding:utf-8
from PySide2.QtWidgets import QApplication,QStyleFactory
import sys
from UartLightTest.mainform import MainWindow
from UartLightTest.com.readlight import readcom
# deprecated

if __name__ == '__main__':
	w = MainWindow()
	# light_cmd = input("输入光机动作指令：动作，串口端口号")
	text = "open"
	portname = "COM3"
	proj_com = readcom(portname)
	pho = readcom(portname)
	# Pho_cmd =  input("输入光度计动作指令：动作，串口端口号")

