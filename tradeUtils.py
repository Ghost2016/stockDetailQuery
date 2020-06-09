#!/usr/bin/env python
#coding: utf-8

import time

# whether in trade time
def isInTradeTime():
    isIn = False
    localTime = time.localtime()
    # localTime = time.localtime(1459926086.7115328)
    currentHour = int(time.strftime("%H", localTime))
    currentMinute = int(time.strftime("%M", localTime))
    # trade only in 9:30 - 10:00
    # 9:30 - 11:30
    if (currentHour == 9 and currentMinute >= 30) or (currentHour == 11 and currentMinute >= 30) or currentHour == 10:
        isIn = True
    # 13:00 - 15:00
    elif (currentHour > 12) and (currentHour < 15) or currentHour == 14:
       isIn = True
    return isIn

if __name__ == "__main__":
    print(isInTradeTime())