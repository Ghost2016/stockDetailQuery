#!/usr/bin/env python
#coding: utf-8
# https://github.com/shidenggui/easyquotation
import easyquotation
import time
quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq'] 
quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
# 查询次数
times=10
def parseIWencai():
    global times
    print(quotation.stocks(['000713'], prefix=False)['000713']['time'])
    print(quotation.stocks(['000713'], prefix=False)['000713']['ask1_volume'])
    # quotation.market_snapshot(prefix=True)
    time.sleep(0.5)
    if not times == 0:
        times = times - 1
        parseIWencai()
    pass

if __name__ == '__main__':
    parseIWencai()
