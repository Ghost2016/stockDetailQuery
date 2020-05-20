import urllib
import requests
import re
import json
import operator, os
import threading, time
# 用于判断是什么系统
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process, Pool, Queue
from selenium.webdriver.chrome.options import Options
# 本机库
# 用于存放历史股票列表
from fileUtils import saveStocks, getStocks
# 交易工具
from tradeUtils import isInTradeTime
# 封装的微信的api
from wechat import login, sendMessageToMyself, sendMessageToFriend
# 常量
from variables import const
global driver, chrome_options
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome('./chromedriver.81')
driver.get('http://account.yunlizhi.cn/#/rootLogin?redirect=%2Froot')
tel=driver.find_element_by_link_text('手机')
tel=driver.find_element_by_xpath('//in/div(text=登录→&class=flex1)[3]/div(class=el-form-item)[1]/div(class=el-form-item__content&style=margin-left: 0px;)[1]/div(class=input-text el-input el-input--suffix)[1]/input[1]')
inputs=driver.find_elements_by_tag_name('input')
inputs
inputs[1].send_keys('15756291158')
# input[1]
inputs[1]
inputs[1].send_keys('111')
inputs[2].send_keys('hope1234')
buttons=driver.find_elements_by_tag_name('button')
buttons
buttons[0].click()
systems=driver.get_elements_by_class_name('system')
systems=driver.find_elements_by_class_name('system')
systems
systems[2].click()
driver.get('http://mp.yunlizhi.cn/#/contractManage/customer?fromsidebar=1')
driver.find_elements_by_link_text('编辑')
driver.find_element_by_xpath('//button[label="编辑"]')
driver.find_element_by_xpath('button[label="编辑"]')
driver.find_element_by_xpath('/button[label="编辑"]')
driver.find_element_by_css_selector('button[label="编辑"]')
driver.find_elements_by_css_selector('button[label="编辑"]')
driver.find_elements_by_css_selector('button[label="编辑"]')[0].click()
driver.find_elements_by_css_selector('button[label="提交"]')[0].click()
driver.find_elements_by_css_selector('button[label="提交"]')
driver.find_elements_by_css_selector('span[label="提交"]')
driver.find_elements_by_css_selector('span[value="提交"]')
driver.find_elements_by_css_selector('span[val="提交"]')
driver.find_elements_by_css_selector('button>span')
driver.find_elements_by_css_selector('button[type="text"]>span')
driver.find_elements_by_css_selector('button.el-button--text>span')
driver.find_elements_by_css_selector('button.el-button--text>span')[0]
driver.find_elements_by_css_selector('button.el-button--text>span')[0].text
driver.find_elements_by_css_selector('button.el-button--text>span')[0].click()
driver.find_elements_by_css_selector('button[label="编辑"]')[1].click()
driver.find_elements_by_css_selector('button.el-button--text>span')[0].click()
history
exit
exit()
