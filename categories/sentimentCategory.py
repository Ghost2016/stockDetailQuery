#!/usr/bin/env python
#coding: utf-8
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from meepwn import crawl_length
from tushareUtils import getLastTradeDay
from utils.common import no_new, no_st

def autoCal(text):
    return {
        'text': text,
        'func': '自动计算'
    }
# 获取情绪策略 - 5个指标 - 淘县出品
def getSentimentOfFirstBrokenBan(day):
    currentDay = day
    lastTradeDay = getLastTradeDay(currentDay)
    theDayBeforeLastTradeDay = getLastTradeDay(lastTradeDay)
    return [
        {
            'text': '昨日的首板今日红盘个数',
            'func': crawl_length('%s涨跌幅大于0 %s涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new))
        },
        {
            'text': '昨日的首板今日大面个数',
            'func': crawl_length('(%s的收盘价格/开盘价格小于0.95)或者(%s的收盘价格/%s收盘价格小于0.95) %s涨停 %s未涨停 %s' % (currentDay, currentDay, lastTradeDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new))
        },
    ]

# 获取情绪策略 - 5个指标 - 淘县出品
def getSentiment(day):
    currentDay = day
    lastTradeDay = getLastTradeDay(currentDay)
    theDayBeforeLastTradeDay = getLastTradeDay(lastTradeDay)
    return [
        {
            'text': '昨日的首板今日红盘个数',
            'func': crawl_length('%s涨跌幅大于0 %s涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new))
        },
        {
            'text': '昨日的首板今日大面个数',
            'func': crawl_length('(%s的收盘价格/开盘价格小于0.95)或者(%s的收盘价格/%s收盘价格小于0.95) %s涨停 %s未涨停 %s' % (currentDay, currentDay, lastTradeDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new))
        },
        {
            'text': '昨日的连板今日红盘个数',
            'func': crawl_length('%s涨跌幅大于0 %s连续涨停天数为2以上 %s' % (currentDay, lastTradeDay, no_st + no_new))
        },
        {
            'text': '昨日的连板今日大面个数',
            'func': crawl_length('(%s的收盘价格/开盘价格小于0.95)或者(%s的收盘价格/%s收盘价格小于0.95) %s连续涨停天数为2以上 %s' % (currentDay, currentDay, lastTradeDay, lastTradeDay, no_st + no_new))
        },
        {
            'text': '昨日的连板今日绿盘个数',
            'func': crawl_length('%s涨跌幅小于0 %s连续涨停天数为2以上 %s' % (currentDay, lastTradeDay, no_st + no_new))
        }
    ]

def getAutoCal():
    return[
        autoCal('涨停数'),
        autoCal('连板数'),
        autoCal('整体封板率'),
        autoCal('首板成功率'),
        autoCal('1进2晋级率'),
        autoCal('2进3晋级率'),
        autoCal('3进4晋级率'),
        autoCal('4进5晋级率'),
        autoCal('5板以上晋级率'),
        autoCal('连板晋级率(2板+)'),
        autoCal('中高位晋级率(3板+)'),
        autoCal('总情绪')
    ]
if __name__ == "__main__":
    getSentiment('20221209')
    
    

# 大环境