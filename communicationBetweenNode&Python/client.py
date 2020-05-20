#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time


# 定义接收到的不同环节码，执行不同逻辑
def foo(var):
    if var == '100':
        # 与服务器交互 虚拟请求数据时间1秒
        time.sleep(1)
        print('100#'+'{"sign":"1", "msg":"登录成功"}')
    elif var == '200':
        # 与服务器交互 虚拟请求数据时间1秒
        time.sleep(1)
        print('200#'+'{"sign":"1", "msg":"进入大厅成功"}')
    elif var == '300':
        # 与服务器交互 虚拟请求数据时间1秒
        time.sleep(1)
        print('300#'+'{"sign":"1", "msg":"匹配成功"}')
    else:
        print('run the orderError')


# 参数为从命令行传过来的参数 sys.argv ['py_test.py', arg1, arg2...]
# 所以取参数要从1开始，就是第二位置开始取
foo(sys.argv[1])