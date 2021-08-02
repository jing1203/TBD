#coding:utf-8
import logging  # 引入logging模块
import os.path
import time
class LogData():
    def __init__(self):
        self.Init()

    def Init(self):
        # 第一步，创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)  # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        self.rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        self.log_path = str(os.getcwd()) + '/Logs/'
        self.log_name = self.log_path + self.rq + '_AutoTest.log'
        self.logfile = self.log_name
        self.fh = logging.FileHandler(self.logfile, mode='w')
        self.fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        # 第三步，定义handler的输出格式
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        self.fh.setFormatter(self.formatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(self.fh)

    def LogWriteInfo(self,s):
        # 日志
        self.logger.info(s)

    def LogWriteErr(self,s):
        # 日志
        self.logger.error(s)

    def LogWriteAuto(self,s):
        #自动化日志
        self.logger.warning(s)

