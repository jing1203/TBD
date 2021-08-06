#coding:utf-8
from PySide2.QtWidgets import QMainWindow,QMessageBox,QApplication
from PySide2.QtCore import *
from PySide2.QtGui import QImage,QPixmap
from form.showimg import Ui_showimg
import sys
"""
光机投屏界面
"""
class SWindow(QMainWindow):
    def __init__(self):
        super(SWindow, self).__init__()
        self.new = Ui_showimg()
        self.new.setupUi(self)

        # 默认白图，幅面1920*1080
        self.LoadImg("white.png")
    
    """
    加载图片
    """
    def LoadImg(self,path):
        img=QImage(path)
        self.new.lab_img.resize(img.width(),img.height())
        self.new.lab_img.setPixmap(QPixmap.fromImage(img))