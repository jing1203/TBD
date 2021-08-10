#coding:utf-8
"""
用于判断是否存在投光，并统计每次投光的时长与次数
"""
from logging import Manager, setLogRecordFactory
from sqlalchemy.sql.expression import false, true
from logwrite import LogData
from readnewlight import readcom2
from readlight import readcom
import threading,time,random
from sqlalchemy.ext.declarative import declarative_base
from dbase import InitDb,AddP,CloseDb,PRecord
from readini import GetTestSet
from threading import Lock, local

Base = declarative_base()

class RecordLight():
    def __init__(self):
        self.ld=LogData()   # 转html报告
        self.isopen=False   # 环境配置  fixture
        self.ledon=False    # 传感器
        self.lightlist=[]
        self.uarttime=0
        self.starttime=0
        self.endtime=0
        self.midtime=0
        self.ldata=""
        self.isinitdb=false
        self.ismodel=False

        self.modelname=""
        self.lightvalue=0#光度计的值
        self.issupport=0#判断是否支撑层
        self.newlv=0#光照计的值
        self.time1=0#支撑层时长
        self.time2=0#投光时长
        self.lightmax=0#紫外光强的最大值
        self.supportlight=0#支撑层的最大光强值
        self.layer=0
        self.plist=[]

        path="sqlite:///test.db"
        self.db2=InitDb(path)
        self.setlist=GetTestSet("power.ini")
        self.GetSetDate()

    def GetSetDate(self):
        if len(self.setlist)>0:
            self.p1_layer1=self.setlist["p1v"]
            self.p1_layerother=self.setlist["p1v2"]
            self.p2v=self.setlist["p2v"]
            self.p1time=self.setlist["p1layer1"]
            self.p1b2=self.setlist["p1b2"]
            self.p1b20=self.setlist["p1b20"]
            self.p1o=self.setlist["p1o"]
            self.p2time=self.setlist["p2time"]
            self.c1=self.setlist["c1"]
            self.b1=self.setlist["b1"]
            self.c2=self.setlist["c2"]
            self.b2=self.setlist["b2"]
            self.minlux=self.setlist["minlux"]
            self.midlux=self.setlist["midlux"]
            self.minmid=self.setlist["midlux1"]
            print(self.setlist)

    def InitCom(self): # 初始化传感器
        comname=self.c1
        self.rc=readcom2(comname)
        self.rc.InitCom(self.b1)
        self.isopen=self.rc.OpenCom()
        self.InitLight()

    def InitLight(self):   # 初始化光度计
        self.oldrc=readcom(self.c2)
        self.oldrc.InitCom(self.b2)
        self.oldrc.OpenCom()

    """
    lvalue = Column(String(64))#光照计的强度值
	ltmp = Column(String(64))#光度计的强度值
	modelname =Column(String(64))#数据库中关联的唯一值
	time1 = Column(String(64))#支撑层曝光时长
	time2 = Column(String(64))#实体层曝光时长
    """
    def Savedata(self):
        p=PRecord()
        p.lvalue=str(self.newlv)
        p.ltmp=str(self.lightvalue)
        p.modelname=self.modelname
        p.time1=str(self.time1)
        p.time2=str(self.time2)
        p.ldate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        p.layer=str(self.layer)
        self.plist.append(p)
        if len(self.plist)>10:
            for e in self.plist:
                s=AddP(e,self.db)
                if s=="aok":
                    pass
                    #self.ShowMsg("数据存储成功！！")
                else:
                    self.ShowMsg("数据存储失败！"+s)
            self.plist.clear()

    def ShowMsg(self,s):
        print(s)
        self.ldata+=s+"\r\n"
        if len(self.ldata)>128:
            self.ld.LogWriteInfo(self.ldata)
            self.ldata=""

    def ReadOldLight(self):
        if self.isinitdb==false:
            path="sqlite:///test.db"
            self.db=InitDb(path)
            self.isinitdb=true
        while True:    #  用例执行指定次数
            try:
                if self.ledon and self.oldrc:  # 测试前置条件：光度计和传感器同时拥有数据
                    lv=self.oldrc.ReadData()
                    self.lightvalue=lv
                    #self.ShowMsg("紫外光强："+str(lv))
                    if self.lightmax<lv:
                        self.lightmax=lv
                        self.ShowMsg("最大紫外光强："+str(self.lightmax))
                        #print("h1-----------"+str(self.issupport))
                    if self.issupport==1 and self.supportlight<lv and lv <15.5:
                        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                        self.supportlight=lv
                        self.ShowMsg("支撑层最大紫外光强："+str(self.supportlight))
                    if lv>0.1:
                        self.Savedata()
                time.sleep(0.1)
            except Exception as e:
                print(e)

    def GetModelName(self):
        mname=""
        print("get model name")
        while True:
            mname=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))+str(random.randint(1000,2000))
            #print("mname1:",mname)
            if self.db2.QueryCount(mname):
                break
        #print(mname)
        return mname

    def DoTimer(self):   #  公用方法
        self.uarttime=int(self.GetTimeSmap())
        self.rt1 = threading.Thread(target = self.DoReceiveAll)
        #self.rt2=threading.Thread(target=self.ReadOldLight)
        self.rt1.start()
        self.ReadOldLight()
        #self.rt2.start()
        #self.rt1.join()
        #self.rt2.join()

    def GetTimeSmap(self):   #  公用方法
        t = time.time()
        tmp=int(round(t * 1000))
        rtmp=0
        try:
            rtmp=tmp-self.uarttime
        except Exception as e:
            print(str(e))
        return str(rtmp)

    def CheckValue(self,layer):   # 用例名称及校验
        if layer==1:
            if self.lightmax>=self.p1_layer1-1 and self.lightmax <= self.p1_layer1+1:
                self.ShowMsg("@@@P1光强校验通过@@@ layer:"+str(layer)+" "+str(self.lightmax))
            else:
                self.ShowMsg("@@@P1光强校验失败！！！！！@@@ layer:"+str(layer)+" "+str(self.lightmax))
            if self.issupport==1:
                if self.supportlight>=self.p2v-1 and self.supportlight <= self.p2v+1:
                    self.ShowMsg("@@@P2光强校验通过@@@ layer:"+str(layer))
                else:
                    self.ShowMsg("@@@P2光强校验失败！！！！@@@ layer:"+str(layer))
                if self.time1>=self.p2time-750 and self.time1 <= self.p2time+750:
                    self.ShowMsg("@@@P2时长校验通过@@@ layer:"+str(layer))
                else:
                    self.ShowMsg("@@@P2时长校验失败！！！！@@@ layer:"+str(layer)+" "+str(self.time1))
            if self.time2>=self.p1time+self.p2time-750 and self.time2<=self.p1time+self.p2time+750:
                self.ShowMsg("@@@P1投光时长校验通过@@@ layer:"+str(layer))
            else:
                self.ShowMsg("@@@P1投光时长校验失败！！！！@@@ layer:"+str(layer)+" "+str(self.time2))
        elif layer>=2 and layer<=20:
            if self.lightmax>=self.p1_layerother-1 and self.lightmax <= self.p1_layerother+1:
                self.ShowMsg("@@@P1光强校验通过@@@ layer:"+str(layer))
            else:
                self.ShowMsg("@@@P1光强校验失败！！！！@@@ layer:"+str(layer))
            if self.issupport==1:
                if self.supportlight>=self.p2v-1 and self.supportlight <= self.p2v+1:
                    self.ShowMsg("@@@P2光强校验通过@@@ layer:"+str(layer))
                else:
                    self.ShowMsg("@@@P2光强校验失败！！！！@@@ layer:"+str(layer))
                if self.time1>=self.p2time-750 and self.time1 <= self.p2time+750:
                    self.ShowMsg("@@@P2时长校验通过@@@ layer:"+str(layer))
                else:
                    self.ShowMsg("@@@P2时长校验失败！！！！@@@ layer:"+str(layer)+" "+str(self.time1))
            if self.time2 >= self.p1b20+self.p2time-750 and self.time2 <= self.p1b2+self.p2time+750:
                self.ShowMsg("@@P1B时间校验通过@@@ layer："+str(layer))
            else:
                self.ShowMsg("@@P1B时间校验失败！！！！@@@ layer："+str(layer)+" "+str(self.time2))
        elif layer>20:
            if self.lightmax>=self.p1_layerother-1 and self.lightmax <= self.p1_layerother+1:
                self.ShowMsg("@@@P1光强校验通过@@@ layer:"+str(layer))
            else:
                self.ShowMsg("@@@P1光强校验失败！！！！@@@ layer:"+str(layer))
            if self.issupport==1:
                if self.supportlight>=self.p2v-1 and self.supportlight <= self.p2v+1:
                    self.ShowMsg("@@@P2光强校验通过@@@ layer:"+str(layer))
                else:
                    self.ShowMsg("@@@P2光强校验失败！！！！@@@ layer:"+str(layer))
                if layer>=21 and layer<=25:
                    if self.time1>=self.p2time+self.p1o-750 and self.time1 <= self.p2time+self.p1o+750:
                        self.ShowMsg("@@@P2时长校验通过@@@ layer:"+str(layer))
                    else:
                        self.ShowMsg("@@@P2时长校验失败！！！！@@@ layer:"+str(layer)+" "+str(self.time1))
                else:
                    if self.time1>=self.p2time-750 and self.time1 <= self.p2time+750:
                        self.ShowMsg("@@@P2时长校验通过@@@ layer:"+str(layer))
                    else:
                        self.ShowMsg("@@@P2时长校验失败！！！！@@@ layer:"+str(layer)+" "+str(self.time1))
            if self.issupport==1:
                if self.time2 >= self.p1o+self.p2time-750 and self.time2 <= self.p1o+self.p2time+750:
                    self.ShowMsg("@@P1B时间校验通过1111@@@ layer："+str(layer))
                else:
                     self.ShowMsg("@@P1B时间校验失败1111！！！！@@@ layer："+str(layer)+" "+str(self.time2))
            else:
                if self.time2 >= self.p1o-750 and self.time2 <= self.p1o+750:
                    self.ShowMsg("@@P1B时间校验通过2222@@@ layer："+str(layer))
                else:
                    self.ShowMsg("@@P1B时间校验失败2222！！！！@@@ layer："+str(layer)+" "+str(self.time2))

    def DoReceiveAll(self):
        ltimes=0
        offtimes=0
        layer=0
        maxv=0
        ztimes=0
        lock=Lock()
        while True:
            if self.rc and self.isopen==True:
                lv=self.rc.ReadData()
                if lv<5:
                    offtimes+=1
                else:
                    offtimes=0
                if offtimes>100:
                    self.ShowMsg("光度计数据低，未发现投光")
                    if self.ismodel==True:
                        self.ShowMsg("模型验证完成---------------")
                        self.ShowMsg("模型验证完成---------------")
                        self.ShowMsg("模型验证完成---------------")
                        self.ShowMsg("模型验证完成---------------")
                        self.ismodel=False
                        self.modelname=""
                    offtimes=0
                    layer=0
                    self.layer=layer
                if lv>0:  # light value
                    #self.Savedata(str(lv),"tmp")
                    #self.ShowMsg("光照数据："+str(lv))
                    if lv> maxv:
                        maxv=lv
                    if lv>self.minlux and self.ledon==False:
                        self.newlv=lv
                        ltimes+=1
                        if ltimes>=1:
                            ltimes=0
                            self.ShowMsg("LED ON___________")
                            self.ledon=True
                            layer+=1
                            self.layer=layer
                            if layer==1 and self.ismodel==False:
                                self.ismodel=True
                                self.modelname=self.GetModelName()
                                self.ShowMsg("开始模型验证")
                                #self.Savedata()
                            self.ShowMsg("开始识别模型层数："+str(layer))
                            self.starttime=int(self.GetTimeSmap())
                            self.lightlist.append(lv)
                            self.ShowMsg("LED ON starttime:"+str(self.starttime))
                    else:
                        if self.ledon==True and lv<=self.minlux:
                            self.newlv=lv
                            ltimes+=1
                            if ltimes>=1:
                                self.ledon=False
                                self.ShowMsg("LED OFF___________")
                                self.endtime=int(self.GetTimeSmap())
                                lighttime=self.endtime-self.starttime
                                self.time2=lighttime
                                self.ShowMsg("LED OFF endtime:"+str(self.endtime))
                                if maxv<100:
                                    self.time1=self.endtime-self.starttime
                                    self.ShowMsg("-------------支撑层投光时长1："+str(self.endtime-self.starttime))
                                else:
                                    if self.midtime>0:
                                        self.time1=self.endtime-self.midtime
                                        self.ShowMsg("-------------支撑层投光时长2："+str(self.endtime-self.midtime))
                                self.ShowMsg("-------------投光时长："+str(lighttime))
                                #self.Savedata()
                                self.CheckValue(layer)
                                lock.acquire()
                                self.starttime=0
                                self.midtime=0
                                self.endtime=0
                                self.time1=0
                                self.time2=0
                                self.lightmax=0
                                self.issupport=0
                                self.supportlight=0
                                lock.release()
                                maxv=0
                        elif self.ledon==True and lv>self.minmid and lv <self.midlux:
                            if self.midtime==0 and((self.lightmax>self.p1_layer1-1 and layer==1) or(self.lightmax>self.p1_layerother-1 and layer>1 and layer<31)):
                                ztimes+=1
                                if ztimes>=2:
                                    self.midtime=int(self.GetTimeSmap())
                                    #self.Savedata()
                                    self.ShowMsg("支撑层开始时间:"+str(self.midtime))
                                    lock.acquire()
                                    self.issupport=1
                                    lock.release()
                                    #print("issupport True:"+str(self.issupport))
                                    ztimes=0

rl=RecordLight()
rl.InitCom()
rl.DoTimer()
