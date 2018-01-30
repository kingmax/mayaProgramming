#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: testing
  Created: 2017/12/18
"""

import sys
import os
import time
import re


f = r'D:\PM-2017-05.log'
keyword = 'test,'

print(time.ctime())
t_start = time.time()
print('start: %s'%t_start)

reg = re.compile(keyword)

out_list = []
num = 0

with open(f, 'r') as fp:
    
    for line in fp:
        num += 1
        #print(num)
        if keyword in line:
        #if re.findall(keyword, line):
        #if reg.findall(line):
            #print(line)
            out_list.append(line)
    print('Number of line: %s'%num)

    
with open('out.txt', 'w') as fp:
    for line in out_list:
        fp.write(line)


print(time.ctime())
t_end = time.time()
print('end:   %s'%t_end)
print('time: %s'%(t_end - t_start))

raw_input()