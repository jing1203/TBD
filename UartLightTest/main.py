#coding:utf-8
from PySide2.QtWidgets import QApplication,QStyleFactory
import sys
from mainform import MainWindow

if __name__ == '__main__':
	app =QApplication(sys.argv)
	app.setStyle(QStyleFactory.create('Fusion'))
	w =MainWindow()
	dk=app.desktop()
	w.SetDk(dk)
	w.show()
	sys.exit(app.exec_())