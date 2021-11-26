#!/usr/bin/env python
#coding: utf-8

import pyautogui as gui
from time import sleep
from verifyCode.getCode import get_verify_code, rename_and_move_verify_code, remove_verify_code
import os
import pyperclip
def saveCode():
    # 打开chrome
    gui.moveTo(x=970, y=1031)
    gui.click()
    # 点击地址栏输入地址
    gui.moveTo(x=321, y=79)
    gui.click()
    gui.hotkey('command','a')
    pyperclip.copy('http://www.iwencai.com/unifiedwap/reptile')
    gui.hotkey('command','v')
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

def innerHandle():
    gui.moveTo(x=200, y=120)
    gui.click()
    sleep(2)
    gui.hotkey('enter')
    gui.hotkey('enter')
    # 移动到验证码
    gui.moveTo(890,446)
    sleep(3)
    # 下载验证码
    gui.rightClick()
    gui.moveTo(956,474)
    gui.click()
    sleep(3)
    gui.hotkey('enter')
    sleep(1)
    # 解析验证码
    result=get_verify_code(os.path.dirname(__file__)+'/getImg.jpeg')
    # 填充到网页上去
    gui.moveTo(990,450)
    gui.click()
    gui.click()
    gui.typewrite(result)
    gui.hotkey('enter')
    gui.moveTo(888,530)
    gui.click()
    print(result)
    
    return result

def handleSessionError():
    result=innerHandle()
    if len(result) != 6:
        remove_verify_code(result)
        return handleSessionError()
    # 解析后移动验证码
    remove_verify_code(result)
    return result


if __name__ == '__main__':
    for i in range(0, 1):
        saveCode()
        sleep(2)
