#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: across Maya version develop testing
  Created: 2018/1/30
"""

'''in Maya2014~2018 testing:
import sys
sys.path.append(r'D:\git\MayaProgramming\poc')

from scriptsTesting import myGUI_Test as myTest
reload(myTest)
myTest.main()
'''

import sys
import Qt
from Qt import QtWidgets, QtGui, QtCore

#ui module is: QtDesigner -> *.ui file -> ui.py (by ui2py_maya2014_2018.py) -> Qt.py --convert ui.py -> ui.py (https://github.com/mottosso/Qt.py/issues/129)
import myGUI_ui as ui
reload(ui)

########################################################################
class MainWindow(QtWidgets.QWidget, ui.Ui_Form):
    """"""
    title = u'ui_Test'
    version = u'2018.01.30.01'
    
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        if parent:
            self.setWindowIcon(parent.windowIcon())
            self.setPalette(parent.palette())
            self.setParent(parent, QtCore.Qt.Window)
        self.setWindowTitle(u'%s %s'%(MainWindow.title, MainWindow.version))
        
        self.connect_action()

    #----------------------------------------------------------------------
    def connect_action(self):
        """"""
        pass

#----------------------------------------------------------------------
def main():
    """"""
    global win
    try:
        win.close()
    except:
        pass
    win = MainWindow(None)
    win.show()

########################################################################
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())