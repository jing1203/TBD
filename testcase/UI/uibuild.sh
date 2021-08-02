#!/bin/bash
pip3 install pynput
pip3 install python_xlib-0.27-py2.py3-none-any.whl
pip3 install pyuserinput
mkdir -f /home/root/uiauto
mkdir -f /home/root/uiauto/logtest
sudo pip3 install sqlalchemy
if [ $? -eq 0 ]
then
echo “执行成功”
else
echo “执行失败”
fi