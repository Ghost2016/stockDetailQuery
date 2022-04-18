#!/usr/bin/env python
#coding: utf-8

import time
import datetime
from chinese_calendar import is_workday
from pyautogui import sleep

from fileUtils import clearStocks
import requests

TIME_NODE = {
    '9': 9,
    '10': 10,
    '11': 11,
    '13': 13,
    '15': 15,
    '30': 30
}

# 是否处于一天的交易时间
def isInTradeTime():
    # return True
    isIn = False
    localTime = time.localtime()
    # localTime = time.localtime(1459925086.7115328)
    currentHour = int(time.strftime("%H", localTime))
    currentMinute = int(time.strftime("%M", localTime))
    # [9:30 - 11:30)
    if (currentHour == TIME_NODE['9'] and currentMinute >= TIME_NODE['30']) or (currentHour == TIME_NODE['11'] and currentMinute < TIME_NODE['30']) or currentHour == TIME_NODE['10']:
        isIn = True
    # [13:00 - 15:00)
    elif (currentHour >= TIME_NODE['13']) and (currentHour < TIME_NODE['15']):
        isIn = True
    return isIn


def isInWorkDay():
    return is_workday(datetime.datetime.now())


def isWeekend():
    day = datetime.datetime.now()
    # Monday == 0 ... Sunday == 6
    if day.weekday() in [5, 6]:
        return True
    else:
        return False

# 当天是可否可以进行交易
def isInTradeDay():
    # return True
    return isInWorkDay() and not isWeekend()


def printBeforeSleep(now, distance):
    print('当前时间%i:%i:%i' % (now.hour, now.minute, now.second))
    print('休息时间%i小时%i分钟%i秒' % (int(distance/3600),
          int(distance % 3600/60), int(distance % 3600 % 60)))
    sleep(distance)

# 休息到下一个交易日交易节点
def sleepToNextTradeDay():
    now=datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    distance = (TIME_NODE['9'] - hour) * 3600 + (TIME_NODE['30'] - minute) * 60 - second
    if(distance < 0):
        # 如果是隔夜，需要加一天
        distance = distance + 3600 * 24
    printBeforeSleep(now, distance)

# 休息到下一个交易时间节点
def sleepToNextTradeTime():
    now=datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    distance = 0
    # 晚上段
    if((hour >= TIME_NODE['15']) or (hour < TIME_NODE['9']) or (hour == TIME_NODE['9'] and minute < TIME_NODE['30'])):
        distance = (TIME_NODE['9'] - hour) * 3600 + (TIME_NODE['30'] - minute) * 60 - second
        if(distance < 0):
            # 如果是隔夜，需要加一天
            distance = distance + 3600 * 24
    elif((hour == TIME_NODE['11'] and minute >= TIME_NODE['30']) or (hour > TIME_NODE['11'] and hour < TIME_NODE['13'])):
        distance = (TIME_NODE['13'] - hour) * 3600 - minute * 60 - second
    printBeforeSleep(now, distance)

# 检查是否应该执行 clearStock
def checkClearStock():
    now=datetime.datetime.now()
    hour = now.hour
    if hour == TIME_NODE['9']:
        clearStocks()

# 发送信息（目前是发送到钉钉上）
def sendMessage(result):
    headers = {
        'content-type': 'application/json',
    }
    data = '{\t"msgtype": "text",\t"text": {\t"content": "霸霸:%s"} }' % result
    requests.post('https://oapi.dingtalk.com/robot/send?access_token=bf8d15a1ccdc83ae88e761b32f70057dd298c25db755f38514c69887199eb2e5', headers=headers, data=data.encode("utf-8").decode("latin1"))


if __name__ == "__main__":
    print(isInTradeTime())
