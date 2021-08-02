#coding:utf-8 
import time,os
from pymouse import PyMouse
from pykeyboard import PyKeyboard

mouse = PyMouse()
k = PyKeyboard()
mouse.click(172,218, 1)
time.sleep(2)


mouse.click(194,437, 1)
time.sleep(2)


mouse.scroll(vertical=-5000)
time.sleep(2)
os.system("notify-send [\"执行完成\"] \"测试执行scroll\"")

mouse.click(1762,829, 1)
time.sleep(2)

# pwd

k.press_key('6')
#mouse.click(1048,380, 1)
time.sleep(2)

k.press_key('6')
#mouse.click(1048,380, 1)
time.sleep(2)

k.press_key('6')
#mouse.click(1048,380, 1)
time.sleep(2)

k.press_key('6')
#mouse.click(1048,380, 1)
time.sleep(2)

k.press_key('6')
#mouse.click(1048,380, 1)
time.sleep(2)

k.press_key('6')
#mouse.click(1048,380, 1)
time.sleep(2)
# end

time.sleep(2)
mouse.click(931,392, 1)

time.sleep(2)
mouse.click(1146,571, 1)

time.sleep(2)
mouse.click(865,440, 1)

time.sleep(2)
mouse.click(1115,636, 1)

time.sleep(2)
