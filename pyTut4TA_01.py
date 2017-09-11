#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: [Python Tutorial for TA] 1.Introduction python from a practical script (check a file does exists)
  Created: 2017/9/11
  
  1.Introduction python from a practical script (check a file does exists)
	a.first 2 lines (coding)
	b.comment for desc, purpose
	c.import modules
	d.variables declaration (a, b = 1, 2)
	e.str, list and len, range
	f.control flow (if elif else, for i in range(5), pass, break, continue)
"""

print('Hello, Welcom to Python World!')

import os

the_file = r'D:\git\mayaProgramming\bmw.jpg'

if os.path.exists(the_file):
    print('Yes, the file does exists!')
else:
    print('No, the file does not exists!')