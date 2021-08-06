#congdings:utf-8
from configparser import ConfigParser
def GetTestTime(path):
    cf = ConfigParser()
    cf.read(path)
    lightcurrent=cf.getint("Sets","LightCurrent")
    fspeed1=cf.getint("Sets","FAN1Speed")
    fspeed2=cf.getint("Sets","FAN2Speed")
    imagestate=cf.getint("Sets","istate")
    comname=cf.get("Sets","com")
    phocom=cf.get("Sets","phocom")
    printlayer=cf.getint("Sets","printlayer")
    printtimes=cf.getint("Sets","printtimes")
    ci=cf.getint("Sets","ci")
    lightv=cf.getint("Sets","lightv")
    ledontime=cf.getint("Sets","ledontime")
    ledofftime=cf.getint("Sets","ledofftime")
    worktime=cf.getint("Sets","worktime")
    resttime=cf.getint("Sets","resttime")
    waittime=cf.getint("Sets","waittime")
    tlist={"lightcurrent":lightcurrent,"fspeed1":fspeed1,
    "fspeed2":fspeed2,"istate":imagestate,"comname":comname,"phocom":phocom,
    "printlayer":printlayer,"printtimes":printtimes,"ci":ci,"lightv":lightv,
    "ledontime":ledontime,"ledofftime":ledofftime,"worktime":worktime,"resttime":resttime,
    "waittime":waittime}
    return tlist

def SetTestTime(vl,path):
    cf = ConfigParser()
    cf.read(path)
    cf.set("Sets","LightCurrent",str(vl["lightcurrent"]))
    cf.set("Sets","FAN1Speed",str(vl["fspeed1"]))
    cf.set("Sets","FAN2Speed",str(vl["fspeed2"]))
    cf.set("Sets","istate",str(vl["istate"]))
    cf.set("Sets","com",vl["comname"])
    cf.write(open(path,"w"))

"""
tlist=GetTestTime("set.ini")
print(tlist)
SetTestTime(tlist,"set.ini")
"""