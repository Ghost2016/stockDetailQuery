#!/usr/bin/env python
#coding: utf-8

import pyautogui as gui
from time import sleep
import datetime
def saveCode():
    # 打开chrome
    gui.moveTo(x=970, y=1031)
    gui.click()
    # 点击地址栏输入地址
    gui.moveTo(x=321, y=79)
    gui.click()
    gui.hotkey('command','a')
    gui.typewrite('http://www.iwencai.com/unifiedwap/reptile')
    sleep(2)
    gui.hotkey('enter')
    gui.hotkey('enter')
    sleep(2)
    # 下载图片
    gui.moveTo(890,446,0.25)
    gui.rightClick()
    gui.moveTo(956,474)
    gui.click()
    sleep(1)
    # gui.typewrite('%f' % datetime.datetime.now().timestamp())
    gui.typewrite('1')
    gui.hotkey('enter')
    # 点击替换
    gui.moveTo(x=664, y=192)
    gui.click()
    


if __name__ == '__main__':
    for i in range(0, 40):
        saveCode()
        sleep(2)