#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: 演示python命令行脚本工具的推荐写法，该脚本简单打印传入的每个参数
  Created: 2017/10/18
"""

#导入需要的各种模块
import sys

#定义帮助函数
#----------------------------------------------------------------------
def usage():
    """打印如何使用这个脚本工具"""
    #print('how to use this script')
    msg = '\nUsage:\n'
    msg += '-'*40
    msg += '\npyCMD_Tool_Template.py [arg1 arg2 ...]\n'
    msg += '-'*40
    print(msg)
    

#定义具体实现的相关函数
#----------------------------------------------------------------------
def do_what(argv):
    """具体实现"""
    print(u'传入了%s个参数'%len(argv))
    for arg in (argv):
        print(arg)


#只在__main__空间时才执行，避免被import时产生副作用
if __name__ == '__main__':
    if len(sys.argv) > 1: #命令行参数是你期待的
        do_what(sys.argv[1:])
    else:
        usage() #否则打印使用帮助

