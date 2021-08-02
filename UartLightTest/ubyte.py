#coding:utf-8



class Ubyte():
    def __init__(self):
        self.speed1=60
        self.speed2=60
        self.ci=400

    def SetIni(self,slist):
        self.slist=slist
        self.speed1=self.slist["fspeed1"]
        self.speed2=self.slist["fspeed2"]
        self.ci=self.slist["ci"]

    def GetSetIniData(self,head):
        sl={}
        dl={}
        if head=="设置光机电流":
            dl={"电流值":str(self.ci)}
        elif head=="设置风扇2":
            dl={"风扇通道2":str(self.speed2)}
        elif head=="设置风扇1":
            dl={"风扇通道1":str(self.speed1)}
        sl={"name":head,"data":dl}
        return sl

    def GetNameData(self,sl):
        head=sl["name"]
        dl=sl["data"]
        if head=="设置光机电流":
            bl=self.IntToByte(int(dl[0][1]))
            data=self.SetLightCurrent(bl[0],bl[1],bl[0],bl[1],bl[0],bl[1])
        elif head=="设置风扇2":
            print(dl[0][1])
            data=self.SetFan2Speed(int(dl[0][1]))
        elif head=="设置风扇1":
            print(dl[0][1])
            data=self.SetFan1Speed(int(dl[0][1]))
        return data

    def PowerOn(self):
        buff=[0x2a,0xfa,0x0d]
        return buff
    """
    关闭风扇与LED
    """
    def PowerOff(self):
        buff=[0x2a,0xfb,0x0d]
        return buff

    def LedOn(self):
        buff = [0x2a, 0x4b, 0x0d]
        return buff

    def LedOff(self):
        buff=[0x2a,0x47,0x0d]
        return buff

    def QueryState(self):
        buff=[0x2a,0x53,0x0d]
        return buff

    def SaveCurrentAndImage(self):
        buff=[0x2a,0xfc,0x0d]
        return buff

    def RefreshHdmi(self):
        buff=[0x2a,0xf9,0x0d]
        return buff

    def SetLightCurrent(self,rl,rm,gl,gm,bl,bm):
        buff=[0x55,0x07,0x54]
        buff.append(rl)
        buff.append(rm)
        buff.append(gl)
        buff.append(gm)
        buff.append(bl)
        buff.append(bm)
        buff.append(self.GetChecknum(buff))
        return buff

    def Gettemperature(self):
        buff=[0x2a,0x4e,0x0d]
        return buff

    def GetLedTime(self):
        buff=[0x2a,0x4f,0x0d]
        return buff

    def clearLedTime(self):
        buff=[0x2a,0xfe,0x0d]
        return buff

    def GetVersion(self):
        buff=[0x2a,0xf5,0x0d]
        return buff

    """
    b的范围0-100
    """
    def SetFan2Speed(self,b):
        buff=[0x2a,0xef,b]
        return buff

    """
    b的范围0-100
    """
    def SetFan1Speed(self,b):
        buff=[0x2a,0xee,b]
        return buff

    """
    b可以设置为0-3
    """
    def SetImage(self,b):
        buff=[0x2a,0xf6,b]
        return buff

    def GetPWMValue(self):
        buff=[0x2a,0x54,0x0d]
        return buff

    def GetChecknum(self,buff):
        crc=0
        for e in buff:
            crc+=e
        if crc>256:
            crc=crc%256
        crc=crc^0xff 
        print("crc:",crc)
        return crc

    def GetTestHeads(self):
        hl=["开机","关机","打开LED","关闭LED","查询LED","保存电流与画面翻转","刷新HDMI","设置光机电流","查询LED温度","读LED工作时间","清除LED工作时间","获取软件版本","设置风扇2","设置风扇1",
            "设置画面倒转","读PWM"]
        return hl

    def IntToByte(self,b):
        bl=[]
        if b<255:
            bl=[b,0]
        else:
           b1=b%256
           b2=b//256
           bl=[b1,b2]
        return bl

    def GetSendData(self,text):
        buff=[]
        if text=="开机":
            buff=self.PowerOn()
        elif text=="关机":
            buff=self.PowerOff()
        elif text=="打开LED":
            buff=self.LedOn()
        elif text=="关闭LED":
            buff=self.LedOff()
        elif text=="查询LED":
            buff=self.QueryState()
        elif text=="保存电流与画面翻转":
            buff=self.SaveCurrentAndImage()
        elif text=="刷新HDMI":
            buff=self.RefreshHdmi()
        elif text=="设置光机电流":
            bl=self.IntToByte(self.ci)
            buff=self.SetLightCurrent(bl[0],bl[1],bl[0],bl[1],bl[0],bl[1])
        elif text=="查询LED温度":
            buff=self.Gettemperature()
        elif text=="读LED工作时间":
            buff=self.GetLedTime()
        elif text=="清除LED工作时间":
            buff=self.clearLedTime()
        elif text=="获取软件版本":
            buff=self.GetVersion()
        elif text=="设置风扇2":
            buff=self.SetFan2Speed(self.speed2)
        elif text=="设置风扇1":
            buff=self.SetFan1Speed(self.speed1)
        elif text=="设置画面倒转":
            buff=self.SetImage(0)
        elif text=="读PWM":
            buff=self.GetPWMValue()
        return buff

    
    