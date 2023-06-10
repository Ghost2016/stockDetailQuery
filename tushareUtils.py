#!/usr/bin/env python
#coding: utf-8

import datetime
import tushare as ts
from tradeUtils import isInWorkDay, isInTradeDay

# 用于存日期的字典的文件名
file='./autoFile/date.txt'
token='cee7373f5534cd6ac10783e468db6710767cf637007930de27ce3a08'
ts.set_token(token)
pro = ts.pro_api()
 
lastDayMap= {}

#保存
def saveFile():
    global lastDayMap
    f = open(file, 'w')
    f.write(str(lastDayMap))
    f.close()
    pass

#读取
def readFile():
    global lastDayMap
    f = open(file, 'r')
    a = f.read()
    lastDayMap = eval(a)
    f.close()
    pass

readFile()

def getTushareInstance():
    return pro


minusOneDay = datetime.timedelta(days = -1)

# date 字符串转 datetime 对象
def dateStrToDateTime(date):
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    return datetime.date(year, month, day)


# 获取最近的一个交易日
# 如果今日放假，那么则返回最后的一个交易日
# 如果今日正常交易，那么就返回今日
def getCurrentTradeDay(day = datetime.datetime.now()):
    if not isInTradeDay(day):
        day = day + minusOneDay
        return getCurrentTradeDay(day)
    return day.strftime('%Y%m%d')


# 获取上一个交易日
# 传入 20230609，返回 20230608
def getLastTradeDay(day = "20230609", **kwargs):
    # 如果在表里面有维护，那么直接取表里面维护的值
    if day in lastDayMap:
        return lastDayMap[day]
    # 不然就根据当前天去取上一个交易日信息并且写入至 date.txt 文件中，方便下次使用
    else:
        dayInDateTime = dateStrToDateTime(day) + minusOneDay
        result = dayInDateTime.strftime('%Y%m%d')
        if isInTradeDay(dayInDateTime):
            theDay = kwargs.get("theDay", day)
            print('写入数据 date.txt:%s:%s' % (theDay, result))
            lastDayMap[theDay] = result
            saveFile()
            return result
        else:
            # theDay 用于标记最初的那个时间
            return getLastTradeDay(result, theDay = kwargs.get("theDay", day))

# 获取上N个交易日
def getLastSpecificTradeDay(num, day=getCurrentTradeDay()):
    if num > 10:
        raise Exception('数字不能超过10')
    while num > 0:
        num = num - 1
        day = getLastTradeDay(day)
        return getLastSpecificTradeDay(num, day)
    return day

if __name__ == "__main__":
    # print(dateStrToDateTime('20230610'))
    # print(getCurrentTradeDay())
    print(getLastTradeDay("20230611"))