#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: [Python Tutorial for TA] 2.A recommended programming 'standard' (print python version, list all file in folder)
  Created: 2017/9/11
  
  2.A recommended programming 'standard'
	a.framework (import, def fn, __main__)
	b.function defining, built-in functions
	c.more data structure (list Comprehensions, tuple, set, dict(for k, v in dict.items()))
	d.the python standard library (sys, os)
"""

import sys
import os

#----------------------------------------------------------------------
def info():
    """print python version"""
    print('version: %s'%sys.version)
    print('platform:%s'%sys.platform)
    print()
    print('-'*20, 'Python Path', '-'*20)
    for p in sys.path:
        print(p)
    print('-'*(40+len(' Python Path ')))

#----------------------------------------------------------------------
def get_files(fd):
    """list all file in the folder"""
    if os.path.exists(fd):
        print('file(s) in %s'%os.path.abspath(fd))
        print('*'*53)
        for f in os.listdir(fd):
            print(f)
        print('*'*53)
    else:
        print('folder does not exists')

#----------------------------------------------------------------------
def main():
    """entry point"""
    info()
    print('\n')
    if len(sys.argv) == 2:
        get_files(sys.argv[1])
    else:
        get_files(os.path.curdir)


#----------------------------------------------------------------------
if __name__ == '__main__':
    main()