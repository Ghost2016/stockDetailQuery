#!/usr/bin/env python
#coding: utf-8

# 此文件用于获取各类策略的收益率

from meepwn import crawl_earning_of_stocks
from tushareUtils import getCurrentTradeDay, getLastTradeDay

currentDay = getCurrentTradeDay()
lastTradeDay = getLastTradeDay()
theDayBeforeLastTradeDay = getLastTradeDay(lastTradeDay)
no_st = " 非st 非退市"
no_new = ' 非新股'
categories = [
  {
    'category': '%s首板 %s' % (lastTradeDay, no_st + no_new),
    'text': '昨日首板理想收益率（封死涨停）'
  },
  {
    'category': '%s未涨停 %s涨停或者曾涨停 %s' % (theDayBeforeLastTradeDay, lastTradeDay, no_st + no_new),
    'text': '昨日首板真实收益率（包含炸板）'
  },
  {
    'category': '%s的几天几板是2天2板 %s涨跌幅 %s ' % (lastTradeDay, currentDay, no_st + no_new),
    'text': '昨日二板理想收益率（封死涨停）'
  },
  {
    'category': '%s未涨停 %s涨停或者曾涨停 %s' % (theDayBeforeLastTradeDay, lastTradeDay, no_st + no_new),
    'text': '昨日二板理想收益率（包含炸板）'
  },
]

if __name__ == "__main__":
    max = len(categories)
    for d in range(0, max):
        category = categories[d]
        print(category['text'], crawl_earning_of_stocks(category['category']))