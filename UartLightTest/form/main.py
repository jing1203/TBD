# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 518)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 481, 51))
        self.cb_comname = QComboBox(self.groupBox)
        self.cb_comname.setObjectName(u"cb_comname")
        self.cb_comname.setGeometry(QRect(10, 20, 69, 22))
        self.btn_serach = QPushButton(self.groupBox)
        self.btn_serach.setObjectName(u"btn_serach")
        self.btn_serach.setGeometry(QRect(90, 20, 75, 23))
        self.btn_open = QPushButton(self.groupBox)
        self.btn_open.setObjectName(u"btn_open")
        self.btn_open.setGeometry(QRect(180, 20, 75, 23))
        self.btn_showimg = QPushButton(self.groupBox)
        self.btn_showimg.setObjectName(u"btn_showimg")
        self.btn_showimg.setGeometry(QRect(270, 20, 75, 23))
        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 260, 481, 241))
        self.txt_send = QLineEdit(Dialog)
        self.txt_send.setObjectName(u"txt_send")
        self.txt_send.setGeometry(QRect(10, 170, 401, 20))
        self.btn_crc = QPushButton(Dialog)
        self.btn_crc.setObjectName(u"btn_crc")
        self.btn_crc.setGeometry(QRect(420, 170, 75, 23))
        self.txt_receive = QLineEdit(Dialog)
        self.txt_receive.setObjectName(u"txt_receive")
        self.txt_receive.setGeometry(QRect(10, 200, 481, 20))
        self.lab_info = QLabel(Dialog)
        self.lab_info.setObjectName(u"lab_info")
        self.lab_info.setGeometry(QRect(10, 230, 481, 16))
        self.cb_test = QComboBox(Dialog)
        self.cb_test.setObjectName(u"cb_test")
        self.cb_test.setGeometry(QRect(10, 140, 161, 22))
        self.btn_set = QPushButton(Dialog)
        self.btn_set.setObjectName(u"btn_set")
        self.btn_set.setGeometry(QRect(180, 140, 75, 23))
        self.btn_send = QPushButton(Dialog)
        self.btn_send.setObjectName(u"btn_send")
        self.btn_send.setGeometry(QRect(260, 140, 75, 23))
        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 70, 481, 51))
        self.cb_pho = QComboBox(self.groupBox_2)
        self.cb_pho.setObjectName(u"cb_pho")
        self.cb_pho.setGeometry(QRect(11, 22, 69, 20))
        self.btn_searchpho = QPushButton(self.groupBox_2)
        self.btn_searchpho.setObjectName(u"btn_searchpho")
        self.btn_searchpho.setGeometry(QRect(86, 21, 75, 23))
        self.btn_openpho = QPushButton(self.groupBox_2)
        self.btn_openpho.setObjectName(u"btn_openpho")
        self.btn_openpho.setGeometry(QRect(167, 21, 75, 23))
        self.btn_readpho = QPushButton(self.groupBox_2)
        self.btn_readpho.setObjectName(u"btn_readpho")
        self.btn_readpho.setGeometry(QRect(250, 21, 75, 23))
        self.btn_outexl = QPushButton(self.groupBox_2)
        self.btn_outexl.setObjectName(u"btn_outexl")
        self.btn_outexl.setGeometry(QRect(330, 21, 75, 23))
        self.txt_current = QLineEdit(Dialog)
        self.txt_current.setObjectName(u"txt_current")
        self.txt_current.setGeometry(QRect(340, 140, 71, 20))
        self.btn_setcurrent = QPushButton(Dialog)
        self.btn_setcurrent.setObjectName(u"btn_setcurrent")
        self.btn_setcurrent.setGeometry(QRect(420, 140, 75, 23))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u5149\u673a\u4e32\u53e3\u8bbe\u7f6e", None))
        self.btn_serach.setText(QCoreApplication.translate("Dialog", u"\u641c\u7d22", None))
        self.btn_open.setText(QCoreApplication.translate("Dialog", u"\u6253\u5f00", None))
        self.btn_showimg.setText(QCoreApplication.translate("Dialog", u"\u6253\u5f00\u6295\u5c4f", None))
        self.btn_crc.setText(QCoreApplication.translate("Dialog", u"\u53d1\u9001", None))
        self.lab_info.setText(QCoreApplication.translate("Dialog", u"\u4fe1\u606f\uff1a", None))
        self.btn_set.setText(QCoreApplication.translate("Dialog", u"\u914d\u7f6e", None))
        self.btn_send.setText(QCoreApplication.translate("Dialog", u"\u53d1\u9001", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"\u5149\u5ea6\u8ba1\u4e32\u53e3\u8bbe\u7f6e", None))
        self.btn_searchpho.setText(QCoreApplication.translate("Dialog", u"\u641c\u7d22", None))
        self.btn_openpho.setText(QCoreApplication.translate("Dialog", u"\u6253\u5f00", None))
        self.btn_readpho.setText(QCoreApplication.translate("Dialog", u"\u8bfb\u5149\u5ea6\u8ba1", None))
        self.btn_outexl.setText(QCoreApplication.translate("Dialog", u"\u5bfc\u51faEXL", None))
        self.btn_setcurrent.setText(QCoreApplication.translate("Dialog", u"\u8bbe\u7f6e\u7535\u6d41", None))
    # retranslateUi

