
#!/usr/bin/env python
#coding: utf-8

import os
import time
# 用于判断是什么系统
import platform

from multiprocessing import Process

# 本机库
# 用于存放历史股票列表
from fileUtils import saveStocks, getStocks
# 交易工具
from tradeUtils import isInTradeTime
# 封装的微信的api
from wechat import login, sendMessageToMyself, sendMessageToFriend

from meepwn import crawl_data_from_wencai


# 如果不在交易时间，则不会进入策略
if not isInTradeTime():
    print('不在交易时间了...')
    os._exit(1)

# 是否是在Mac上进行操作
isOnMac = (platform.system() == 'Darwin')
# 是否需要使用微信来发送消息
# useWeChatToSendMessage=False
useWeChatToSendMessage=True

# 先登录微信
useWeChatToSendMessage and login()

# 存放当前的票的列表的Set
current_stock_list = set()
# 存放所有进来过的票的列表
total_stock_list = getStocks()
result=[]
timer=1
# 使用set进行对比，得到新增加的票
def getFirstInStock(l):
    global current_stock_list, total_stock_list
    # print('存放所有的票的列表:', total_stock_list)
    current_stock_list=set(l)
    # 取并后取异或得到新进来的票
    result = (current_stock_list | total_stock_list) ^ total_stock_list
    if not len(result) == 0:
        print('新进来的票:', result)
        # 进行弹窗提示
        showMessage(list(result)[0])
        # 发送微信消息
        useWeChatToSendMessage and sendMessage(result)
        # 获取全部的股票的列表
        total_stock_list= total_stock_list | result
        # 保存全部股票的列表
        saveStocks(total_stock_list)
        # pass

# 发送信息（目前是发送到微信）
def sendMessage(result):
    sendMessageToMyself(result)
    # sendMessageToFriend(result)

# 弹出提示（目前是调用Mac自带的弹出提示，windows可能需要更换其他的提示）
def showMessage(stockname) :
    if isOnMac:
        # os.popen("osascript -e 'display notification \"" + stockname + "\" with title \"有新的票来了\"'")
        os.system("osascript -e 'beep 3'")
        os.system("osascript -e 'display notification \"软件\" with title \"更新完成\"'")

# 遍历策略
def parseIWencai():
    global timer
    while isInTradeTime():
        print('第%s次' % timer)
        stockList = crawl_data_from_wencai()
        # 获取首次进策略的票
        getFirstInStock(stockList)
        # 休息5s
        time.sleep(5)
        # 次数自加1
        timer=timer + 1
        # timer = 10 / 0
        # 如果过了交易时间
        if not isInTradeTime():
            print('过了交易时间了')
            return false
        else:
            pass
# 循环
def doLoop(fn):
    global driver
    # 父进程创建一个Queue，并传递给各个子进程，存储数据
    gt = Process(target=fn)
    gt.start()
    gt.join()
    print('结束了')
    # 退出`
    os._exit(1)

if __name__ == '__main__':
    # 微信消息测试
    useWeChatToSendMessage and sendMessage('这只是一条测试数据，用于检测是否能够成功从电脑端发消息')
    # 不断查询问财
    doLoop(parseIWencai)