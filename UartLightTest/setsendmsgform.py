#coding:utf-8
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import * 
from PySide2.QtCore import QTimer,Signal
from PySide2.QtWidgets import QMessageBox,QTableWidgetItem
from form.set import Ui_setform

class SetSmsgwindow(QtWidgets.QWidget):
    _signal = Signal(dict)
    def __init__(self):  
        super(SetSmsgwindow,self).__init__()  
        self.new=Ui_setform()
        self.new.setupUi(self)
        self.InitHead()
        self.new.btn_ok.clicked.connect(self.GetSet)
        self.new.btn_esc.clicked.connect(self.WEsc)
        self.name=""

    def InitHead(self):
        self.new.tb_lv.setColumnCount(2)
        self.new.tb_lv.setHorizontalHeaderLabels(['名称', '值'])

    def SetMsg(self,sl):
        self.new.tb_lv.setColumnCount(2)
        self.name=sl['name']
        dl=sl["data"]
        slen=len(dl)
        self.new.tb_lv.setRowCount(slen)
        self.new.tb_lv.setHorizontalHeaderLabels(['名称', '值'])
        i=0
        for e in dl.keys():
            self.new.tb_lv.setItem(i, 0, QTableWidgetItem(str(e)))#设置0行i列的内容为Value
            self.new.tb_lv.setItem(i, 1, QTableWidgetItem(dl[e]))#设置0行i列的内容为Value
            self.new.tb_lv.setColumnWidth(i,200)#设置i列的宽度
            self.new.tb_lv.setRowHeight(0,50)#设置i行的高度
            self.new.tb_lv.setRowHeight(1,50)#设置i行的高度
            i+=1
        self.new.tb_lv.verticalHeader().setVisible(True)#
        self.new.tb_lv.horizontalHeader().setVisible(True)#

    def WEsc(self):
        self.close()

    def GetSet(self):
        cols=self.new.tb_lv.columnCount()
        rows=self.new.tb_lv.rowCount()
        i=0
        j=0
        sl=[]
        for i in range(0,rows):
            al=[]
            for j in range(0,cols):
                al.append(self.new.tb_lv.item(i,j).text())
            sl.append(al)
        dl={}
        dl['data']=sl
        dl['name']=self.name
        self.name=""
        self._signal.emit(dl)
        self.close()