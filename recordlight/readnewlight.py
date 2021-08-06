#coding:utf-8
import serial
import time
import struct
import serial.tools.list_ports as getport
class readcom2():
    '''
    传感器
    '''
    def __init__(self,portname):
        self.portname=portname
        self.com=serial.Serial()
        self.lbuff=[]
        self.isstart=False
        self.ShowPorts()
        self.lightdata=[0xa5,0x51,0xf6]

    def InitCOm(self,b):
        self.com.port = self.portname
        self.com.baudrate = b
        self.com.bytesize = 8 
        self.com.stopbits = 1
        self.com.parity = serial.PARITY_NONE

    def OpenCom(self):
        self.com.open()
        isok=False
        if self.com.isOpen():
            isok=True
        return isok

    def HexToString(self,data):
        hstr=""
        for e  in data:
            hstr+=hex(e)+" "
        return hstr

    def CheckData(self,buff):
        xd=0.0
        #print("验证数据：",self.HexToString(buff))
        if len(buff)==9:
            if buff[0]==0x5a and buff[1]==0x5a:
                if buff[2]==0x15:
                    x=0
                    for i in range(0,8):
                        x+=buff[i]
                    if x==buff[8] or x%256==buff[8]:
                        lux=(buff[4]<<24)|(buff[5]<<16)|(buff[6]<<8)|buff[7]
                        lux=lux/100
                        xd=lux
        return xd

    def isDataOK(self,buff):
        blen=len(buff)
        xd=0.0
        for i in range(0,blen):
            if i>=1:
                if buff[i-1]==0x5a and buff[i]==0x5a and self.isstart==False:
                    self.isstart=True
                    self.lbuff.append(buff[i-1])
                if self.isstart:
                    self.lbuff.append(buff[i])
                if len(self.lbuff)==9 and self.isstart==True:
                    xd=self.CheckData(self.lbuff)
                    self.isstart=False 
                    self.lbuff=[]
                elif len(self.lbuff)>9 and self.isstart==True:
                    print("数据核对失败")
                    self.isstart=False 
                    self.lbuff=[]
            else:
                if self.isstart:
                    self.lbuff.append(buff[i])
                if len(self.lbuff)==9 and self.isstart==True:
                    xd=self.CheckData(self.lbuff)
                    self.isstart=False 
                    self.lbuff=[]
                elif len(self.lbuff)>9 and self.isstart==True:
                    print("数据核对失败")
                    self.isstart=False 
                    self.lbuff=[]
        return xd

    def ShowPorts(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list)> 0:
            clist=[]
            for e in port_list:
                port_list_0 =list(e)
                port_serial = port_list_0[0]
                clist.append(port_serial)
            print(clist)

    def ReadData(self):
        self.com.write(self.lightdata)
        time.sleep(0.1)
        slen=self.com.in_waiting
        b = self.com.read(slen)
        #print(self.HexToString(b))
        d=self.isDataOK(b)
        #print(d)
        return d
"""
rc=readcom2("COM13")
rc.InitCOm(9600)
rc.OpenCom()
for i in range(0,20):
    rc.ReadData()
"""