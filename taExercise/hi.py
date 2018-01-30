#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: 
  Created: 2017/11/2
"""

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

########################################################################
class Window(QtWidgets.QMainWindow):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        super(Window, self).__init__()
        self.initUI()

    #----------------------------------------------------------------------
    def initUI(self):
        """"""
        
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('MyWindow')
        self.show()



if __name__ == '__main__':
    print('hi')
    
    print('2')
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())