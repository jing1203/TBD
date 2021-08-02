#coding:utf-8
import os,time
lpath="/ps/ps_"+time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+"/"
def makedir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path+' 创建成功')
    else:
        print(path+' 目录已存在')

def saveimg(name):
    spath=os.getcwd()
    makedir(str(spath)+lpath)
    spath=str(spath)+lpath+name
    isok= False
    try:
        os.system("scrot "+spath)
        isok=True
    except Exception as e:
        print(str(e))
    return  isok