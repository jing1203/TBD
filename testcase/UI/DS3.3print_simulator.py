# -*- coding: utf-8 -*-
import time
import os
import logging
from threading import Timer

# path = "/home/heygears/app/release/LOG/2020_08_27/PrintEngine_20200827_215451.log"
PATH = "/home/root/app/.a2d/logs/"

#file_handler = logging.FileHandler(f'/home/root/logtest/test_interrupt{current_time}')
#mylog.addHandler(file_handler)



import time, os
from pymouse import PyMouse
from filetools.db_reader import print_record
from filetools.logwriter import LogData

def start_print():
    time.sleep(5)
    mouse.click(84,208, 1)

    time.sleep(2)
    mouse.click(83,209, 1)

    time.sleep(2)
    mouse.click(461,12, 1)

    time.sleep(2)
    mouse.click(463,392, 1)

    time.sleep(2)
    mouse.click(846,1590, 1)

    time.sleep(2)
    mouse.click(598,7, 1)

    time.sleep(2)
    mouse.click(587,233, 1)

    time.sleep(2)
    mouse.click(706,1270, 1)



def confirm_finish():

    time.sleep(2)
    mouse.click(706,1271, 1)

    time.sleep(2)
    mouse.click(565,13, 1)

    time.sleep(2)
    mouse.click(540,143, 1)

    time.sleep(2)
    mouse.click(616,1209, 1)

    time.sleep(2)
    mouse.click(643,1656, 1)


def printfinish_record():
    start_print()
    # latest_path, lens = get_latestpath()
    record_cnt = print_record()
    while True:
        confirm_finish()
        time.sleep(5)
        cur_cnt = print_record()
        if cur_cnt != record_cnt:
            mylog.LogWriteInfo("当前打印记录新增1条，开始进入下一条打印，当前打印记录%s，历史打印记录%s" %(cur_cnt, record_cnt))
            start_print()
        else:
            time.sleep(120)
            continue

if __name__ == '__main__':
    # time.sleep(25)
    # 后台日志 - 关键字：
    # 打印完成： onPrintFinish
    # 打印终止： onPrintAbort
    # 投屏错误： error: "DLP4700::Connect | Failed to open a device in the library(4)"
    # 下位机通讯中断：SlaveCmd::fail
    # 后台断开：ClientClosed
    mouse = PyMouse()

    flag_finish = "打印结束"
    flag_interr = "onPrintAbort"
    flag_screen_error = '''error: "DLP4700::Connect | Failed to open a device in the library(4)"'''
    flag_back_disconnect = "ClientClosed"
    mylog = LogData()
    printfinish_record()
