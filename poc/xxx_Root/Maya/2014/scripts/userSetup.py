#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: for using Qt.py
  Created: 2018/3/9
  Ref:     https://groups.google.com/forum/#!topic/python_inside_maya/WP4sKwFnsKw  (it now supports multiple userSetup.py files)
"""

import os

os.environ['QT_PREFERRED_BINDING'] = os.pathsep.join(['PySide2', 'PySide'])

print('from userSetup.py:: %s'%os.environ['QT_PREFERRED_BINDING'])
