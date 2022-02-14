#!/usr/bin/env python
#coding: utf-8
# -*- coding=utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from time import sleep
from verifyCode.getCode import get_verify_code, remove_verify_code
import os
from utils.mydriver import getDriver

fileName = 'getImg.png'
driver = None
iwencaiUrl = 'http://www.iwencai.com/unifiedwap/reptile'

# 处理session过期的问题
def handleSessionError():
    result = getCodeByDriver()
    if len(result) != 6:
        remove_verify_code()
        return handleSessionError()
    # 解析后移动验证码
    remove_verify_code()
    return result

# 通过chromeDriver获取验证码
def getCodeByDriver():
    global driver
    print(driver)
    if not driver:
        driver = getDriver()
    driver.get(iwencaiUrl)
    img, button, input = None, None, None
    
    # 图片
    try:
        button = driver.find_element_by_id('capCheck')
        input = driver.find_element_by_id('capInput')
        img = driver.find_element_by_id('capImg')
        if (button == None) or (input == None) or (img == None):
            raise BaseException()
    except BaseException:
        print("没有找到指定元素")
        return getCodeByDriver()
    # 存储图片
    img.screenshot('./verifyCode/' + fileName)
    sleep(1)
    # 解析验证码
    result = get_verify_code(os.path.dirname(__file__)+'/' + fileName)
    print('result', result)
    input.clear()
    input.send_keys(result)
    # 提交
    button.click()
    return result

# 关闭浏览器，退出driver
def quitDriver():
    global driver
    if not driver == None:
        driver.quit()
        driver = None
    driver = None

if __name__ == '__main__':
    handleSessionError()
