# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'showimg.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_showimg(object):
    def setupUi(self, showimg):
        if not showimg.objectName():
            showimg.setObjectName(u"showimg")
        showimg.resize(400, 300)
        self.lab_img = QLabel(showimg)
        self.lab_img.setObjectName(u"lab_img")
        self.lab_img.setGeometry(QRect(0, 0, 54, 12))

        self.retranslateUi(showimg)

        QMetaObject.connectSlotsByName(showimg)
    # setupUi

    def retranslateUi(self, showimg):
        showimg.setWindowTitle(QCoreApplication.translate("showimg", u"showimg", None))
        self.lab_img.setText(QCoreApplication.translate("showimg", u"TextLabel", None))
    # retranslateUi

