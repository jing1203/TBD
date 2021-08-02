import time
import os
import logging
from pymouse import PyMouse
from pykeyboard import PyKeyboard

##A2D2.0
FILE_DST = "/home/root/app/release/version"
VER_LOW = "3.0.1.23"
VER_HIGH = "3.0.1.24"
current_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
logging.basicConfig(level=logging.INFO)
mylog = logging.getLogger(name='A2D2.0')
file_handler = logging.FileHandler("/home/root/uiauto0831/logtest/UPDATE_BACK%s"%current_time)
mylog.addHandler(file_handler)

def update():
    mouse.click(1086, 792, 1)
    time.sleep(2)

    mouse.click(1086, 792, 1)
    time.sleep(2)


    mouse.click(1762, 829, 1)
    time.sleep(1)

    mouse.click(1762, 829, 1)
    time.sleep(1)

    mouse.click(955, 336, 1)
    time.sleep(1)

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)
    #
    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)


    # end
    mouse.click(1008, 660, 1)
    time.sleep(2)

    mouse.click(830, 260, 1)
    time.sleep(2)

    mouse.click(1100, 600, 1)

    time.sleep(2)
    mouse.click(1600, 923, 1)

    time.sleep(2)
    mylog.info("update")
    print("update")
    pass

def rollback():
    mouse.click(172, 218, 1)
    time.sleep(2)

    mouse.click(194, 437, 1)
    time.sleep(2)

    mouse.scroll(vertical=-8000)
    time.sleep(2)
    os.system("notify-send [\"执行完成\"] \"测试执行scroll\"")

    mouse.click(1762, 829, 1)
    time.sleep(2)

    mouse.click(955, 336, 1)
    time.sleep(1)
    # pwd

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)
    #
    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)

    k.press_key('6')
    # mouse.click(1048,380, 1)
    time.sleep(2)
    # end

    time.sleep(2)
    mouse.click(931, 392, 1)

    time.sleep(2)
    mouse.click(1146, 571, 1)

    time.sleep(2)
    mouse.click(865, 440, 1)

    time.sleep(2)
    mouse.click(1115, 636, 1)

    time.sleep(2)

    mouse.click(1115, 718, 1)

    time.sleep(2)
    mylog.info("rollback")
    print("rollback")
    pass



if __name__ == '__main__':
    time.sleep(90)
    mouse = PyMouse()
    k = PyKeyboard()
    with open(FILE_DST) as f:
        ver = f.read().split("=")[1].strip()
        mylog.info("current ver is %s"%ver)
        print("current ver is %s"%ver)
        if ver == VER_LOW:
            update()
        elif ver == VER_HIGH:
            rollback()
        # else:
        #     mylog.info("no target version")
        #     print("no target version")
        f.close()