# -*- coding: utf-8 -*-
import time
import os
import logging
from threading import Timer

# path = "/home/heygears/app/release/LOG/2020_08_27/PrintEngine_20200827_215451.log"
PATH = "/home/root/app/.a2d/logs/"
current_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
logging.basicConfig(level=logging.INFO)
mylog = logging.getLogger(name='A2D2.0')
file_handler = logging.FileHandler('/home/root/uiauto0831/logtest/test_print%s'%current_time)
#file_handler = logging.FileHandler(f'/home/root/logtest/test_interrupt{current_time}')
#mylog.addHandler(file_handler)

def totimeStamp(timet):
    # timet = '201205_033230'
    split = timet.split("_")
    join = split[0] + split[1]

    date = ["20" + join[0:2], join[2:4], join[4:6]]
    time1 = [join[6:8], join[8:10], join[10:12]]
    date = "-".join(date)
    time1 = ":".join(time1)
    timeArray = time.strptime((date + " " + time1), "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    return timestamp

def get_latestpath():
    file_dict = {}
    lists = os.listdir(PATH)
    for i in lists:

        if '2' in i:
            path_parent = os.path.join(PATH, i)

            lists2 = os.listdir(os.path.join(PATH, i))

            for j in lists2:
                if 'backend' not in j:
                    continue
                if j.endswith('.1'):
                    continue
                
                else:
                    time_s = os.path.join(path_parent, j).split("d_")[1].split(".")[0]
                    time_s = totimeStamp(time_s)
                    ctime = os.stat(path_parent).st_ctime
                    #file_dict[ctime] = os.path.join(path_parent, j)
                    file_dict[time_s] = os.path.join(path_parent, j)
                    # print(ctime, os.path.join(path_parent, j), time_s)

    lens = len(file_dict.keys())
    max_ctime=max(file_dict.keys())
    sorted_d = sorted(file_dict.items(), key=lambda k: k[0])

    return file_dict[max_ctime], lens

def redirect(lens):
    newlastest, new_lens = get_latestpath()
    mylog.info('redirect')
    if lens != new_lens:
        tag = 0
        latest_path = newlastest
        lens = new_lens
        mylog.info('tag is %s,latest_path is %s' % (tag, latest_path))
        return tag ,latest_path ,lens 

import time, os
from pymouse import PyMouse

def start_print():
    time.sleep(5)
    mouse.click(173, 208, 1)
    time.sleep(2)
    mouse.click(584, 276, 1)
    time.sleep(2)
    mouse.click(1725, 869, 1)
    time.sleep(2)
    mouse.click(1102, 921, 1)
    time.sleep(2)
    mouse.click(1095, 915, 1)
    time.sleep(2)
    mouse.click(1094, 934, 1)
    current_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    mylog.info('print sttart ----%s'%current_time)


def confirm_finish():
    mouse.click(980, 747, 1)  # confirm finish
    time.sleep(2)
    mouse.click(980, 747, 1)  # confirm finish
    time.sleep(2)
    mouse.click(980, 747, 1)  # confirm finish
    time.sleep(2)
    mouse.click(980, 747, 1)  # confirm finish
    time.sleep(2)
    
    mouse.scroll(vertical=-1000)
    time.sleep(2)
    
    mouse.scroll(vertical=-1000)
    time.sleep(2)
    
    mouse.click(1331, 971, 1)  # commit log
    time.sleep(2)
    mouse.click(1331, 971, 1)  # commit log
    current_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    mylog.info('print finish ----%s'%current_time)
    os.system("notify-send [\"执行完成\"] \"测试执行已经完成，共执行指令7条\"")

def printfinish_record():
    start_print()
    tag = 0
    latest_path, lens = get_latestpath()
    mylog.info('tag is %s,latest_path is %s'%(tag, latest_path))
    while True:

        with open(latest_path, 'r') as f:
            f.seek(tag)
            aa = f.read()
            tag = f.tell()
            if flag_finish in aa:
                mylog.info('print finish')
                confirm_finish()
                t = Timer(60, redirect, args=[lens])
                t.start()
                start_print()
            if flag_screen_error in aa:
                mylog.info('投屏错误DLP4700 erro:')
            if flag_back_disconnect in aa:
                mylog.info('back_ground disconnect:')
                break
            newlastest, new_lens = get_latestpath()
            #mylog.info('newlastest is %s,latest_path is %s'%(newlastest, latest_path))
            if lens != new_lens:
                tag = 0
                latest_path = newlastest
                mylog.info('tag is %s,latest_path is %s'%(tag, latest_path))


if __name__ == '__main__':
    # time.sleep(25)
    # 后台日志 - 关键字：
    # 打印完成： onPrintFinish
    # 打印终止： onPrintAbort
    # 投屏错误： error: "DLP4700::Connect | Failed to open a device in the library(4)"
    # 下位机通讯中断：SlaveCmd::fail
    # 后台断开：ClientClosed
    mouse = PyMouse()
    tag = 0
    latest_path, lens = get_latestpath()
    flag_finish = "打印结束"
    flag_interr = "onPrintAbort"
    flag_screen_error = '''error: "DLP4700::Connect | Failed to open a device in the library(4)"'''
    flag_back_disconnect = "ClientClosed"
    mylog.info('--start writing  main-----')

    printfinish_record()
