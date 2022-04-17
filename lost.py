
#!/usr/bin/env python
#coding: utf-8

# 亏钱效应来源 统计点来源于当日涨停与曾涨停票 昨日涨停与曾涨停票
# 1. 当日回撤大于 10%
# 2. 两日回撤超过 15%


from meepwn import crawl_stock_data
from tushareUtils import getLastTradeDay


def fetchLost():
    day = '20220411'
    lastDay = getLastTradeDay(day)
    stocks = crawl_stock_data('((%s的最高价 - %s的收盘价)/%s的收盘价>0.10 非st 非创业板 非科创板' % (day, day, lastDay))
    index=0
    for stock in stocks:
        topValue = stock['最高价:不复权[%s]' % day]
        closeValue = stock['收盘价:不复权[%s]' % day]
        lastDayCloseValue = stock['收盘价:不复权[%s]' % lastDay]
        percent = (float(topValue) - float(closeValue))/lastDayCloseValue * 100
        index+=1
        print(index, stock['股票简称'], '回撤值', percent)
    pass

if __name__ == "__main__":
    fetchLost()
    pass