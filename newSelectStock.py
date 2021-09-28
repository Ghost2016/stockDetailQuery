
#!/usr/bin/env python
#coding: utf-8

import time
# 用于判断是什么系统
import platform

# 用于存放历史股票列表
from fileUtils import saveStocks, getStocks, clearStocks
# 交易工具
from tradeUtils import isInTradeTime, isInTradeDay, sleepToNextTradeTime, sleepToNextTradeDay

from meepwn import crawl_data_from_wencai

import pyautogui as gui

# 是否是在Mac上进行操作
isOnMac = (platform.system() == 'Darwin')
# 是否需要使用微信来发送消息
# useWeChatToSendMessage=False
useWeChatToSendMessage=True


# 存放当前的票的列表的Set
current_stock_list = set()
# 存放所有进来过的票的列表
total_stock_list = set()
result=[]
timer=1
# 使用set进行对比，得到新增加的票
def getFirstInStock(l):
    if l == '000000':
        useWeChatToSendMessage and sendMessage('There is something wrong with the network.')
        # Todo 添加验证码逻辑
        time.sleep(999999)
        return
    global current_stock_list, total_stock_list
    # print('存放所有的票的列表:', total_stock_list)
    current_stock_list=set(l)
    # 取并后取异或得到新进来的票
    result = (current_stock_list | total_stock_list) ^ total_stock_list
    if not len(result) == 0:
        print('新进来的票:', result)
        # 发送微信消息
        useWeChatToSendMessage and sendMessage(result)
        # 获取全部的股票的列表
        total_stock_list= total_stock_list | result
        # 保存全部股票的列表
        saveStocks(total_stock_list)
        # pass

# 发送信息（目前是发送到微信）
def sendMessage(result):
    gui.typewrite(message='%s' % result)
    gui.hotkey('enter')

# 遍历策略 !
def parseIWencai():
    global timer,total_stock_list
    # 如果不是在交易日
    if(not isInTradeDay()):
        print('不是在交易日 开始')
        sleepToNextTradeDay()
        clearStocks()
        total_stock_list=set()
        print('不是在交易日 结束')
        return False 
    # 如果不在交易时间内
    if(not isInTradeTime()):
        print('未在交易时间内 开始')
        sleepToNextTradeTime()
        clearStocks()
        total_stock_list=set()
        print('未在交易时间内 结束')
        return False 
    print('第%s次' % timer)
    stockList = crawl_data_from_wencai()
    # 获取首次进策略的票
    getFirstInStock(stockList)
    # 休息5s
    time.sleep(3)
    # 次数自加1
    timer=timer + 1
        

if __name__ == '__main__':

    str=input('是否要清除股票池 ' + 'y/n?')
    if(not str=='n'):
        clearStocks()
    total_stock_list = getStocks()
    time.sleep(1)

    # 切换到微信
    useWeChatToSendMessage and gui.hotkey('command','option','shift','w')
    time.sleep(1)

    # # 微信消息测试
    # useWeChatToSendMessage and sendMessage('Ready to run.')
    time.sleep(1)
    
    while True:
        parseIWencai()