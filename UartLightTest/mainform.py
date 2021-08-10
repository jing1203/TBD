#coding:utf-8

from UartLightTest.com.logwrite import LogData
import time
from UartLightTest.com.ubyte import Ubyte
from UartLightTest.com.readini import GetTestTime
from UartLightTest.com.dbase import PRecord,xmldbhelpper
from sqlalchemy.ext.declarative import declarative_base
from UartLightTest.com.readlight import readcom
import datetime
from UartLightTest.com.exhelpper import Exhelp
from UartLightTest.com.datahandler import Data_Handler as dh
import warnings

Base = declarative_base()
class MainWindow():
    def __init__(self):
        etime=time.strftime('%Y%m%d%H%M', time.localtime(time.time()))


    def InitData(self):
        # self.serachports()
        # self.com = readcom(portname)
        # self.openProjCom(text, portname)
        # self.OpenPhoCom(text, portname)
        # self.com.readyRead.connect(self.readData)
        self.isopen = False
        self.lbuff = []
        self.isok = False
        self.ld = LogData()
        self.lstr = ""
        self.scount = 0

        self.ub = Ubyte()
        self.isauto=False
        self.isreadversion=False

        self.plist=[]
        self.testindex=0
        self.InitDb()
        self.rstate=0
        self.imglist=["white.png","photometer.png","grid.png","black.png"]
        self.lightv=0
        self.ltmp=0
        self.slist=GetTestTime("config/set.ini")
        print("读取配置：",self.slist)
        self.testtime=self.slist["printtimes"]
        self.testlayer=self.slist["printlayer"]
        self.ci=self.slist["ci"]
        self.ub.SetIni(self.slist)
        # self.new.cb_comname.setCurrentText(self.slist["comname"])
        # self.new.cb_pho.setCurrentText(self.slist["phocom"])
        self.testint=0
        self.starttime=None
        self.readlightv=self.slist["lightv"]
        self.ledontime=self.slist["ledontime"]
        self.ledofftime=self.slist["ledofftime"]

        self.ex=Exhelp()
        self.worktime=self.slist["worktime"]
        self.resttime=self.slist["resttime"]

        self.imgtype=0
        self.autotime=0
        print("------AUTO 测试次数"+str(self.autotime*self.testlayer+self.testindex)+"--------\r\n")
        self.isledoff=False
        #定时器开启，用于判断数据是否超时,发送数据后按1秒来执行
        # self.readwaittime=self.slist["waittime"]
        # self.waitcomtimer= QTimer()
        # self.waitcomtimer.setTimerType(Qt.PreciseTimer)
        # self.waitcomtimer.timeout.connect(self.callwait)
        self.wsec=0 #用于判断是否超时
        self.retrytimes=0#重试次数
        self.uarttime=0

        self.frameBspath = "/dev/fb2"

    '''
    测试用例的前置准备：开启光度计
    '''
    def OpenPhoCom(self, text, portname):
        try:
            if text == "open":
                # self.rc=readcom(self.new.cb_pho.currentText())
                self.rc = readcom(portname)
                self.rc.InitCom(9600)
                self.rc.OpenCom()
                self.uarttime = dh.GetTimeSmap(0)
            elif text == "close":
                self.rc.CloseCom()
        except Exception as e:
            self.ShowMsg("光度计串口设置失败：" + str(e))

    '''
    测试用例的前置准备：开启光机 
    '''
    def openProjCom(self, text, portname):
        try:
            if text == "openCom":
                self.com = readcom(portname)
                if self.com.OpenCom():
                    self.com.CloseCom()
                self.com.InitCom(9600)
                self.isopen = True
                self.ShowMsg("串口打开成功")
            elif text == "closeCom":
                self.com.CloseCom()
                self.isopen = False
                self.ShowMsg("串口关闭成功")
        except Exception as e:
            self.ShowMsg("光机串口打开失败：" + str(e))

    '''
    通讯处理：超时响应
    '''
    def callwait(self):

        self.wsec+=1
        if self.wsec==self.readwaittime:
            if self.retrytimes<3:
                self.ShowMsg("数据超时，尝试重新执行，对变量进行初始化，重新执行！重试次数："+str(self.retrytimes))
                self.ShowMsg("数据超时，尝试重新执行，对变量进行初始化，重新执行！重试次数："+str(self.retrytimes))
                self.ShowMsg("数据超时，尝试重新执行，对变量进行初始化，重新执行！重试次数："+str(self.retrytimes))
                self.ShowMsg("数据超时，尝试重新执行，对变量进行初始化，重新执行！重试次数："+str(self.retrytimes))
                self.ShowMsg("数据超时，尝试重新执行，对变量进行初始化，重新执行！重试次数："+str(self.retrytimes))
                self.wsec=0
                self.testint=0
                # self.waitcomtimer.stop()
                self.retrytimes+=1
            else:
                self.ShowMsg("重试次数超出3次，不再重试！！！！")
                self.ShowMsg("重试次数超出3次，不再重试！！！！")
                self.ShowMsg("重试次数超出3次，不再重试！！！！")
                self.ShowMsg("重试次数超出3次，不再重试！！！！")
                self.ShowMsg("重试次数超出3次，不再重试！！！！")

    '''
    通讯处理：响应UI ，后台写入数据
    '''
    def callsw(self,msg):
        warnings.warn(" is deprecated", DeprecationWarning)
        print(msg)
        data=self.ub.GetNameData(msg)
        self.WriteData(data)

    '''
      通讯处理
      '''
    def GetTimeOneHr(self):
        isok=False
        if self.starttime==None:
            self.starttime=datetime.datetime.now()
        else:
            dt1=datetime.datetime.now()
            s2=str(dt1-self.starttime)
            sl=s2.split(":")
            if len(sl)>0:
                rh=sl[0]
                if int(rh)>=self.worktime:
                    isok=True
                    self.starttime=datetime.datetime.now()
        return isok


    '''
    通讯处理
    '''
    def GetTime10min(self):
        for i in range(0,self.resttime):
            self.Delay_MSec(1000)
            self.ShowMsg("运行一小时，等待休息时间："+str(i))


    '''
    测试前置条件准备：设置电流值 
    '''
    def SetCurrent(self, cs):
        '''

        :param cs: 输入设置的电流值
        :return:  无
        '''
        try:
            # cs=self.new.txt_current.text()
            ci = int(cs)
            self.ci = ci
            self.slist["ci"] = ci
            self.ub.SetIni(self.slist)
        except Exception as e:
            self.ShowMsg("设置电流失败："+str(e))

    '''
    测试步骤：发送通讯数据
    '''
    def SendBytesByStr(self,hexstr):
        # warnings.warn(" turn to fixture, deprecated", DeprecationWarning)
        # hexstr=self.new.txt_send.text()
        if len(hexstr)>0:
            hexstr=hexstr.rstrip()
            bl=self.HexToBytes(hexstr)
            self.WriteData(bl)

    '''
    用例的数据获取：使用光度计的读值进行光强值获取
    '''
    def TestLightPho(self):
        try:
            lv=self.rc.ReadData()
            self.ld.LogWriteInfo("当前光强值为 "+ lv)
        except Exception as e:
            self.ld.LogWriteInfo("当前光强值为 " + str(e))
            # self.ShowMsg("读取光度计失败："+str(e))

    '''
    光机投图用例中的测试步骤：改变投图
    '''
    def ChangImage(self,b):

        if b==0:
            dh.img2fb("src/projectImg/white.png", self.frameBspath)
        elif b==1:
            dh.img2fb("src/projectImg/grid.png", self.frameBspath)
        elif b==2:
            dh.img2fb("src/projectImg/photometer.png", self.frameBspath)
        elif b==3:
            dh.img2fb("src/projectImg/black.png", self.frameBspath)

    '''
    所有用例的前置条件准备：数据初始化
    '''
    def StartAutoTest(self, text):
        '''

        :param text: 开关光机
        :return:
        '''
        if text == "send":
            # self.new.btn_send.setText("关闭")
            # self.new.btn_send.setStyleSheet("background-color:gold")
            self.ld.InitPath()
            self.isauto=True
            self.testint=0
            self.testtime=self.slist["printtimes"]
            self.testlayer=self.slist["printlayer"]
            self.testindex=0
            self.autotime=0
            self.isledoff=False
            self.StopTim()
            self.RunTest()
        elif text=="close":
            pass


    '''
    所有用例的全部执行：发送通讯数据
    '''
    def SendTest(self, text):
        # text=self.new.cb_test.currentText()
        if text=="Auto":
            # btext=self.new.btn_send.text()  todo: btext 是？
            btext = None
            self.StartAutoTest(btext)
        else:
            buff=self.ub.GetSendData(text)
            self.WriteData(buff)


    '''
    测试用例：通讯接口用例
    '''
    def RunTest(self):
        '''
        全部用例都执行，无限循环
        :return: 无
        '''
        ql=[]
        cdata=""
        fl=[]
        delaytime=150
        while True:
            self.Delay_MSec(delaytime)
            if self.isauto:
                if self.isledoff:
                    return
                else:
                    if self.rstate==0:
                        print("PowerOn case")
                        if self.GetTimeOneHr():
                            self.GetTime10min()
                        if self.autotime < self.testtime:
                            ql=self.ub.PowerOn()
                            if self.testint==0:
                                self.WriteData(ql)
                                self.StartTim()
                                cdata+="------AUTO 开机--------\r\n"
                                # self.new.textBrowser.append("------AUTO 开机--------\r\n")
                                self.ld.LogWriteInfo("------AUTO 开机--------\r\n")
                                self.testint=1
                        else:
                            # print("head09")
                            cdata+="测试已完成"
                            # self.new.textBrowser.append("------测试完成--------\r\n")
                            self.ld.LogWriteAuto(cdata)
                            cdata=""
                            break
                    elif self.rstate == 1:
                        print("PowerOff case")
                        self.ld.LogWriteAuto("PowerOff case")
                        if self.testint == 0:
                            ql=self.ub.LedOff()
                            self.WriteData(ql)
                            self.StartTim()
                            cdata+="------AUTO LED OFF--------\r\n"
                            # self.new.textBrowser.append("------AUTO LED OFF--------\r\n")
                            self.ld.LogWriteAuto(cdata)
                            self.testint=1
                    elif (self.rstate==4 and self.testindex==0) or (self.rstate==6):
                        # print("head02")
                        self.ld.LogWriteAuto("进入-AUTO 设置背景图 光强校准case")
                        if self.testint==0:
                            if self.imgtype==1:
                                dh.img2fb("src/projectImg/black.png", self.frameBspath)
                                cdata+="------AUTO 设置背景图 光强校准图--------\r\n"
                                self.ld.LogWriteAuto(cdata)
                                self.imgtype = 2
                            elif self.imgtype==2:
                                dh.img2fb("src/projectImg/grid.png", self.frameBspath)
                                cdata+="------AUTO 设置背景图 网格图--------\r\n"
                                self.ld.LogWriteAuto(cdata)
                                self.imgtype=0
                            elif self.imgtype==0:
                                dh.img2fb("src/projectImg/white.png", self.frameBspath)
                                cdata+="------AUTO 设置背景图 白图--------\r\n"
                                self.ld.LogWriteAuto(cdata)
                                self.imgtype=1
                            bl=self.ub.IntToByte(self.ci)
                            ql=self.ub.SetLightCurrent(bl[0],bl[1],bl[0],bl[1],bl[0],bl[1])
                            self.WriteData(ql)
                            # self.StartTim()
                            cdata+="------AUTO 设置电流 "+str(self.ci)+"--------\r\n"
                            self.ld.LogWriteAuto(cdata)
                            self.testint=1
                            self.testindex+=1
                    elif self.rstate==2: 
                        print("head03")
                        if self.testint==0:
                            ql=self.ub.LedOn()
                            self.WriteData(ql)
                            self.StartTim()
                            self.testint=1
                    elif self.rstate==3:
                        for i in range(0,4):
                            self.Delay_MSec(self.ledontime)
                            lv=self.rc.ReadData()
                            self.ShowMsg("光强值："+str(lv))
                            cdata+="------AUTO "+"光强值："+str(lv)+"--------\r\n"
                            self.lightv=lv
                            fl.append(lv)
                        self.lightv=self.GetRealValue(fl)
                        cdata+="------AUTO "+"光强值采样值："+str(lv)+"--------\r\n"
                        if self.lightv>self.readlightv:
                            pass
                        else:
                            self.ld.LogWriteErr("光强数据错误："+str(self.lightv))
                        print("head04")
                        if self.testint==0:
                            dh.img2fb("src/projectImg/black.png", self.frameBspath)
                            cdata+="------AUTO 设置背景图 黑图--------\r\n"
                            ql=self.ub.LedOff()
                            self.WriteData(ql)
                            self.StartTim()
                            cdata+="------AUTO LED OFF 3秒--------\r\n"
                            # self.new.textBrowser.append("------AUTO LED OFF 3秒--------\r\n")
                            self.testint=1
                            self.isledoff=True
                            self.Delay_MSec(self.ledofftime)
                            #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                            #time.sleep(self.ledofftime//1000)
                            self.isledoff=False
                            #self.Delay_MSec(self.ledofftime)
                            #delaytime=self.ledofftime
                    elif self.rstate==4:
                        print("Gettemperature case")
                        print(self.testint)
                        if self.testint==0:
                            ql=self.ub.Gettemperature()
                            self.WriteData(ql)
                            self.StartTim()
                            cdata+="------AUTO 读LED温度--------\r\n"
                            # self.new.textBrowser.append("------AUTO 读LED温度--------\r\n")
                            self.ld.LogWriteInfo(cdata)
                            self.testint=1
                    elif self.rstate==5:
                        print("head06")
                        cdata+="------AUTO 测试次数"+str(self.autotime*self.testlayer+self.testindex)+"--------\r\n"
                        self.ld.LogWriteInfo(cdata)
                        self.rstate=6
                        if self.testindex==self.testlayer:
                            if self.testint==0:
                                ql=self.ub.PowerOff()
                                cdata+="------AUTO 关闭光机与风扇--------\r\n"
                                self.ld.LogWriteAuto(cdata)
                                cdata=""
                                self.WriteData(ql)
                                self.StartTim()
                                self.autotime+=1
                                self.testint=1
                                self.testindex=0
                        else:
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!############")
                            self.ld.LogWriteAuto(cdata)
                            cdata=""
            else:
                break

    '''
    数据校验
    '''
    def CheckBuff(self, buff):
        if self.isreadversion:
            vstr = buff.decode("utf-8")
            self.ShowMsg("读取软件版本："+vstr)
            self.isreadversion = False
        else:
            for e in buff:
                if e==0x2a and self.isok == False:
                    self.isok=True
                if self.isok:
                    self.lbuff.append(e)
                if self.isok and e == 0x0d:
                    self.ShowMsg("验证数据："+dh.HexString(self.lbuff))
                    self.GetData(self.lbuff)
                    self.isok=False
                    self.lbuff=[]

    """
    获取串口通讯的测试结果
    """
    def GetData(self, buff):
        if len(buff) >= 3:
            if buff[1] == 0xfa:
                self.ShowMsg("开机"+dh.GetRealState(buff[2]))
                self.ShowReceive(buff, "PowerOn")
                if buff[2] == 0x00 and self.isauto:
                    dh.Delay_MSec(250)
                    self.rstate = 1
                    self.testint = 0
                    self.StopTim()
                    if self.retrytimes >= 1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes = 0
            elif buff[1] == 0xfb:
                self.ShowMsg("PowerOff"+dh.GetRealState(buff[2]))
                self.ShowReceive(buff, "PowerOff")
                if buff[2] == 0x00 and self.isauto:
                    self.Delay_MSec(250)
                    self.rstate = 0
                    self.testint = 0
                    self.StopTim()
                    if self.retrytimes >= 1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+ str(self.retrytimes))
                        self.retrytimes = 0
            elif buff[1] == 0x4b:
                self.ShowMsg("LedOn" + dh.GetRealState(buff[2]))
                self.ShowReceive(buff, "LedOn")
                if buff[2] == 0x00 and self.isauto:
                    dh.Delay_MSec(250)
                    self.rstate = 3
                    self.testint = 0
                    self.StopTim()
                    if self.retrytimes >= 1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes = 0
            elif buff[1] == 0x47:
                self.ShowMsg("LedOff "+dh.GetRealState(buff[2]))
                self.ShowReceive(buff, "LedOff ")
                if buff[2] == 0x00 and self.isauto:
                    dh.Delay_MSec(250)
                    self.rstate = 4
                    self.testint = 0
                    print("自动化：", self.rstate)
                    self.StopTim()
                    if self.retrytimes >= 1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes = 0
            elif buff[1] == 0x53:
                self.ShowMsg("QueryLedState"+dh.GetRealState(buff[2]))
                self.ShowReceive(buff, "QueryLedState")
            elif buff[1] == 0xfc:
                self.ShowMsg("SaveCurrentAndImage" + dh.GetRealState(buff[2]))
                self.ShowReceive(buff, "SaveCurrentAndImage")
            elif buff[1] == 0xf9:
                self.ShowMsg("RefreshHdmi" + dh.GetRealState(buff[2]))
                self.ShowReceive(buff, "RefreshHdmi")
            elif buff[1] == 0x54:
                self.ShowMsg("SetLightCurrent"+dh.GetRealState(buff[2]))
                self.ShowReceive(buff, "SetLightCurrent")
                if buff[2]==0x00 and self.isauto:
                    self.Delay_MSec(250)
                    self.rstate=2
                    self.testint=0
                    self.StopTim()
                    if self.retrytimes>=1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes=0
            elif buff[1] == 0x4e:
                if buff[2]==0xff:
                    self.ShowMsg("Gettemperature error")
                    self.ShowReceive(buff,"Gettemperature")
                else:
                    self.ShowMsg("GetLedtemperature："+str(buff[2])+"摄氏度")
                    self.ShowReceive(buff,"GetLedtemperature："+str(buff[2])+"摄氏度")
                    if self.isauto:
                        self.Delay_MSec(250)
                        self.StopTim()
                        self.rstate=5
                        self.testint=0
                        self.ltmp=buff[2]
                        self.AddRecord(self.lightv,self.ltmp)
                        self.lightv=0
                        self.ltmp=0
                    if self.retrytimes>=1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes=0
            elif buff[1] == 0x4f:
                if buff[2] == 0xff:
                    self.ShowMsg("GetLedTime error")
                    self.ShowReceive(buff,"GetLedTime error")
                else:
                    self.ShowMsg("GetLedTime"+str(dh.GetRealInt([buff[2],buff[3]])))
                    self.ShowReceive(buff,"GetLedTime"+str(dh.GetRealInt([buff[2],buff[3]])))
            elif buff[1] == 0xfe:
                self.ShowMsg("clearLedTime"+dh.GetRealState(buff[2]))
                self.ShowReceive(buff,"clearLedTime")
            elif buff[1] == 0xf5:
                self.ShowMsg("GetVersion"+dh.GetRealState(buff[2]))
                self.ShowReceive(buff,"GetVersion")
            elif buff[1] == 0xef:
               self.ShowMsg("SetFan2Speed"+dh.GetRealState(buff[2]))
               self.ShowReceive(buff,"SetFan2Speed")
            elif buff[1] == 0xee:
               self.ShowMsg("SetFan1Speed"+dh.GetRealState(buff[2]))
               self.ShowReceive(buff,"SetFan1Speed")
            elif buff[1] == 0xf6:
               self.ShowMsg("SetImage"+dh.GetRealState(buff[2]))
               self.ShowReceive(buff,"SetImage")
            elif buff[1] == 0x54:
                if buff[2] == 0xff:
                    self.ShowMsg("GetPWMValue error")
                    self.ShowReceive(buff,"GetPWMValue error")
                else:
                    self.ShowMsg("GetPWMValue"+str(dh.GetRealInt([buff[2],buff[3]])))
                    self.ShowReceive(buff,"GetPWMValue"+str(dh.GetRealInt([buff[2],buff[3]])))

    def ShowMsg(self,s):
        # self.new.textBrowser.append(s)
        self.lstr+=s+"\r\n"
        self.scount+=1
        if self.scount>=200:
            # self.new.textBrowser.clear()
            self.scount=0
        if len(self.lstr)>=64:
            self.ld.LogWriteInfo(self.lstr)
            self.lstr=""
        # self.new.textBrowser.moveCursor(QtGui.QTextCursor.End)

    '''
    待转化成测试报告
    '''
    def ShowReceive(self,buff,text):
        data=dh.HexString(buff)
        # self.new.txt_receive.setText(data)
        if buff[3]==0xff:
            self.ld.LogWriteErr(text+"异常")
            pass
        else:
            pass
            self.ld.LogWriteInfo(text )

    '''
    通讯处理：测试结果数据获取
    '''
    def readData(self):
        lbyte=self.com.readLine()
        if len(lbyte)>0:
            lbuff=dh.bytestoint(lbyte)
            self.ShowMsg(dh.HexString(lbuff)+dh.GetTimeSmap(self.uarttime))
            self.CheckBuff(lbuff)

    '''
    通讯动作 action，所有用例都引用（更倾向于处理成静态方法）
    '''
    def WriteData(self, buff):
        if self.isopen:
            self.com.write_data(bytearray(buff))
            self.ld.LogWriteInfo("发送数据:"+dh.HexString(buff)+dh.GetTimeSmap(self.uarttime))
            # self.new.txt_send.setText(self.HexString(buff))

    def serachports(self):
        # 串口搜索
        pass

    def StartTim(self):
        self.wsec = 0
        self.waitcomtimer.start(1000)

    def StopTim(self):
        self.waitcomtimer.stop()
        self.wsec = 0

    def InitDb(self):

        path = "sqlite:///test.db"  # 存储记录用的数据库所在位置
        self.db=xmldbhelpper(Base, path)

    def AddRecord(self, lv, lt):
        p = PRecord()
        p.lvalue=lv
        p.ltmp=lt
        p.ldate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.plist.append(p)
        if len(self.plist)>=20:
            for e in self.plist:
                a=self.db.AddPRecord(e)
                if a=="aok":
                    print("数据存储成功")
                else:
                    print("数据存储失败！！！")
            self.plist=[]

    def OutExcel(self):
        sname = "out"
        sl = self.db.QueryAll()
        self.ex.MakeSaveEx(sname, sl)
