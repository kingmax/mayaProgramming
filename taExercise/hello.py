#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: 
  Created: 2017/11/2
"""

import sys


#----------------------------------------------------------------------
def usage():
    """"""
    msg = u'怎么使用'
    print(msg)
    

#----------------------------------------------------------------------
def do():
    """"""
    print('hello, world')
    

#----------------------------------------------------------------------
def main():
    """"""
    do()

    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
    else:
        for arg in sys.argv:
            print(arg)
        main()


    
    
    
