#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: 
  Created: 2017/11/2
"""

import sys

from PySide import QtGui
from PySide import QtCore

import maya.cmds as cmds

#----------------------------------------------------------------------
def listObjs():
    """"""
    objs = cmds.ls(sl=True)
    for obj in objs:
        print(obj)




########################################################################
class Window(QtGui.QMainWindow):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        super(Window, self).__init__()
        self.initUI()

    #----------------------------------------------------------------------
    def initUI(self):
        """"""
        
        self.btn = QtGui.QPushButton(self)
        self.btn.setText('list sel')
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.btn_click)

        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('MyWindow')
        self.show()

    #----------------------------------------------------------------------
    def btn_click(self):
        """"""
        listObjs()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())