#coding:utf-8
from form.main import Ui_Dialog
from PySide2.QtWidgets import QMainWindow,QTreeWidgetItem,QFileDialog,QMessageBox,QApplication,QStyleFactory
from PySide2.QtCore import QTimer,Qt,QIODevice,QTime,QCoreApplication,QEventLoop
from PySide2 import QtGui
from PySide2.QtSerialPort import QSerialPort,QSerialPortInfo
from logwrite import LogData
import time
from ubyte import Ubyte
from readini import GetTestTime
from imgshow import SWindow
from dbase import PRecord,xmldbhelpper
from sqlalchemy.ext.declarative import declarative_base
from readlight import readcom
import datetime
from exhelpper import Exhelp
from setsendmsgform import SetSmsgwindow

Base = declarative_base()
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dk=None
        self.new =Ui_Dialog()
        self.new.setupUi(self)
        #etime=time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        self.setWindowTitle("UartLight Test 20210728")
        self.InitData()

    def InitData(self):
        self.serachports()
        self.com=QSerialPort()
        self.com.readyRead.connect(self.readData)
        self.isopen=False
        self.new.btn_open.clicked.connect(self.openCom)
        self.new.btn_serach.clicked.connect(self.serachports)
        self.lbuff=[]
        self.isok=False
        self.ld=LogData()
        self.lstr=""
        self.scount=0
        self.ub=Ubyte()
        self.isauto=False
        self.isreadversion=False
        self.new.cb_test.clear()
        self.new.cb_test.addItems(self.ub.GetTestHeads())
        self.new.cb_test.addItem("自动化")
        self.new.btn_send.clicked.connect(self.SendTest)
        self.new.btn_showimg.clicked.connect(self.ShowImage)
        self.new.btn_searchpho.clicked.connect(self.serachports)
        self.new.btn_openpho.clicked.connect(self.OpenPhoCom)
        self.new.btn_setcurrent.clicked.connect(self.SetCurrent)
        self.new.btn_crc.clicked.connect(self.SendBytesByStr)
        self.new.btn_readpho.clicked.connect(self.TestLightPho)
        self.new.btn_outexl.clicked.connect(self.OutExcel)
        self.new.btn_set.clicked.connect(self.ShowSetW)
        self.w =SWindow()
        self.plist=[]
        self.testindex=0
        self.InitDb()
        self.rstate=0
        self.imglist=["f.png","light.png","s10.png","black.png"]
        self.lightv=0
        self.ltmp=0
        self.slist=GetTestTime("set.ini")
        print("读取配置：",self.slist)
        self.testtime=self.slist["printtimes"]
        self.testlayer=self.slist["printlayer"]
        self.ci=self.slist["ci"]
        self.ub.SetIni(self.slist)
        self.new.cb_comname.setCurrentText(self.slist["comname"])
        self.openCom()
        self.new.cb_pho.setCurrentText(self.slist["phocom"])
        self.OpenPhoCom()
        self.testint=0
        self.starttime=None
        self.readlightv=self.slist["lightv"]
        self.ledontime=self.slist["ledontime"]
        self.ledofftime=self.slist["ledofftime"]
        self.ex=Exhelp()
        self.worktime=self.slist["worktime"]
        self.resttime=self.slist["resttime"]
        self.sw=SetSmsgwindow()
        self.sw._signal.connect(self.callsw)
        self.imgtype=0
        self.autotime=0
        print("------AUTO 测试次数"+str(self.autotime*self.testlayer+self.testindex)+"--------\r\n")
        self.isledoff=False
        #定时器开启，用于判断数据是否超时,发送数据后按1秒来执行
        self.readwaittime=self.slist["waittime"]
        self.waitcomtimer= QTimer()
        self.waitcomtimer.setTimerType(Qt.PreciseTimer)
        self.waitcomtimer.timeout.connect(self.callwait)
        self.wsec=0#用于判断是否超时
        self.retrytimes=0#重试次数
        self.uarttime=0

    def StartTim(self):
        self.wsec=0
        self.waitcomtimer.start(1000)

    def StopTim(self):
        self.waitcomtimer.stop()
        self.wsec=0

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
                self.waitcomtimer.stop()
                self.retrytimes+=1
            else:
                self.ShowMsg("重试次数超出3次，不再重试！！！！")
                self.ShowMsg("重试次数超出3次，不再重试！！！！")
                self.ShowMsg("重试次数超出3次，不再重试！！！！")
                self.ShowMsg("重试次数超出3次，不再重试！！！！")
                self.ShowMsg("重试次数超出3次，不再重试！！！！")

    def GetTimeSmap(self):
        t = time.time()
        tmp=int(round(t * 1000))
        rtmp=0
        try:
            rtmp=tmp-self.uarttime
        except Exception as e:
            print(str(e))
        return str(rtmp)
        
    def callsw(self,msg):
        print(msg)
        data=self.ub.GetNameData(msg)
        self.WriteData(data)

    def ShowSetW(self):
        text=self.new.cb_test.currentText()
        sl=self.ub.GetSetIniData(text)
        self.sw.SetMsg(sl)
        self.sw.show()

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

    def OutExcel(self):
        sname="out"
        sl=self.db.QueryAll()
        self.ex.MakeSaveEx(sname,sl)
        self.ShowBox("EXCLE导出成功！！")

    def GetTime10min(self):
        for i in range(0,self.resttime):
            self.Delay_MSec(1000)
            self.ShowMsg("运行一小时，等待休息时间："+str(i))

    def OpenPhoCom(self):
        try:
            text=self.new.btn_openpho.text()
            if text=="打开":
                self.rc=readcom(self.new.cb_pho.currentText())
                self.rc.InitCOm(9600)
                self.rc.OpenCom()
                self.new.btn_openpho.setText("关闭")
                self.new.btn_openpho.setStyleSheet("background-color:gold")
                self.uarttime=self.GetTimeSmap()
            elif text=="关闭":
                self.rc.CloseCom()
                self.new.btn_openpho.setText("打开")
                self.new.btn_openpho.setStyleSheet("")
        except Exception as e:
            self.ShowMsg("光度计串口设置失败："+str(e))

    def SetCurrent(self):
        try:
            cs=self.new.txt_current.text()
            ci=int(cs)
            self.ci=ci
            self.slist["ci"]=ci
            self.ub.SetIni(self.slist)
        except Exception as e:
            self.ShowMsg("设置电流失败："+str(e))

    def HexToBytes(self,dstr):
        sl=dstr.split(" ")
        bl=[]
        if len(sl)>0:
            for e in sl:
                bl.append(int(e,16))
        return bl

    def SendBytesByStr(self):
        hexstr=self.new.txt_send.text()
        if len(hexstr)>0:
            hexstr=hexstr.rstrip()
            bl=self.HexToBytes(hexstr)
            self.WriteData(bl)

    def TestLightPho(self):
        try:
            lv=self.rc.ReadData()
            self.ShowMsg("光强值："+str(lv))
        except Exception as e:
            self.ShowMsg("读取光度计失败："+str(e))
    """
    数据库相关操作
    """
    def InitDb(self):
        path="sqlite:///test.db"
        self.db=xmldbhelpper(Base,path)

    def AddRecord(self,lv,lt):
        p=PRecord()
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
    """
    结束数据库操作
    """
    def GetRealValue(self,sl):
        slen=len(sl)
        maxv=0.0
        minv=0.0
        sumv=0.0
        for i in range(0,slen):
            if i==0:
                maxv=float(sl[i])
                minv=float(sl[i])
            else:
                if float(sl[i])>maxv:
                    maxv=float(sl[i])
                if float(sl[i])<minv:
                    minv=float(sl[i])
            sumv+=float(sl[i])
        ev=(sumv-maxv-minv)//(slen-2)
        return ev

    def SetDk(self,dk):
        self.dk=dk

    def ShowImage(self):
        if self.w.isVisible():
            self.w.close()
        else:
            if self.dk:
                dc=self.dk.screenCount()
                print(dc)
                if dc==2:
                    self.w.setGeometry(self.dk.screenGeometry(1))
                else:
                    self.w.setGeometry(self.dk.screenGeometry(0))
                self.w.showFullScreen()

    def Delay_MSec(self,msec):
        t = QTime.currentTime().addMSecs(msec)
        while( QTime.currentTime() < t ):
            QCoreApplication.processEvents(QEventLoop.AllEvents, 100)

    def ChangImage(self,b):
        if b==0:
            self.w.LoadImg("f.png")
        elif b==1:
            self.w.LoadImg("s10.png")
        elif b==2:
            self.w.LoadImg("light.png")
        elif b==3:
            self.w.LoadImg("black.png")

    def StartAutoTest(self,text):
        if text=="发送":
            self.new.btn_send.setText("关闭")
            self.new.btn_send.setStyleSheet("background-color:gold")
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
        elif text=="关闭":
            self.new.btn_send.setText("发送")
            self.isauto=False
            self.new.btn_send.setStyleSheet("")

    def SendTest(self):
        text=self.new.cb_test.currentText()
        if text=="自动化":
            btext=self.new.btn_send.text()
            self.StartAutoTest(btext)
        else:
            buff=self.ub.GetSendData(text)
            self.WriteData(buff)
    
    def RunTest(self):
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
                        print("head0")
                        if self.GetTimeOneHr():
                            self.GetTime10min()
                        if self.autotime<self.testtime:
                            ql=self.ub.PowerOn()
                            if self.testint==0:
                                self.WriteData(ql)
                                self.StartTim()
                                cdata+="------AUTO 开机--------\r\n"
                                self.new.textBrowser.append("------AUTO 开机--------\r\n")
                                self.testint=1
                        else:
                            print("head09")
                            cdata+="测试已完成"
                            self.new.textBrowser.append("------测试完成--------\r\n")
                            self.ld.LogWriteAuto(cdata)
                            cdata=""
                            break
                    elif self.rstate==1:
                        print("head01")
                        if self.testint==0:
                            ql=self.ub.LedOff()
                            self.WriteData(ql)
                            self.StartTim()
                            cdata+="------AUTO LED OFF--------\r\n"
                            self.new.textBrowser.append("------AUTO LED OFF--------\r\n")
                            self.testint=1
                    elif (self.rstate==4 and self.testindex==0) or (self.rstate==6):
                        print("head02")
                        if self.testint==0:
                            if self.imgtype==1:
                                self.w.LoadImg(self.imglist[1])
                                cdata+="------AUTO 设置背景图 光强校准--------\r\n"
                                self.new.textBrowser.append("------AUTO 设置背景图 光强校准--------\r\n")
                                self.imgtype=2
                            elif self.imgtype==2:
                                self.w.LoadImg(self.imglist[2])
                                cdata+="------AUTO 设置背景图 马克图--------\r\n"
                                self.new.textBrowser.append("------AUTO 设置背景图 马克图--------\r\n")
                                self.imgtype=0
                            elif self.imgtype==0:
                                self.w.LoadImg(self.imglist[0])
                                cdata+="------AUTO 设置背景图 白图--------\r\n"
                                self.new.textBrowser.append("------AUTO 设置背景图 白图--------\r\n")
                                self.imgtype=1
                            bl=self.ub.IntToByte(self.ci)
                            ql=self.ub.SetLightCurrent(bl[0],bl[1],bl[0],bl[1],bl[0],bl[1])
                            self.WriteData(ql)
                            self.StartTim()
                            cdata+="------AUTO 设置电流 "+str(self.ci)+"--------\r\n"
                            self.new.textBrowser.append("------AUTO 设置电流 "+str(self.ci)+"--------\r\n")
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
                            self.w.LoadImg(self.imglist[3])
                            cdata+="------AUTO 设置背景图 黑图--------\r\n"
                            self.new.textBrowser.append("------AUTO 设置背景图 黑图--------\r\n")
                            ql=self.ub.LedOff()
                            self.WriteData(ql)
                            self.StartTim()
                            cdata+="------AUTO LED OFF 3秒--------\r\n"
                            self.new.textBrowser.append("------AUTO LED OFF 3秒--------\r\n")
                            self.testint=1
                            self.isledoff=True
                            self.Delay_MSec(self.ledofftime)
                            #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                            #time.sleep(self.ledofftime//1000)
                            #print("##############################")
                            self.isledoff=False
                            #self.Delay_MSec(self.ledofftime)
                            #delaytime=self.ledofftime
                    elif self.rstate==4:
                        print("head05")
                        print(self.testint)
                        if self.testint==0:
                            ql=self.ub.Gettemperature()
                            self.WriteData(ql)
                            self.StartTim()
                            cdata+="------AUTO 读LED温度--------\r\n"
                            self.new.textBrowser.append("------AUTO 读LED温度--------\r\n")
                            self.testint=1
                    elif self.rstate==5:
                        print("head06")
                        cdata+="------AUTO 测试次数"+str(self.autotime*self.testlayer+self.testindex)+"--------\r\n"
                        self.new.textBrowser.append("------AUTO 测试次数"+str(self.autotime*self.testlayer+self.testindex)+"--------\r\n")
                        self.rstate=6
                        if self.testindex==self.testlayer:
                            if self.testint==0:
                                ql=self.ub.PowerOff()
                                cdata+="------AUTO 关闭光机与风扇--------\r\n"
                                self.new.textBrowser.append("------AUTO 关闭光机与风扇--------\r\n")
                                #self.new.textBrowser.append(cdata)
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

    def openCom(self):
        try:
            text=self.new.btn_open.text()
            if text=="打开":
                if self.com.isOpen():
                    self.com.close()
                self.com.setPortName(self.new.cb_comname.currentText())
                self.com.setBaudRate(9600)
                self.com.setParity(QSerialPort.NoParity)
                if self.com.open(QIODevice.ReadWrite):
                    self.com.setDataTerminalReady(True)
                else:
                    print("open file")
                self.new.btn_open.setText("关闭")
                self.new.btn_open.setStyleSheet("background:gold")
                self.isopen=True
                self.ShowMsg("串口打开成功")
            elif text=="关闭":
                self.com.close()
                self.new.btn_open.setText("打开")
                self.new.btn_open.setStyleSheet("")
                self.isopen=False
                self.ShowMsg("串口关闭成功")
        except Exception as e:
            self.ShowMsg("光机串口打开失败："+str(e))

    def CheckBuff(self,buff):
        if self.isreadversion:
            vstr=buff.decode("utf-8")
            self.ShowMsg("读取软件版本："+vstr)
            self.isreadversion=False
        else:
            for e in buff:
                if e==0x2a and self.isok==False:
                    self.isok=True
                if self.isok:
                    self.lbuff.append(e)
                if self.isok and e==0x0d:
                    self.ShowMsg("验证数据："+self.HexString(self.lbuff))
                    self.GetData(self.lbuff)
                    self.isok=False
                    self.lbuff=[]

    def GetRealState(self,b):
        s=""
        if b==0x00:
            s="正常"
        elif b==0xff:
            s="异常"
        else:
            s="其他异常"+hex(b)
        return s

    def GetRealInt(self,bl):
        b=(bl[1]//16)*16*16*16+(bl[1]%16)*16*16+(bl[0]//16)*16+bl[0]%16
        return b

    def GetData(self,buff):
        if len(buff)>=3:
            if buff[1]==0xfa:
                self.ShowMsg("开机"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"开机")
                if buff[2]==0x00 and self.isauto:
                    self.Delay_MSec(250)
                    self.rstate=1
                    self.testint=0
                    self.StopTim()
                    if self.retrytimes>=1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes=0
            elif buff[1]==0xfb:
                self.ShowMsg("关机"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"关机")
                if buff[2]==0x00 and self.isauto:
                    self.Delay_MSec(250)
                    self.rstate=0
                    self.testint=0
                    self.StopTim()
                    if self.retrytimes>=1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes=0
            elif buff[1]==0x4b:
                self.ShowMsg("LED ON"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"LED ON")
                if buff[2]==0x00 and self.isauto:
                    self.Delay_MSec(250)
                    self.rstate=3
                    self.testint=0
                    self.StopTim()
                    if self.retrytimes>=1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes=0
            elif buff[1]==0x47:
                self.ShowMsg("LED OFF"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"LED OFF")
                if buff[2]==0x00 and self.isauto:
                    self.Delay_MSec(250)
                    self.rstate=4
                    self.testint=0
                    print("自动化：",self.rstate)
                    self.StopTim()
                    if self.retrytimes>=1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes=0
            elif buff[1]==0x53:
                self.ShowMsg("查询LED状态"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"查询LED状态")
            elif buff[1]==0xfc:
                self.ShowMsg("保存电流与画面翻转"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"保存电流与画面翻转")
            elif buff[1]==0xf9:
                self.ShowMsg("刷新HDMI"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"刷新HDMI")
            elif buff[1]==0x54:
                self.ShowMsg("设置电流值"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"设置电流值")
                if buff[2]==0x00 and self.isauto:
                    self.Delay_MSec(250)
                    self.rstate=2
                    self.testint=0
                    self.StopTim()
                    if self.retrytimes>=1:
                        self.ShowMsg("数据回传成功，对重试次数清0，当前重试次数："+str(self.retrytimes))
                        self.retrytimes=0
            elif buff[1]==0x4e:
                if buff[2]==0xff:
                    self.ShowMsg("获取LED温度异常")
                    self.ShowReceive(buff,"获取LED温度")
                else:
                    self.ShowMsg("LED温度："+str(buff[2])+"摄氏度")
                    self.ShowReceive(buff,"LED温度："+str(buff[2])+"摄氏度")
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
            elif buff[1]==0x4f:
                if buff[2]==0xff:
                    self.ShowMsg("LED工作时间获取错误")
                    self.ShowReceive(buff,"LED工作时间获取错误")
                else:
                    self.ShowMsg("LED工作时间"+str(self.GetRealInt([buff[2],buff[3]])))
                    self.ShowReceive(buff,"LED工作时间"+str(self.GetRealInt([buff[2],buff[3]])))
            elif buff[1]==0xfe:
                self.ShowMsg("重置LED电流"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"重置LED电流")
            elif buff[1]==0xf5:
                self.ShowMsg("获取软件版本"+self.GetRealState(buff[2]))
                self.ShowReceive(buff,"获取软件版本")
            elif buff[1]==0xef:
               self.ShowMsg("设置风扇2通道转速"+self.GetRealState(buff[2])) 
               self.ShowReceive(buff,"设置风扇2通道转速")
            elif buff[1]==0xee:
               self.ShowMsg("设置风扇1通道转速"+self.GetRealState(buff[2])) 
               self.ShowReceive(buff,"设置风扇1通道转速")
            elif buff[1]==0xf6:
               self.ShowMsg("设置画面翻转"+self.GetRealState(buff[2]))
               self.ShowReceive(buff,"设置画面翻转")
            elif buff[1]==0x54:
                if buff[2]==0xff:
                    self.ShowMsg("获取PWM值异常")
                    self.ShowReceive(buff,"获取PWM值异常")
                else:
                    self.ShowMsg("获取PWM值"+str(self.GetRealInt([buff[2],buff[3]])))
                    self.ShowReceive(buff,"获取PWM值"+str(self.GetRealInt([buff[2],buff[3]])))

    def HexString(self,bl):
        s=""
        blen=len(bl)
        for i in range(0,blen):
            if i==blen-1:
                s+=hex(bl[i])
            else:
                s+=hex(bl[i])+" "
        return s

    def bytestoint(self,buff):
        blist=[]
        for e in buff:
            blist.append(int.from_bytes(e,byteorder='big',signed=False))
        return blist

    def ShowMsg(self,s):
        self.new.textBrowser.append(s)
        self.lstr+=s+"\r\n"
        self.scount+=1
        if self.scount>=200:
            self.new.textBrowser.clear()
            self.scount=0
        if len(self.lstr)>=64:
            self.ld.LogWriteInfo(self.lstr)
            self.lstr=""
        self.new.textBrowser.moveCursor(QtGui.QTextCursor.End)

    def ShowReceive(self,buff,text):
        data=self.HexString(buff)
        self.new.txt_receive.setText(data)
        if buff[3]==0xff:
            self.new.lab_info.setText("<font color=\"#FF0000\">"+text+"异常</font> ")
        else:
            self.new.lab_info.setText("<font color=\"#0000FF\">"+text+"</font> ")

    def readData(self):
        lbyte=self.com.readLine()
        if len(lbyte)>0:
            lbuff=self.bytestoint(lbyte)
            self.ShowMsg(self.HexString(lbuff)+self.GetTimeSmap())
            self.CheckBuff(lbuff)

    def WriteData(self,buff):
        if self.isopen:
            self.com.write(bytearray(buff))
            self.ShowMsg("发送数据:"+self.HexString(buff)+self.GetTimeSmap())
            self.new.txt_send.setText(self.HexString(buff))

    def serachports(self):
        comlist=QSerialPortInfo.availablePorts()
        self.new.cb_comname.clear()
        self.new.cb_pho.clear()
        for e in comlist:
            self.new.cb_comname.addItem(e.portName())
            self.new.cb_pho.addItem(e.portName())

    def ShowBox(self,msg):
        reply = QMessageBox.information(self, "串口测试", msg, QMessageBox.Yes)
			
    def closeEvent(self, event):
        try:
            if self.w.isVisible():
                self.w.close()
        except Exception as e:
            print(e)
        reply = QMessageBox.question(self, "串口测试", "您确定要退出吗？", QMessageBox.Yes |
                                QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()