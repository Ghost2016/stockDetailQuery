#!/usr/bin/env python
#coding: utf-8

import datetime
# import tushare as ts

# 用于存日期的字典的文件名
file='./autoFile/date.txt'
token='cee7373f5534cd6ac10783e468db6710767cf637007930de27ce3a08'
# ts.set_token(token)
# pro = ts.pro_api()
 
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

# def getTushareInstance():
#     return pro


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
def getCurrentTradeDay():
    now = str(datetime.datetime.now().date()).replace('-', '')
    return 
    # dat = getTushareInstance().trade_cal(exchange='', start_date=now, end_date=now)
    # if dat.iat[0,2] == 0:
    #     return dat.iat[0, 3]
    # return now

# 获取上一个交易日
# 传入 20230609，返回 20230608
def getLastTradeDay(day = "20230609", **kwargs):
    # 如果在表里面有维护，那么直接取表里面维护的值
    if day in lastDayMap:
        return lastDayMap[day]
    # dat = getTushareInstance().trade_cal(exchange='', start_date=day, end_date=day)
    # lastDayMap[day] = dat.iat[0, 3]
    # saveFile()
    # return dat.iat[0, 3]
    return getCurrentTradeDay()

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
    # TODO
    # dat = getTushareInstance().trade_cal(exchange='', start_date='20220331', end_date='20220408')
    # print(dat)
    pass
