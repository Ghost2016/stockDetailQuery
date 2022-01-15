#!/usr/bin/env python
#coding: utf-8

from selenium.webdriver.chrome.options import Options
from utils.user_agent import getUserAgent
from selenium import webdriver
def getDriver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('–incognito')
    chrome_options.add_argument('--user-agent={}'.format(getUserAgent()))
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    
    return driver

if __name__ == "__main__":
    dd = getDriver()
    dd.get('https://www.baidu.com')