#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: a single python file script tool demo
  Created: 2018/3/8
"""

import sys

try:
    #default support maya 2017+ (PySide2)
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    #using _libs/Qt.py support others maya version (2014~2016, PySide, PyQt4, PyQt5..)
    from Qt import QtWidgets, QtGui, QtCore

########################################################################
class Window(QtWidgets.QMainWindow):
    """testing window"""

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""

        super(Window, self).__init__(parent)
        self.initUI()

    #----------------------------------------------------------------------
    def initUI(self):
        """"""
        btn = QtWidgets.QPushButton('click me', self)
        btn.move(100, 80)
        btn.clicked.connect(self.btn_clicked)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('MyWindow')
        #self.show()

    #----------------------------------------------------------------------
    def btn_clicked(self):
        """"""
        print('btn clicked')


#----------------------------------------------------------------------
def main():
    """in maya, always call the py module's main function"""
    global win
    try:
        win.close()
    except:
        pass
    
    win = Window()
    win.show()


#----------------------------------------------------------------------
#standalone for ui testing
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())