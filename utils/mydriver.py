#!/usr/bin/env python
#coding: utf-8

from selenium.webdriver.chrome.options import Options
from utils.user_agent import getheaders
from selenium import webdriver
def getDriver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('–incognito')
    chrome_options.add_argument('--user-agent={}'.format(getheaders()['User-Agent']))
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    
    return driver
