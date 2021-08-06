#coding:utf-8
import serial
import time
import struct
class readcom():
    def __init__(self,portname):
        self.portname=portname
        self.com=serial.Serial()
        self.data=[0x01,0x03,0x00,0x64,0x00,0x03,0x44,0x14]

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

    def CloseCom(self):
        if self.com.is_open:
            self.com.close()

    def HexToString(self,data):
        hstr=""
        for e  in data:
            hstr+=hex(e)+" "
        return hstr

    def ReadData(self):
        sb=bytearray(self.data)
        print(sb)
        self.com.write(sb)
        time.sleep(0.5)
        slen=self.com.in_waiting
        b = self.com.read(slen)
        print(self.HexToString(b))
        lf=b[5:9]
        print(lf)
        dl=[]
        dl.append(lf[3])
        dl.append(lf[2])
        dl.append(lf[1])
        dl.append(lf[0])
        f=struct.unpack("f",bytearray(dl))
        print(f)
        return f[0]