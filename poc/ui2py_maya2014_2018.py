#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: compile *.ui to *_ui.py
  Created: 2017/11/8
"""

import os
import sys

try:
    #for PySide2 (>=Maya2017 default)
    from pyside2uic import compileUi
except:
    try:
        #for PySide (Maya2014~2016 defalut)
        from pysideuic import compileUi
    except Exception as ex:
        print('ERROR::Only support pyside(Maya2014~2016) OR pyside2(>=Maya2017)')
        print(ex.message)


#----------------------------------------------------------------------
def ui2py(uifile):
    """"""
    if os.path.exists(uifile):
        outfile = '%s.py'%uifile.replace('.', '_')
        with open(outfile, 'w') as pyfile:
            compileUi(uifile, pyfile)
            print('%s to %s finished.'%(uifile, outfile))
    else:
        print('uifile does not exists! <- %s'%uifile)

        
#----------------------------------------------------------------------
def usage():
    """"""
    print('usage:')
    print('ui2py_pyside.py *.ui [uifile2 uifile3 ...]')
    print('output: *_ui.py')



########################################################################
if __name__ == '__main__':
    print('ui2py_pyside *.ui [Support pyside(Maya2014~2016) OR pyside2(>=Maya2017)]')
    if len(sys.argv) > 1:
        uifile_list = sys.argv[1:]
        for uifile in uifile_list:
            try:
                ui2py(uifile)
            except Exception as ex:
                print(ex.message)
    else:
        usage()
