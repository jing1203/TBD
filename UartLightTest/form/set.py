# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_setform(object):
    def setupUi(self, setform):
        if not setform.objectName():
            setform.setObjectName(u"setform")
        setform.resize(368, 303)
        self.tb_lv = QTableWidget(setform)
        self.tb_lv.setObjectName(u"tb_lv")
        self.tb_lv.setGeometry(QRect(10, 10, 256, 281))
        self.btn_ok = QPushButton(setform)
        self.btn_ok.setObjectName(u"btn_ok")
        self.btn_ok.setGeometry(QRect(280, 10, 75, 23))
        self.btn_esc = QPushButton(setform)
        self.btn_esc.setObjectName(u"btn_esc")
        self.btn_esc.setGeometry(QRect(280, 40, 75, 23))

        self.retranslateUi(setform)

        QMetaObject.connectSlotsByName(setform)
    # setupUi

    def retranslateUi(self, setform):
        setform.setWindowTitle(QCoreApplication.translate("setform", u"\u914d\u7f6e\u53c2\u6570", None))
        self.btn_ok.setText(QCoreApplication.translate("setform", u"\u786e\u5b9a", None))
        self.btn_esc.setText(QCoreApplication.translate("setform", u"\u53d6\u6d88", None))
    # retranslateUi

