
#!/usr/bin/env python
#coding: utf-8

import time

# 用于存放历史股票列表
from fileUtils import saveStocks, getStocks, clearStocks
# 交易工具
from tradeUtils import checkClearStock, isInTradeTime, isInTradeDay, sendMessage, sleepToNextTradeTime, sleepToNextTradeDay

from meepwn import crawl_stock_name
from verifyCode.codeUtils import handleSessionError, quitDriver
import requests

# 存放当前的票的列表的Set
current_stock_list = set()
# 存放所有进来过的票的列表
total_stock_list = set()
result=[]
timer=1
# 使用set进行对比，得到新增加的票
def getFirstInStock(l):
    if l == '000000':
        # 添加验证码逻辑
        handleSessionError()
        return
    global current_stock_list, total_stock_list
    # print('存放所有的票的列表:', total_stock_list)
    current_stock_list=set(l)
    # 取并后取异或得到新进来的票
    result = (current_stock_list | total_stock_list) ^ total_stock_list
    if not len(result) == 0:
        print('新进来的票:', result)
        # 发消息
        sendMessage(result)
        # 获取全部的股票的列表
        total_stock_list= total_stock_list | result
        # 保存全部股票的列表
        saveStocks(total_stock_list)
        # pass

# 遍历策略 !
def parseIWencai():
    global timer,total_stock_list
    # 如果不是在交易日
    if(not isInTradeDay()):
        print('不是在交易日 开始')
        quitDriver()
        sleepToNextTradeDay()
        clearStocks()
        total_stock_list=set()
        print('不是在交易日 结束')
        return False 
    # 如果不在交易时间内
    if(not isInTradeTime()):
        print('未在交易时间内 开始')
        quitDriver()
        sleepToNextTradeTime()
        checkClearStock()
        print('未在交易时间内 结束')
        return False 
    print('第%s次' % timer)
    stockList = crawl_stock_name()
    # stockList = crawl_stock_name('昨日未涨停 当日涨停 非st')
    # 获取首次进策略的票
    getFirstInStock(stockList)
    # 休息5s
    time.sleep(2)
    # 次数自加1
    timer=timer + 1

def startQuery():
    global total_stock_list
    str=input('是否要清除股票池 ' + 'y/n?')
    if(not str=='n'):
        clearStocks()
    total_stock_list = getStocks()
    while True:
        parseIWencai()

if __name__ == '__main__':
    # sendMessage('发送首次涨停的票')
    startQuery()