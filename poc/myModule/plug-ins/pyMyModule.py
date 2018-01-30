#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: Maya Python API 2.0 test
  Created: 2018/1/30
"""

import sys
import maya.api.OpenMaya as om

#Maya 2016, 2017, 2018..
#When writing a plugin that uses the new API, 
#the plugin must define a variable called maya_useNewAPI so that Maya will know to pass it objects from the new API rather than the old one. 
#https://help.autodesk.com/view/MAYAUL/2016/ENU/?guid=__py_ref_index_html
maya_useNewAPI = True

#----------------------------------------------------------------------
def maya_useNewAPI():
    """
    Maya 2013, 2014, 2015
    When writing a plugin which uses the new API, 
    the plugin must define a function called maya_useNewAPI so that Maya will know to pass it objects from the new API rather than the old one.
    """
    pass




########################################################################
if __name__ == '__main__':
    print(sys.executable)
    print('maya_userNewAPI: %s, type:%s'%(maya_useNewAPI, type(maya_useNewAPI)))